// p2 — 软件光栅化器（GAMES101 L06–L09, L12, L14）
// 功能：三角形填充（重心坐标）+ z-buffer 深度测试 + 透视 correct 插值对比 +
//       Blinn-Phong 逐像素着色 + 程序化棋盘纹理（含纹理畸变可视化）。
// 输出（P6 二进制 PPM）：
//   cube_raster.ppm        800x800 主图（透视 correct 开）
//   cube_compare.ppm       800x400 左:线性插值(错) 右:透视correct(对)
//   cube_ssaa.ppm          400x400 4x4 超采样抗锯齿 vs 无 AA（左右对比）
// 仅标准库，C++17。
#include "geom.hpp"

#include <cstdio>
#include <cstdint>
#include <cstring>
#include <array>
#include <string>
#include <vector>
#include <limits>

using namespace g101;

// ---------- 帧缓冲 ----------
struct Frame {
    int w, h;
    std::vector<float> color;  // RGB 线性累积
    std::vector<float> zbuf;   // NDC 深度 [-1,1]，越小越近
    explicit Frame(int w_, int h_)
        : w(w_), h(h_), color(size_t(w_) * h_ * 3, 0.f),
          zbuf(size_t(w_) * h_, std::numeric_limits<float>::infinity()) {}
    void reset() {
        std::fill(color.begin(), color.end(), 0.f);
        std::fill(zbuf.begin(), zbuf.end(), std::numeric_limits<float>::infinity());
    }
    bool writePPM(const std::string& path, float gamma = 2.2f) const {
        FILE* f = std::fopen(path.c_str(), "wb");
        if (!f) return false;
        std::fprintf(f, "P6\n%d %d\n255\n", w, h);
        std::vector<uint8_t> row(size_t(w) * 3);
        for (int y = 0; y < h; ++y) {
            for (int x = 0; x < w; ++x) {
                size_t i = (size_t(y) * w + x) * 3;
                for (int c = 0; c < 3; ++c) {
                    float v = color[i + c];
                    v = v <= 0.f ? 0.f : (v >= 1.f ? 1.f : std::pow(v, 1.f / gamma));  // L13 gamma
                    row[i + c] = uint8_t(v * 255.f + 0.5f);
                }
            }
            std::fwrite(row.data(), 1, row.size(), f);
        }
        std::fclose(f);
        return true;
    }
};

// ---------- 三角形顶点属性 ----------
struct Vertex {
    Vec3 pos;     // 模型空间
    Vec3 normal;  // 模型空间（未变换）
    Vec2 uv;
};
struct ScreenVert {  // 屏幕空间 + 插值属性
    float x = 0.f, y = 0.f, z = 0.f;  // z: NDC 深度
    float w = 1.f;                    // 视空间 -z（透视 correct 权重，L06/L12）
    Vec3 n{0, 0, 0};                  // 世界空间法线
    Vec2 uv{0, 0};
};

// ---------- 模型矩阵 ----------
static Mat4 modelMatrix(float degY, float degX) {
    return rotateY(deg2rad(degY)) * rotateX(deg2rad(degX));
}

// ---------- 视锥裁剪（齐次空间，6 平面 Sutherland-Hodgman）----------
struct HomVert { Vec4 c; ScreenVert s; };  // s 中 x,y,z 先存"裁剪前"信息占位，除法后填

static bool inside(const Vec4& c) {
    return c.w + c.x > -1e-5f && c.w - c.x > -1e-5f &&
           c.w + c.y > -1e-5f && c.w - c.y > -1e-5f &&
           c.w + c.z > -1e-5f && c.w - c.z > -1e-5f;
}
static Vec4 lerpV(const Vec4& a, const Vec4& b, float t) {
    return {a.x + (b.x - a.x) * t, a.y + (b.y - a.y) * t,
            a.z + (b.z - a.z) * t, a.w + (b.w - a.w) * t};
}
static ScreenVert lerpS(const ScreenVert& a, const ScreenVert& b, float t) {
    ScreenVert r;
    r.x = a.x + (b.x - a.x) * t; r.y = a.y + (b.y - a.y) * t; r.z = a.z + (b.z - a.z) * t;
    r.w = a.w + (b.w - a.w) * t;
    r.n = Vec3::lerp(a.n, b.n, t);
    r.uv = {a.uv.x + (b.uv.x - a.uv.x) * t, a.uv.y + (b.uv.y - a.uv.y) * t};
    return r;
}

// 把齐次裁剪空间点映射为 ScreenVert（含 viewport）
static ScreenVert toScreen(const Vec4& clip, int W, int H) {
    Vec3 ndc = clip.perspDiv();
    ScreenVert s;
    s.x = (ndc.x * 0.5f + 0.5f) * W;
    s.y = (1 - (ndc.y * 0.5f + 0.5f)) * H;  // 翻转 y（屏幕 y 向下）
    s.z = ndc.z;
    s.w = clip.w;  // = 视空间 -z
    return s;
}

// 裁剪一个三角形（输入为带屏幕属性+齐次坐标的三元组），输出 0–2 个三角形
static void clipTriangle(const std::array<HomVert, 3>& tri, int W, int H,
                         std::vector<std::array<ScreenVert, 3>>& outTris) {
    // 对 6 个平面依次裁剪。为简洁使用统一写法：先求交点列表。
    std::vector<HomVert> poly;
    for (int p = 0; p < 6; ++p) {
        std::vector<HomVert> src = poly.empty() ? std::vector<HomVert>(tri.begin(), tri.end()) : poly;
        poly.clear();
        size_t n = src.size();
        for (size_t i = 0; i < n; ++i) {
            const HomVert& a = src[i];
            const HomVert& b = src[(i + 1) % n];
            auto test = [&](const Vec4& c) -> bool {
                switch (p) {
                    case 0: return c.x + c.w >= -1e-5f;  // left
                    case 1: return c.w - c.x >= -1e-5f;  // right
                    case 2: return c.y + c.w >= -1e-5f;  // bottom
                    case 3: return c.w - c.y >= -1e-5f;  // top
                    case 4: return c.z + c.w >= -1e-5f;  // near
                    default: return c.w - c.z >= -1e-5f; // far
                }
            };
            bool ain = test(a.c), bin = test(b.c);
            if (ain) poly.push_back(a);
            if (ain != bin) {
                // 解平面 c[p/2] ± c.w = 0 上线段参数 t
                float t = 0.f;
                float fa = 0, fb = 0;
                switch (p) {
                    case 0: fa = a.c.x + a.c.w; fb = b.c.x + b.c.w; break;
                    case 1: fa = a.c.w - a.c.x; fb = b.c.w - b.c.x; break;
                    case 2: fa = a.c.y + a.c.w; fb = b.c.y + b.c.w; break;
                    case 3: fa = a.c.w - a.c.y; fb = b.c.w - b.c.y; break;
                    case 4: fa = a.c.z + a.c.w; fb = b.c.z + b.c.w; break;
                    default: fa = a.c.w - a.c.z; fb = b.c.w - b.c.z; break;
                }
                float d = fa - fb;
                t = std::abs(d) < 1e-9f ? 0.f : fa / d;
                t = std::min(1.f, std::max(0.f, t));
                HomVert h;
                h.c = lerpV(a.c, b.c, t);
                h.s = lerpS(a.s, b.s, t);  // 屏幕属性按齐次插值（近似；w>0 段内足够）
                poly.push_back(h);
            }
        }
        if (poly.size() < 3) { outTris.clear(); return; }
    }
    // 扇形三角化 + 齐次->屏幕
    std::vector<ScreenVert> scr(poly.size());
    for (size_t i = 0; i < poly.size(); ++i) {
        ScreenVert s = toScreen(poly[i].c, W, H);
        s.n = poly[i].s.n; s.uv = poly[i].s.uv; s.w = poly[i].c.w;
        scr[i] = s;
    }
    for (size_t i = 1; i + 1 < scr.size(); ++i) {
        std::array<ScreenVert, 3> t{scr[0], scr[i], scr[i + 1]};
        outTris.push_back(t);
    }
}

// ---------- 纹理与光照 ----------
static Vec3 checkerTexture(Vec2 uv) {  // 程序化 8x8 棋盘（L12）
    float su = std::floor(uv.x * 8.f), sv = std::floor(uv.y * 8.f);
    bool even = (int(su + sv) % 2) == 0;
    return even ? Vec3{0.85f, 0.16f, 0.14f} : Vec3{0.92f, 0.88f, 0.80f};
}

static Vec3 blinnPhong(const Vec3& n, const Vec3& wo, const Vec3& albedo,
                       const Vec3& lightPos, const Vec3& eyePos) {  // L14
    Vec3 nn = n.normalized();
    Vec3 lo = (lightPos - wo).normalized();          // 指向光
    Vec3 v = (eyePos - wo).normalized();             // 指向眼
    Vec3 h = (lo + v).normalized();                  // 半角向量
    float ndl = std::max(0.f, nn.dot(lo));
    float ndh = std::max(0.f, nn.dot(h));
    const Vec3 Kd = albedo * 0.75f;
    const Vec3 Ks = {0.6f, 0.6f, 0.6f};
    const float shininess = 80.f;
    float atten = 3.2f / (lightPos - wo).length();   // 简化 1/r 衰减
    Vec3 amb = albedo * 0.12f;
    Vec3 dif = Kd * ndl * atten;
    Vec3 spc = Ks * std::pow(ndh, shininess) * (ndl > 0 ? 1.f : 0.f) * atten;
    return amb + dif + spc;
}

// ---------- 光栅化一个三角形（L08 + z-buffer L07 + correct 插值 L12）----------
struct RasterOptions {
    bool perspectiveCorrect = true;
    int ssSamples = 1;  // n x n 超采样（L09）
    float offsetX = 0.f, offsetY = 0.f;  // 子像素偏移
    Vec3 lightPos{4, 6, 6};
    Vec3 eyePos{0, 1.2f, 6};
};

static inline float edgeFn(const Vec2& a, const Vec2& b, const Vec2& c) {  // 2D 叉积（L08）
    return (c.x - a.x) * (b.y - a.y) - (b.x - a.x) * (c.y - a.y);
}

static void rasterizeTriangle(Frame& fb, const ScreenVert& a, const ScreenVert& b,
                              const ScreenVert& c, const RasterOptions& opt) {
    Vec2 A{a.x, a.y}, B{b.x, b.y}, C{c.x, c.y};
    float area = edgeFn(A, B, C);
    if (area == 0.f) return;
    const float areaAbs = std::abs(area);
    // 有向面积 < 0：顶点序在屏幕上顺时针；本 demo 双面都画，因此边函数统一按同一侧判定
    const float sgn = area > 0 ? 1.f : -1.f;

    int n = opt.ssSamples;
    float minX = std::min({A.x, B.x, C.x}), maxX = std::max({A.x, B.x, C.x});
    float minY = std::min({A.y, B.y, C.y}), maxY = std::max({A.y, B.y, C.y});
    int x0 = std::max(0, int(std::floor(minX))), x1 = std::min(fb.w - 1, int(std::ceil(maxX)));
    int y0 = std::max(0, int(std::floor(minY))), y1 = std::min(fb.h - 1, int(std::ceil(maxY)));

    for (int py = y0; py <= y1; ++py) {
        for (int px = x0; px <= x1; ++px) {
            size_t fidx = size_t(py) * fb.w + px;
            float bestZ = std::numeric_limits<float>::infinity();
            Vec3 bestCol{0, 0, 0};
            for (int sy = 0; sy < n; ++sy) {
                for (int sx = 0; sx < n; ++sx) {
                    // 采样点：像素中心 + 子样本网格（L08 约定 / L09 超采样）
                    Vec2 P{px + (sx + 0.5f) / n, py + (sy + 0.5f) / n};
                    // 重心坐标（边函数，L08）
                    float al = edgeFn(B, C, P) * sgn, be = edgeFn(C, A, P) * sgn, ga = edgeFn(A, B, P) * sgn;
                    const float eps = -1e-4f * areaAbs;
                    if (al < eps || be < eps || ga < eps) continue;  // 外侧
                    al /= areaAbs; be /= areaAbs; ga /= areaAbs;

                    // 深度：屏幕空间线性插值（z-buffer 用，L07）
                    float z = al * a.z + be * b.z + ga * c.z;
                    if (z >= bestZ || z >= fb.zbuf[fidx]) continue;  // 更深的子样本跳过

                    // 属性插值：线性 or 透视 correct（L06/L08/L12）
                    float w = al * a.w + be * b.w + ga * c.w;  // 视深度（≈ -z_view）
                    float al2, be2, ga2;
                    if (opt.perspectiveCorrect) {
                        al2 = al / a.w; be2 = be / b.w; ga2 = ga / c.w;
                        float sum = al2 + be2 + ga2;
                        al2 /= sum; be2 /= sum; ga2 /= sum;
                    } else {
                        al2 = al; be2 = be; ga2 = ga;
                    }
                    Vec3 nrm = a.n * al2 + b.n * be2 + c.n * ga2;
                    Vec2 uv{a.uv.x * al2 + b.uv.x * be2 + c.uv.x * ga2,
                            a.uv.y * al2 + b.uv.y * be2 + c.uv.y * ga2};
                    // 该像素对应世界点：由视深度 w 沿像素射线反推（近似视场角正切 ~tan20°）
                    float ndcx = (P.x / fb.w) * 2 - 1, ndcy = 1 - (P.y / fb.h) * 2;
                    Vec3 dir = (Vec3{ndcx * 0.42f * (fb.w / float(fb.h)), ndcy * 0.42f, -1.f}).normalized();
                    Vec3 worldP = opt.eyePos + dir * (w > 0.001f ? w : 0.001f);
                    Vec3 albedo = checkerTexture(uv);
                    bestCol = blinnPhong(nrm, worldP, albedo, opt.lightPos, opt.eyePos);
                    bestZ = z;
                }
            }
            if (bestZ < fb.zbuf[fidx]) {  // 整像素取最近子样本（demo 简化，见 README）
                fb.zbuf[fidx] = bestZ;
                size_t i = fidx * 3;
                fb.color[i] = bestCol.x; fb.color[i + 1] = bestCol.y; fb.color[i + 2] = bestCol.z;
            }
        }
    }
}

// ---------- 构建单位立方体（2x2x2，中心原点）----------
static std::vector<Vertex> makeCube() {
    auto face = [](Vec3 a, Vec3 b, Vec3 c, Vec3 d, Vec3 n) {
        std::vector<Vertex> v;
        auto mk = [&](Vec3 p, Vec2 uv) { v.push_back({p * 0.5f, n, uv}); };
        mk(a, {0, 0}); mk(b, {1, 0}); mk(c, {1, 1});
        mk(a, {0, 0}); mk(c, {1, 1}); mk(d, {0, 1});
        return v;
    };
    std::vector<Vertex> verts;
    for (auto& f : { face({-1,-1,1},{1,-1,1},{1,1,1},{-1,1,1}, {0,0,1}),
                     face({1,-1,-1},{-1,-1,-1},{-1,1,-1},{1,1,-1}, {0,0,-1}),
                     face({1,-1,1},{1,-1,-1},{1,1,-1},{1,1,1}, {1,0,0}),
                     face({-1,-1,-1},{-1,-1,1},{-1,1,1},{-1,1,-1}, {-1,0,0}),
                     face({-1,1,1},{1,1,1},{1,1,-1},{-1,1,-1}, {0,1,0}),
                     face({-1,-1,-1},{1,-1,-1},{1,-1,1},{-1,-1,1}, {0,-1,0}) })
        verts.insert(verts.end(), f.begin(), f.end());
    return verts;
}

// 把一个模型变换后送入管线：MVP -> 裁剪 -> 光栅化
static void drawMesh(Frame& fb, const std::vector<Vertex>& verts, const Mat4& model,
                     const Mat4& view, const Mat4& proj, const RasterOptions& opt) {
    Mat4 mv = view * model;
    Mat4 mvp = proj * mv;
    // 法线用逆转置（L14）。模型仿射部分 3x3 求逆+转置：
    float a00 = model.m[0][0], a01 = model.m[0][1], a02 = model.m[0][2];
    float a10 = model.m[1][0], a11 = model.m[1][1], a12 = model.m[1][2];
    float a20 = model.m[2][0], a21 = model.m[2][1], a22 = model.m[2][2];
    float det = a00 * (a11 * a22 - a12 * a21) - a01 * (a10 * a22 - a12 * a20) + a02 * (a10 * a21 - a11 * a20);
    float invdet = std::abs(det) > 1e-12f ? 1.f / det : 0.f;
    auto inv3 = [&](int r, int c) {
        // 伴随矩阵 / det（逆的 (r,c) 元素）
        float cof[3][3];
        cof[0][0] = a11 * a22 - a12 * a21; cof[0][1] = -(a10 * a22 - a12 * a20); cof[0][2] = a10 * a21 - a11 * a20;
        cof[1][0] = -(a01 * a22 - a02 * a21); cof[1][1] = a00 * a22 - a02 * a20; cof[1][2] = -(a00 * a21 - a01 * a20);
        cof[2][0] = a01 * a12 - a02 * a11; cof[2][1] = -(a00 * a12 - a02 * a10); cof[2][2] = a00 * a11 - a01 * a10;
        return cof[c][r] * invdet;  // 转置 -> 逆转置
    };
    for (size_t i = 0; i + 2 < verts.size(); i += 3) {
        std::array<HomVert, 3> tri;
        const Vertex* vv[3] = {&verts[i], &verts[i + 1], &verts[i + 2]};
        for (int k = 0; k < 3; ++k) {
            Vec4 clip = mvp * Vec4(vv[k]->pos, 1.f);
            ScreenVert s;
            s.n = {inv3(0, 0) * vv[k]->normal.x + inv3(0, 1) * vv[k]->normal.y + inv3(0, 2) * vv[k]->normal.z,
                   inv3(1, 0) * vv[k]->normal.x + inv3(1, 1) * vv[k]->normal.y + inv3(1, 2) * vv[k]->normal.z,
                   inv3(2, 0) * vv[k]->normal.x + inv3(2, 1) * vv[k]->normal.y + inv3(2, 2) * vv[k]->normal.z};
            s.uv = vv[k]->uv;
            tri[k] = {clip, s};
        }
        std::vector<std::array<ScreenVert, 3>> tris;
        clipTriangle(tri, fb.w, fb.h, tris);
        for (auto& t : tris) rasterizeTriangle(fb, t[0], t[1], t[2], opt);
    }
}

int main() {
    auto cube = makeCube();
    Vec3 eye(0, 1.2f, 6);
    Mat4 view = lookAt(eye, {0, 0, 0}, {0, 1, 0});
    Mat4 proj = perspective(deg2rad(40), 1.f, 0.5f, 20.f);
    Mat4 model = modelMatrix(25, -15);

    RasterOptions opt; opt.eyePos = eye;

    // 1) 主图
    {
        Frame fb(800, 800);
        drawMesh(fb, cube, model, view, proj, opt);
        fb.writePPM("cube_raster.ppm");
        std::printf("[p2] cube_raster.ppm (Blinn-Phong + z-buffer + correct 插值)\n");
    }
    // 2) 透视 correct 对比
    {
        Frame fb(800, 400);
        RasterOptions a = opt; a.perspectiveCorrect = false;
        Frame left(400, 400), right(400, 400);
        Mat4 side = translation({-1.3f, 0, 0}) * model;
        drawMesh(left, cube, side, view, proj, a);
        drawMesh(right, cube, model, view, proj, opt);
        for (int y = 0; y < 400; ++y)
            for (int x = 0; x < 400; ++x) {
                size_t si = (size_t(y) * 400 + x) * 3;
                size_t dl = (size_t(y) * 800 + x) * 3, dr = (size_t(y) * 800 + 400 + x) * 3;
                for (int c = 0; c < 3; ++c) {
                    fb.color[dl + c] = left.color[si + c];
                    fb.color[dr + c] = right.color[si + c];
                }
            }
        fb.writePPM("cube_compare.ppm");
        std::printf("[p2] cube_compare.ppm (左:线性插值-错 / 右:perspective correct)\n");
    }
    // 3) 超采样 AA 对比
    {
        Frame raw(400, 400), ss(400, 400);
        RasterOptions a = opt; a.ssSamples = 1;
        RasterOptions b = opt; b.ssSamples = 4;
        Mat4 m2 = modelMatrix(40, -20) * translation({0.6f, 0, 0});
        drawMesh(raw, cube, m2, view, proj, a);
        drawMesh(ss, cube, m2, view, proj, b);
        Frame fb(800, 400);
        for (int y = 0; y < 400; ++y)
            for (int x = 0; x < 400; ++x) {
                size_t si = (size_t(y) * 400 + x) * 3;
                for (int c = 0; c < 3; ++c) {
                    fb.color[(size_t(y) * 800 + x) * 3 + c] = raw.color[si + c];
                    fb.color[(size_t(y) * 800 + 400 + x) * 3 + c] = ss.color[si + c];
                }
            }
        fb.writePPM("cube_ssaa.ppm");
        std::printf("[p2] cube_ssaa.ppm (左:1x / 右:4x4 超采样)\n");
    }
    return 0;
}
