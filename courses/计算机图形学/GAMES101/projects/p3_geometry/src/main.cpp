// p3 — 几何表示（GAMES101 L10–L11）
// 两条线各自演示：
//   A. 显式表示：.obj 子集（v/f）加载 + 射线-三角求交（Möller–Trumbore）+ 平面填充渲染
//      -> mesh.ppm（立方体+四面体立于半空间平面上，平面明暗 flat shading）
//   B. 隐式表示：半空间/CSG "瑞士奶酪"（球 减 6 个孔球），sphere tracing 光线行进
//      -> csg.ppm
// 同时打印网格拓扑统计（V/E/F 与欧拉示性数），验证 L11 的 F-E+V=2。
// 仅标准库，C++17。输出 P6 PPM。
#include "geom.hpp"

#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <cmath>
#include <array>
#include <string>
#include <vector>
#include <set>
#include <tuple>
#include <algorithm>
#include <limits>

using namespace g101;

// ---------- 光线求交通用 ----------
struct Hit {
    bool hit = false;
    float t = std::numeric_limits<float>::infinity();
    Vec3 pos, normal;
    int material = 0;  // 0 平面 1 网格 2 CSG
};
struct Ray { Vec3 o, d; };

// Möller–Trumbore 射线-三角形（L08 重心坐标的光追版，L10 表）
static bool rayTriangle(const Ray& r, const Vec3& a, const Vec3& b, const Vec3& c,
                        float& tOut, float& u, float& v) {
    Vec3 e1 = b - a, e2 = c - a;
    Vec3 pvec = r.d.cross(e2);
    float det = e1.dot(pvec);
    if (std::abs(det) < 1e-9f) return false;
    float inv = 1.f / det;
    Vec3 tvec = r.o - a;
    u = tvec.dot(pvec) * inv;
    if (u < 0 || u > 1) return false;
    Vec3 qvec = tvec.cross(e1);
    v = r.d.dot(qvec) * inv;
    if (v < 0 || u + v > 1) return false;
    tOut = e2.dot(qvec) * inv;
    return tOut > 1e-4f;
}

// ---------- .obj 子集加载（v x y z / f i j k，1-based，三角化扇形）----------
struct Mesh {
    std::vector<Vec3> v;
    std::vector<std::array<int, 3>> f;  // 索引
    std::vector<Vec3> fn;               // 面法线（叉积，L02）

    size_t edgeCount() const {  // 无向边（索引对）集合
        std::set<std::pair<int, int>> e;
        for (auto& tr : f)
            for (int k = 0; k < 3; ++k) {
                int i = tr[k], j = tr[(k + 1) % 3];
                e.insert(std::minmax(i, j));
            }
        return e.size();
    }
    void buildNormals() {
        fn.resize(f.size());
        for (size_t i = 0; i < f.size(); ++i)
            fn[i] = (v[f[i][1]] - v[f[i][0]]).cross(v[f[i][2]] - v[f[i][0]]).normalized();
    }
};

static bool loadOBJSubset(const std::string& path, Mesh& m) {
    FILE* fp = std::fopen(path.c_str(), "rb");
    if (!fp) return false;
    char line[512];
    while (std::fgets(line, sizeof(line), fp)) {
        if (line[0] == 'v' && line[1] == ' ') {
            Vec3 p; sscanf(line + 2, "%f %f %f", &p.x, &p.y, &p.z);
            m.v.push_back(p);
        } else if (line[0] == 'f' && line[1] == ' ') {
            int idx[64], k = 0;
            char* s = line + 2;
            while (k < 64) {
                int id;
                char* end;
                id = (int)std::strtol(s, &end, 10);
                if (end == s) break;
                idx[k++] = id > 0 ? id - 1 : (int)m.v.size() + id;  // 支持负索引
                s = end;
                while (*s == ' ' || *s == '\t' || *s == '\r' || *s == '\n') ++s;
            }
            for (int i = 1; i + 1 < k; ++i) m.f.push_back({idx[0], idx[i], idx[i + 1]});  // 扇形三角化（L10）
        }
    }
    std::fclose(fp);
    m.buildNormals();
    return !m.f.empty();
}

// 射线-网格：对每面做 Möller–Trumbore（O(F)，p4 会换成 BVH 的话题）
static bool rayMesh(const Ray& r, const Mesh& m, const Mat4& xf, Hit& best) {
    std::vector<Vec3> wv(m.v.size());
    for (size_t i = 0; i < m.v.size(); ++i) wv[i] = mulPoint(xf, m.v[i]);
    for (size_t fi = 0; fi < m.f.size(); ++fi) {
        auto& tr = m.f[fi];
        float t, u, v;
        if (!rayTriangle(r, wv[tr[0]], wv[tr[1]], wv[tr[2]], t, u, v)) continue;
        if (t >= best.t) continue;
        Vec3 n = mulVector(xf, m.fn[fi]);
        if (n.dot(r.d) > 0) n = -n;  // 面向光线
        best = {true, t, r.o + r.d * t, n.normalized(), 1};
    }
    return best.hit;
}

// ---------- 场景 A：网格 ----------
static bool hitSceneA(const Ray& r, const Mesh& cube, const Mesh& tetra, Hit& best) {
    // 地面半空间 y <= -0.2（平面法线 +y）
    if (std::abs(r.d.y) > 1e-6f) {
        float t = (-0.2f - r.o.y) / r.d.y;
        if (t > 1e-4f && t < best.t)
            best = {true, t, r.o + r.d * t, Vec3{0, 1, 0}, 0};
    }
    rayMesh(r, cube, translation({-0.75f, 0.3f, 0}) * rotateY(deg2rad(20)), best);
    rayMesh(r, tetra, translation({0.85f, 0.35f, 0.1f}) * rotateY(deg2rad(-30)), best);
    return best.hit;
}

// ---------- 场景 B：CSG 瑞士奶酪（半空间/隐式，L10–L11）----------
static float sdSphere(Vec3 p, Vec3 c, float R) { return (p - c).length() - R; }
// f = max( 大球 , -孔1 , -孔2 , ... )：交 = max（负集）——半空间思想推广
static float swissCheese(Vec3 p) {
    float d = sdSphere(p, {0, 0.15f, 0}, 1.0f);
    float holes[6] = {0};
    Vec3 dirs[6] = {{1,0,0},{-1,0,0},{0,1,0},{0,-1,0},{0,0,1},{0,0,-1}};
    for (int i = 0; i < 6; ++i) {
        Vec3 c = Vec3{0, 0.15f, 0} + dirs[i] * 0.75f;
        holes[i] = sdSphere(p, c, 0.35f);
    }
    float hmin = holes[0];
    for (int i = 1; i < 6; ++i) hmin = std::min(hmin, holes[i]);
    return std::max(d, -hmin);
}
static Vec3 csgNormal(Vec3 p) {  // 数值梯度（∇d，L11：SDF 法线）
    const float e = 1e-4f;
    return Vec3{swissCheese(p + Vec3{e,0,0}) - swissCheese(p - Vec3{e,0,0}),
                swissCheese(p + Vec3{0,e,0}) - swissCheese(p - Vec3{0,e,0}),
                swissCheese(p + Vec3{0,0,e}) - swissCheese(p - Vec3{0,0,e})}.normalized();
}
// sphere tracing：步距 = f(p)（永不穿表面的最大安全步，L11）
static bool marchCheese(const Ray& r, Hit& best) {
    float t = 0.f;
    for (int i = 0; i < 512; ++i) {
        Vec3 p = r.o + r.d * t;
        float d = swissCheese(p);
        if (d < 1e-4f) {
            if (t < best.t) best = {true, t, p, csgNormal(p), 2};
            return true;
        }
        if (t > 30.f) break;
        t += d * 0.9f;  // CSG 后只是"近似距离场"，留 10% 余量防过步
    }
    return false;
}
static bool hitSceneB(const Ray& r, Hit& best) {
    if (std::abs(r.d.y) > 1e-6f) {
        float t = (-1.1f - r.o.y) / r.d.y;
        if (t > 1e-4f && t < best.t)
            best = {true, t, r.o + r.d * t, Vec3{0, 1, 0}, 0};
    }
    marchCheese(r, best);
    return best.hit;
}

// ---------- 着色 ----------
static Vec3 checkerGround(Vec3 p) {
    int c = int(std::floor(p.x * 2.f) + std::floor(p.z * 2.f));
    return (c % 2 == 0) ? Vec3{0.75f, 0.72f, 0.68f} : Vec3{0.25f, 0.27f, 0.32f};
}
static Vec3 shade(const Hit& h, const Vec3& eye, const Vec3& light) {
    Vec3 base = h.material == 0 ? checkerGround(h.pos)
              : h.material == 1 ? Vec3{0.75f, 0.30f, 0.22f}   // 网格：陶土色
                                : Vec3{0.20f, 0.65f, 0.60f};  // CSG：青玉色
    float ndl = std::max(0.f, h.normal.normalized().dot((light - h.pos).normalized()));
    float dist = (light - h.pos).length();
    float att = 6.f / (dist * dist);
    return base * (0.10f + 0.9f * ndl * std::min(1.f, att * 30.f));  // 环境+漫反射（L14）
}

// ---------- 相机 + 输出 ----------
static void render(int W, int H, bool sceneB, const Mesh& cube, const Mesh& tetra,
                   const std::string& path) {
    Vec3 eye(3.4f, 2.2f, 4.2f);
    Vec3 center(0, 0.2f, 0);
    Vec3 up(0, 1, 0);
    Vec3 d = (center - eye).normalized();
    Vec3 rgt = d.cross(up).normalized();
    Vec3 u = rgt.cross(d);
    float tanHalf = 0.42f;
    std::vector<uint8_t> img(size_t(W) * H * 3);
    Vec3 light(3, 5, 3);
    for (int y = 0; y < H; ++y) {
        for (int x = 0; x < W; ++x) {
            float u01 = (x + 0.5f) / W, v01 = 1 - (y + 0.5f) / H;
            Vec3 dir = (d + rgt * ((u01 - 0.5f) * 2 * tanHalf * (W / float(H))) +
                            u * ((v01 - 0.5f) * 2 * tanHalf)).normalized();
            Ray ray{eye, dir};
            Hit best;
            Vec3 col;
            if (sceneB) { hitSceneB(ray, best); }
            else { hitSceneA(ray, cube, tetra, best); }
            if (best.hit) col = shade(best, eye, light);
            else {  // 天空渐变
                float tt = 0.5f * (dir.y + 1.f);
                col = Vec3::lerp({1, 1, 1}, {0.5f, 0.7f, 1.0f}, tt) * 0.9f;
            }
            size_t i = (size_t(y) * W + x) * 3;
            float val[3] = {col.x, col.y, col.z};
            for (int c = 0; c < 3; ++c) {
                float g = std::pow(std::min(1.f, std::max(0.f, val[c])), 1.f / 2.2f);  // gamma（L13）
                img[i + c] = uint8_t(g * 255.f + 0.5f);
            }
        }
    }
    FILE* fp = std::fopen(path.c_str(), "wb");
    if (fp) {
        std::fprintf(fp, "P6\n%d %d\n255\n", W, H);
        std::fwrite(img.data(), 1, img.size(), fp);
        std::fclose(fp);
    }
    std::printf("[p3] wrote %s\n", path.c_str());
}

int main() {
    Mesh cube, tetra;
    if (!loadOBJSubset("data/cube.obj", cube)) { std::printf("[p3] data/cube.obj 未找到\n"); return 1; }
    if (!loadOBJSubset("data/tetra.obj", tetra)) { std::printf("[p3] data/tetra.obj 未找到\n"); return 1; }

    // 拓扑统计（L11）：V - E + F，闭合流形应为 2
    auto stat = [](const char* name, const Mesh& m) {
        long chi = (long)m.v.size() - (long)m.edgeCount() + (long)m.f.size();
        std::printf("[p3] %-6s V=%zu E=%zu F=%zu  V-E+F=%ld\n", name, m.v.size(),
                    m.edgeCount(), m.f.size(), chi);
    };
    stat("tetra", tetra);   // 共享顶点 -> 4-6+4 = 2 ✓
    stat("cube", cube);     // 每面独立顶点（24）-> 不为 2；"顶点焊接(weld)" 是网格处理第一步（L11）

    render(640, 640, false, cube, tetra, "mesh.ppm");
    render(640, 640, true, cube, tetra, "csg.ppm");
    return 0;
}
