# 汇编assembly

NASM 和 MASM 是汇编语言，它们不提供标准库，但可以通过系统调用或操作系统API来实现功能。

一、调试信息打印方法

1. Linux/Unix (NASM) 系统调用

section .data
    debug_msg db 'Debug info: value = ', 0
    newline db 10, 0
    value_buffer times 11 db 0  ; 存储转换后的数字
    
section .text
    global _start

; 打印字符串 (rax=地址, rdx=长度)
print_string:
    mov rsi, rax        ; 字符串地址
    mov rdx, rdi        ; 长度
    mov rax, 1          ; sys_write
    mov rdi, 1          ; stdout
    syscall
    ret

; 打印整数 (rax=数字)
print_int:
    mov rbx, 10         ; 基数10
    mov rcx, value_buffer+10
    mov byte [rcx], 0   ; 字符串终止符
    
.convert_loop:
    dec rcx
    xor rdx, rdx
    div rbx
    add dl, '0'
    mov [rcx], dl
    test rax, rax
    jnz .convert_loop
    
    ; 计算长度并打印
    mov rax, rcx
    mov rdi, value_buffer+10
    sub rdi, rcx
    call print_string
    ret

; 调试输出示例
debug_print:
    ; 打印标签
    mov rax, debug_msg
    mov rdi, 20
    call print_string
    
    ; 打印值 (假设值在 rbx 中)
    mov rax, rbx
    call print_int
    
    ; 换行
    mov rax, newline
    mov rdi, 1
    call print_string
    ret

_start:
    mov rbx, 1234       ; 要调试的值
    call debug_print
    
    ; 退出
    mov rax, 60
    xor rdi, rdi
    syscall


2. Windows (MASM) API 调用

.386
.model flat, stdcall
option casemap:none

include windows.inc
include kernel32.inc
includelib kernel32.lib

.data
    debug_msg db 'Debug: Value = ', 0
    buffer db 16 dup(0)
    newline db 13, 10, 0
    
.data?
    stdout_handle dd ?
    
.code
; 整数转字符串
int_to_str proc value:DWORD
    mov eax, value
    mov ecx, 10
    lea edi, buffer+15
    mov byte ptr [edi], 0
    
convert_loop:
    dec edi
    xor edx, edx
    div ecx
    add dl, '0'
    mov [edi], dl
    test eax, eax
    jnz convert_loop
    ret
int_to_str endp

; 调试打印
debug_print proc value:DWORD
    ; 获取标准输出句柄
    invoke GetStdHandle, STD_OUTPUT_HANDLE
    mov stdout_handle, eax
    
    ; 打印标签
    invoke WriteConsoleA, stdout_handle, 
                       offset debug_msg, 
                       sizeof debug_msg - 1, 
                       NULL, NULL
    
    ; 转换并打印数字
    invoke int_to_str, value
    lea esi, edi
    mov ecx, offset buffer+15
    sub ecx, esi
    invoke WriteConsoleA, stdout_handle, 
                       esi, 
                       ecx, 
                       NULL, NULL
    
    ; 换行
    invoke WriteConsoleA, stdout_handle, 
                       offset newline, 
                       2, 
                       NULL, NULL
    ret
debug_print endp

start:
    invoke debug_print, 1234
    invoke ExitProcess, 0
end start


二、更简单的调试方法

1. 使用寄存器值退出码（快速检查）

; NASM Linux - 用退出码返回调试值
section .text
global _start

_start:
    mov rbx, 0x1234     ; 要调试的值
    
    ; 查看方法：运行后 echo $?
    mov rdi, rbx        ; 退出码 = 调试值
    mov rax, 60         ; sys_exit
    syscall


2. 使用 GDB 调试

# 编译带调试信息
nasm -f elf64 -g -F dwarf program.asm
ld -o program program.o

# 使用 GDB
gdb ./program
(gdb) break _start
(gdb) run
(gdb) info registers
(gdb) x/10x $rsp


3. 内联调试宏（NASM）

%macro DEBUG_PRINT 1
    pusha
    ; 保存值到已知位置
    mov [debug_value], %1
    ; 这里可以添加系统调用打印
    popa
%endmacro

section .data
    debug_value dq 0


三、实用工具推荐

1. 简单打印库（可引用）

• AsmIO：提供简单的输入输出函数

• FreshLib：完整的汇编库

• 自己封装常用函数：
; 保存为 print.asm
print_str:  ; (str_ptr, length)
print_int:  ; (number)
print_hex:  ; (number)
print_char: ; (char)


2. 调试宏集合

%macro BREAKPOINT 0
    int3
%endmacro

%macro PRINT_REG 1
    ; 打印寄存器 %1 的值
%endmacro

%macro DUMP_MEM 2
    ; 打印内存地址 %1 开始的 %2 字节
%endmacro


四、MASM 开发环境配置

Visual Studio 设置

; 在 VS 中启用控制台输出
invoke AllocConsole
invoke GetStdHandle, STD_OUTPUT_HANDLE
mov hConsole, eax


五、最简单的调试输出方案

对于 NASM：

# 编译运行查看寄存器
nasm -f elf64 test.asm
ld -o test test.o
./test
echo $?  # 查看退出码（低8位）


对于 MASM：

; 用 MessageBox 显示调试信息
invoke MessageBox, NULL, 
                  addr debug_str, 
                  addr caption, 
                  MB_OK


建议

1. 初学者：先用系统调用/API实现简单打印函数
2. 复杂项目：封装调试库，使用条件汇编
3. 生产环境：用调试器（GDB/OllyDbg/x64dbg）

汇编调试比较原始，但能深入理解计算机工作原理。最简单的开始方式是：用退出码传递值，用 echo $? 查看。

c
c++代码里卖弄套汇编代码

汇编，mysql clickHouse中使用

assembly language

在 ClickHouse 项目中，汇编代码（Assembly Code）主要用于极致性能优化，尤其是在处理字符串处理、哈希计算、SIMD 指令加速等关键路径上。由于 ClickHouse 是一个高性能列式数据库，对 CPU 利用率要求极高，因此在一些热点函数中使用了手写或自动向量化（如通过 LLVM 生成）的汇编代码。

不过，ClickHouse 并不大量使用手写汇编（hand-written assembly），而是更多依赖 C++ 编译器优化 + 内联汇编（inline assembly） + 内在函数（Intrinsics） + LLVM IR 优化 来实现高性能。


##  一、ClickHouse 中汇编代码的几种形式

| 类型 | 说明 | 示例场景 |
|------|------|---------|
| 1. 内联汇编（GCC/Clang `asm`） | 直接嵌入汇编指令 | 性能计数器、内存屏障 |
| 2. 内在函数（Intrinsics） | 使用 `__builtin_` 或 `__m128i` 等调用 SIMD 指令 | 字符串匹配、CRC32、哈希 |
| 3. LLVM IR 生成（间接汇编） | 通过 Clang 生成高效汇编 | 向量化表达式执行 |
| 4. 预编译的 `.s` 汇编文件 | 极少数情况下使用 | 特定平台优化（如 ARM64） |


##  二、汇编相关代码的位置（基于 GitHub 仓库）

你可以在 ClickHouse 源码中搜索以下目录和文件：

### 1. `src/Common/` —— 公共性能优化

- `PaddedPODArray.h`  
  使用内存对齐技巧，便于 SIMD 指令优化（间接影响汇编输出）。

- `CPUInfo.cpp` / `CPUInfo.h`  
  检测 CPU 特性（如 SSE4.2、AVX2、NEON），用于运行时选择最优实现。

- `Memcpy.h` / `InlineString.h`  
  包含对 `memcpy`、字符串操作的优化，可能使用 `__builtin_memcpy` 或手写循环（编译后生成高效汇编）。

### 2. `src/Functions/` —— 函数向量化（关键！）

这是最可能生成高效汇编的地方，尤其是通过 LLVM JIT 编译表达式。

- `FunctionsString.cpp`  
  如 `length`, `substring`, `position` 等函数，在向量化执行时会被 LLVM 编译为带 SIMD 的汇编。

- `FunctionsHashing.cpp`  
  使用 `CityHash`, `xxHash`，其中部分实现使用了 SSE/AVX 内在函数。

- `FunctionsMath.cpp`  
  数学函数向量化，LLVM 会自动向量化循环。

>  注意：这些函数本身是 C++，但 ClickHouse 使用 JIT 编译 将表达式编译为 LLVM IR，再由 LLVM 生成高度优化的汇编代码（支持 AVX2、AVX-512）。

### 3. `src/Interpreters/` —— 查询执行引擎

- `ExpressionJIT.cpp`  
  实现了基于 LLVM 的 JIT 编译器，将 SQL 表达式编译为本地机器码（即汇编）。

- `JITCompiledExpression.h/cpp`  
  存储编译后的机器码，直接执行，性能接近手写汇编。

>  这是 ClickHouse 高性能的核心之一：把 WHERE、SELECT 中的表达式编译成原生汇编执行。

### 4. `src/base/hashing/` —— 哈希函数优化

- `city.h`, `xxhash.h`, `mum.h`  
  这些哈希函数大量使用 SSE4.2、AVX2 内在函数，例如：

```cpp
#if defined(__SSE4_2__)
    #include <nmmintrin.h>
    crc = _mm_crc32_u64(crc, *reinterpret_cast<const UInt64*>(data));
#endif
```

这些内在函数会被编译为 `crc32` 汇编指令。


### 5. `src/base/polyfill/` —— 跨平台优化

- `sse2neon.h`  
  在 ARM 上模拟 SSE 指令，用于跨平台 SIMD 支持。


### 6. 汇编文件（`.s` 或 `.S`）—— 极少数

ClickHouse 几乎不使用纯 `.s` 汇编文件，因为：

- 维护成本高
- 难以跨平台（x86_64 vs ARM64）
- LLVM 已能生成高质量汇编

但在某些第三方库或特殊场景下可能有：

- `contrib/` 目录下的库（如 `double-conversion`, `re2`）可能包含汇编
- `src/Functions/URL/` 中某些解析函数可能使用手写循环（编译后高效）


##  三、如何查找汇编相关代码？

### 方法 1：搜索内在函数（Intrinsics）

```bash
grep -r "__builtin_" src/
grep -r "_mm_" src/           # SSE/AVX
grep -r "vmov" src/          # NEON ARM SIMD
grep -r "asm" src/           # 内联汇编
```

### 方法 2：查看 JIT 生成的代码（运行时）

启动 ClickHouse 服务时加参数：

```bash
clickhouse-server --enable_jit_compilation=1 --compile_expressions=1
```

然后在查询中使用复杂表达式，JIT 会生成机器码。

你可以用 `perf` 工具查看热点函数的汇编：

```bash
perf record -g clickhouse-client --query "SELECT sum(number*2+1) FROM numbers(1e8)"
perf report
```

进入后按 `Enter` 查看热点函数，再按 `a` 查看汇编代码（需有 debug symbols）。

---

##  四、总结：ClickHouse 的“汇编”真相

| 误解 | 真相 |
|------|------|
| “ClickHouse 有很多手写汇编” | ❌ 实际极少，主要靠 LLVM JIT + 内在函数 + 编译器优化 |
| “性能来自汇编” | ✅ 更准确说是：向量化执行 + JIT 编译 + SIMD + 零拷贝 |
| “可以读到 `.s` 文件” | ❌ 几乎没有纯汇编文件，性能代码在 C++ 中通过 intrinsic 实现 |


##  推荐关注的核心目录

| 目录 | 作用 |
|------|------|
| `src/Interpreters/JIT/` | JIT 编译器，生成高效汇编 |
| `src/Functions/` | 向量化函数，LLVM 优化热点 |
| `src/base/hashing/` | 哈希函数，使用 `__builtin` 和 SIMD intrinsic |
| `src/Common/` | 内存对齐、高效内存操作 |


如果你想看：
- 一个 JIT 编译表达式的完整流程
- 如何用 `perf` 查看 ClickHouse 查询的汇编热点
- 手写 SIMD 优化一个字符串函数

我可以继续深入，带你从 C++ 代码到生成的汇编指令全程追踪！🚀

 grep -r "__builtin_" ./src
./src/DataTypes/Serializations/SerializationArray.cpp:            if (unlikely(__builtin_add_overflow(current_offset, current_size, &current_offset)))
./src/DataTypes/Serializations/SerializationFixedString.cpp:    if (unlikely(__builtin_mul_overflow(limit, n, &max_bytes)))
./src/DataTypes/Serializations/SerializationFixedString.cpp:    if (unlikely(__builtin_add_overflow(initial_size, max_bytes, &new_data_size)))
./src/Common/HashTable/Hash.h:                __builtin_memcpy(&value, pos, 1);
./src/Common/HashTable/Hash.h:                __builtin_memcpy(&value, pos, 2);
./src/Common/HashTable/Hash.h:                __builtin_memcpy(&value, pos, 3);
./src/Common/HashTable/Hash.h:                __builtin_memcpy(&value, pos, 4);
./src/Common/HashTable/Hash.h:                __builtin_memcpy(&value, pos, 5);
./src/Common/HashTable/Hash.h:                __builtin_memcpy(&value, pos, 6);
./src/Common/HashTable/Hash.h:                __builtin_memcpy(&value, pos, 7);
./src/Common/HashTable/HashTable.h:        __builtin_prefetch(&buf[place]);
./src/Common/examples/symbol_index.cpp:    return __builtin_return_address(0);
./src/Common/clickhouse_malloc.cpp:    if (__builtin_mul_overflow(number_of_members, size, &real_size))
./src/Common/UTF8Helpers.h:        res += __builtin_popcount(_mm_movemask_epi8(
./src/Common/PODArray.cpp:    if (__builtin_mul_overflow(num_elements, element_size, &amount))
./src/Common/PODArray.cpp:    if (__builtin_add_overflow(byte_size(num_elements, element_size), pad_left + pad_right, &amount))
./src/Common/StringSearcher.h:                const auto offset = __builtin_ctz(mask);
./src/Common/StringSearcher.h:                const auto offset = __builtin_ctz(mask);
./src/Common/checkStackSize.cpp:    const void * frame_address = __builtin_frame_address(0);
./src/Common/BitHelpers.h:        return __builtin_clz(x);
./src/Common/BitHelpers.h:        return __builtin_clzl(x);
./src/Common/BitHelpers.h:        return __builtin_clzll(x);
./src/Common/BitHelpers.h:// Unsafe since __builtin_ctz()-family explicitly state that result is undefined on x == 0
./src/Common/BitHelpers.h:        return __builtin_ctz(x);
./src/Common/BitHelpers.h:        return __builtin_ctzl(x);
./src/Common/BitHelpers.h:        return __builtin_ctzll(x);
./src/Functions/roundToExp2.cpp:    return x <= 0 ? 0 : (T(1) << (31 - __builtin_clz(x)));
./src/Functions/roundToExp2.cpp:    return x <= 0 ? 0 : (T(1) << (63 - __builtin_clzll(x)));
./src/Columns/ColumnVector.cpp:    const UInt64 leading_zeroes = __builtin_clzll(mask);
./src/Interpreters/AggregationCommon.h:    __builtin_memcpy(&out, &res, sizeof(T));
./src/Compression/CompressionCodecFPC.cpp:        if (__builtin_add_overflow(tail_size1, tail_size2, &expected_size)
./src/Compression/CompressionCodecFPC.cpp:            || __builtin_add_overflow(expected_size, 1, &expected_size)) [[unlikely]]







wdidada@LAPTOP-wdidada:~/clickhouse$ grep -r "_mm_" src/
src/DataTypes/Serializations/SerializationString.cpp:                        _mm_storeu_si128(sse_dst_pos + j, _mm_loadu_si128(sse_src_pos + j));
src/Common/IPv6ToBinary.cpp:    uint16_t mask = _mm_movemask_epi8(_mm_cmpeq_epi8(
src/Common/IPv6ToBinary.cpp:        _mm_loadu_si128(reinterpret_cast<const __m128i *>(addr)),
src/Common/IPv6ToBinary.cpp:        _mm_loadu_si128(reinterpret_cast<const __m128i *>(cidr_addr))));
src/Common/HashTable/Hash.h:    return _mm_crc32_u64(-1ULL, x);
src/Common/HashTable/Hash.h:    return _mm_crc32_u64(updated_value, x);
src/Common/HashTable/Hash.h:        crc = _mm_crc32_u64(crc, x.items[0]);
src/Common/HashTable/Hash.h:        crc = _mm_crc32_u64(crc, x.items[1]);
src/Common/HashTable/Hash.h:        crc = _mm_crc32_u64(crc, x.items[0]);
src/Common/HashTable/Hash.h:        crc = _mm_crc32_u64(crc, x.items[1]);
src/Common/HashTable/Hash.h:        crc = _mm_crc32_u64(crc, x.items[2]);
src/Common/HashTable/Hash.h:        crc = _mm_crc32_u64(crc, x.items[3]);
src/Common/HashTable/StringHashTable.h:        res = _mm_crc32_u64(res, key);
src/Common/HashTable/StringHashTable.h:        res = _mm_crc32_u64(res, key.items[0]);
src/Common/HashTable/StringHashTable.h:        res = _mm_crc32_u64(res, key.items[1]);
src/Common/HashTable/StringHashTable.h:        res = _mm_crc32_u64(res, key.a);
src/Common/HashTable/StringHashTable.h:        res = _mm_crc32_u64(res, key.b);
src/Common/HashTable/StringHashTable.h:        res = _mm_crc32_u64(res, key.c);
src/Common/remapExecutable.cpp:            _mm_storeu_si128(dst, _mm_loadu_si128(src));
src/Common/UTF8Helpers.cpp:        const auto lower_bound = _mm_set1_epi8(32);
src/Common/UTF8Helpers.cpp:        const auto upper_bound = _mm_set1_epi8(126);
src/Common/UTF8Helpers.cpp:            __m128i bytes = _mm_loadu_si128(reinterpret_cast<const __m128i *>(&data[i]));
src/Common/UTF8Helpers.cpp:            const uint16_t non_regular_width_mask = _mm_movemask_epi8(
src/Common/UTF8Helpers.cpp:                _mm_or_si128(
src/Common/UTF8Helpers.cpp:                    _mm_cmplt_epi8(bytes, lower_bound),
src/Common/UTF8Helpers.cpp:                    _mm_cmpgt_epi8(bytes, upper_bound)));
src/Common/memcmpSmall.h:        uint16_t mask = _mm_cmp_epi8_mask(
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(a + offset)),
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(b + offset)),
src/Common/memcmpSmall.h:        uint16_t mask = _mm_cmp_epi8_mask(
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(a + offset)),
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(b + offset)),
src/Common/memcmpSmall.h:    const __m128i zero16 = _mm_setzero_si128();
src/Common/memcmpSmall.h:        uint16_t mask = _mm_cmpneq_epi8_mask(_mm_loadu_si128(reinterpret_cast<const __m128i *>(longest + offset)), zero16);
src/Common/memcmpSmall.h:        uint16_t mask = _mm_cmp_epi8_mask(
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(a + offset)),
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(b + offset)),
src/Common/memcmpSmall.h:        uint16_t mask = _mm_cmp_epi8_mask(
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(a + offset)),
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(b + offset)),
src/Common/memcmpSmall.h:        uint16_t mask = _mm_cmp_epi8_mask(
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(a + offset)),
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(b + offset)),
src/Common/memcmpSmall.h:    uint16_t mask = _mm_cmp_epi8_mask(
src/Common/memcmpSmall.h:        _mm_loadu_si128(reinterpret_cast<const __m128i *>(a)), _mm_loadu_si128(reinterpret_cast<const __m128i *>(b)), _MM_CMPINT_NE);
src/Common/memcmpSmall.h:        == _mm_cmp_epi8_mask(
src/Common/memcmpSmall.h:               _mm_loadu_si128(reinterpret_cast<const __m128i *>(a)), _mm_loadu_si128(reinterpret_cast<const __m128i *>(b)), _MM_CMPINT_EQ);
src/Common/memcmpSmall.h:    const __m128i zero16 = _mm_setzero_si128();
src/Common/memcmpSmall.h:        uint16_t mask = _mm_cmp_epi8_mask(
src/Common/memcmpSmall.h:            zero16, _mm_loadu_si128(reinterpret_cast<const __m128i *>(reinterpret_cast<const char *>(data) + offset)), _MM_CMPINT_NE);
src/Common/memcmpSmall.h:        uint16_t mask = _mm_movemask_epi8(_mm_cmpeq_epi8(
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(a + offset)),
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(b + offset))));
src/Common/memcmpSmall.h:        uint16_t mask = _mm_movemask_epi8(_mm_cmpeq_epi8(
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(a + offset)),
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(b + offset))));
src/Common/memcmpSmall.h:    const __m128i zero16 = _mm_setzero_si128();
src/Common/memcmpSmall.h:        uint16_t mask = _mm_movemask_epi8(_mm_cmpeq_epi8(_mm_loadu_si128(reinterpret_cast<const __m128i *>(longest + offset)), zero16));
src/Common/memcmpSmall.h:        uint16_t mask = _mm_movemask_epi8(_mm_cmpeq_epi8(
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(a + offset)),
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(b + offset))));
src/Common/memcmpSmall.h:        uint16_t mask = _mm_movemask_epi8(_mm_cmpeq_epi8(
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(a + offset)),
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(b + offset))));
src/Common/memcmpSmall.h:        uint16_t mask = _mm_movemask_epi8(_mm_cmpeq_epi8(
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(a + offset)),
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(b + offset))));
src/Common/memcmpSmall.h:    uint16_t mask = _mm_movemask_epi8(
src/Common/memcmpSmall.h:        _mm_cmpeq_epi8(_mm_loadu_si128(reinterpret_cast<const __m128i *>(a)), _mm_loadu_si128(reinterpret_cast<const __m128i *>(b))));
src/Common/memcmpSmall.h:        == _mm_movemask_epi8(_mm_cmpeq_epi8(
src/Common/memcmpSmall.h:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(a)), _mm_loadu_si128(reinterpret_cast<const __m128i *>(b))));
src/Common/memcmpSmall.h:    const __m128i zero16 = _mm_setzero_si128();
src/Common/memcmpSmall.h:        uint16_t mask = _mm_movemask_epi8(
src/Common/memcmpSmall.h:            _mm_cmpeq_epi8(zero16, _mm_loadu_si128(reinterpret_cast<const __m128i *>(reinterpret_cast<const char *>(data) + offset))));
src/Common/StringUtils.cpp:    __m128i masks = _mm_setzero_si128();
src/Common/StringUtils.cpp:        __m128i bytes = _mm_loadu_si128(reinterpret_cast<const __m128i *>(data + i));
src/Common/StringUtils.cpp:        masks = _mm_or_si128(masks, bytes);
src/Common/StringUtils.cpp:    int mask = _mm_movemask_epi8(masks);
src/Common/benchmarks/integer_hash_tables_and_hashes.cpp:            return _mm_crc32_u64(-1ULL, x);
src/Common/UTF8Helpers.h:    const auto threshold = _mm_set1_epi8(0xBF);
src/Common/UTF8Helpers.h:        res += __builtin_popcount(_mm_movemask_epi8(
src/Common/UTF8Helpers.h:            _mm_cmpgt_epi8(_mm_loadu_si128(reinterpret_cast<const __m128i *>(data)), threshold)));
src/Common/memcpySmall.h:            _mm_storeu_si128(reinterpret_cast<__m128i *>(dst),
src/Common/memcpySmall.h:                _mm_loadu_si128(reinterpret_cast<const __m128i *>(src)));
src/Common/memcpySmall.h:            /// Avoid clang loop-idiom optimization, which transforms _mm_storeu_si128 to built-in memcpy
src/Common/StringSearcher.h:    __m128i cache = _mm_setzero_si128();
src/Common/StringSearcher.h:        first_needle_character_vec = _mm_set1_epi8(first_needle_character);
src/Common/StringSearcher.h:            second_needle_character_vec = _mm_set1_epi8(second_needle_character);
src/Common/StringSearcher.h:            cache = _mm_srli_si128(cache, 1);
src/Common/StringSearcher.h:                cache = _mm_insert_epi8(cache, *needle_pos, N - 1);
src/Common/StringSearcher.h:            const __m128i haystack_characters = _mm_loadu_si128(reinterpret_cast<const __m128i *>(pos));
src/Common/StringSearcher.h:            const __m128i comparison_result = _mm_cmpeq_epi8(haystack_characters, cache);
src/Common/StringSearcher.h:            const uint16_t comparison_result_mask = _mm_movemask_epi8(comparison_result);
src/Common/StringSearcher.h:                    const __m128i haystack_characters = _mm_loadu_si128(reinterpret_cast<const __m128i *>(haystack));
src/Common/StringSearcher.h:                    const __m128i comparison_result = _mm_cmpeq_epi8(haystack_characters, first_needle_character_vec);
src/Common/StringSearcher.h:                    const uint16_t comparison_result_mask = _mm_movemask_epi8(comparison_result);
src/Common/StringSearcher.h:                const __m128i haystack_characters_from_1st = _mm_loadu_si128(reinterpret_cast<const __m128i *>(haystack));
src/Common/StringSearcher.h:                const __m128i haystack_characters_from_2nd = _mm_loadu_si128(reinterpret_cast<const __m128i *>(haystack + 1));
src/Common/StringSearcher.h:                const __m128i comparison_result_1st = _mm_cmpeq_epi8(haystack_characters_from_1st, first_needle_character_vec);
src/Common/StringSearcher.h:                const __m128i comparison_result_2nd = _mm_cmpeq_epi8(haystack_characters_from_2nd, second_needle_character_vec);
src/Common/StringSearcher.h:                const __m128i comparison_result_combined = _mm_and_si128(comparison_result_1st, comparison_result_2nd);
src/Common/StringSearcher.h:                const uint16_t comparison_result_mask = _mm_movemask_epi8(comparison_result_combined);
src/Common/StringSearcher.h:                    const __m128i haystack_characters = _mm_loadu_si128(reinterpret_cast<const __m128i *>(haystack));
src/Common/StringSearcher.h:                    const __m128i comparison_result_cache = _mm_cmpeq_epi8(haystack_characters, cache);
src/Common/StringSearcher.h:                    const uint16_t mask_offset = _mm_movemask_epi8(comparison_result_cache);
src/Common/StringSearcher.h:    __m128i cachel = _mm_setzero_si128(), cacheu = _mm_setzero_si128();
src/Common/StringSearcher.h:        patl = _mm_set1_epi8(l);
src/Common/StringSearcher.h:        patu = _mm_set1_epi8(u);
src/Common/StringSearcher.h:            cachel = _mm_srli_si128(cachel, 1);
src/Common/StringSearcher.h:            cacheu = _mm_srli_si128(cacheu, 1);
src/Common/StringSearcher.h:                cachel = _mm_insert_epi8(cachel, std::tolower(*needle_pos), N - 1);
src/Common/StringSearcher.h:                cacheu = _mm_insert_epi8(cacheu, std::toupper(*needle_pos), N - 1);
src/Common/StringSearcher.h:            const auto v_haystack = _mm_loadu_si128(reinterpret_cast<const __m128i *>(pos));
src/Common/StringSearcher.h:            const auto v_against_l = _mm_cmpeq_epi8(v_haystack, cachel);
src/Common/StringSearcher.h:            const auto v_against_u = _mm_cmpeq_epi8(v_haystack, cacheu);
src/Common/StringSearcher.h:            const auto v_against_l_or_u = _mm_or_si128(v_against_l, v_against_u);
src/Common/StringSearcher.h:            const auto mask = _mm_movemask_epi8(v_against_l_or_u);
src/Common/StringSearcher.h:                const auto v_haystack = _mm_loadu_si128(reinterpret_cast<const __m128i *>(haystack));
src/Common/StringSearcher.h:                const auto v_against_l = _mm_cmpeq_epi8(v_haystack, patl);
src/Common/StringSearcher.h:                const auto v_against_u = _mm_cmpeq_epi8(v_haystack, patu);
src/Common/StringSearcher.h:                const auto v_against_l_or_u = _mm_or_si128(v_against_l, v_against_u);
src/Common/StringSearcher.h:                const auto mask = _mm_movemask_epi8(v_against_l_or_u);
src/Common/StringSearcher.h:                    const auto v_haystack_offset = _mm_loadu_si128(reinterpret_cast<const __m128i *>(haystack));
src/Common/StringSearcher.h:                    const auto v_against_l_offset = _mm_cmpeq_epi8(v_haystack_offset, cachel);
src/Common/StringSearcher.h:                    const auto v_against_u_offset = _mm_cmpeq_epi8(v_haystack_offset, cacheu);
src/Common/StringSearcher.h:                    const auto v_against_l_or_u_offset = _mm_or_si128(v_against_l_offset, v_against_u_offset);
src/Common/StringSearcher.h:                    const auto mask_offset = _mm_movemask_epi8(v_against_l_or_u_offset);
src/Common/StringSearcher.h:    __m128i cachel = _mm_setzero_si128();
src/Common/StringSearcher.h:    __m128i cacheu = _mm_setzero_si128();
src/Common/StringSearcher.h:        patl = _mm_set1_epi8(l);
src/Common/StringSearcher.h:        patu = _mm_set1_epi8(u);
src/Common/StringSearcher.h:                cachel = _mm_srli_si128(cachel, 1);
src/Common/StringSearcher.h:                cacheu = _mm_srli_si128(cacheu, 1);
src/Common/StringSearcher.h:                cachel = _mm_srli_si128(cachel, 1);
src/Common/StringSearcher.h:                cacheu = _mm_srli_si128(cacheu, 1);
src/Common/StringSearcher.h:                    cachel = _mm_insert_epi8(cachel, l_seq[j], N - 1);
src/Common/StringSearcher.h:                    cacheu = _mm_insert_epi8(cacheu, u_seq[j], N - 1);
src/Common/StringSearcher.h:            const auto v_haystack = _mm_loadu_si128(reinterpret_cast<const __m128i *>(pos));
src/Common/StringSearcher.h:            const auto v_against_l = _mm_cmpeq_epi8(v_haystack, cachel);
src/Common/StringSearcher.h:            const auto v_against_u = _mm_cmpeq_epi8(v_haystack, cacheu);
src/Common/StringSearcher.h:            const auto v_against_l_or_u = _mm_or_si128(v_against_l, v_against_u);
src/Common/StringSearcher.h:            const auto mask = _mm_movemask_epi8(v_against_l_or_u);
src/Common/StringSearcher.h:                const auto v_haystack = _mm_loadu_si128(reinterpret_cast<const __m128i *>(haystack));
src/Common/StringSearcher.h:                const auto v_against_l = _mm_cmpeq_epi8(v_haystack, patl);
src/Common/StringSearcher.h:                const auto v_against_u = _mm_cmpeq_epi8(v_haystack, patu);
src/Common/StringSearcher.h:                const auto v_against_l_or_u = _mm_or_si128(v_against_l, v_against_u);
src/Common/StringSearcher.h:                const auto mask = _mm_movemask_epi8(v_against_l_or_u);
src/Common/StringSearcher.h:                    const auto v_haystack_offset = _mm_loadu_si128(reinterpret_cast<const __m128i *>(haystack));
src/Common/StringSearcher.h:                    const auto v_against_l_offset = _mm_cmpeq_epi8(v_haystack_offset, cachel);
src/Common/StringSearcher.h:                    const auto v_against_u_offset = _mm_cmpeq_epi8(v_haystack_offset, cacheu);
src/Common/StringSearcher.h:                    const auto v_against_l_or_u_offset = _mm_or_si128(v_against_l_offset, v_against_u_offset);
src/Common/StringSearcher.h:                    const auto mask_offset_both = _mm_movemask_epi8(v_against_l_or_u_offset);
src/Functions/FunctionsCodingIP.cpp:        __m128i mask = _mm_loadu_si128(reinterpret_cast<const __m128i *>(getCIDRMaskIPv6(bits_to_keep).data()));
src/Functions/FunctionsCodingIP.cpp:        __m128i lower = _mm_and_si128(_mm_loadu_si128(reinterpret_cast<const __m128i *>(src)), mask);
src/Functions/FunctionsCodingIP.cpp:        _mm_storeu_si128(reinterpret_cast<__m128i *>(dst_lower), lower);
src/Functions/FunctionsCodingIP.cpp:        __m128i inv_mask = _mm_xor_si128(mask, _mm_cmpeq_epi32(_mm_setzero_si128(), _mm_setzero_si128()));
src/Functions/FunctionsCodingIP.cpp:        __m128i upper = _mm_or_si128(lower, inv_mask);
src/Functions/FunctionsCodingIP.cpp:        _mm_storeu_si128(reinterpret_cast<__m128i *>(dst_upper), upper);
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                        _mm_cvtepi8_epi64(_mm_loadu_si128(reinterpret_cast<const __m128i *>(first_null_map + i + 2))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                        _mm_cvtepi8_epi64(_mm_loadu_si128(reinterpret_cast<const __m128i *>(first_null_map + i))))
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                        _mm_cvtepi8_epi32(_mm_loadu_si128(reinterpret_cast<const __m128i *>(first_null_map + i + 4))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                        _mm_cvtepi8_epi32(_mm_loadu_si128(reinterpret_cast<const __m128i *>(first_null_map + i))))
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                        _mm_cvtepi8_epi16(_mm_loadu_si128(reinterpret_cast<const __m128i *>(first_null_map + i + 8))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                        _mm_cvtepi8_epi16(_mm_loadu_si128(reinterpret_cast<const __m128i *>(first_null_map + i))))
src/Functions/GatherUtils/sliceHasImplAnyAll.h:    const __m128i zeros = _mm_setzero_si128();
src/Functions/GatherUtils/sliceHasImplAnyAll.h:            const __m128i second_data = _mm_loadu_si128(reinterpret_cast<const __m128i *>(second.data + j));
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                _mm_set_epi64x(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:            for (; i < first.size - 1 && !has_mask; has_mask = _mm_test_all_ones(bitmask), i += 2)
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                const __m128i first_data = _mm_loadu_si128(reinterpret_cast<const __m128i *>(first.data + i));
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                    _mm_cvtepi8_epi64(_mm_loadu_si128(reinterpret_cast<const __m128i *>(first_null_map + i)))
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                    _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                            _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_cmpeq_epi64(second_data, first_data)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_shuffle_epi32(first_nm_mask, _MM_SHUFFLE(1,0,3,2)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_cmpeq_epi64(second_data, _mm_shuffle_epi32(first_data, _MM_SHUFFLE(1,0,3,2))))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                    __m128i v_i = _mm_set1_epi64x(first.data[i]);
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                    bitmask = _mm_or_si128(bitmask, _mm_cmpeq_epi64(second_data, v_i));
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                    has_mask = _mm_test_all_ones(bitmask);
src/Functions/GatherUtils/sliceHasImplAnyAll.h:    const __m128i zeros = _mm_setzero_si128();
src/Functions/GatherUtils/sliceHasImplAnyAll.h:            const __m128i second_data = _mm_loadu_si128(reinterpret_cast<const __m128i *>(second.data + j));
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                _mm_set_epi32(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:            for (; i < first.size - 3 && !has_mask; has_mask = _mm_test_all_ones(bitmask), i += 4)
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                const __m128i first_data = _mm_loadu_si128(reinterpret_cast<const __m128i *>(first.data + i));
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                    _mm_cvtepi8_epi32(_mm_loadu_si128(reinterpret_cast<const __m128i *>(first_null_map + i)))
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                    _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                        _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                            _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_cmpeq_epi32(second_data, first_data)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_shuffle_epi32(first_nm_mask, _MM_SHUFFLE(2,1,0,3)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_cmpeq_epi32(second_data, _mm_shuffle_epi32(first_data, _MM_SHUFFLE(2,1,0,3))))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                            _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_shuffle_epi32(first_nm_mask, _MM_SHUFFLE(1,0,3,2)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_cmpeq_epi32(second_data, _mm_shuffle_epi32(first_data, _MM_SHUFFLE(1,0,3,2)))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_shuffle_epi32(first_nm_mask, _MM_SHUFFLE(0,3,2,1)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_cmpeq_epi32(second_data, _mm_shuffle_epi32(first_data, _MM_SHUFFLE(0,3,2,1)))))
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                    __m128i r_i = _mm_set1_epi32(first.data[i]);
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                    bitmask = _mm_or_si128(bitmask, _mm_cmpeq_epi32(second_data, r_i));
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                    has_mask = _mm_test_all_ones(bitmask);
src/Functions/GatherUtils/sliceHasImplAnyAll.h:    const __m128i zeros = _mm_setzero_si128();
src/Functions/GatherUtils/sliceHasImplAnyAll.h:            const __m128i second_data = _mm_loadu_si128(reinterpret_cast<const __m128i *>(second.data + j));
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                _mm_set_epi16(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:            for (; i < first.size-7 && !has_mask; has_mask = _mm_test_all_ones(bitmask), i += 8)
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                const __m128i first_data = _mm_loadu_si128(reinterpret_cast<const __m128i *>(first.data + i));
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                    _mm_cvtepi8_epi16(_mm_loadu_si128(reinterpret_cast<const __m128i *>(first_null_map + i)))
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                    _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                            _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi16(second_data, first_data)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(13,12,11,10,9,8,7,6,5,4,3,2,1,0,15,14)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi16(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(13,12,11,10,9,8,7,6,5,4,3,2,1,0,15,14))))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(11,10,9,8,7,6,5,4,3,2,1,0,15,14,13,12)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi16(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(11,10,9,8,7,6,5,4,3,2,1,0,15,14,13,12)))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(9,8,7,6,5,4,3,2,1,0,15,14,13,12,11,10)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi16(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(9,8,7,6,5,4,3,2,1,0,15,14,13,12,11,10)))))
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(7,6,5,4,3,2,1,0,15,14,13,12,11,10,9,8)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi16(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(7,6,5,4,3,2,1,0,15,14,13,12,11,10,9,8)))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(5,4,3,2,1,0,15,14,13,12,11,10,9,8,7,6)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_cmpeq_epi16(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(5,4,3,2,1,0,15,14,13,12,11,10,9,8,7,6))))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(3,2,1,0,15,14,13,12,11,10,9,8,7,6,5,4)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi16(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(3,2,1,0,15,14,13,12,11,10,9,8,7,6,5,4)))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(1,0,15,14,13,12,11,10,9,8,7,6,5,4,3,2)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi16(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(1,0,15,14,13,12,11,10,9,8,7,6,5,4,3,2))))))
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                    __m128i v_i = _mm_set1_epi16(first.data[i]);
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                    bitmask = _mm_or_si128(bitmask, _mm_cmpeq_epi16(second_data, v_i));
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                    has_mask = _mm_test_all_ones(bitmask);
src/Functions/GatherUtils/sliceHasImplAnyAll.h:    const __m128i zeros = _mm_setzero_si128();
src/Functions/GatherUtils/sliceHasImplAnyAll.h:            const __m128i second_data = _mm_loadu_si128(reinterpret_cast<const __m128i *>(second.data + j));
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                _mm_set_epi8(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:            for (; i < first.size - 15 && !has_mask; has_mask = _mm_test_all_ones(bitmask), i += 16)
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                const __m128i first_data = _mm_loadu_si128(reinterpret_cast<const __m128i *>(first.data + i));
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                    _mm_loadu_si128(reinterpret_cast<const __m128i *>(first_null_map + i))
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                    _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                        _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                            _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi8(second_data, first_data)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,15)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi8(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,15))))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(13,12,11,10,9,8,7,6,5,4,3,2,1,0,15,14)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi8(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(13,12,11,10,9,8,7,6,5,4,3,2,1,0,15,14)))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(12,11,10,9,8,7,6,5,4,3,2,1,0,15,14,13)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi8(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(12,11,10,9,8,7,6,5,4,3,2,1,0,15,14,13)))))
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(11,10,9,8,7,6,5,4,3,2,1,0,15,14,13,12)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi8(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(11,10,9,8,7,6,5,4,3,2,1,0,15,14,13,12)))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(10,9,8,7,6,5,4,3,2,1,0,15,14,13,12,11)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi8(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(10,9,8,7,6,5,4,3,2,1,0,15,14,13,12,11))))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(9,8,7,6,5,4,3,2,1,0,15,14,13,12,11,10)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi8(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(9,8,7,6,5,4,3,2,1,0,15,14,13,12,11,10)))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(8,7,6,5,4,3,2,1,0,15,14,13,12,11,10,9)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi8(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(8,7,6,5,4,3,2,1,0,15,14,13,12,11,10,9))))))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                            _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(7,6,5,4,3,2,1,0,15,14,13,12,11,10,9,8)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi8(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(7,6,5,4,3,2,1,0,15,14,13,12,11,10,9,8)))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(6,5,4,3,2,1,0,15,14,13,12,11,10,9,8,7)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi8(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(6,5,4,3,2,1,0,15,14,13,12,11,10,9,8,7))))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(5,4,3,2,1,0,15,14,13,12,11,10,9,8,7,6)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi8(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(5,4,3,2,1,0,15,14,13,12,11,10,9,8,7,6)))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(4,3,2,1,0,15,14,13,12,11,10,9,8,7,6,5)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi8(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(4,3,2,1,0,15,14,13,12,11,10,9,8,7,6,5)))))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(3,2,1,0,15,14,13,12,11,10,9,8,7,6,5,4)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi8(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(3,2,1,0,15,14,13,12,11,10,9,8,7,6,5,4)))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(2,1,0,15,14,13,12,11,10,9,8,7,6,5,4,3)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi8(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(2,1,0,15,14,13,12,11,10,9,8,7,6,5,4,3))))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                    _mm_or_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(1,0,15,14,13,12,11,10,9,8,7,6,5,4,3,2)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi8(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(1,0,15,14,13,12,11,10,9,8,7,6,5,4,3,2)))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                        _mm_andnot_si128(
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_shuffle_epi8(first_nm_mask, _mm_set_epi8(0,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1)),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                                            _mm_cmpeq_epi8(second_data, _mm_shuffle_epi8(first_data, _mm_set_epi8(0,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1)))))))),
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                    __m128i v_i = _mm_set1_epi8(first.data[i]);
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                    bitmask = _mm_or_si128(bitmask, _mm_cmpeq_epi8(second_data, v_i));
src/Functions/GatherUtils/sliceHasImplAnyAll.h:                    has_mask = _mm_test_all_ones(bitmask);
src/Functions/FunctionsStringSimilarity.cpp:        return _mm_crc32_u64(code_points[2], combined) & 0xFFFFu;
src/Functions/FunctionsStringHash.cpp:        return _mm_crc32_u64(crc, val);
src/Functions/FunctionsStringHash.cpp:        return _mm_crc32_u32(crc, val);
src/Functions/FunctionsStringHash.cpp:        return _mm_crc32_u16(crc, val);
src/Functions/FunctionsStringHash.cpp:        return _mm_crc32_u8(crc, val);
src/Functions/toValidUTF8.cpp:            while (p < simd_end && !_mm_movemask_epi8(_mm_loadu_si128(reinterpret_cast<const __m128i *>(p))))
src/Functions/LowerUpperUTF8Impl.h:        const auto v_zero = _mm_setzero_si128();
src/Functions/LowerUpperUTF8Impl.h:        const auto v_not_case_lower_bound = _mm_set1_epi8(not_case_lower_bound - 1);
src/Functions/LowerUpperUTF8Impl.h:        const auto v_not_case_upper_bound = _mm_set1_epi8(not_case_upper_bound + 1);
src/Functions/LowerUpperUTF8Impl.h:        const auto v_flip_case_mask = _mm_set1_epi8(flip_case_mask);
src/Functions/LowerUpperUTF8Impl.h:            const auto chars = _mm_loadu_si128(reinterpret_cast<const __m128i *>(src));
src/Functions/LowerUpperUTF8Impl.h:            const auto is_not_ascii = _mm_cmplt_epi8(chars, v_zero);
src/Functions/LowerUpperUTF8Impl.h:            const auto mask_is_not_ascii = _mm_movemask_epi8(is_not_ascii);
src/Functions/LowerUpperUTF8Impl.h:                    = _mm_and_si128(_mm_cmpgt_epi8(chars, v_not_case_lower_bound), _mm_cmplt_epi8(chars, v_not_case_upper_bound));
src/Functions/LowerUpperUTF8Impl.h:                const auto mask_is_not_case = _mm_movemask_epi8(is_not_case);
src/Functions/LowerUpperUTF8Impl.h:                    _mm_storeu_si128(reinterpret_cast<__m128i *>(dst), chars);
src/Functions/LowerUpperUTF8Impl.h:                    const auto xor_mask = _mm_and_si128(v_flip_case_mask, is_not_case);
src/Functions/LowerUpperUTF8Impl.h:                    const auto cased_chars = _mm_xor_si128(chars, xor_mask);
src/Functions/LowerUpperUTF8Impl.h:                    _mm_storeu_si128(reinterpret_cast<__m128i *>(dst), cased_chars);
src/Functions/LowerUpperImpl.h:            const auto v_not_case_lower_bound = _mm_set1_epi8(not_case_lower_bound - 1);
src/Functions/LowerUpperImpl.h:            const auto v_not_case_upper_bound = _mm_set1_epi8(not_case_upper_bound + 1);
src/Functions/LowerUpperImpl.h:            const auto v_flip_case_mask = _mm_set1_epi8(flip_case_mask);
src/Functions/LowerUpperImpl.h:                const auto chars = _mm_loadu_si128(reinterpret_cast<const __m128i *>(src));
src/Functions/LowerUpperImpl.h:                    = _mm_and_si128(_mm_cmpgt_epi8(chars, v_not_case_lower_bound), _mm_cmplt_epi8(chars, v_not_case_upper_bound));
src/Functions/LowerUpperImpl.h:                const auto xor_mask = _mm_and_si128(v_flip_case_mask, is_not_case);
src/Functions/LowerUpperImpl.h:                const auto cased_chars = _mm_xor_si128(chars, xor_mask);
src/Functions/LowerUpperImpl.h:                _mm_storeu_si128(reinterpret_cast<__m128i *>(dst), cased_chars);
src/Functions/isValidUTF8.cpp:        const __m128i first_len_tbl = _mm_setr_epi8(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 3);
src/Functions/isValidUTF8.cpp:        const __m128i first_range_tbl = _mm_setr_epi8(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8);
src/Functions/isValidUTF8.cpp:            = _mm_setr_epi8(0x00, 0x80, 0x80, 0x80, 0xA0, 0x80, 0x90, 0x80, 0xC2, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F);
src/Functions/isValidUTF8.cpp:            = _mm_setr_epi8(0x7F, 0xBF, 0xBF, 0xBF, 0xBF, 0x9F, 0xBF, 0x8F, 0xF4, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80);
src/Functions/isValidUTF8.cpp:        const __m128i df_ee_tbl = _mm_setr_epi8(0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0);
src/Functions/isValidUTF8.cpp:        const __m128i ef_fe_tbl = _mm_setr_epi8(0, 3, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
src/Functions/isValidUTF8.cpp:        __m128i prev_input = _mm_set1_epi8(0);
src/Functions/isValidUTF8.cpp:        __m128i prev_first_len = _mm_set1_epi8(0);
src/Functions/isValidUTF8.cpp:        __m128i error = _mm_set1_epi8(0);
src/Functions/isValidUTF8.cpp:            const __m128i high_nibbles = _mm_and_si128(_mm_srli_epi16(input, 4), _mm_set1_epi8(0x0F));
src/Functions/isValidUTF8.cpp:            __m128i first_len = _mm_shuffle_epi8(first_len_tbl, high_nibbles);
src/Functions/isValidUTF8.cpp:            __m128i range = _mm_shuffle_epi8(first_range_tbl, high_nibbles);
src/Functions/isValidUTF8.cpp:            range = _mm_or_si128(range, _mm_alignr_epi8(first_len, prev_first_len, 15));
src/Functions/isValidUTF8.cpp:            tmp1 = _mm_subs_epu8(first_len, _mm_set1_epi8(1));
src/Functions/isValidUTF8.cpp:            tmp2 = _mm_subs_epu8(prev_first_len, _mm_set1_epi8(1));
src/Functions/isValidUTF8.cpp:            range = _mm_or_si128(range, _mm_alignr_epi8(tmp1, tmp2, 14));
src/Functions/isValidUTF8.cpp:            tmp1 = _mm_subs_epu8(first_len, _mm_set1_epi8(2));
src/Functions/isValidUTF8.cpp:            tmp2 = _mm_subs_epu8(prev_first_len, _mm_set1_epi8(2));
src/Functions/isValidUTF8.cpp:            range = _mm_or_si128(range, _mm_alignr_epi8(tmp1, tmp2, 13));
src/Functions/isValidUTF8.cpp:            shift1 = _mm_alignr_epi8(input, prev_input, 15);
src/Functions/isValidUTF8.cpp:            pos = _mm_sub_epi8(shift1, _mm_set1_epi8(0xEF));
src/Functions/isValidUTF8.cpp:            tmp1 = _mm_subs_epu8(pos, _mm_set1_epi8(0xF0));
src/Functions/isValidUTF8.cpp:            range2 = _mm_shuffle_epi8(df_ee_tbl, tmp1);
src/Functions/isValidUTF8.cpp:            tmp2 = _mm_adds_epu8(pos, _mm_set1_epi8(112));
src/Functions/isValidUTF8.cpp:            range2 = _mm_add_epi8(range2, _mm_shuffle_epi8(ef_fe_tbl, tmp2));
src/Functions/isValidUTF8.cpp:            range = _mm_add_epi8(range, range2);
src/Functions/isValidUTF8.cpp:            __m128i minv = _mm_shuffle_epi8(range_min_tbl, range);
src/Functions/isValidUTF8.cpp:            __m128i maxv = _mm_shuffle_epi8(range_max_tbl, range);
src/Functions/isValidUTF8.cpp:            error = _mm_or_si128(error, _mm_cmplt_epi8(input, minv));
src/Functions/isValidUTF8.cpp:            error = _mm_or_si128(error, _mm_cmpgt_epi8(input, maxv));
src/Functions/isValidUTF8.cpp:            check_packed(_mm_loadu_si128(reinterpret_cast<const __m128i *>(data)));
src/Functions/isValidUTF8.cpp:        _mm_store_si128(reinterpret_cast<__m128i *>(buf), _mm_loadu_si128(reinterpret_cast<const __m128i *>(data - 1)));
src/Functions/isValidUTF8.cpp:        check_packed(_mm_loadu_si128(reinterpret_cast<__m128i *>(buf + 1)));
src/Functions/isValidUTF8.cpp:        return _mm_testz_si128(error, error);
src/Functions/FunctionsStringDistance.cpp:            __m128i s1 = _mm_loadu_si128(reinterpret_cast<const __m128i *>(haystack));
src/Functions/FunctionsStringDistance.cpp:            __m128i s2 = _mm_loadu_si128(reinterpret_cast<const __m128i *>(needle));
src/Functions/FunctionsStringDistance.cpp:            auto result_mask = _mm_cmpestrm(s1, 16, s2, 16, mode);
src/Functions/FunctionsStringDistance.cpp:            const __m128i mask_hi = _mm_unpackhi_epi64(result_mask, result_mask);
src/Functions/FunctionsStringDistance.cpp:            res += _mm_popcnt_u64(_mm_cvtsi128_si64(result_mask)) + _mm_popcnt_u64(_mm_cvtsi128_si64(mask_hi));
src/Functions/divide/divideImpl.cpp:        _mm_storeu_si128(reinterpret_cast<__m128i *>(c_pos),
src/Functions/divide/divideImpl.cpp:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(a_pos)) / divider);
src/Functions/FunctionsRound.h:    static VectorType load(const ScalarType * in) { return _mm_loadu_ps(in); }
src/Functions/FunctionsRound.h:    static VectorType load1(const ScalarType in) { return _mm_load1_ps(&in); }
src/Functions/FunctionsRound.h:    static void store(ScalarType * out, VectorType val) { _mm_storeu_ps(out, val);}
src/Functions/FunctionsRound.h:    static VectorType multiply(VectorType val, VectorType scale) { return _mm_mul_ps(val, scale); }
src/Functions/FunctionsRound.h:    static VectorType divide(VectorType val, VectorType scale) { return _mm_div_ps(val, scale); }
src/Functions/FunctionsRound.h:    template <RoundingMode mode> static VectorType apply(VectorType val) { return _mm_round_ps(val, int(mode)); }
src/Functions/FunctionsRound.h:    static VectorType load(const ScalarType * in) { return _mm_loadu_pd(in); }
src/Functions/FunctionsRound.h:    static VectorType load1(const ScalarType in) { return _mm_load1_pd(&in); }
src/Functions/FunctionsRound.h:    static void store(ScalarType * out, VectorType val) { _mm_storeu_pd(out, val);}
src/Functions/FunctionsRound.h:    static VectorType multiply(VectorType val, VectorType scale) { return _mm_mul_pd(val, scale); }
src/Functions/FunctionsRound.h:    static VectorType divide(VectorType val, VectorType scale) { return _mm_div_pd(val, scale); }
src/Functions/FunctionsRound.h:    template <RoundingMode mode> static VectorType apply(VectorType val) { return _mm_round_pd(val, int(mode)); }
src/Columns/ColumnVector.cpp:                    __m128i copy_batch = _mm_loadu_si128(reinterpret_cast<const __m128i *>(data_copy_begin_ptr));
src/Columns/ColumnVector.cpp:                    _mm_storeu_si128(reinterpret_cast<__m128i *>(result_data_copy), copy_batch);
src/Columns/ColumnVector.cpp:            __m128i copy_element_data = _mm_set1_epi32(data[offset_index]);
src/Columns/ColumnVector.cpp:                _mm_storeu_si128(reinterpret_cast<__m128i *>(result_data_tmp), copy_element_data);
src/Columns/ColumnVector.cpp:                __m128i copy_batch = _mm_loadu_si128(reinterpret_cast<const __m128i *>(data_copy_begin_ptr));
src/Columns/ColumnVector.cpp:                _mm_storeu_si128(reinterpret_cast<__m128i *>(result_data), copy_batch);
src/Columns/ColumnsCommon.cpp:    static const __m128i zero16 = _mm_setzero_si128();
src/Columns/ColumnsCommon.cpp:        static_cast<UInt64>(_mm_movemask_epi8(_mm_cmpeq_epi8(
src/Columns/ColumnsCommon.cpp:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(bytes64)), zero16)))
src/Columns/ColumnsCommon.cpp:        | (static_cast<UInt64>(_mm_movemask_epi8(_mm_cmpeq_epi8(
src/Columns/ColumnsCommon.cpp:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(bytes64 + 16)), zero16))) << 16)
src/Columns/ColumnsCommon.cpp:        | (static_cast<UInt64>(_mm_movemask_epi8(_mm_cmpeq_epi8(
src/Columns/ColumnsCommon.cpp:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(bytes64 + 32)), zero16))) << 32)
src/Columns/ColumnsCommon.cpp:        | (static_cast<UInt64>(_mm_movemask_epi8(_mm_cmpeq_epi8(
src/Columns/ColumnsCommon.cpp:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(bytes64 + 48)), zero16))) << 48);
src/Columns/ColumnsCommon.h:    const __m128i zero16 = _mm_setzero_si128();
src/Columns/ColumnsCommon.h:        (static_cast<UInt64>(_mm_movemask_epi8(_mm_cmpeq_epi8(
src/Columns/ColumnsCommon.h:        _mm_loadu_si128(reinterpret_cast<const __m128i *>(bytes64)), zero16))) & 0xffff)
src/Columns/ColumnsCommon.h:        | ((static_cast<UInt64>(_mm_movemask_epi8(_mm_cmpeq_epi8(
src/Columns/ColumnsCommon.h:        _mm_loadu_si128(reinterpret_cast<const __m128i *>(bytes64 + 16)), zero16))) << 16) & 0xffff0000)
src/Columns/ColumnsCommon.h:        | ((static_cast<UInt64>(_mm_movemask_epi8(_mm_cmpeq_epi8(
src/Columns/ColumnsCommon.h:        _mm_loadu_si128(reinterpret_cast<const __m128i *>(bytes64 + 32)), zero16))) << 32) & 0xffff00000000)
src/Columns/ColumnsCommon.h:        | ((static_cast<UInt64>(_mm_movemask_epi8(_mm_cmpeq_epi8(
src/Columns/ColumnsCommon.h:        _mm_loadu_si128(reinterpret_cast<const __m128i *>(bytes64 + 48)), zero16))) << 48) & 0xffff000000000000);
src/Interpreters/examples/hash_map_string_2.cpp:    return 0xFFFF == _mm_movemask_epi8(_mm_cmpeq_epi8(
src/Interpreters/examples/hash_map_string_2.cpp:        _mm_loadu_si128(reinterpret_cast<const __m128i *>(p1)),
src/Interpreters/examples/hash_map_string_2.cpp:        _mm_loadu_si128(reinterpret_cast<const __m128i *>(p2))));
src/Interpreters/examples/hash_map_string_2.cpp:    return !_mm_movemask_ps(_mm_cmpneq_ps(                    /// Looks like incorrect while comparing subnormal floats.
src/Interpreters/examples/hash_map_string_2.cpp:        _mm_loadu_ps(reinterpret_cast<const float *>(p1)),
src/Interpreters/examples/hash_map_string_2.cpp:        _mm_loadu_ps(reinterpret_cast<const float *>(p2))));
src/Interpreters/examples/hash_map_string_2.cpp:    __m128i zero16 = _mm_setzero_si128();
src/Interpreters/examples/hash_map_string_2.cpp:        if (!_mm_testc_si128(
src/Interpreters/examples/hash_map_string_2.cpp:            _mm_xor_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                _mm_loadu_si128(reinterpret_cast<const __m128i *>(p1)),
src/Interpreters/examples/hash_map_string_2.cpp:                _mm_loadu_si128(reinterpret_cast<const __m128i *>(p2)))))
src/Interpreters/examples/hash_map_string_2.cpp:    __m128i zero16 = _mm_setzero_si128();
src/Interpreters/examples/hash_map_string_2.cpp:        if (_mm_testc_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                _mm_xor_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                    _mm_loadu_si128(&reinterpret_cast<const __m128i *>(p1)[0]),
src/Interpreters/examples/hash_map_string_2.cpp:                    _mm_loadu_si128(&reinterpret_cast<const __m128i *>(p2)[0])))
src/Interpreters/examples/hash_map_string_2.cpp:            && _mm_testc_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                _mm_xor_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                    _mm_loadu_si128(&reinterpret_cast<const __m128i *>(p1)[1]),
src/Interpreters/examples/hash_map_string_2.cpp:                    _mm_loadu_si128(&reinterpret_cast<const __m128i *>(p2)[1])))
src/Interpreters/examples/hash_map_string_2.cpp:            && _mm_testc_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                _mm_xor_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                    _mm_loadu_si128(&reinterpret_cast<const __m128i *>(p1)[2]),
src/Interpreters/examples/hash_map_string_2.cpp:                    _mm_loadu_si128(&reinterpret_cast<const __m128i *>(p2)[2])))
src/Interpreters/examples/hash_map_string_2.cpp:            && _mm_testc_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                _mm_xor_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                    _mm_loadu_si128(&reinterpret_cast<const __m128i *>(p1)[3]),
src/Interpreters/examples/hash_map_string_2.cpp:                    _mm_loadu_si128(&reinterpret_cast<const __m128i *>(p2)[3]))))
src/Interpreters/examples/hash_map_string_2.cpp:            if (!_mm_testc_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                _mm_xor_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                    _mm_loadu_si128(&reinterpret_cast<const __m128i *>(p1)[2]),
src/Interpreters/examples/hash_map_string_2.cpp:                    _mm_loadu_si128(&reinterpret_cast<const __m128i *>(p2)[2]))))
src/Interpreters/examples/hash_map_string_2.cpp:            if (!_mm_testc_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                _mm_xor_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                    _mm_loadu_si128(&reinterpret_cast<const __m128i *>(p1)[1]),
src/Interpreters/examples/hash_map_string_2.cpp:                    _mm_loadu_si128(&reinterpret_cast<const __m128i *>(p2)[1]))))
src/Interpreters/examples/hash_map_string_2.cpp:            if (!_mm_testc_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                _mm_xor_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                    _mm_loadu_si128(&reinterpret_cast<const __m128i *>(p1)[0]),
src/Interpreters/examples/hash_map_string_2.cpp:                    _mm_loadu_si128(&reinterpret_cast<const __m128i *>(p2)[0]))))
src/Interpreters/examples/hash_map_string_2.cpp:        if (_mm_testc_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                _mm_xor_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                    _mm_loadu_si128(&reinterpret_cast<const __m128i *>(p1)[0]),
src/Interpreters/examples/hash_map_string_2.cpp:                    _mm_loadu_si128(&reinterpret_cast<const __m128i *>(p2)[0])))
src/Interpreters/examples/hash_map_string_2.cpp:            & _mm_testc_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                _mm_xor_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                    _mm_loadu_si128(&reinterpret_cast<const __m128i *>(p1)[1]),
src/Interpreters/examples/hash_map_string_2.cpp:                    _mm_loadu_si128(&reinterpret_cast<const __m128i *>(p2)[1]))))
src/Interpreters/examples/hash_map_string_2.cpp:        if (_mm_testc_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                _mm_xor_si128(
src/Interpreters/examples/hash_map_string_2.cpp:                    _mm_loadu_si128(&reinterpret_cast<const __m128i *>(p1)[0]),
src/Interpreters/examples/hash_map_string_2.cpp:                    _mm_loadu_si128(&reinterpret_cast<const __m128i *>(p2)[0]))))
src/Interpreters/examples/hash_map_string_3.cpp:            res = _mm_crc32_u64(res, word);
src/Interpreters/examples/hash_map_string_3.cpp:        res = _mm_crc32_u64(res, word);
src/Interpreters/examples/hash_map_string_3.cpp:            res0 = _mm_crc32_u64(res0, word0);
src/Interpreters/examples/hash_map_string_3.cpp:            res1 = _mm_crc32_u64(res1, word1);
src/Interpreters/examples/hash_map_string_3.cpp:        res0 = _mm_crc32_u64(res0, word0);
src/Interpreters/examples/hash_map_string_3.cpp:        res1 = _mm_crc32_u64(res1, word1);
src/Interpreters/AggregationCommon.h:    __m128i res = _mm_shuffle_epi8(
src/Interpreters/AggregationCommon.h:        _mm_loadu_si128(reinterpret_cast<const __m128i *>(srcs[0] + elem_sizes[0] * idx)),
src/Interpreters/AggregationCommon.h:        _mm_loadu_si128(reinterpret_cast<const __m128i *>(masks)));
src/Interpreters/AggregationCommon.h:        res = _mm_xor_si128(res,
src/Interpreters/AggregationCommon.h:            _mm_shuffle_epi8(
src/Interpreters/AggregationCommon.h:                _mm_loadu_si128(reinterpret_cast<const __m128i *>(srcs[i] + elem_sizes[i] * idx)),
src/Interpreters/AggregationCommon.h:                _mm_loadu_si128(reinterpret_cast<const __m128i *>(&masks[i * sizeof(T)]))));
src/Interpreters/ITokenExtractor.cpp:        const __m128i haystack = _mm_loadu_si128(reinterpret_cast<const __m128i *>(data + *pos));
src/Interpreters/ITokenExtractor.cpp:        const auto alnum_chars_ranges = _mm_set_epi8(0, 0, 0, 0, 0, 0, 0, 0,
src/Interpreters/ITokenExtractor.cpp:        const unsigned result_bitmask = _mm_cvtsi128_si32(_mm_cmpestrm(alnum_chars_ranges, 8, haystack, haystack_length, _SIDD_CMP_RANGES));
src/Interpreters/ITokenExtractor.cpp:        const auto number_begin =      _mm_set1_epi8('0' - 1);
src/Interpreters/ITokenExtractor.cpp:        const auto number_end =        _mm_set1_epi8('9' + 1);
src/Interpreters/ITokenExtractor.cpp:        const auto alpha_lower_begin = _mm_set1_epi8('a' - 1);
src/Interpreters/ITokenExtractor.cpp:        const auto alpha_lower_end =   _mm_set1_epi8('z' + 1);
src/Interpreters/ITokenExtractor.cpp:        const auto alpha_upper_begin = _mm_set1_epi8('A' - 1);
src/Interpreters/ITokenExtractor.cpp:        const auto alpha_upper_end =   _mm_set1_epi8('Z' + 1);
src/Interpreters/ITokenExtractor.cpp:        const auto zero =              _mm_set1_epi8(0);
src/Interpreters/ITokenExtractor.cpp:        // < 0 since _mm_cmplt_epi8 threats chars as SIGNED, and so all chars > 0x80 are negative.
src/Interpreters/ITokenExtractor.cpp:        const unsigned result_bitmask = _mm_movemask_epi8(_mm_or_si128(_mm_or_si128(_mm_or_si128(
src/Interpreters/ITokenExtractor.cpp:                _mm_cmplt_epi8(haystack, zero),
src/Interpreters/ITokenExtractor.cpp:                _mm_and_si128(_mm_cmpgt_epi8(haystack, number_begin),      _mm_cmplt_epi8(haystack, number_end))),
src/Interpreters/ITokenExtractor.cpp:                _mm_and_si128(_mm_cmpgt_epi8(haystack, alpha_lower_begin), _mm_cmplt_epi8(haystack, alpha_lower_end))),
src/Interpreters/ITokenExtractor.cpp:                _mm_and_si128(_mm_cmpgt_epi8(haystack, alpha_upper_begin), _mm_cmplt_epi8(haystack, alpha_upper_end))));
src/Interpreters/sortBlock.cpp:                __m128i permutation_data_vector = _mm_loadu_si128(reinterpret_cast<const __m128i *>(permutation_data + i + j * 2));
src/Interpreters/sortBlock.cpp:                __m128i permutation_equals_vector = _mm_cmpeq_epi8(permutation_data_vector, permutation_compare_values_vectors[j]);
src/Interpreters/sortBlock.cpp:                permutation_compare_values_vectors[j] = _mm_add_epi64(permutation_compare_values_vectors[j], permutation_add_vector);
src/Interpreters/sortBlock.cpp:                permutation_equals_vector_mask &= _mm_movemask_epi8(permutation_equals_vector);
src/IO/ReadHelpers.cpp:                auto rc = _mm_set1_epi8('\r');
src/IO/ReadHelpers.cpp:                auto nc = _mm_set1_epi8('\n');
src/IO/ReadHelpers.cpp:                auto dc = _mm_set1_epi8(delimiter);
src/IO/ReadHelpers.cpp:                    __m128i bytes = _mm_loadu_si128(reinterpret_cast<const __m128i *>(next_pos));
src/IO/ReadHelpers.cpp:                    auto eq = _mm_or_si128(_mm_or_si128(_mm_cmpeq_epi8(bytes, rc), _mm_cmpeq_epi8(bytes, nc)), _mm_cmpeq_epi8(bytes, dc));
src/IO/ReadHelpers.cpp:                    uint16_t bit_mask = _mm_movemask_epi8(eq);
src/IO/WriteBufferValidUTF8.cpp:        while (p < simd_end && !_mm_movemask_epi8(_mm_loadu_si128(reinterpret_cast<const __m128i*>(p))))
src/Storages/MergeTree/MergeTreeRangeReader.cpp:    const __m128i zero16 = _mm_setzero_si128();
src/Storages/MergeTree/MergeTreeRangeReader.cpp:                static_cast<UInt64>(_mm_movemask_epi8(_mm_cmpeq_epi8(
src/Storages/MergeTree/MergeTreeRangeReader.cpp:                        _mm_loadu_si128(reinterpret_cast<const __m128i *>(pos)),
src/Storages/MergeTree/MergeTreeRangeReader.cpp:                | (static_cast<UInt64>(_mm_movemask_epi8(_mm_cmpeq_epi8(
src/Storages/MergeTree/MergeTreeRangeReader.cpp:                        _mm_loadu_si128(reinterpret_cast<const __m128i *>(pos + 16)),
src/Storages/MergeTree/MergeTreeRangeReader.cpp:                | (static_cast<UInt64>(_mm_movemask_epi8(_mm_cmpeq_epi8(
src/Storages/MergeTree/MergeTreeRangeReader.cpp:                        _mm_loadu_si128(reinterpret_cast<const __m128i *>(pos + 32)),
src/Storages/MergeTree/MergeTreeRangeReader.cpp:                | (static_cast<UInt64>(_mm_movemask_epi8(_mm_cmpeq_epi8(
src/Storages/MergeTree/MergeTreeRangeReader.cpp:                        _mm_loadu_si128(reinterpret_cast<const __m128i *>(pos + 48)),
src/Storages/MergeTree/MergeTreeRangeReader.cpp:    const __m128i zero16 = _mm_setzero_si128();
src/Storages/MergeTree/MergeTreeRangeReader.cpp:        __m128i src = _mm_loadu_si128(reinterpret_cast<__m128i *>(first_begin));
src/Storages/MergeTree/MergeTreeRangeReader.cpp:        __m128i inv_mask = _mm_cmpeq_epi8(src, zero16);
src/Storages/MergeTree/MergeTreeRangeReader.cpp:            ~static_cast<UInt64>(_mm_extract_epi64(inv_mask, 0)),
src/Storages/MergeTree/MergeTreeRangeReader.cpp:            ~static_cast<UInt64>(_mm_extract_epi64(inv_mask, 1)),
src/Compression/LZ4_decompress_faster.cpp:  *  and compiler library has the corresponding intrinsic: '_mm_shuffle_pi8'.
src/Compression/LZ4_decompress_faster.cpp:  *  unalignedStore(op, _mm_shuffle_pi8(
src/Compression/LZ4_decompress_faster.cpp:        [[maybe_unused]] __m64 shuffled = _mm_shuffle_pi8(__m64{}, __m64{});
src/Compression/LZ4_decompress_faster.cpp:        [[maybe_unused]] __m64 shuffled = _mm_shuffle_pi8(__m64{}, __m64{});
src/Compression/LZ4_decompress_faster.cpp:    _mm_storeu_si128(reinterpret_cast<__m128i *>(op),
src/Compression/LZ4_decompress_faster.cpp:        _mm_shuffle_epi8(
src/Compression/LZ4_decompress_faster.cpp:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(match)),
src/Compression/LZ4_decompress_faster.cpp:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(masks + 8 * offset))));
src/Compression/LZ4_decompress_faster.cpp:    _mm_storeu_si128(reinterpret_cast<__m128i *>(dst),
src/Compression/LZ4_decompress_faster.cpp:        _mm_loadu_si128(reinterpret_cast<const __m128i *>(src)));
src/Compression/LZ4_decompress_faster.cpp:    _mm_storeu_si128(reinterpret_cast<__m128i *>(op),
src/Compression/LZ4_decompress_faster.cpp:        _mm_shuffle_epi8(
src/Compression/LZ4_decompress_faster.cpp:            _mm_loadu_si128(reinterpret_cast<const __m128i *>(match)),
src/Compression/LZ4_decompress_faster.cpp:            _mm_load_si128(reinterpret_cast<const __m128i *>(masks) + offset)));
src/Compression/LZ4_decompress_faster.cpp:    _mm_storeu_si128(reinterpret_cast<__m128i *>(dst),
src/Compression/LZ4_decompress_faster.cpp:        _mm_loadu_si128(reinterpret_cast<const __m128i *>(src)));
src/Compression/LZ4_decompress_faster.cpp:    _mm_storeu_si128(reinterpret_cast<__m128i *>(dst + 16),
src/Compression/LZ4_decompress_faster.cpp:        _mm_loadu_si128(reinterpret_cast<const __m128i *>(src + 16)));


