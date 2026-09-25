// p1: 向量/矩阵库 + 变换演示（GAMES101 L02–L06）
// 输出两张 PPM（P3 文本）：
//   transforms_2d.ppm : 2D "小房子" 的 8 种仿射变换（L03–L04）
//   mvp_cube.ppm      : 立方体绕 y 轴旋转 + lookAt + 透视投影的线框（L05–L06）
// 运行：bin/p1（无需参数）。仅标准库，C++17。
#include "geom.hpp"

#include <cstdio>
#include <cstdint>
#include <string>
#include <vector>

using namespace g101;

// ---------- 极简画布与 PPM 输出 ----------
struct Canvas {
    int w, h;
    std::vector<uint8_t> rgb;  // row-major, 3 通道
    explicit Canvas(int w_, int h_) : w(w_), h(h_), rgb(size_t(w_) * h_ * 3, 0) {
        clear({24, 26, 34});
    }
    void clear(const Vec3& c) {
        for (size_t i = 0; i < size_t(w) * h; ++i) {
            rgb[i * 3] = uint8_t(c.x * 255);
            rgb[i * 3 + 1] = uint8_t(c.y * 255);
            rgb[i * 3 + 2] = uint8_t(c.z * 255);
        }
    }
    void setPixel(int x, int y, const Vec3& c) {
        if (x < 0 || y < 0 || x >= w || y >= h) return;
        size_t i = (size_t(y) * w + x) * 3;
        rgb[i] = uint8_t(c.x * 255); rgb[i + 1] = uint8_t(c.y * 255); rgb[i + 2] = uint8_t(c.z * 255);
    }
    // Bresenham 直线（L10 图元：线的光栅化入门版）
    void line(Vec2 a, Vec2 b, const Vec3& c) {
        int x0 = int(a.x), y0 = int(a.y), x1 = int(b.x), y1 = int(b.y);
        int dx = std::abs(x1 - x0), dy = -std::abs(y1 - y0);
        int sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1;
        for (int err = dx + dy;;) {
            setPixel(x0, y0, c);
            if (x0 == x1 && y0 == y1) break;
            int e2 = 2 * err;
            if (e2 >= dy) { err += dy; x0 += sx; }
            if (e2 <= dx) { err += dx; y0 += sy; }
        }
    }
    bool writePPM(const std::string& path) const {
        FILE* f = std::fopen(path.c_str(), "wb");
        if (!f) return false;
        std::fprintf(f, "P3\n%d %d\n255\n", w, h);
        for (int y = 0; y < h; ++y) {
            for (int x = 0; x < w; ++x) {
                size_t i = (size_t(y) * w + x) * 3;
                std::fprintf(f, "%d %d %d\n", rgb[i], rgb[i + 1], rgb[i + 2]);
            }
        }
        std::fclose(f);
        return true;
    }
};

// ---------- 2D 演示：小房子 ----------
// 模型坐标：以原点为中心的房子轮廓（线段对列表）
static const Vec2 kHouse[][2] = {
    {{-10, -10}, {10, -10}}, {{10, -10}, {10, 5}}, {{10, 5}, {-10, 5}},
    {{-10, 5}, {-10, -10}},  {{-10, 5}, {0, 18}},  {{0, 18}, {10, 5}},
    {{-3, -10}, {-3, -2}},   {{-3, -2}, {3, -2}},  {{3, -2}, {3, -10}},  // 门
};

static Vec2 apply2D(const Mat4& m, Vec2 p) {  // 2D 齐次：点在 z=0, w=1
    Vec4 q = m * Vec4(p.x, p.y, 0.f, 1.f);
    return {q.x / q.w, q.y / q.w};
}

static void demo2D() {
    constexpr int W = 800, H = 800;
    Canvas cv(W, H);
    const float s = 8.f;  // 模型单位 -> 像素
    struct Cell { const char* tag; Mat4 m; Vec3 color; };
    std::vector<Cell> cells = {
        {"I",       Mat4::identity(),                                          {0.95f, 0.95f, 0.95f}},
        {"T(20,10)", translation({20, 10, 0}),                                 {1.00f, 0.55f, 0.20f}},
        {"R(45)",    rotateZ(deg2rad(45)),                                     {0.30f, 0.85f, 0.90f}},
        {"S(1.5,.7)", scaling({1.5f, 0.7f, 1}),                                {0.60f, 1.00f, 0.40f}},
        {"T.R.S",   translation({15, -15, 0}) * rotateZ(deg2rad(30)) * scaling({1.3f, 1.3f, 1}), {0.95f, 0.35f, 0.65f}},
        {"R@(-5,10)", rotateAbout({-5, 10, 0}, deg2rad(-60)),                  {0.75f, 0.55f, 1.00f}},
        {"Shear",   [] { Mat4 m = Mat4::identity(); m.m[0][1] = 0.6f; return m; }(), {0.50f, 1.00f, 0.80f}},
        {"R(90)T",  rotateZ(deg2rad(90)) * translation({20, 0, 0}),            {1.00f, 0.90f, 0.30f}},
    };
    for (size_t idx = 0; idx < cells.size(); ++idx) {
        int col = int(idx) % 4, row = int(idx) / 4;
        float cx = (col + 0.5f) * W / 4, cy = (row + 0.5f) * H / 4;  // 格子中心（屏幕 y 向下）
        const Mat4& m = cells[idx].m;
        // 先变换模型，再映射到格子：世界(y 上) -> 屏幕(y 下)
        auto toScreen = [&](Vec2 p) {
            Vec2 t = apply2D(m, p);
            return Vec2(cx + t.x * s, cy - t.y * s);
        };
        for (auto& seg : kHouse) cv.line(toScreen(seg[0]), toScreen(seg[1]), cells[idx].color);
    }
    cv.writePPM("transforms_2d.ppm");
    std::printf("[p1] wrote transforms_2d.ppm (8 种 2D 仿射变换)\n");
}

// ---------- 3D 演示：立方体 MVP 线框 ----------
static void demoMVP() {
    constexpr int W = 800, H = 800;
    Canvas cv(W, H);

    Vec3 cubeV[8] = {
        {-1, -1, -1}, {1, -1, -1}, {1, 1, -1}, {-1, 1, -1},
        {-1, -1, 1},  {1, -1, 1},  {1, 1, 1},  {-1, 1, 1},
    };
    // 12 条边（索引对）
    static const int edges[12][2] = {
        {0,1},{1,2},{2,3},{3,0}, {4,5},{5,6},{6,7},{7,4}, {0,4},{1,5},{2,6},{3,7},
    };
    // 4 个相位：模型旋转 + 固定相机
    Vec3 eye(0, 1.2f, 6);
    Mat4 view = lookAt(eye, {0, 0, 0}, {0, 1, 0});
    Mat4 proj = perspective(deg2rad(40), 1.f /*aspect*/, 0.5f, 20.f);

    auto project = [&](const Mat4& model, int i) -> Vec2 {
        Vec4 clip = proj * view * model * Vec4(cubeV[i], 1.f);
        Vec3 ndc = clip.perspDiv();  // NDC，透视除法（L06）
        return {ndc.x * 0.5f * W + W * 0.5f, (1 - (ndc.y * 0.5f + 0.5f)) * H};
    };

    for (int k = 0; k < 4; ++k) {
        float cx = (k % 2 + 0.5f) * W / 2, cy = (k / 2 + 0.5f) * H / 2;
        float ang = kPi * 0.25f * k + 0.2f;
        // 模型矩阵：先缩放（压扁演示非均匀），再绕 y 旋转，再微绕 x（L04 顺序）
        Mat4 model = translation({(k % 2 == 0 ? -0.12f : 0.12f), 0, 0}) *
                     rotateY(ang) * rotateX(0.18f) * scaling({0.9f, 0.6f, 0.9f});
        Vec3 col = k == 0 ? Vec3{0.95f, 0.95f, 0.95f}
                 : k == 1 ? Vec3{1.00f, 0.55f, 0.20f}
                 : k == 2 ? Vec3{0.30f, 0.85f, 0.90f}
                          : Vec3{0.95f, 0.35f, 0.65f};
        for (auto& e : edges) {
            Vec2 a = project(model, e[0]), b = project(model, e[1]);
            // 把每个投影点平移到所属子格中心附近（粗裁剪，只画近处边的可见性留给 z-buffer 讲）
            auto shift = [&](Vec2 p) {
                float px = p.x * 0.32f + cx, py = p.y * 0.32f + cy;
                return Vec2{px, py};
            };
            cv.line(shift(a), shift(b), col);
        }
    }
    cv.writePPM("mvp_cube.ppm");
    std::printf("[p1] wrote mvp_cube.ppm (MVP + 透视除法线框，4 个旋转相位)\n");

    // 顺带验证 L05 刚体求逆：view * inverseRigid(view) ≈ I
    Mat4 id = view * inverseRigid(view);
    float err = 0;
    Mat4 I = Mat4::identity();
    for (int i = 0; i < 4; ++i) for (int j = 0; j < 4; ++j) err = std::max(err, std::abs(id.m[i][j] - I.m[i][j]));
    std::printf("[p1] inverseRigid(view)*view 最大偏差 = %.3e（应≈0）\n", err);
}

int main() {
    demo2D();
    demoMVP();
    return 0;
}
