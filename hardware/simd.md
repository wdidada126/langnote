# simd

single instruction, multiple data

SIMD全称Single Instruction Multiple Data，单指令多数据流，能够复制多个操作数，并把它们打包在大型寄存器的一组指令集。

gedit code.c
gcc -O1 -S code.c（O为大写o）
-O1代表采用第一级优化，运行这条指令将产生code.s的汇编文件。
cat code.s
将会包含以下汇编代码文本。
gcc -O1 -c code.c
将产生code.o二进制格式文件，无法直接查看。
但可以通过反汇编器（将二进制格式文件反汇编为汇编代码文本）进行查看
输入指令：objdump -d code.o
https://blog.csdn.net/ACHENJIE/article/details/89172614

SIMD技术发展史
关于SIMD技术,我先做个简单介绍吧
处理器在处理数据的时候,为了适应并行性的要求,除了SISD(单指令单数据,也就是我们常见的加减法的那种)以外,又开发出了**SIMD**(单指令多数据)MISD(多指令单数据)MIMD(多指令多数据)等方式来处理数据,其中MISD多用于DSP这种数据处理形式比较单一的处理器内,现在广泛应用的是**SIMD**和MIMD,在现在的计算机中,CPU和ATI显卡是**SIMD**架构的,而NV显卡是MIMD架构的.背景介绍完毕.
那么,**SIMD**到底是个什么样的**技术**呢,形象来说,就是把几个数放在一起,然后成组的进行运算,有点类似数组的感觉对于多媒体数据来说,因为数据的相关性较强(这个的具体原理我会另撰文介绍....旁白:又不一定拖到什么时候了....你真是比乌龟还慢.....)所以特别适合使用这种操作来对同时对多个数据进行运算,它实现了空间上的并行运算操作
在PC领域,**SIMD****技术**最早出现在奔腾MMX处理器上,对应的是MMX指令集,当时的MMX指令集是对整数运算进行的**SIMD**支持,利用64位的浮点数寄存器来运作,可以同时存储2个32位整数或4个16位短整数进行运算,成倍的提升了处理器的媒体运算性能,也催生的多媒体电脑这一概念,但是缺点也同时存在着,那就是会占用浮点寄存器,造成MMX指令与浮点指令不能同时运作,在MMX中插入浮点运算需要先对MMX状态和数据进行清空,频繁切换会产生较大的性能损失.同时这种冲突的架构使得处理器的流水线化变得较为困难,限制了其应用
随之而来的是AMD的3DNOW!指令集,它实现了浮点数的**SIMD**运算,单指令周期内最多可得到4个单精度浮点数结果,从而极大的提高了处理器的游戏性能,使得AMD超越了INTEL而成为了游戏性能最强的处理器
不过,好景不长,翌年,INTEL发布了迄今为止最有影响力的**SIMD**指令集,SSE指令集.
SSE是streaming SIMD extend的缩写,意为流式单指令多数据拓展.INTEL在奔腾3中加入了该指令集,SSE中加入8个128位XMM寄存器.同时SSE加入了对于IEEE754浮点数运算的支持来取代原来的X87浮点协处理器.XMM寄存器中允许存放2个64位双精度浮点数或4个32位单精度浮点数进行运算,从而达到了和3DNOW!相同的结果,也就是自此之后,AMD不再开发3DNOW!指令集而改为兼容INTEL指令集.但是,整数**SIMD**运算占用浮点寄存器并没被解决,一直到SSE2的出现
SSE2首先出现在奔腾4处理器上,它允许在原有的XMM寄存器内存储4个32位整数或8个16位短整数进行运算,同时支持了64位拓展并增加了8个XMM寄存器.
之后的SSE3，SSE4都是补充,增加了超线程支持,增加了局部运算支持.
然后就是今天的主题了,也就是AVX指令集.AVX把原来的128位XMM寄存器升级为了256位YMM指令集,并且加入了三运算数和四运算数支持(很多人说只支持3运算数,但是我看了下AVX第五版本是加入了对四运算数的支持),并且在FMA中加入了积和熔加支持(上文部分涉及到了VEX,请自行百度).在AVX中,可以同时实现4个双精度浮点数的多运算数操作.AMD在对此指令集的支持上又有所不同,AMD是提供的2个128位XMM来合并成1个256位YMM寄存器,这个与推土机的双整数单元共享一个浮点单元的架构有关.他可以同时分给每个整数单元一个128位寄存器或合并起来使用一个256位寄存器,灵活性更好.但随之而来的是效率问题....理论上4模块的AMD推土机的效率也只有SNB的1/4
无论如何,AVX会带给我们前所未有的性能提升.依照官方数据,AVX的性能提升将与当年MMX的效果相当,中央处理器的运算能力将得到极大地提升.

另注,WIN7 SP1正式加入对于AVX指令集的支持

2011.2.18
晓可

[使用SIMD技术提高C++程序性能](https://blog.csdn.net/zhangzq86/article/details/54969005)

![使用SIMD技术的多种方法](../imgs/使用SIMD技术的多种方法.png)

第一种方法是使用著名的IPP库

https://software.intel.com/en-us/intel-ipp/

第二种方法是使用编译器的自动向量化（Auto-vectorization）支持
如果使用GCC编译器，增加-ftree-vectorizer-verbose=1

SIMD 指令（Single Instruction, Multiple Data）是单指令多数据的并行计算技术。让我详细解释其规范和实现：

1. SIMD 基本概念

1.1 核心思想

一条指令同时处理多个数据元素
// 传统标量运算（SISD）
float a[4] = {1.0, 2.0, 3.0, 4.0};
float b[4] = {5.0, 6.0, 7.0, 8.0};
float c[4];

for (int i = 0; i < 4; i++) {
    c[i] = a[i] + b[i];  // 4次加法指令
}

// SIMD 向量运算
__m128 va = _mm_load_ps(a);  // 一次加载4个float
__m128 vb = _mm_load_ps(b);  // 一次加载4个float  
__m128 vc = _mm_add_ps(va, vb);  // 一次加法，4个float同时计算
_mm_store_ps(c, vc);        // 一次存储4个float


2. 主要 SIMD 指令集规范

2.1 x86/x64 架构 SIMD 演进

指令集 位宽 寄存器 主要特性

MMX 64位 MM0-MM7 整数运算，与FPU寄存器复用

SSE 128位 XMM0-XMM15 浮点运算，独立寄存器

SSE2 128位 XMM0-XMM15 整数运算，双精度浮点

SSE3/SSSE3/SSE4 128位 XMM0-XMM15 水平运算、排列操作等

AVX 256位 YMM0-YMM15 三操作数格式，非破坏性操作

AVX2 256位 YMM0-YMM15 FMA、聚集加载等

AVX-512 512位 ZMM0-ZMM31 掩码寄存器、更多操作
2.2 ARM 架构 SIMD
指令集 位宽 寄存器 特性

NEON 128位 Q0-Q15 ARMv7/ARMv8 标准SIMD

SVE 可变长 Z0-Z31 可伸缩向量，128-2048位

SVE2 可变长 Z0-Z31 增强的SVE功能

3. x86 SIMD 指令规范详解

3.1 基本数据类型

#include <immintrin.h>  // SIMD 头文件

// 基本向量类型
__m128  v4f;     // 4个float (32x4=128位)
__m128d v2d;     // 2个double (64x2=128位) 
__m128i v16c;    // 16个char (8x16=128位)
__m128i v8s;     // 8个short (16x8=128位)
__m128i v4i;     // 4个int (32x4=128位)

// AVX 256位类型
__m256  v8f;     // 8个float (32x8=256位)
__m256d v4d;     // 4个double (64x4=256位)
__m256i v32c;    // 32个char (8x32=256位)

// AVX-512 512位类型
__m512  v16f;    // 16个float (32x16=512位)
__m512d v8d;     // 8个double (64x8=512位)
__m512i v64c;    // 64个char (8x64=512位)


3.2 常用指令分类

加载/存储指令

// 对齐加载
__m128 v = _mm_load_ps(float* ptr);     // 必须16字节对齐
__m256 v = _mm256_load_ps(float* ptr);  // 必须32字节对齐

// 未对齐加载  
__m128 v = _mm_loadu_ps(float* ptr);    // 任意对齐
__m256 v = _mm256_loadu_ps(float* ptr);

// 存储指令
_mm_store_ps(float* ptr, __m128 v);     // 对齐存储
_mm_storeu_ps(float* ptr, __m128 v);    // 未对齐存储

// 设置常量
__m128 v = _mm_set_ps(4.0, 3.0, 2.0, 1.0);  // [4,3,2,1]
__m128 v = _mm_set1_ps(1.0);                 // [1,1,1,1]
__m128 v = _mm_setzero_ps();                 // [0,0,0,0]


算术运算指令

// 浮点运算
__m128 result = _mm_add_ps(a, b);    // a + b
__m128 result = _mm_sub_ps(a, b);    // a - b  
__m128 result = _mm_mul_ps(a, b);    // a * b
__m128 result = _mm_div_ps(a, b);    // a / b

// 融合乘加 (FMA) - AVX2/AVX-512
__m128 result = _mm_fmadd_ps(a, b, c);  // a*b + c

// 整数运算
__m128i result = _mm_add_epi32(a, b);   // 32位整数加法
__m128i result = _mm_mullo_epi16(a, b); // 16位整数乘法（低半部分）


比较和逻辑指令

// 浮点比较
__m128 mask = _mm_cmpeq_ps(a, b);    // a == b
__m128 mask = _mm_cmpgt_ps(a, b);    // a > b
__m128 mask = _mm_cmplt_ps(a, b);    // a < b

// 位运算
__m128 result = _mm_and_ps(a, b);    // 按位与
__m128 result = _mm_or_ps(a, b);     // 按位或  
__m128 result = _mm_xor_ps(a, b);     // 按位异或


排列和洗牌指令

// 洗牌操作
__m128 result = _mm_shuffle_ps(a, b, _MM_SHUFFLE(3,2,1,0));
// 控制字: [3,2,1,0] 表示从a取[3],a取[2],b取[1],b取[0]

// 排列操作 (AVX2)
__m128i result = _mm_permutevar8x32_epi32(a, idx);

// 混合操作
__m128 result = _mm_blend_ps(a, b, 0b1010);  // 根据掩码混合


4. ARM NEON 指令规范

4.1 NEON 数据类型

#include <arm_neon.h>

// NEON 向量类型
float32x4_t v4f;     // 4个float32
float64x2_t v2d;     // 2个float64  
int8x16_t   v16c;    // 16个int8
int16x8_t   v8s;     // 8个int16
int32x4_t   v4i;     // 4个int32
uint8x16_t  v16uc;   // 16个uint8


4.2 NEON 指令示例

// 加载/存储
float32x4_t v = vld1q_f32(float* ptr);    // 加载4个float
void vst1q_f32(float* ptr, float32x4_t v); // 存储4个float

// 算术运算
float32x4_t result = vaddq_f32(a, b);     // a + b
float32x4_t result = vmulq_f32(a, b);     // a * b
float32x4_t result = vmlaq_f32(c, a, b);  // c + a*b (乘加)

// 比较操作
uint32x4_t mask = vceqq_f32(a, b);        // a == b
uint32x4_t mask = vcgtq_f32(a, b);         // a > b

// 洗牌操作
float32x4_t result = vrev64q_f32(a);       // 反转64位内的元素


5. SIMD 编程实践

5.1 向量化循环示例

// 标量版本
void scalar_add(float* a, float* b, float* c, int n) {
    for (int i = 0; i < n; i++) {
        c[i] = a[i] + b[i];
    }
}

// SIMD 向量化版本 (SSE)
void vectorized_add(float* a, float* b, float* c, int n) {
    // 确保内存对齐（性能关键）
    assert((uintptr_t)a % 16 == 0);
    assert((uintptr_t)b % 16 == 0); 
    assert((uintptr_t)c % 16 == 0);
    
    // 主循环：每次处理4个元素
    int i = 0;
    for (; i <= n - 4; i += 4) {
        __m128 va = _mm_load_ps(a + i);  // 加载4个float
        __m128 vb = _mm_load_ps(b + i);
        __m128 vc = _mm_add_ps(va, vb);  // 4个加法同时执行
        _mm_store_ps(c + i, vc);         // 存储4个结果
    }
    
    // 处理剩余元素（标量）
    for (; i < n; i++) {
        c[i] = a[i] + b[i];
    }
}


5.2 复杂运算：点积计算

float dot_product_sse(float* a, float* b, int n) {
    __m128 sum = _mm_setzero_ps();
    
    for (int i = 0; i < n; i += 4) {
        __m128 va = _mm_load_ps(a + i);
        __m128 vb = _mm_load_ps(b + i);
        __m128 product = _mm_mul_ps(va, vb);
        sum = _mm_add_ps(sum, product);
    }
    
    // 水平求和：sum[0]+sum[1]+sum[2]+sum[3]
    sum = _mm_hadd_ps(sum, sum);
    sum = _mm_hadd_ps(sum, sum);
    
    float result;
    _mm_store_ss(&result, sum);
    return result;
}


6. 编译器自动向量化

6.1 帮助编译器自动向量化

// 使用编译指示提示向量化
#pragma omp simd
for (int i = 0; i < n; i++) {
    c[i] = a[i] + b[i];
}

// 使用C++11属性
void vectorized_func(float* a, float* b, float* c, int n) 
    [[omp::simd]] 
{
    for (int i = 0; i < n; i++) {
        c[i] = a[i] + b[i];
    }
}


6.2 编译选项

# GCC/Clang 自动向量化选项
gcc -O3 -march=native -ftree-vectorize -fopt-info-vec
clang -O3 -march=native -Rpass=vectorize

# 特定指令集
gcc -msse4.2    # 启用SSE4.2
gcc -mavx2      # 启用AVX2  
gcc -mavx512f   # 启用AVX-512

# ARM NEON
gcc -mfpu=neon  # ARMv7 NEON
gcc -march=armv8-a+simd  # ARMv8 NEON


7. 性能优化注意事项

7.1 内存对齐

// 手动对齐内存
float* aligned_a = (float*)aligned_alloc(32, n * sizeof(float));
// 使用32字节对齐（AVX要求）

// C++17 对齐分配
float* aligned_b = new (std::align_val_t(32)) float[n];


7.2 避免 Gather/Scatter 开销

// 避免：聚集加载（性能差）
__m256i indices = _mm256_set_epi32(7, 6, 5, 4, 3, 2, 1, 0);
__m256 data = _mm256_i32gather_ps(base, indices, 4);

// 优先：连续内存访问
__m256 data = _mm256_load_ps(base);  // 连续加载8个float


7.3 数据布局优化

// 结构数组 (AOS) - 不利于向量化
struct Point { float x, y, z; };
Point points[1000];  // 内存布局: x,y,z, x,y,z, ...

// 数组结构 (SOA) - 利于向量化
struct Points {
    float x[1000];  // 连续x坐标
    float y[1000];  // 连续y坐标  
    float z[1000];  // 连续z坐标
};


8. 检测和兼容性

8.1 CPU 特性检测

#include <cpuid.h>

void check_simd_features() {
    unsigned int eax, ebx, ecx, edx;
    
    // 检查SSE系列
    __cpuid(1, eax, ebx, ecx, edx);
    bool sse_supported = edx & (1 << 25);  // SSE
    bool sse2_supported = edx & (1 << 26); // SSE2
    bool sse3_supported = ecx & (1 << 0);  // SSE3
    
    // 检查AVX系列  
    bool avx_supported = ecx & (1 << 28);  // AVX
    bool avx2_supported = ebx & (1 << 5);  // AVX2
    
    // 检查AVX-512
    __cpuid_count(7, 0, eax, ebx, ecx, edx);
    bool avx512f_supported = ebx & (1 << 16);  // AVX-512 Foundation
}


8.2 运行时分发

// 根据CPU能力选择实现
void optimized_add(float* a, float* b, float* c, int n) {
    if (has_avx512()) {
        avx512_add(a, b, c, n);
    } else if (has_avx2()) {
        avx2_add(a, b, c, n);
    } else if (has_sse41()) {
        sse41_add(a, b, c, n);
    } else {
        scalar_add(a, b, c, n);
    }
}


总结

SIMD 指令核心要点：

方面 关键规范 最佳实践

数据并行 单指令多数据 处理连续数据块

寄存器宽度 128位(SSE)、256位(AVX)、512位(AVX-512) 匹配数据尺寸

内存对齐 16/32/64字节边界 使用对齐分配

指令流水线 多端口执行单元 避免依赖链

数据布局 连续内存访问 使用SOA布局

性能收益：正确使用SIMD可获得2-8倍性能提升，是现代高性能计算的基础技术。
