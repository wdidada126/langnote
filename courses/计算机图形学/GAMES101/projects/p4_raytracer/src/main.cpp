// p4 — 光线追踪 → 简单路径追踪（GAMES101 L15–L16；官方 Lecture 15–20）
// 场景：3 个球（Lambertian / 金属镜面 / 玻璃）+ 地面。
// 模式：
//   whitted : Whitted 递归光线（反射 + Snell 折射 + 直接光照），确定性、无噪点
//   path    : 路径追踪（Lambertian+镜面，MC 半球采样，渲染方程逐样本估计，L15–L16）
//   path+blur: 同 path，再对结果做 3x3 箱式"朴素降噪"（演示降噪能掩盖什么）
// 用法：bin/p4 [whitted|path] [spp] [宽] [文件名] [blur]
//   例：./bin/p4 path 16  512 path_16.ppm
//       ./bin/p4 path 1024 512 path_1024.ppm   <- 对比噪声收敛（README）
// 仅标准库，C++17，P6 PPM 输出，线性域累加 + gamma 2.2 编码（L13）。
#include "geom.hpp"

#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <cmath>
#include <random>
#include <string>
#include <vector>
#include <limits>

using namespace g101;

// ---------- 最小球求交（L10 隐式方程；L16 的 BVH 留给选做）----------
struct Sphere {
    Vec3 c; float r;
    int type;              // 0 lambert, 1 metal, 2 glass
    Vec3 albedo;
    float ior = 1.5f;      // 玻璃
};
struct Hit {
    float t;
    Vec3 p, n;
    const Sphere* mat;
};

static bool hitSphere(const Sphere& s, Vec3 o, Vec3 d, Hit& h) {
    Vec3 oc = o - s.c;
    float b = oc.dot(d), c = oc.dot(oc) - s.r * s.r;
    float disc = b * b - c;
    if (disc < 0) return false;
    float sq = std::sqrt(disc);
    float t = -b - sq;
    if (t < 1e-4f) t = -b + sq;
    if (t < 1e-4f) return false;
    h.t = t; h.p = o + d * t; h.n = (h.p - s.c) / s.r; h.mat = &s;
    return true;
}

struct Scene {
    std::vector<Sphere> spheres;
    float groundY = -1.0f;
    const Sphere* glass = nullptr;
    bool hit(const Vec3& o, const Vec3& d, Hit& h) const {
        bool any = false;
        for (auto& s : spheres) {
            Hit t;
            if (hitSphere(s, o, d, t) && (!any || t.t < h.t)) { h = t; any = true; }
        }
        if (std::abs(d.y) > 1e-6f) {  // 地面 = 半空间（L10）
            float t = (groundY - o.y) / d.y;
            if (t > 1e-4f && (!any || t < h.t)) h = {t, o + d * t, Vec3{0, 1, 0}, nullptr}, any = true;
        }
        return any;
    }
};

// ---------- 方向工具 ----------
static Vec3 reflect(const Vec3& v, const Vec3& n) { return v - n * (2.f * v.dot(n)); }  // L16
// Snell（L16）：eta = n1/n2；cos1 = -v·n（v 指向表面）；返回折射方向，全反射返回 false
static bool refract(const Vec3& v, const Vec3& n, float eta, Vec3& out) {
    float cos1 = std::min(-v.dot(n), 1.f);
    float sin2t = eta * eta * (1.f - cos1 * cos1);
    if (sin2t > 1.f) return false;
    float cos2 = std::sqrt(1.f - sin2t);
    out = v * eta + n * (eta * cos1 - cos2);
    return true;
}
// 正交基（用于半球采样）
static void onBasis(const Vec3& n, Vec3& u, Vec3& v) {
    Vec3 a = std::abs(n.x) > 0.9f ? Vec3{0, 1, 0} : Vec3{1, 0, 0};
    u = n.cross(a).normalized();
    v = n.cross(u);
}
// 均匀半球采样（L15 MC）：xi1,xi2 -> 方向
static Vec3 randomHemisphere(float xi1, float xi2) {
    float z = xi1;                       // cosθ 均匀
    float r = std::sqrt(std::max(0.f, 1 - z * z));
    float phi = 2 * kPi * xi2;
    return {r * std::cos(phi), r * std::sin(phi), z};
}
// cos 加权半球采样（L15 重要性采样：对 Lambert 零方差）
static Vec3 randomCosineHemisphere(float xi1, float xi2) {
    float z = std::sqrt(xi1);            // cosθ = sqrt(xi1)
    float r = std::sqrt(std::max(0.f, 1 - z * z));
    float phi = 2 * kPi * xi2;
    return {r * std::cos(phi), r * std::sin(phi), z};
}

static Scene makeScene() {
    Scene sc;
    sc.spheres = {
        {{-1.3f, -0.45f, 0.f}, 0.55f, 0, {0.65f, 0.22f, 0.18f}, 1.f},  // 漫反射红
        {{0.1f, -0.3f, 0.25f}, 0.65f, 1, {0.85f, 0.85f, 0.88f}, 1.f},  // 金属镜面
        {{-0.1f, -0.3f, -1.15f}, 0.5f, 0, {0.2f, 0.5f, 0.65f}, 1.f},   // 漫反射青
        {{1.25f, 0.15f, -0.25f}, 0.8f, 2, {1.f, 1.f, 1.f}, 1.5f},      // 玻璃
    };
    sc.glass = &sc.spheres.back();
    return sc;
}

// 直接光照（点光源 + 阴影光线）：Whitted 模式的局部着色（L14 + L16 阴影）
static Vec3 localShade(const Scene& sc, const Hit& h, const Vec3& eye) {
    const Vec3 lightPos(2.5f, 4.5f, 3.5f);
    const Vec3 lightColor(1.05f, 1.0f, 0.92f);
    if (!h.mat) {  // 地面棋盘
        int k = int(std::floor(h.p.x * 1.6f) + std::floor(h.p.z * 1.6f));
        Vec3 alb = (k % 2 == 0) ? Vec3{0.72f, 0.70f, 0.66f} : Vec3{0.20f, 0.22f, 0.26f};
        float ndl = std::max(0.f, h.n.dot((lightPos - h.p).normalized()));
        return alb * (0.08f + ndl * 0.9f * 3.f / (lightPos - h.p).length());
    }
    const Sphere& s = *h.mat;
    Vec3 lo = (lightPos - h.p).normalized();
    // 阴影光线（L16：被挡则只有环境）
    Hit shadow;
    bool inShadow = sc.hit(h.p + h.n * 1e-3f, lo, shadow) && shadow.t < (lightPos - h.p).length();
    float ndl = std::max(0.f, h.n.dot(lo));
    Vec3 base{0, 0, 0};
    if (s.type == 0) {  // Lambert
        base = s.albedo * (0.06f + (inShadow ? 0.f : ndl * 2.2f / (lightPos - h.p).length()) * lightColor);
    } else if (s.type == 1) {  // 金属：镜面高光 + 反射环境（Whitted 递归里再补）
        Vec3 v = (eye - h.p).normalized();
        float ndh = std::max(0.f, h.n.dot((lo + v).normalized()));
        base = s.albedo * (0.05f + std::pow(ndh, 90.f) * (inShadow ? 0.f : 1.5f));
    } else {  // 玻璃：菲涅尔近似的边缘反光 + 高光
        Vec3 v = (eye - h.p).normalized();
        float fres = 0.04f + 0.96f * std::pow(1 - std::max(0.f, v.dot(h.n)), 5.f);
        base = Vec3{fres, fres, fres} * (inShadow ? 0.1f : ndl * 1.2f) + Vec3{0.02f, 0.02f, 0.02f};
    }
    return base;
}

// ---------- Whitted 递归（L16）----------
static Vec3 traceWhitted(const Scene& sc, Vec3 o, Vec3 d, const Vec3& eye, int depth) {
    Hit h;
    if (depth <= 0 || !sc.hit(o, d, h)) {  // 背景（天空）
        float t = 0.5f * (d.y + 1.f);
        return Vec3::lerp({1, 1, 1}, {0.45f, 0.65f, 0.95f}, t) * 0.9f;
    }
    Vec3 col = localShade(sc, h, eye);
    const Sphere* s = h.mat;
    Vec3 n = h.n;
    if (s && s->type == 1) {  // 镜面反射光线
        col += s->albedo * 0.9f * traceWhitted(sc, h.p + n * 1e-3f, reflect(d, n), eye, depth - 1);
    } else if (s && s->type == 2) {  // 玻璃：折射（含全反射）+ 菲涅尔反射
        float eta = d.dot(n) < 0 ? 1.f / s->ior : s->ior;
        Vec3 nn = d.dot(n) < 0 ? n : -n;
        Vec3 refr;
        if (refract(d.normalized(), nn, eta, refr))
            col += traceWhitted(sc, h.p + refr * 1e-3f, refr, eye, depth - 1);
        else
            col += traceWhitted(sc, h.p + n * 1e-3f, reflect(d, n), eye, depth - 1);
        Vec3 v = -d;
        float fres = 0.04f + 0.96f * std::pow(1 - std::max(0.f, v.dot(nn)), 5.f);
        col += fres * 0.5f * traceWhitted(sc, h.p + nn * 1e-3f, reflect(d, n), eye, depth - 1);
    }
    return col;
}

// ---------- 路径追踪（L15–L16 渲染方程 MC 估计）----------
// L_o ≈ L_e + f_r·L_i·cosθ / p(ω)；Lambert: f_r=albedo/π, cosθ 抵消采样 p=cosθ/π -> 权重 albedo
static Vec3 tracePath(const Scene& sc, Vec3 o, Vec3 d, std::mt19937& rng, int maxDepth, bool cosine) {
    Vec3 flux{1, 1, 1};  //  throughput
    Vec3 sum{0, 0, 0};
    for (int bounce = 0; bounce <= maxDepth; ++bounce) {
        Hit h;
        if (!sc.hit(o, d, h)) {  // 命中光源/环境 -> 发射
            float t = 0.5f * (d.y + 1.f);
            sum += flux * Vec3::lerp({1, 1, 1}, {0.45f, 0.65f, 0.95f}, t);
            break;
        }
        const Sphere* s = h.mat;
        // 直接光：一条阴影光线（NEE 的最简形式，L16）
        const Vec3 lightPos(2.5f, 4.5f, 3.5f);
        {
            Vec3 lo = (lightPos - h.p).normalized();
            Hit shadow;
            bool vis = !sc.hit(h.p + h.n * 1e-3f, lo, shadow) || shadow.t > (lightPos - h.p).length();
            if (vis && !h.mat) {  // 地面棋盘直接光
                int k = int(std::floor(h.p.x * 1.6f) + std::floor(h.p.z * 1.6f));
                Vec3 alb = (k % 2 == 0) ? Vec3{0.72f, 0.70f, 0.66f} : Vec3{0.20f, 0.22f, 0.26f};
                float ndl = std::max(0.f, h.n.dot(lo));
                sum += flux * alb * ndl * 3.f / ((lightPos - h.p).length() * (lightPos - h.p).length());
            } else if (vis && s && s->type == 0) {
                float ndl = std::max(0.f, h.n.dot(lo));
                sum += flux * s->albedo * ndl * 3.f / ((lightPos - h.p).length() * (lightPos - h.p).length());
            }
        }
        if (!s) {  // 地面不反弹（避免全场景无限弹）：当作纯吸收 Lambert 终止
            break;
        }
        std::uniform_real_distribution<float> U(0.f, 1.f);
        if (s->type == 0) {  // Lambert：按 cos 加权或均匀半球采样
            Vec3 u, v; onBasis(h.n, u, v);
            Vec3 dir = cosine ? randomCosineHemisphere(U(rng), U(rng)) : randomHemisphere(U(rng), U(rng));
            Vec3 w = (u * dir.x + v * dir.y + h.n * dir.z).normalized();
            // cos 加权: f_r*cos/p = alb；均匀半球: f_r*cos/p = 2*alb*cos（p=1/2π）
            float wgt = cosine ? 1.f : 2.f * std::max(0.f, h.n.dot(w));
            flux = flux * (s->albedo * wgt);
            o = h.p + h.n * 1e-3f; d = w;
        } else if (s->type == 1) {  // 镜面：确定方向弹射（pdf=δ，权重=albedo）
            flux = flux * s->albedo;
            o = h.p + h.n * 1e-3f; d = reflect(d, h.n);
        } else {  // 玻璃：折射优先（p4 简化：不采样），全反射则反弹
            float eta = d.dot(h.n) < 0 ? 1.f / s->ior : s->ior;
            Vec3 nn = d.dot(h.n) < 0 ? h.n : -h.n;
            Vec3 refr;
            if (refract(d.normalized(), nn, eta, refr)) { o = h.p + refr * 1e-3f; d = refr; }
            else { o = h.p + nn * 1e-3f; d = reflect(d, nn); }
        }
        if (bounce > 2) {  // 无偏俄罗斯轮盘赌（L16）：以 0.8 概率存活并加权 1/0.8
            if (U(rng) > 0.8f) break;
            flux = flux * (1.f / 0.8f);
        }
    }
    return sum;
}

// ---------- 渲染与输出 ----------
static void boxBlur3x3(std::vector<float>& img, int W, int H, int ch) {
    std::vector<float> tmp = img;
    for (int y = 1; y + 1 < H; ++y)
        for (int x = 1; x + 1 < W; ++x)
            for (int c = 0; c < ch; ++c) {
                float s = 0;
                for (int dy = -1; dy <= 1; ++dy)
                    for (int dx = -1; dx <= 1; ++dx)
                        s += tmp[((y + dy) * W + x + dx) * ch + c];
                img[((y) * W + x) * ch + c] = s / 9.f;
            }
}

int main(int argc, char** argv) {
    std::string mode = argc > 1 ? argv[1] : "path";
    int spp = argc > 2 ? std::atoi(argv[2]) : 64;
    int W = argc > 3 ? std::atoi(argv[3]) : 512;
    std::string out = argc > 4 ? argv[4] : (mode + "_" + std::to_string(spp) + ".ppm");
    bool blur = argc > 5 && std::string(argv[5]) == "blur";
    bool cosine = mode == "path" || mode == "pathcos";

    Scene sc = makeScene();
    std::mt19937 rng(12345);
    std::uniform_real_distribution<float> U(0.f, 1.f);

    Vec3 eye(0, 1.2f, 5.0f), center(0, -0.2f, 0), up(0, 1, 0);
    Vec3 fwd = (center - eye).normalized();
    Vec3 rgt = fwd.cross(up).normalized(), ul = rgt.cross(fwd);
    float tanH = 0.42f;

    std::vector<float> img(size_t(W) * W * 3, 0.f);
    for (int y = 0; y < W; ++y) {
        for (int x = 0; x < W; ++x) {
            Vec3 acc{0, 0, 0};
            for (int s = 0; s < spp; ++s) {
                // 像素内多采样（stratified）：抗锯齿 + 路径采样的随机性（L09/L15）
                float jx = (x + (s % 4 + 0.5f) / 4 + U(rng) * 0.25f - 0.125f) / W;
                float jy = (y + (s / 4 % 4 + 0.5f) / 4 + U(rng) * 0.25f - 0.125f) / W;
                if (spp == 1) { jx = (x + 0.5f) / W; jy = (y + 0.5f) / W; }
                Vec3 dir = (fwd + rgt * ((jx - 0.5f) * 2 * tanH) + ul * ((0.5f - jy) * 2 * tanH)).normalized();
                if (mode == "whitted")
                    acc += traceWhitted(sc, eye, dir, eye, 6);
                else
                    acc += tracePath(sc, eye, dir, rng, 8, cosine);
            }
            Vec3 c = acc / (float)spp;
            size_t i = (size_t(y) * W + x) * 3;
            img[i] = c.x; img[i + 1] = c.y; img[i + 2] = c.z;
        }
    }
    if (blur) boxBlur3x3(img, W, W, 3);

    FILE* fp = std::fopen(out.c_str(), "wb");
    if (!fp) { std::printf("[p4] cannot write %s\n", out.c_str()); return 1; }
    std::fprintf(fp, "P6\n%d %d\n255\n", W, W);
    std::vector<uint8_t> row(size_t(W) * 3);
    for (int y = 0; y < W; ++y) {
        for (int x = 0; x < W; ++x) {
            size_t i = (size_t(y) * W + x) * 3;
            size_t j = size_t(x) * 3;  // row 只有一行宽，须用行内偏移（否则越界）
            for (int c = 0; c < 3; ++c) {
                float v = img[i + c];
                v = v / (1 + v);                              // Reinhard 色调映射（L13）
                v = std::pow(std::min(1.f, std::max(0.f, v)), 1 / 2.2f);  // gamma（L13）
                row[j + c] = uint8_t(v * 255 + 0.5f);
            }
        }
        std::fwrite(row.data(), 1, row.size(), fp);
    }
    std::fclose(fp);
    std::printf("[p4] %s: mode=%s spp=%d size=%d%s -> %s\n",
                mode.c_str(), mode.c_str(), spp, W, blur ? " +blur" : "", out.c_str());
    return 0;
}
