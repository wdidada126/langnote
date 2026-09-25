// geom.hpp — GAMES101 迷你几何/线性代数库（L02–L06）
// 仅标准库，C++17。行约定：列向量 v' = M * v；矩阵元素 m[r][c]（行主序）。
#pragma once
#include <cmath>
#include <algorithm>

namespace g101 {

constexpr float kPi = 3.14159265358979323846f;
inline float deg2rad(float d) { return d * kPi / 180.0f; }

struct Vec2 {
    float x = 0.f, y = 0.f;
    Vec2() = default;
    Vec2(float x_, float y_) : x(x_), y(y_) {}
    Vec2 operator+(const Vec2& o) const { return {x + o.x, y + o.y}; }
    Vec2 operator-(const Vec2& o) const { return {x - o.x, y - o.y}; }
    Vec2 operator*(float s) const { return {x * s, y * s}; }
};

struct Vec3 {
    float x = 0.f, y = 0.f, z = 0.f;
    Vec3() = default;
    Vec3(float x_, float y_, float z_) : x(x_), y(y_), z(z_) {}
    Vec3 operator+(const Vec3& o) const { return {x + o.x, y + o.y, z + o.z}; }
    Vec3 operator-(const Vec3& o) const { return {x - o.x, y - o.y, z - o.z}; }
    Vec3 operator*(float s) const { return {x * s, y * s, z * s}; }
    Vec3 operator/(float s) const { return {x / s, y / s, z / s}; }
    Vec3 operator-() const { return {-x, -y, -z}; }
    Vec3& operator+=(const Vec3& o) { x += o.x; y += o.y; z += o.z; return *this; }
    float dot(const Vec3& o) const { return x * o.x + y * o.y + z * o.z; }
    Vec3 cross(const Vec3& o) const {
        return {y * o.z - z * o.y, z * o.x - x * o.z, x * o.y - y * o.x};
    }
    float length() const { return std::sqrt(dot(*this)); }
    Vec3 normalized() const {
        float l = length();
        return l > 1e-12f ? (*this) / l : Vec3{0, 0, 0};
    }
    static Vec3 lerp(const Vec3& a, const Vec3& b, float t) { return a * (1 - t) + b * t; }
};
inline Vec3 operator*(float s, const Vec3& v) { return v * s; }

struct Vec4 {
    float x = 0.f, y = 0.f, z = 0.f, w = 0.f;
    Vec4() = default;
    Vec4(float x_, float y_, float z_, float w_) : x(x_), y(y_), z(z_), w(w_) {}
    explicit Vec4(const Vec3& v, float w_) : x(v.x), y(v.y), z(v.z), w(w_) {}
    Vec3 xyz() const { return {x, y, z}; }
    // 透视除法（L03/L06）：w != 1 时还原
    Vec3 perspDiv() const {
        float iw = std::abs(w) > 1e-12f ? 1.0f / w : 0.0f;
        return {x * iw, y * iw, z * iw};
    }
};

struct Mat4 {
    float m[4][4]{};  // m[row][col]，零初始化

    static Mat4 identity() {
        Mat4 r;
        for (int i = 0; i < 4; ++i) r.m[i][i] = 1.f;
        return r;
    }
};

inline Mat4 operator*(const Mat4& a, const Mat4& b) {  // C = A*B（先 B 后 A，L03）
    Mat4 c;
    for (int r = 0; r < 4; ++r)
        for (int col = 0; col < 4; ++col) {
            float s = 0.f;
            for (int k = 0; k < 4; ++k) s += a.m[r][k] * b.m[k][col];
            c.m[r][col] = s;
        }
    return c;
}

inline Vec4 operator*(const Mat4& a, const Vec4& v) {
    return {a.m[0][0] * v.x + a.m[0][1] * v.y + a.m[0][2] * v.z + a.m[0][3] * v.w,
            a.m[1][0] * v.x + a.m[1][1] * v.y + a.m[1][2] * v.z + a.m[1][3] * v.w,
            a.m[2][0] * v.x + a.m[2][1] * v.y + a.m[2][2] * v.z + a.m[2][3] * v.w,
            a.m[3][0] * v.x + a.m[3][1] * v.y + a.m[3][2] * v.z + a.m[3][3] * v.w};
}

// 把 Vec3 当"点"（w=1）或"向量"（w=0）变换
inline Vec3 mulPoint(const Mat4& a, const Vec3& p) { return (a * Vec4(p, 1.f)).xyz(); }
inline Vec3 mulVector(const Mat4& a, const Vec3& v) { return (a * Vec4(v, 0.f)).xyz(); }

// ---- 基本变换（L04）----
inline Mat4 translation(const Vec3& t) {
    Mat4 r = Mat4::identity();
    r.m[0][3] = t.x; r.m[1][3] = t.y; r.m[2][3] = t.z;
    return r;
}
inline Mat4 scaling(const Vec3& s) {
    Mat4 r = Mat4::identity();
    r.m[0][0] = s.x; r.m[1][1] = s.y; r.m[2][2] = s.z;
    return r;
}
inline Mat4 rotateZ(float rad) {  // 右手系，逆时针（从 +z 俯视 xy 平面）
    Mat4 r = Mat4::identity();
    float c = std::cos(rad), s = std::sin(rad);
    r.m[0][0] = c;  r.m[0][1] = -s;
    r.m[1][0] = s;  r.m[1][1] = c;
    return r;
}
inline Mat4 rotateX(float rad) {
    Mat4 r = Mat4::identity();
    float c = std::cos(rad), s = std::sin(rad);
    r.m[1][1] = c;  r.m[1][2] = -s;
    r.m[2][1] = s;  r.m[2][2] = c;
    return r;
}
inline Mat4 rotateY(float rad) {
    Mat4 r = Mat4::identity();
    float c = std::cos(rad), s = std::sin(rad);
    r.m[0][0] = c;   r.m[0][2] = s;
    r.m[2][0] = -s;  r.m[2][2] = c;
    return r;
}
// 绕原点平移 t 的特定点旋转（L04 技巧：T(c) R T(-c)）
inline Mat4 rotateAbout(const Vec3& c, float rad) {
    return translation(c) * rotateZ(rad) * translation(-c);
}

// ---- 视图 / 投影（L05–L06）----
inline Mat4 lookAt(const Vec3& eye, const Vec3& center, const Vec3& up) {
    Vec3 d = (center - eye).normalized();   // 视线
    Vec3 r = d.cross(up).normalized();      // 右
    Vec3 u = r.cross(d);                    // 上
    Mat4 v = Mat4::identity();
    v.m[0][0] = r.x;  v.m[0][1] = r.y;  v.m[0][2] = r.z;  v.m[0][3] = -r.dot(eye);
    v.m[1][0] = u.x;  v.m[1][1] = u.y;  v.m[1][2] = u.z;  v.m[1][3] = -u.dot(eye);
    v.m[2][0] = -d.x; v.m[2][1] = -d.y; v.m[2][2] = -d.z; v.m[2][3] = d.dot(eye);
    return v;
}
// 正交投影：视景体 [l,r]x[b,t]x[-f,-n] -> NDC [-1,1]^3（z 取负，远为正深度，L06）
inline Mat4 ortho(float l, float r, float b, float t, float n, float f) {
    Mat4 m = Mat4::identity();
    m.m[0][0] = 2 / (r - l);      m.m[0][3] = -(r + l) / (r - l);
    m.m[1][1] = 2 / (t - b);      m.m[1][3] = -(t + b) / (t - b);
    m.m[2][2] = -2 / (f - n);     m.m[2][3] = -(f + n) / (f - n);
    return m;
}
// 透视：先把视锥压成长方体（w = -z），再正交（L06 推导）
inline Mat4 perspective(float fovyRad, float aspect, float n, float f) {
    float top = n * std::tan(fovyRad / 2), right = aspect * top;
    Mat4 persp2ortho = Mat4::identity();
    persp2ortho.m[3][2] = -1.f;
    return ortho(-right, right, -top, top, n, f) * persp2ortho;
}

// 刚体变换求逆（L05 捷径）：M = T(t)R -> M^-1 = [R^T | -R^T t]
inline Mat4 inverseRigid(const Mat4& m) {
    Mat4 r = Mat4::identity();
    for (int i = 0; i < 3; ++i)
        for (int j = 0; j < 3; ++j) r.m[i][j] = m.m[j][i];  // R^T
    Vec3 t{m.m[0][3], m.m[1][3], m.m[2][3]};
    Vec3 rt = mulVector(r, t);
    r.m[0][3] = -rt.x; r.m[1][3] = -rt.y; r.m[2][3] = -rt.z;
    return r;
}

}  // namespace g101
