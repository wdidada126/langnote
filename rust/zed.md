# zed

## build
没有图形界面，编译不了
纯命令行的不行
	
https://github.com/zed-industries/zed/blob/main/docs/src/development/macos.md

  cargo:warning=/Applications/Xcode_15.4.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX14.5.sdk/usr/include/c++/v1/__memory/pointer_traits.h:182:20: note: in instantiation of template class 'std::pointer_traits<rust::Slice<const unsigned char>::iterator>' requested here
  cargo:warning=    decltype((void)pointer_traits<_Pointer>::to_address(std::declval<const _Pointer&>()))
  cargo:warning=                   ^
  cargo:warning=/Applications/Xcode_15.4.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX14.5.sdk/usr/include/c++/v1/__memory/pointer_traits.h:195:59: note: during template argument deduction for class template partial specialization '_HasToAddress<_Pointer, decltype((void)pointer_traits<_Pointer>::to_address(std::declval<const _Pointer &>()))>' [with _Pointer = rust::Slice<const unsigned char>::iterator]
  cargo:warning=  static const bool value = _HasArrow<_Pointer>::value || _HasToAddress<_Pointer>::value;
  cargo:warning=                                                          ^
  cargo:warning=/Applications/Xcode_15.4.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX14.5.sdk/usr/include/c++/v1/__memory/pointer_traits.h:195:59: note: in instantiation of template class 'std::_HasToAddress<rust::Slice<const unsigned char>::iterator>' requested here
  cargo:warning=/Applications/Xcode_15.4.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX14.5.sdk/usr/include/c++/v1/__type_traits/conjunction.h:27:32: note: in instantiation of template class 'std::_IsFancyPointer<rust::Slice<const unsigned char>::iterator>' requested here
  cargo:warning=__expand_to_true<__enable_if_t<_Pred::value>...> __and_helper(int);
  cargo:warning=                               ^
  cargo:warning=/Applications/Xcode_15.4.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX14.5.sdk/usr/include/c++/v1/__type_traits/conjunction.h:38:39: note: while substituting explicitly-specified template arguments into function template '__and_helper' 
  cargo:warning=using _And _LIBCPP_NODEBUG = decltype(std::__and_helper<_Pred...>(0));
  cargo:warning=                                      ^
  cargo:warning=/Applications/Xcode_15.4.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX14.5.sdk/usr/include/c++/v1/__memory/pointer_traits.h:200:5: note: (skipping 4 contexts in backtrace; use -ftemplate-backtrace-limit=0 to see all)
  cargo:warning=    _And<is_class<_Pointer>, _IsFancyPointer<_Pointer> >::value
  cargo:warning=    ^
  cargo:warning=/Applications/Xcode_15.4.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX14.5.sdk/usr/include/c++/v1/__iterator/concepts.h:193:7: note: in instantiation of requirement here
  cargo:warning=    { _VSTD::to_address(__i) } -> same_as<add_pointer_t<iter_reference_t<_Ip>>>;
  cargo:warning=      ^~~~~~~~~~~~~~~~~~~~~~
  cargo:warning=/Applications/Xcode_15.4.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX14.5.sdk/usr/include/c++/v1/__config:897:17: note: expanded from macro '_VSTD'
  cargo:warning=#  define _VSTD std
  cargo:warning=                ^
  cargo:warning=/Applications/Xcode_15.4.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX14.5.sdk/usr/include/c++/v1/__iterator/concepts.h:192:3: note: while substituting template arguments into constraint expression here
  cargo:warning=  requires(const _Ip& __i) {
  cargo:warning=  ^~~~~~~~~~~~~~~~~~~~~~~~~~
  cargo:warning=/Applications/Xcode_15.4.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX14.5.sdk/usr/include/c++/v1/__ranges/concepts.h:122:5: note: while checking the satisfaction of concept 'contiguous_iterator<rust::Slice<const unsigned char>::iterator>' requested here
  cargo:warning=    contiguous_iterator<iterator_t<_Tp>> &&
  cargo:warning=    ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  cargo:warning=/Applications/Xcode_15.4.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX14.5.sdk/usr/include/c++/v1/__ranges/concepts.h:122:5: note: while substituting template arguments into constraint expression here
  cargo:warning=    contiguous_iterator<iterator_t<_Tp>> &&
  cargo:warning=    ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  cargo:warning=/Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/webrtc-sys-8f834a218b870a1b/out/cxxbridge/include/rust/cxx.h:282:15: note: while checking the satisfaction of concept 'contiguous_range<rust::Slice<const unsigned char>>' requested here
  cargo:warning=static_assert(std::ranges::contiguous_range<rust::Slice<const uint8_t>>);
  cargo:warning=              ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  cargo:warning=/Applications/Xcode_15.4.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX14.5.sdk/usr/include/c++/v1/__memory/pointer_traits.h:38:8: note: template is declared here
  cargo:warning=struct __pointer_traits_element_type;
  cargo:warning=       ^
  cargo:warning=1 error generated.

  exit status: 0
  exit status: 0
  exit status: 0
  exit status: 1
  cargo:warning=ToolExecError: command did not execute successfully (status code exit status: 1): env -u IPHONEOS_DEPLOYMENT_TARGET LC_ALL="C" "c++" "-O0" "-ffunction-sections" "-fdata-sections" "-fPIC" "-gdwarf-2" "-fno-omit-frame-pointer" "--target=arm64-apple-macosx" "-mmacosx-version-min=10.15.7" "-I" "/Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/webrtc-sys-8f834a218b870a1b/out/cxxbridge/include" "-I" "/Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/webrtc-sys-8f834a218b870a1b/out/cxxbridge/crate" "-I" "./include" "-I" "/Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/scratch-3f78e32e64413657/out/livekit_webrtc/livekit/mac-arm64-release-webrtc-b99fd2c-6/mac-arm64-release/include" "-I" "/Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/scratch-3f78e32e64413657/out/livekit_webrtc/livekit/mac-arm64-release-webrtc-b99fd2c-6/mac-arm64-release/include/third_party/abseil-cpp/" "-I" "/Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/scratch-3f78e32e64413657/out/livekit_webrtc/livekit/mac-arm64-release-webrtc-b99fd2c-6/mac-arm64-release/include/third_party/libyuv/include/" "-I" "/Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/scratch-3f78e32e64413657/out/livekit_webrtc/livekit/mac-arm64-release-webrtc-b99fd2c-6/mac-arm64-release/include/third_party/libc++/" "-I" "/Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/scratch-3f78e32e64413657/out/livekit_webrtc/livekit/mac-arm64-release-webrtc-b99fd2c-6/mac-arm64-release/include/sdk/objc" "-I" "/Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/scratch-3f78e32e64413657/out/livekit_webrtc/livekit/mac-arm64-release-webrtc-b99fd2c-6/mac-arm64-release/include/sdk/objc/base" "-isysroot/Applications/Xcode_15.4.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX14.5.sdk" "-stdlib=libc++" "-std=c++20" "-DWEBRTC_APM_DEBUG_DUMP=0" "-D__STDC_CONSTANT_MACROS" "-D__STDC_FORMAT_MACROS" "-D_FORTIFY_SOURCE=2" "-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_NONE" "-DNDEBUG" "-DNVALGRIND" "-DDYNAMIC_ANNOTATIONS_ENABLED=0" "-DWEBRTC_ENABLE_PROTOBUF=0" "-DWEBRTC_STRICT_FIELD_TRIALS=0" "-DWEBRTC_INCLUDE_INTERNAL_AUDIO_DEVICE" "-DRTC_USE_LIBAOM_AV1_ENCODER" "-DRTC_ENABLE_VP9" "-DRTC_DAV1D_IN_INTERNAL_DECODER_FACTORY" "-DWEBRTC_HAVE_SCTP" "-DWEBRTC_USE_H264" "-DWEBRTC_ARCH_ARM64" "-DWEBRTC_HAS_NEON" "-DWEBRTC_LIBRARY_IMPL" "-DWEBRTC_ENABLE_SYMBOL_EXPORT" "-DWEBRTC_ENABLE_AVX2" "-DWEBRTC_NON_STATIC_TRACE_EVENT_HANDLERS=0" "-DWEBRTC_POSIX" "-DWEBRTC_MAC" "-DABSL_ALLOCATOR_NOTHROW=1" "-DLIBYUV_DISABLE_LSX" "-DLIBYUV_DISABLE_LASX" "-DLIVEKIT_TEST" "-o" "/Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/webrtc-sys-8f834a218b870a1b/out/0602fb52cb66f316-audio_mixer.o" "-c" "src/audio_mixer.cpp"
  exit status: 0
  exit status: 0

  --- stderr

  CXX include path:
    /Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/webrtc-sys-8f834a218b870a1b/out/cxxbridge/include
    /Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/webrtc-sys-8f834a218b870a1b/out/cxxbridge/crate


  error occurred in cc-rs: command did not execute successfully (status code exit status: 1): env -u IPHONEOS_DEPLOYMENT_TARGET LC_ALL="C" "c++" "-O0" "-ffunction-sections" "-fdata-sections" "-fPIC" "-gdwarf-2" "-fno-omit-frame-pointer" "--target=arm64-apple-macosx" "-mmacosx-version-min=10.15.7" "-I" "/Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/webrtc-sys-8f834a218b870a1b/out/cxxbridge/include" "-I" "/Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/webrtc-sys-8f834a218b870a1b/out/cxxbridge/crate" "-I" "./include" "-I" "/Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/scratch-3f78e32e64413657/out/livekit_webrtc/livekit/mac-arm64-release-webrtc-b99fd2c-6/mac-arm64-release/include" "-I" "/Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/scratch-3f78e32e64413657/out/livekit_webrtc/livekit/mac-arm64-release-webrtc-b99fd2c-6/mac-arm64-release/include/third_party/abseil-cpp/" "-I" "/Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/scratch-3f78e32e64413657/out/livekit_webrtc/livekit/mac-arm64-release-webrtc-b99fd2c-6/mac-arm64-release/include/third_party/libyuv/include/" "-I" "/Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/scratch-3f78e32e64413657/out/livekit_webrtc/livekit/mac-arm64-release-webrtc-b99fd2c-6/mac-arm64-release/include/third_party/libc++/" "-I" "/Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/scratch-3f78e32e64413657/out/livekit_webrtc/livekit/mac-arm64-release-webrtc-b99fd2c-6/mac-arm64-release/include/sdk/objc" "-I" "/Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/scratch-3f78e32e64413657/out/livekit_webrtc/livekit/mac-arm64-release-webrtc-b99fd2c-6/mac-arm64-release/include/sdk/objc/base" "-isysroot/Applications/Xcode_15.4.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX14.5.sdk" "-stdlib=libc++" "-std=c++20" "-DWEBRTC_APM_DEBUG_DUMP=0" "-D__STDC_CONSTANT_MACROS" "-D__STDC_FORMAT_MACROS" "-D_FORTIFY_SOURCE=2" "-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_NONE" "-DNDEBUG" "-DNVALGRIND" "-DDYNAMIC_ANNOTATIONS_ENABLED=0" "-DWEBRTC_ENABLE_PROTOBUF=0" "-DWEBRTC_STRICT_FIELD_TRIALS=0" "-DWEBRTC_INCLUDE_INTERNAL_AUDIO_DEVICE" "-DRTC_USE_LIBAOM_AV1_ENCODER" "-DRTC_ENABLE_VP9" "-DRTC_DAV1D_IN_INTERNAL_DECODER_FACTORY" "-DWEBRTC_HAVE_SCTP" "-DWEBRTC_USE_H264" "-DWEBRTC_ARCH_ARM64" "-DWEBRTC_HAS_NEON" "-DWEBRTC_LIBRARY_IMPL" "-DWEBRTC_ENABLE_SYMBOL_EXPORT" "-DWEBRTC_ENABLE_AVX2" "-DWEBRTC_NON_STATIC_TRACE_EVENT_HANDLERS=0" "-DWEBRTC_POSIX" "-DWEBRTC_MAC" "-DABSL_ALLOCATOR_NOTHROW=1" "-DLIBYUV_DISABLE_LSX" "-DLIBYUV_DISABLE_LASX" "-DLIVEKIT_TEST" "-o" "/Users/runner/work/github_codespaces_compile/github_codespaces_compile/rust/macos/zed/target/debug/build/webrtc-sys-8f834a218b870a1b/out/0602fb52cb66f316-audio_mixer.o" "-c" "src/audio_mixer.cpp"






你遇到的错误是 **macOS 编译 Zed 时在 `webrtc-sys` crate 的 C++ FFI 构建过程中失败**。从日志来看，核心问题是：

```
static_assert(std::ranges::contiguous_range<rust::Slice<const uint8_t>>);
```

编译器报错表明：**C++ STL 检查到 `rust::Slice<const uint8_t>` 不满足 `std::ranges::contiguous_range` 这个概念（concept）**，因此触发了断言失败。

---

## 错误原因分析

### 背景知识

- `rust::Slice<T>` 是 [cxx](https://github.com/dtolnay/cxx) 提供的一个类型，用于安全地将 Rust 的 slice (`&[T]`) 暴露给 C++。
- `std::ranges::contiguous_range` 是 C++20 中的概念，要求一个范围的数据在内存中是连续存储的（如 `std::vector<T>`、`T[]` 等）。
- 在某些 C++ 版本或 STL 实现中（特别是 Apple Clang + libc++），对 iterator 和 range 的 concept 检查更加严格。

### ❗ 问题本质

`rust::Slice<T>::iterator` 并没有完全实现为标准库所认可的“contiguous iterator”，所以当 C++20 的 `static_assert` 检查这个特性时，就会失败。

---

## ✅ 解决方案建议

### ✅ 方案一：修改 `cxx` 或 `webrtc-sys` 源码跳过检查（推荐）

找到触发 `static_assert` 的头文件位置，通常是：

```cpp
#include "rust/cxx.h"
```

或者具体某个 `webrtc-sys` 的绑定头文件中，有类似这行代码：

```cpp
static_assert(std::ranges::contiguous_range<rust::Slice<const uint8_t>>);
```

你可以临时注释掉这一行：

```cpp
// static_assert(std::ranges::contiguous_range<rust::Slice<const uint8_t>>);
```

> ⚠️ 注意：这是一个 workaround。如果将来你需要依赖该约束的功能，请确保你的迭代器行为与 contiguous range 兼容。

---

### ✅ 方案二：降级 C++ 标准（绕开 concept 检查）

尝试在构建时指定更低的 C++ 标准版本，例如使用 `-std=c++17` 而不是默认的 `-std=c++20`。

#### 方法：设置 `CXXFLAGS` 环境变量

```bash
export CXXFLAGS="-std=c++17"
cargo build
```

如果你只想针对 `webrtc-sys` 设置：

```bash
CXXFLAGS_x86_64_apple_darwin="-std=c++17" \
CXXFLAGS_aarch64_apple_darwin="-std=c++17" \
cargo build
```

> macOS 上通常使用 `aarch64-apple-darwin`（Apple Silicon/M1芯片）或 `x86_64-apple-darwin`（Intel Mac）作为目标三元组。

---

### ✅ 方案三：使用 patch 替换 cxx/rust-slice 的实现（高级）

如果你不想修改源码，也可以 fork 或 patch `cxx` crate 来提供兼容的 iterator 实现。

但这比较复杂，适合维护自己的 fork 或做长期支持。

---

### ✅ 方案四：使用 nightly Rust + feature gate（不推荐）

有些情况下，使用 Rust nightly 并启用特定 feature 可以控制 cxx 的生成方式，但目前 cxx 并未提供太多配置选项来规避这个问题。

---

## 补充调试技巧

### 查看具体的错误源头文件

你可以通过以下方式获取更详细的构建命令和错误位置：

```bash
RUST_LOG=debug cargo build --verbose
```

找到执行失败的 `.cpp` 文件，然后查看它 include 的 header，确认是哪个模块引入了那个 `static_assert`。

---

## 总结

| 方法 | 描述 |
|------|------|
| ✅ 注释掉 `static_assert` | 最简单直接的方法，适用于开发阶段 |
| ✅ 使用 `-std=c++17` 编译标志 | 绕过 C++20 的 concept 检查 |
| ✅ Patch `cxx` | 高级用法，适合长期维护 |
| ❌ 忽略错误 | 不可行，因为这是编译期静态断言 |

---

如果你能贴出触发 `static_assert` 的具体 `.h` 或 `.cpp` 文件内容，我可以帮你精准定位并给出 patch 建议。

如果你想我帮你写一段兼容 `contiguous_range` 的 `rust::Slice` 自定义迭代器实现，也可以告诉我 

--- 

是否需要我为你生成一个 patch 文件或提供适配代码？