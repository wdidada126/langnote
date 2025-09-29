# gcc
g++ -fdump-class-hierarchy vtable_example.cpp

## doc
ldd cpp11_getline
        linux-vdso.so.1 (0x00007fffd93a8000)
        libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007f19c2eac000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f19c2c83000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f19c2b9c000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f19c3131000)
        libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007f19c2b78000)


nm cpp11_getline
0000000000003da0 d _DYNAMIC
0000000000003fa0 d _GLOBAL_OFFSET_TABLE_
0000000000002000 R _IO_stdin_used
                 w _ITM_deregisterTMCloneTable
                 w _ITM_registerTMCloneTable
                 U _ZNSolsEPFRSoS_E@GLIBCXX_3.4
                 U _ZNSolsEi@GLIBCXX_3.4
                 U _ZSt21ios_base_library_initv@GLIBCXX_3.4.32
0000000000004040 B _ZSt4cout@GLIBCXX_3.4
                 U _ZSt4endlIcSt11char_traitsIcEERSt13basic_ostreamIT_T0_ES6_@GLIBCXX_3.4
0000000000002004 r _ZStL19piecewise_construct
                 U _ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@GLIBCXX_3.4
00000000000020e8 r __FRAME_END__
000000000000200c r __GNU_EH_FRAME_HDR
0000000000004010 D __TMC_END__
000000000000038c r __abi_tag
0000000000004010 B __bss_start
                 w __cxa_finalize@GLIBC_2.2.5
0000000000004000 D __data_start
0000000000001140 t __do_global_dtors_aux
0000000000003d98 d __do_global_dtors_aux_fini_array_entry
0000000000004008 D __dso_handle
0000000000003d90 d __frame_dummy_init_array_entry
                 w __gmon_start__
                 U __libc_start_main@GLIBC_2.34
0000000000004010 D _edata
0000000000004158 B _end
00000000000011d0 T _fini
0000000000001000 T _init
00000000000010a0 T _start
0000000000004150 b completed.0
0000000000004000 W data_start
00000000000010d0 t deregister_tm_clones
0000000000001180 t frame_dummy
0000000000001189 T main
0000000000001100 t register_tm_clones

在Linux系统中，查找库文件的路径不仅仅局限于`/usr/lib/x86_64-linux-gnu/`。实际上，动态链接库和静态库可以在多个标准位置被找到，并且用户也可以通过多种方式自定义搜索路径。以下是一些常见的库文件默认搜索路径：

1. 标准库路径：
   - `/lib` 和 `/usr/lib`：这些目录通常包含系统的核心库文件。
   - `/lib64` 和 `/usr/lib64`：在64位系统上，用于存放64位库文件的位置。
   - `/usr/local/lib`：这个目录通常用于存放用户自行安装的应用程序的库文件。
   - `/opt`：一些第三方软件可能会将它们的库文件放置在这个目录下。

2. 编译时指定的路径：
   - 使用 `-L` 参数可以指定额外的库搜索路径给编译器。例如，如果你有一个库位于 `/home/user/mylibs/libfoo.a`，你可以使用 `gcc -L/home/user/mylibs -lfoo ...` 来告诉编译器去哪里寻找这个库。

3. 环境变量：
   - `LD_LIBRARY_PATH`：这是一个环境变量，它允许你指定一个由冒号分隔的路径列表，这些路径会被添加到运行时的库搜索路径之前。
   - `LIBRARY_PATH`：对于编译和链接阶段，这个环境变量可以用来指定额外的静态库搜索路径。

4. 配置文件：
   - `/etc/ld.so.conf` 及其包含的其他配置文件（通常是位于 `/etc/ld.so.conf.d/` 目录下的文件）可以用来定义额外的库搜索路径。一旦修改了这些文件，需要运行 `ldconfig` 命令来更新缓存。

5. 链接选项：
   - 在编译时使用 `-Wl,-rpath` 选项可以直接嵌入库的搜索路径到可执行文件中。这意味着即使没有设置 `LD_LIBRARY_PATH` 环境变量，程序仍然能找到所需的库文件。

6. 工具辅助查找：
   - `ldd` 命令可以帮助查看一个已编译的可执行文件依赖哪些共享库及其实际加载路径。
   - `locate` 或 `find` 命令可以根据库文件名在整个文件系统中进行搜索。

7. 特殊用途路径：
   - 对于特定架构或平台的库文件，可能存在于像 `/usr/lib/x86_64-linux-gnu/` 这样的子目录中。这取决于系统的具体配置和使用的包管理系统。

综上所述，除了`/usr/lib/x86_64-linux-gnu/`之外，还有许多其他位置可以存储库文件。根据你的需求和系统配置的不同，你可能需要检查上述提到的一个或多个位置[9]。如果你正在寻找某个具体的库文件但不确定它的位置，可以尝试使用 `find` 或者 `locate` 命令来进行全局搜索，或者利用 `ldd` 来查看某个可执行文件所依赖的库的实际位置。此外，确保你的系统上的 `ldconfig` 数据库是最新的也很重要，这样动态链接器才能正确地找到所有必要的库文件。

Fedora：可以尝试运行 dnf update 来获取最新的软件包列表，并检查是否有 GCC 15.1 可用。
Arch Linux：由于 Arch Linux 采用滚动更新模式，它通常能迅速提供最新的软件包，可以通过 pacman -Syu 来更新系统并查看是否包含 GCC 15.1。

GNU GCC 15.1已于2025年4月25日 10:52:00 GMT发布。

在 Ubuntu 24.04 上，如果你想直接通过 `apt` 安装 GCC 14 或 GCC 15（如果官方仓库已提供），可以按照以下步骤操作：

---
## 方法 1：检查 Ubuntu 24.04 官方仓库
Ubuntu 24.04 (Noble Numbat) 默认可能只提供较新的GCC版本（如 GCC 13/14），但GCC15可能需要从其他源安装。

### 1. 更新软件包列表
```bash
sudo apt update
```

### 2. 搜索可用的 GCC 版本
```bash
apt search gcc- | grep "^gcc-"
```
如果输出包含 `gcc-14` 或 `gcc-15`，说明可以直接安装。

### 3. 安装 GCC 14（如果可用）
```bash
sudo apt install gcc-14 g++-14
```

### 4. 安装 GCC 15（如果可用）
```bash
sudo apt install gcc-15 g++-15
```

### 5. 切换默认GCC版本（可选）
```bash
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-14 100
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-14 100
```
然后运行：
```bash
sudo update-alternatives --config gcc
sudo update-alternatives --config g++
```
选择你想要的版本。

## 方法 2：从 Ubuntu Toolchain PPA 安装（如果官方仓库没有）
如果 Ubuntu 24.04 官方仓库没有 GCC 15，可以使用 `ubuntu-toolchain-r` PPA：

### 1. 添加 Toolchain PPA
```bash
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt update
```

### 2. 安装 GCC 15
```bash
sudo apt install gcc-15 g++-15
```
sudo apt install gcc-13 g++-13 -y
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following additional packages will be installed:
  cpp-13 gcc-13-base libasan8 libatomic1 libcc1-0 libgcc-13-dev libgcc-s1 libgomp1 libhwasan0 libitm1 liblsan0 libquadmath0 libstdc++-13-dev libstdc++6
  libtsan2 libubsan1
Suggested packages:
  gcc-13-locales cpp-13-doc g++-13-multilib gcc-13-doc gcc-13-multilib libstdc++-13-doc
The following NEW packages will be installed:
  cpp-13 g++-13 gcc-13 gcc-13-base libasan8 libgcc-13-dev libhwasan0 libstdc++-13-dev libtsan2
The following packages will be upgraded:
  libatomic1 libcc1-0 libgcc-s1 libgomp1 libitm1 liblsan0 libquadmath0 libstdc++6 libubsan1
9 upgraded, 9 newly installed, 0 to remove and 56 not upgraded.
Need to get 212 MB of archives.

### 3. 切换默认版本（可选）
```bash
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-15 100
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-15 100
```
然后运行：
```bash
sudo update-alternatives --config gcc
sudo update-alternatives --config g++
```

## 验证安装
```bash
gcc --version
g++ --version
```
应该显示你安装的版本（如 `gcc-15`）。

## 方法 3：手动下载 .deb 安装（如果 PPA 不可用）
如果上述方法都不行，可以从 Debian Sid 或 Ubuntu 开发版 下载 `.deb` 包手动安装：

1. 从 [Ubuntu Packages](https://packages.ubuntu.com/) 或 [Debian Packages](https://packages.debian.org/) 搜索 `gcc-15`。
2. 下载 `.deb` 文件：
   ```bash
   wget http://archive.ubuntu.com/ubuntu/pool/universe/g/gcc-15/gcc-15_15.0.0-1ubuntu1_amd64.deb
   ```
3. 安装：
```bash
sudo dpkg -i gcc-15*.deb
sudo apt --fix-broken install  # 解决依赖问题
```

### 总结
| 方法 | 适用场景 | 命令 |
|------|---------|------|
| 官方仓库 | Ubuntu 24.04 已提供 | `sudo apt install gcc-14` |
| Toolchain PPA | 获取最新版本 | `sudo add-apt-repository ppa:ubuntu-toolchain-r/test` |
| 手动 .deb 安装 | 无其他选择时 | `sudo dpkg -i gcc-15.deb` |

如果你只需要GCC 14，官方仓库可能已经提供；GCC 15可能需要PPA或手动安装。

sudo apt install -y g++-13
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
g++-13 is already the newest version (13.1.0-8ubuntu1~22.04).
The following packages were automatically installed and are no longer required:
  liblldb-15 liblldb-17
Use 'sudo apt autoremove' to remove them.
0 upgraded, 0 newly installed, 0 to remove and 28 not upgraded.
wdidada@LAPTOP-wdidada:/mnt/d/develops/git/github/cpp/boost_test$ dpkg -l g++-13
Desired=Unknown/Install/Remove/Purge/Hold
| Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
|/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
||/ Name           Version               Architecture Description
+++-==============-=====================-============-=================================
ii  g++-13         13.1.0-8ubuntu1~22.04 amd64        GNU C++ compiler
wdidada@LAPTOP-wdidada:/mnt/d/develops/git/github/cpp/boost_test$ dpkg -L g++-13
/.
/usr
/usr/bin
/usr/bin/x86_64-linux-gnu-g++-13
/usr/libexec
/usr/libexec/gcc
/usr/libexec/gcc/x86_64-linux-gnu
/usr/libexec/gcc/x86_64-linux-gnu/13
/usr/libexec/gcc/x86_64-linux-gnu/13/cc1plus
/usr/libexec/gcc/x86_64-linux-gnu/13/g++-mapper-server
/usr/share
/usr/share/doc
/usr/share/doc/gcc-13-base
/usr/share/doc/gcc-13-base/C++
/usr/share/doc/gcc-13-base/C++/README.C++
/usr/share/doc/gcc-13-base/C++/changelog.gz
/usr/share/lintian
/usr/share/lintian/overrides
/usr/share/lintian/overrides/g++-13
/usr/share/man
/usr/share/man/man1
/usr/share/man/man1/x86_64-linux-gnu-g++-13.1.gz
/usr/bin/g++-13
/usr/share/doc/g++-13
/usr/share/man/man1/g++-13.1.gz


dpkg -L liblldb-15
/.
/usr
/usr/lib
/usr/lib/llvm-15
/usr/lib/llvm-15/lib
/usr/lib/llvm-15/lib/liblldbIntelFeatures.so.15
/usr/lib/x86_64-linux-gnu
/usr/lib/x86_64-linux-gnu/liblldb-15.so.1
/usr/share
/usr/share/doc
/usr/share/doc/liblldb-15
/usr/share/doc/liblldb-15/copyright
/usr/share/lintian
/usr/share/lintian/overrides
/usr/share/lintian/overrides/liblldb-15
/usr/lib/llvm-15/lib/liblldb.so.1
/usr/lib/x86_64-linux-gnu/liblldb-15.so
/usr/share/doc/liblldb-15/NEWS.Debian.gz
/usr/share/doc/liblldb-15/changelog.Debian.gz
wdidada@LAPTOP-wdidada:/mnt/d/develops/git/github/cpp/boost_test$ dpkg -L liblldb-17
/.
/usr
/usr/lib
/usr/lib/llvm-17
/usr/lib/llvm-17/lib
/usr/lib/llvm-17/lib/liblldbIntelFeatures.so.17
/usr/lib/x86_64-linux-gnu
/usr/lib/x86_64-linux-gnu/liblldb-17.so.1
/usr/share
/usr/share/doc
/usr/share/doc/liblldb-17
/usr/share/doc/liblldb-17/changelog.Debian.gz
/usr/share/doc/liblldb-17/copyright
/usr/share/lintian
/usr/share/lintian/overrides
/usr/share/lintian/overrides/liblldb-17
/usr/lib/llvm-17/lib/liblldb.so.1
/usr/lib/x86_64-linux-gnu/liblldb-17.so

dpkg -S /usr/include/c++/13/string_view
libstdc++-13-dev:amd64: /usr/include/c++/13/string_view


dpkg -L libstdc++-13-dev
/.
/usr
/usr/include
/usr/include/c++
/usr/include/c++/13
/usr/include/c++/13/algorithm
/usr/include/c++/13/any
/usr/include/c++/13/array
/usr/include/c++/13/atomic
/usr/include/c++/13/backward
/usr/include/c++/13/backward/auto_ptr.h
/usr/include/c++/13/backward/backward_warning.h
/usr/include/c++/13/backward/binders.h
/usr/include/c++/13/backward/hash_fun.h
/usr/include/c++/13/backward/hash_map
/usr/include/c++/13/backward/hash_set
/usr/include/c++/13/backward/hashtable.h
/usr/include/c++/13/backward/strstream
/usr/include/c++/13/barrier
/usr/include/c++/13/bit
/usr/include/c++/13/bits
/usr/include/c++/13/bits/algorithmfwd.h
/usr/include/c++/13/bits/align.h
/usr/include/c++/13/bits/alloc_traits.h
/usr/include/c++/13/bits/allocated_ptr.h
/usr/include/c++/13/bits/allocator.h
/usr/include/c++/13/bits/atomic_base.h
/usr/include/c++/13/bits/atomic_futex.h
/usr/include/c++/13/bits/atomic_lockfree_defines.h
/usr/include/c++/13/bits/atomic_timed_wait.h
/usr/include/c++/13/bits/atomic_wait.h
/usr/include/c++/13/bits/basic_ios.h
/usr/include/c++/13/bits/basic_ios.tcc
/usr/include/c++/13/bits/basic_string.h
/usr/include/c++/13/bits/basic_string.tcc
/usr/include/c++/13/bits/boost_concept_check.h
/usr/include/c++/13/bits/c++0x_warning.h
/usr/include/c++/13/bits/char_traits.h
/usr/include/c++/13/bits/charconv.h
/usr/include/c++/13/bits/chrono.h
/usr/include/c++/13/bits/chrono_io.h
/usr/include/c++/13/bits/codecvt.h
/usr/include/c++/13/bits/concept_check.h
/usr/include/c++/13/bits/cow_string.h
/usr/include/c++/13/bits/cpp_type_traits.h
/usr/include/c++/13/bits/cxxabi_forced.h
/usr/include/c++/13/bits/cxxabi_init_exception.h
/usr/include/c++/13/bits/deque.tcc
/usr/include/c++/13/bits/enable_special_members.h
/usr/include/c++/13/bits/erase_if.h
/usr/include/c++/13/bits/exception.h
/usr/include/c++/13/bits/exception_defines.h
/usr/include/c++/13/bits/exception_ptr.h
/usr/include/c++/13/bits/forward_list.h
/usr/include/c++/13/bits/forward_list.tcc
/usr/include/c++/13/bits/fs_dir.h
/usr/include/c++/13/bits/fs_fwd.h
/usr/include/c++/13/bits/fs_ops.h
/usr/include/c++/13/bits/fs_path.h
/usr/include/c++/13/bits/fstream.tcc
/usr/include/c++/13/bits/functexcept.h
/usr/include/c++/13/bits/functional_hash.h
/usr/include/c++/13/bits/gslice.h
/usr/include/c++/13/bits/gslice_array.h
/usr/include/c++/13/bits/hash_bytes.h
/usr/include/c++/13/bits/hashtable.h
/usr/include/c++/13/bits/hashtable_policy.h
/usr/include/c++/13/bits/indirect_array.h
/usr/include/c++/13/bits/invoke.h
/usr/include/c++/13/bits/ios_base.h
/usr/include/c++/13/bits/istream.tcc
/usr/include/c++/13/bits/iterator_concepts.h
/usr/include/c++/13/bits/list.tcc
/usr/include/c++/13/bits/locale_classes.h
/usr/include/c++/13/bits/locale_classes.tcc
/usr/include/c++/13/bits/locale_conv.h
/usr/include/c++/13/bits/locale_facets.h
/usr/include/c++/13/bits/locale_facets.tcc
/usr/include/c++/13/bits/locale_facets_nonio.h
/usr/include/c++/13/bits/locale_facets_nonio.tcc
/usr/include/c++/13/bits/localefwd.h
/usr/include/c++/13/bits/mask_array.h
/usr/include/c++/13/bits/max_size_type.h
/usr/include/c++/13/bits/memory_resource.h
/usr/include/c++/13/bits/memoryfwd.h
/usr/include/c++/13/bits/mofunc_impl.h
/usr/include/c++/13/bits/move.h
/usr/include/c++/13/bits/move_only_function.h
/usr/include/c++/13/bits/nested_exception.h
/usr/include/c++/13/bits/new_allocator.h
/usr/include/c++/13/bits/node_handle.h
/usr/include/c++/13/bits/ostream.tcc
/usr/include/c++/13/bits/ostream_insert.h
/usr/include/c++/13/bits/parse_numbers.h
/usr/include/c++/13/bits/postypes.h
/usr/include/c++/13/bits/predefined_ops.h
/usr/include/c++/13/bits/ptr_traits.h
/usr/include/c++/13/bits/quoted_string.h
/usr/include/c++/13/bits/random.h
/usr/include/c++/13/bits/random.tcc
/usr/include/c++/13/bits/range_access.h
/usr/include/c++/13/bits/ranges_algo.h
/usr/include/c++/13/bits/ranges_algobase.h
/usr/include/c++/13/bits/ranges_base.h
/usr/include/c++/13/bits/ranges_cmp.h
/usr/include/c++/13/bits/ranges_uninitialized.h
/usr/include/c++/13/bits/ranges_util.h
/usr/include/c++/13/bits/refwrap.h
/usr/include/c++/13/bits/regex.h
/usr/include/c++/13/bits/regex.tcc
/usr/include/c++/13/bits/regex_automaton.h
/usr/include/c++/13/bits/regex_automaton.tcc
/usr/include/c++/13/bits/regex_compiler.h
/usr/include/c++/13/bits/regex_compiler.tcc
/usr/include/c++/13/bits/regex_constants.h
/usr/include/c++/13/bits/regex_error.h
/usr/include/c++/13/bits/regex_executor.h
/usr/include/c++/13/bits/regex_executor.tcc
/usr/include/c++/13/bits/regex_scanner.h
/usr/include/c++/13/bits/regex_scanner.tcc
/usr/include/c++/13/bits/requires_hosted.h
/usr/include/c++/13/bits/semaphore_base.h
/usr/include/c++/13/bits/shared_ptr.h
/usr/include/c++/13/bits/shared_ptr_atomic.h
/usr/include/c++/13/bits/shared_ptr_base.h
/usr/include/c++/13/bits/slice_array.h
/usr/include/c++/13/bits/specfun.h
/usr/include/c++/13/bits/sstream.tcc
/usr/include/c++/13/bits/std_abs.h
/usr/include/c++/13/bits/std_function.h
/usr/include/c++/13/bits/std_mutex.h
/usr/include/c++/13/bits/std_thread.h
/usr/include/c++/13/bits/stl_algo.h
/usr/include/c++/13/bits/stl_algobase.h
/usr/include/c++/13/bits/stl_bvector.h
/usr/include/c++/13/bits/stl_construct.h
/usr/include/c++/13/bits/stl_deque.h
/usr/include/c++/13/bits/stl_function.h
/usr/include/c++/13/bits/stl_heap.h
/usr/include/c++/13/bits/stl_iterator.h
/usr/include/c++/13/bits/stl_iterator_base_funcs.h
/usr/include/c++/13/bits/stl_iterator_base_types.h
/usr/include/c++/13/bits/stl_list.h
/usr/include/c++/13/bits/stl_map.h
/usr/include/c++/13/bits/stl_multimap.h
/usr/include/c++/13/bits/stl_multiset.h
/usr/include/c++/13/bits/stl_numeric.h
/usr/include/c++/13/bits/stl_pair.h
/usr/include/c++/13/bits/stl_queue.h
/usr/include/c++/13/bits/stl_raw_storage_iter.h
/usr/include/c++/13/bits/stl_relops.h
/usr/include/c++/13/bits/stl_set.h
/usr/include/c++/13/bits/stl_stack.h
/usr/include/c++/13/bits/stl_tempbuf.h
/usr/include/c++/13/bits/stl_tree.h
/usr/include/c++/13/bits/stl_uninitialized.h
/usr/include/c++/13/bits/stl_vector.h
/usr/include/c++/13/bits/stream_iterator.h
/usr/include/c++/13/bits/streambuf.tcc
/usr/include/c++/13/bits/streambuf_iterator.h
/usr/include/c++/13/bits/string_view.tcc
/usr/include/c++/13/bits/stringfwd.h
/usr/include/c++/13/bits/this_thread_sleep.h
/usr/include/c++/13/bits/uniform_int_dist.h
/usr/include/c++/13/bits/unique_lock.h
/usr/include/c++/13/bits/unique_ptr.h
/usr/include/c++/13/bits/unordered_map.h
/usr/include/c++/13/bits/unordered_set.h
/usr/include/c++/13/bits/uses_allocator.h
/usr/include/c++/13/bits/uses_allocator_args.h
/usr/include/c++/13/bits/utility.h
/usr/include/c++/13/bits/valarray_after.h
/usr/include/c++/13/bits/valarray_array.h
/usr/include/c++/13/bits/valarray_array.tcc
/usr/include/c++/13/bits/valarray_before.h
/usr/include/c++/13/bits/vector.tcc
/usr/include/c++/13/bitset
/usr/include/c++/13/cassert
/usr/include/c++/13/ccomplex
/usr/include/c++/13/cctype
/usr/include/c++/13/cerrno
/usr/include/c++/13/cfenv
/usr/include/c++/13/cfloat
/usr/include/c++/13/charconv
/usr/include/c++/13/chrono
/usr/include/c++/13/cinttypes
/usr/include/c++/13/ciso646
/usr/include/c++/13/climits
/usr/include/c++/13/clocale
/usr/include/c++/13/cmath
/usr/include/c++/13/codecvt
/usr/include/c++/13/compare
/usr/include/c++/13/complex
/usr/include/c++/13/complex.h
/usr/include/c++/13/concepts
/usr/include/c++/13/condition_variable
/usr/include/c++/13/coroutine
/usr/include/c++/13/csetjmp
/usr/include/c++/13/csignal
/usr/include/c++/13/cstdalign
/usr/include/c++/13/cstdarg
/usr/include/c++/13/cstdbool
/usr/include/c++/13/cstddef
/usr/include/c++/13/cstdint
/usr/include/c++/13/cstdio
/usr/include/c++/13/cstdlib
/usr/include/c++/13/cstring
/usr/include/c++/13/ctgmath
/usr/include/c++/13/ctime
/usr/include/c++/13/cuchar
/usr/include/c++/13/cwchar
/usr/include/c++/13/cwctype
/usr/include/c++/13/cxxabi.h
/usr/include/c++/13/debug
/usr/include/c++/13/debug/assertions.h
/usr/include/c++/13/debug/bitset
/usr/include/c++/13/debug/debug.h
/usr/include/c++/13/debug/deque
/usr/include/c++/13/debug/formatter.h
/usr/include/c++/13/debug/forward_list
/usr/include/c++/13/debug/functions.h
/usr/include/c++/13/debug/helper_functions.h
/usr/include/c++/13/debug/list
/usr/include/c++/13/debug/macros.h
/usr/include/c++/13/debug/map
/usr/include/c++/13/debug/map.h
/usr/include/c++/13/debug/multimap.h
/usr/include/c++/13/debug/multiset.h
/usr/include/c++/13/debug/safe_base.h
/usr/include/c++/13/debug/safe_container.h
/usr/include/c++/13/debug/safe_iterator.h
/usr/include/c++/13/debug/safe_iterator.tcc
/usr/include/c++/13/debug/safe_local_iterator.h
/usr/include/c++/13/debug/safe_local_iterator.tcc
/usr/include/c++/13/debug/safe_sequence.h
/usr/include/c++/13/debug/safe_sequence.tcc
/usr/include/c++/13/debug/safe_unordered_base.h
/usr/include/c++/13/debug/safe_unordered_container.h
/usr/include/c++/13/debug/safe_unordered_container.tcc
/usr/include/c++/13/debug/set
/usr/include/c++/13/debug/set.h
/usr/include/c++/13/debug/stl_iterator.h
/usr/include/c++/13/debug/string
/usr/include/c++/13/debug/unordered_map
/usr/include/c++/13/debug/unordered_set
/usr/include/c++/13/debug/vector
/usr/include/c++/13/decimal
/usr/include/c++/13/decimal/decimal
/usr/include/c++/13/decimal/decimal.h
/usr/include/c++/13/deque
/usr/include/c++/13/exception
/usr/include/c++/13/execution
/usr/include/c++/13/expected
/usr/include/c++/13/experimental
/usr/include/c++/13/experimental/algorithm
/usr/include/c++/13/experimental/any
/usr/include/c++/13/experimental/array
/usr/include/c++/13/experimental/bits
/usr/include/c++/13/experimental/bits/fs_dir.h
/usr/include/c++/13/experimental/bits/fs_fwd.h
/usr/include/c++/13/experimental/bits/fs_ops.h
/usr/include/c++/13/experimental/bits/fs_path.h
/usr/include/c++/13/experimental/bits/lfts_config.h
/usr/include/c++/13/experimental/bits/net.h
/usr/include/c++/13/experimental/bits/numeric_traits.h
/usr/include/c++/13/experimental/bits/shared_ptr.h
/usr/include/c++/13/experimental/bits/simd.h
/usr/include/c++/13/experimental/bits/simd_builtin.h
/usr/include/c++/13/experimental/bits/simd_converter.h
/usr/include/c++/13/experimental/bits/simd_detail.h
/usr/include/c++/13/experimental/bits/simd_fixed_size.h
/usr/include/c++/13/experimental/bits/simd_math.h
/usr/include/c++/13/experimental/bits/simd_neon.h
/usr/include/c++/13/experimental/bits/simd_ppc.h
/usr/include/c++/13/experimental/bits/simd_scalar.h
/usr/include/c++/13/experimental/bits/simd_x86.h
/usr/include/c++/13/experimental/bits/simd_x86_conversions.h
/usr/include/c++/13/experimental/bits/string_view.tcc
/usr/include/c++/13/experimental/buffer
/usr/include/c++/13/experimental/chrono
/usr/include/c++/13/experimental/contract
/usr/include/c++/13/experimental/deque
/usr/include/c++/13/experimental/executor
/usr/include/c++/13/experimental/filesystem
/usr/include/c++/13/experimental/forward_list
/usr/include/c++/13/experimental/functional
/usr/include/c++/13/experimental/internet
/usr/include/c++/13/experimental/io_context
/usr/include/c++/13/experimental/iterator
/usr/include/c++/13/experimental/list
/usr/include/c++/13/experimental/map
/usr/include/c++/13/experimental/memory
/usr/include/c++/13/experimental/memory_resource
/usr/include/c++/13/experimental/net
/usr/include/c++/13/experimental/netfwd
/usr/include/c++/13/experimental/numeric
/usr/include/c++/13/experimental/optional
/usr/include/c++/13/experimental/propagate_const
/usr/include/c++/13/experimental/random
/usr/include/c++/13/experimental/ratio
/usr/include/c++/13/experimental/regex
/usr/include/c++/13/experimental/scope
/usr/include/c++/13/experimental/set
/usr/include/c++/13/experimental/simd
/usr/include/c++/13/experimental/socket
/usr/include/c++/13/experimental/source_location
/usr/include/c++/13/experimental/string
/usr/include/c++/13/experimental/string_view
/usr/include/c++/13/experimental/synchronized_value
/usr/include/c++/13/experimental/system_error
/usr/include/c++/13/experimental/timer
/usr/include/c++/13/experimental/tuple
/usr/include/c++/13/experimental/type_traits
/usr/include/c++/13/experimental/unordered_map
/usr/include/c++/13/experimental/unordered_set
/usr/include/c++/13/experimental/utility
/usr/include/c++/13/experimental/vector
/usr/include/c++/13/ext
/usr/include/c++/13/ext/algorithm
/usr/include/c++/13/ext/aligned_buffer.h
/usr/include/c++/13/ext/alloc_traits.h
/usr/include/c++/13/ext/atomicity.h
/usr/include/c++/13/ext/bitmap_allocator.h
/usr/include/c++/13/ext/cast.h
/usr/include/c++/13/ext/cmath
/usr/include/c++/13/ext/codecvt_specializations.h
/usr/include/c++/13/ext/concurrence.h
/usr/include/c++/13/ext/debug_allocator.h
/usr/include/c++/13/ext/enc_filebuf.h
/usr/include/c++/13/ext/extptr_allocator.h
/usr/include/c++/13/ext/functional
/usr/include/c++/13/ext/hash_map
/usr/include/c++/13/ext/hash_set
/usr/include/c++/13/ext/iterator
/usr/include/c++/13/ext/malloc_allocator.h
/usr/include/c++/13/ext/memory
/usr/include/c++/13/ext/mt_allocator.h
/usr/include/c++/13/ext/new_allocator.h
/usr/include/c++/13/ext/numeric
/usr/include/c++/13/ext/numeric_traits.h
/usr/include/c++/13/ext/pb_ds
/usr/include/c++/13/ext/pb_ds/assoc_container.hpp
/usr/include/c++/13/ext/pb_ds/detail
/usr/include/c++/13/ext/pb_ds/detail/bin_search_tree_
/usr/include/c++/13/ext/pb_ds/detail/bin_search_tree_/bin_search_tree_.hpp
/usr/include/c++/13/ext/pb_ds/detail/bin_search_tree_/constructors_destructor_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/bin_search_tree_/debug_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/bin_search_tree_/erase_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/bin_search_tree_/find_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/bin_search_tree_/info_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/bin_search_tree_/insert_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/bin_search_tree_/iterators_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/bin_search_tree_/node_iterators.hpp
/usr/include/c++/13/ext/pb_ds/detail/bin_search_tree_/point_iterators.hpp
/usr/include/c++/13/ext/pb_ds/detail/bin_search_tree_/policy_access_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/bin_search_tree_/r_erase_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/bin_search_tree_/rotate_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/bin_search_tree_/split_join_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/bin_search_tree_/traits.hpp
/usr/include/c++/13/ext/pb_ds/detail/binary_heap_
/usr/include/c++/13/ext/pb_ds/detail/binary_heap_/binary_heap_.hpp
/usr/include/c++/13/ext/pb_ds/detail/binary_heap_/const_iterator.hpp
/usr/include/c++/13/ext/pb_ds/detail/binary_heap_/constructors_destructor_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/binary_heap_/debug_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/binary_heap_/entry_cmp.hpp
/usr/include/c++/13/ext/pb_ds/detail/binary_heap_/entry_pred.hpp
/usr/include/c++/13/ext/pb_ds/detail/binary_heap_/erase_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/binary_heap_/find_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/binary_heap_/info_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/binary_heap_/insert_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/binary_heap_/iterators_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/binary_heap_/point_const_iterator.hpp
/usr/include/c++/13/ext/pb_ds/detail/binary_heap_/policy_access_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/binary_heap_/resize_policy.hpp
/usr/include/c++/13/ext/pb_ds/detail/binary_heap_/split_join_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/binary_heap_/trace_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/binomial_heap_
/usr/include/c++/13/ext/pb_ds/detail/binomial_heap_/binomial_heap_.hpp
/usr/include/c++/13/ext/pb_ds/detail/binomial_heap_/constructors_destructor_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/binomial_heap_/debug_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/binomial_heap_base_
/usr/include/c++/13/ext/pb_ds/detail/binomial_heap_base_/binomial_heap_base_.hpp
/usr/include/c++/13/ext/pb_ds/detail/binomial_heap_base_/constructors_destructor_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/binomial_heap_base_/debug_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/binomial_heap_base_/erase_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/binomial_heap_base_/find_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/binomial_heap_base_/insert_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/binomial_heap_base_/split_join_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/branch_policy
/usr/include/c++/13/ext/pb_ds/detail/branch_policy/branch_policy.hpp
/usr/include/c++/13/ext/pb_ds/detail/branch_policy/null_node_metadata.hpp
/usr/include/c++/13/ext/pb_ds/detail/branch_policy/traits.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/cc_ht_map_.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/cmp_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/cond_key_dtor_entry_dealtor.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/constructor_destructor_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/constructor_destructor_no_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/constructor_destructor_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/debug_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/debug_no_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/debug_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/entry_list_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/erase_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/erase_no_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/erase_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/find_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/find_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/info_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/insert_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/insert_no_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/insert_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/iterators_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/policy_access_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/resize_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/resize_no_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/resize_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/size_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cc_hash_table_map_/trace_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/cond_dealtor.hpp
/usr/include/c++/13/ext/pb_ds/detail/container_base_dispatch.hpp
/usr/include/c++/13/ext/pb_ds/detail/debug_map_base.hpp
/usr/include/c++/13/ext/pb_ds/detail/eq_fn
/usr/include/c++/13/ext/pb_ds/detail/eq_fn/eq_by_less.hpp
/usr/include/c++/13/ext/pb_ds/detail/eq_fn/hash_eq_fn.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/constructor_destructor_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/constructor_destructor_no_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/constructor_destructor_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/debug_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/debug_no_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/debug_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/erase_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/erase_no_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/erase_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/find_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/find_no_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/find_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/gp_ht_map_.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/info_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/insert_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/insert_no_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/insert_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/iterator_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/policy_access_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/resize_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/resize_no_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/resize_store_hash_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/gp_hash_table_map_/trace_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/hash_fn
/usr/include/c++/13/ext/pb_ds/detail/hash_fn/direct_mask_range_hashing_imp.hpp
/usr/include/c++/13/ext/pb_ds/detail/hash_fn/direct_mod_range_hashing_imp.hpp
/usr/include/c++/13/ext/pb_ds/detail/hash_fn/linear_probe_fn_imp.hpp
/usr/include/c++/13/ext/pb_ds/detail/hash_fn/mask_based_range_hashing.hpp
/usr/include/c++/13/ext/pb_ds/detail/hash_fn/mod_based_range_hashing.hpp
/usr/include/c++/13/ext/pb_ds/detail/hash_fn/probe_fn_base.hpp
/usr/include/c++/13/ext/pb_ds/detail/hash_fn/quadratic_probe_fn_imp.hpp
/usr/include/c++/13/ext/pb_ds/detail/hash_fn/ranged_hash_fn.hpp
/usr/include/c++/13/ext/pb_ds/detail/hash_fn/ranged_probe_fn.hpp
/usr/include/c++/13/ext/pb_ds/detail/hash_fn/sample_probe_fn.hpp
/usr/include/c++/13/ext/pb_ds/detail/hash_fn/sample_range_hashing.hpp
/usr/include/c++/13/ext/pb_ds/detail/hash_fn/sample_ranged_hash_fn.hpp
/usr/include/c++/13/ext/pb_ds/detail/hash_fn/sample_ranged_probe_fn.hpp
/usr/include/c++/13/ext/pb_ds/detail/left_child_next_sibling_heap_
/usr/include/c++/13/ext/pb_ds/detail/left_child_next_sibling_heap_/const_iterator.hpp
/usr/include/c++/13/ext/pb_ds/detail/left_child_next_sibling_heap_/constructors_destructor_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/left_child_next_sibling_heap_/debug_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/left_child_next_sibling_heap_/erase_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/left_child_next_sibling_heap_/info_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/left_child_next_sibling_heap_/insert_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/left_child_next_sibling_heap_/iterators_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/left_child_next_sibling_heap_/left_child_next_sibling_heap_.hpp
/usr/include/c++/13/ext/pb_ds/detail/left_child_next_sibling_heap_/node.hpp
/usr/include/c++/13/ext/pb_ds/detail/left_child_next_sibling_heap_/point_const_iterator.hpp
/usr/include/c++/13/ext/pb_ds/detail/left_child_next_sibling_heap_/policy_access_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/left_child_next_sibling_heap_/trace_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/list_update_map_
/usr/include/c++/13/ext/pb_ds/detail/list_update_map_/constructor_destructor_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/list_update_map_/debug_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/list_update_map_/entry_metadata_base.hpp
/usr/include/c++/13/ext/pb_ds/detail/list_update_map_/erase_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/list_update_map_/find_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/list_update_map_/info_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/list_update_map_/insert_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/list_update_map_/iterators_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/list_update_map_/lu_map_.hpp
/usr/include/c++/13/ext/pb_ds/detail/list_update_map_/trace_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/list_update_policy
/usr/include/c++/13/ext/pb_ds/detail/list_update_policy/lu_counter_metadata.hpp
/usr/include/c++/13/ext/pb_ds/detail/list_update_policy/sample_update_policy.hpp
/usr/include/c++/13/ext/pb_ds/detail/ov_tree_map_
/usr/include/c++/13/ext/pb_ds/detail/ov_tree_map_/constructors_destructor_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/ov_tree_map_/debug_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/ov_tree_map_/erase_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/ov_tree_map_/info_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/ov_tree_map_/insert_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/ov_tree_map_/iterators_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/ov_tree_map_/node_iterators.hpp
/usr/include/c++/13/ext/pb_ds/detail/ov_tree_map_/ov_tree_map_.hpp
/usr/include/c++/13/ext/pb_ds/detail/ov_tree_map_/policy_access_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/ov_tree_map_/split_join_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/ov_tree_map_/traits.hpp
/usr/include/c++/13/ext/pb_ds/detail/pairing_heap_
/usr/include/c++/13/ext/pb_ds/detail/pairing_heap_/constructors_destructor_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/pairing_heap_/debug_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/pairing_heap_/erase_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/pairing_heap_/find_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/pairing_heap_/insert_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/pairing_heap_/pairing_heap_.hpp
/usr/include/c++/13/ext/pb_ds/detail/pairing_heap_/split_join_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/pat_trie_
/usr/include/c++/13/ext/pb_ds/detail/pat_trie_/constructors_destructor_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/pat_trie_/debug_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/pat_trie_/erase_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/pat_trie_/find_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/pat_trie_/info_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/pat_trie_/insert_join_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/pat_trie_/iterators_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/pat_trie_/pat_trie_.hpp
/usr/include/c++/13/ext/pb_ds/detail/pat_trie_/pat_trie_base.hpp
/usr/include/c++/13/ext/pb_ds/detail/pat_trie_/policy_access_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/pat_trie_/r_erase_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/pat_trie_/rotate_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/pat_trie_/split_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/pat_trie_/synth_access_traits.hpp
/usr/include/c++/13/ext/pb_ds/detail/pat_trie_/trace_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/pat_trie_/traits.hpp
/usr/include/c++/13/ext/pb_ds/detail/pat_trie_/update_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/priority_queue_base_dispatch.hpp
/usr/include/c++/13/ext/pb_ds/detail/rb_tree_map_
/usr/include/c++/13/ext/pb_ds/detail/rb_tree_map_/constructors_destructor_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/rb_tree_map_/debug_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/rb_tree_map_/erase_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/rb_tree_map_/find_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/rb_tree_map_/info_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/rb_tree_map_/insert_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/rb_tree_map_/node.hpp
/usr/include/c++/13/ext/pb_ds/detail/rb_tree_map_/rb_tree_.hpp
/usr/include/c++/13/ext/pb_ds/detail/rb_tree_map_/split_join_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/rb_tree_map_/traits.hpp
/usr/include/c++/13/ext/pb_ds/detail/rc_binomial_heap_
/usr/include/c++/13/ext/pb_ds/detail/rc_binomial_heap_/constructors_destructor_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/rc_binomial_heap_/debug_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/rc_binomial_heap_/erase_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/rc_binomial_heap_/insert_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/rc_binomial_heap_/rc.hpp
/usr/include/c++/13/ext/pb_ds/detail/rc_binomial_heap_/rc_binomial_heap_.hpp
/usr/include/c++/13/ext/pb_ds/detail/rc_binomial_heap_/split_join_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/rc_binomial_heap_/trace_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/resize_policy
/usr/include/c++/13/ext/pb_ds/detail/resize_policy/cc_hash_max_collision_check_resize_trigger_imp.hpp
/usr/include/c++/13/ext/pb_ds/detail/resize_policy/hash_exponential_size_policy_imp.hpp
/usr/include/c++/13/ext/pb_ds/detail/resize_policy/hash_load_check_resize_trigger_imp.hpp
/usr/include/c++/13/ext/pb_ds/detail/resize_policy/hash_load_check_resize_trigger_size_base.hpp
/usr/include/c++/13/ext/pb_ds/detail/resize_policy/hash_prime_size_policy_imp.hpp
/usr/include/c++/13/ext/pb_ds/detail/resize_policy/hash_standard_resize_policy_imp.hpp
/usr/include/c++/13/ext/pb_ds/detail/resize_policy/sample_resize_policy.hpp
/usr/include/c++/13/ext/pb_ds/detail/resize_policy/sample_resize_trigger.hpp
/usr/include/c++/13/ext/pb_ds/detail/resize_policy/sample_size_policy.hpp
/usr/include/c++/13/ext/pb_ds/detail/splay_tree_
/usr/include/c++/13/ext/pb_ds/detail/splay_tree_/constructors_destructor_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/splay_tree_/debug_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/splay_tree_/erase_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/splay_tree_/find_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/splay_tree_/info_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/splay_tree_/insert_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/splay_tree_/node.hpp
/usr/include/c++/13/ext/pb_ds/detail/splay_tree_/splay_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/splay_tree_/splay_tree_.hpp
/usr/include/c++/13/ext/pb_ds/detail/splay_tree_/split_join_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/splay_tree_/traits.hpp
/usr/include/c++/13/ext/pb_ds/detail/standard_policies.hpp
/usr/include/c++/13/ext/pb_ds/detail/thin_heap_
/usr/include/c++/13/ext/pb_ds/detail/thin_heap_/constructors_destructor_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/thin_heap_/debug_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/thin_heap_/erase_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/thin_heap_/find_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/thin_heap_/insert_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/thin_heap_/split_join_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/thin_heap_/thin_heap_.hpp
/usr/include/c++/13/ext/pb_ds/detail/thin_heap_/trace_fn_imps.hpp
/usr/include/c++/13/ext/pb_ds/detail/tree_policy
/usr/include/c++/13/ext/pb_ds/detail/tree_policy/node_metadata_selector.hpp
/usr/include/c++/13/ext/pb_ds/detail/tree_policy/order_statistics_imp.hpp
/usr/include/c++/13/ext/pb_ds/detail/tree_policy/sample_tree_node_update.hpp
/usr/include/c++/13/ext/pb_ds/detail/tree_trace_base.hpp
/usr/include/c++/13/ext/pb_ds/detail/trie_policy
/usr/include/c++/13/ext/pb_ds/detail/trie_policy/node_metadata_selector.hpp
/usr/include/c++/13/ext/pb_ds/detail/trie_policy/order_statistics_imp.hpp
/usr/include/c++/13/ext/pb_ds/detail/trie_policy/prefix_search_node_update_imp.hpp
/usr/include/c++/13/ext/pb_ds/detail/trie_policy/sample_trie_access_traits.hpp
/usr/include/c++/13/ext/pb_ds/detail/trie_policy/sample_trie_node_update.hpp
/usr/include/c++/13/ext/pb_ds/detail/trie_policy/trie_policy_base.hpp
/usr/include/c++/13/ext/pb_ds/detail/trie_policy/trie_string_access_traits_imp.hpp
/usr/include/c++/13/ext/pb_ds/detail/type_utils.hpp
/usr/include/c++/13/ext/pb_ds/detail/types_traits.hpp
/usr/include/c++/13/ext/pb_ds/detail/unordered_iterator
/usr/include/c++/13/ext/pb_ds/detail/unordered_iterator/const_iterator.hpp
/usr/include/c++/13/ext/pb_ds/detail/unordered_iterator/iterator.hpp
/usr/include/c++/13/ext/pb_ds/detail/unordered_iterator/point_const_iterator.hpp
/usr/include/c++/13/ext/pb_ds/detail/unordered_iterator/point_iterator.hpp
/usr/include/c++/13/ext/pb_ds/exception.hpp
/usr/include/c++/13/ext/pb_ds/hash_policy.hpp
/usr/include/c++/13/ext/pb_ds/list_update_policy.hpp
/usr/include/c++/13/ext/pb_ds/priority_queue.hpp
/usr/include/c++/13/ext/pb_ds/tag_and_trait.hpp
/usr/include/c++/13/ext/pb_ds/tree_policy.hpp
/usr/include/c++/13/ext/pb_ds/trie_policy.hpp
/usr/include/c++/13/ext/pod_char_traits.h
/usr/include/c++/13/ext/pointer.h
/usr/include/c++/13/ext/pool_allocator.h
/usr/include/c++/13/ext/random
/usr/include/c++/13/ext/random.tcc
/usr/include/c++/13/ext/rb_tree
/usr/include/c++/13/ext/rc_string_base.h
/usr/include/c++/13/ext/rope
/usr/include/c++/13/ext/ropeimpl.h
/usr/include/c++/13/ext/slist
/usr/include/c++/13/ext/sso_string_base.h
/usr/include/c++/13/ext/stdio_filebuf.h
/usr/include/c++/13/ext/stdio_sync_filebuf.h
/usr/include/c++/13/ext/string_conversions.h
/usr/include/c++/13/ext/throw_allocator.h
/usr/include/c++/13/ext/type_traits.h
/usr/include/c++/13/ext/typelist.h
/usr/include/c++/13/ext/vstring.h
/usr/include/c++/13/ext/vstring.tcc
/usr/include/c++/13/ext/vstring_fwd.h
/usr/include/c++/13/ext/vstring_util.h
/usr/include/c++/13/fenv.h
/usr/include/c++/13/filesystem
/usr/include/c++/13/format
/usr/include/c++/13/forward_list
/usr/include/c++/13/fstream
/usr/include/c++/13/functional
/usr/include/c++/13/future
/usr/include/c++/13/initializer_list
/usr/include/c++/13/iomanip
/usr/include/c++/13/ios
/usr/include/c++/13/iosfwd
/usr/include/c++/13/iostream
/usr/include/c++/13/istream
/usr/include/c++/13/iterator
/usr/include/c++/13/latch
/usr/include/c++/13/limits
/usr/include/c++/13/list
/usr/include/c++/13/locale
/usr/include/c++/13/map
/usr/include/c++/13/math.h
/usr/include/c++/13/memory
/usr/include/c++/13/memory_resource
/usr/include/c++/13/mutex
/usr/include/c++/13/new
/usr/include/c++/13/numbers
/usr/include/c++/13/numeric
/usr/include/c++/13/optional
/usr/include/c++/13/ostream
/usr/include/c++/13/parallel
/usr/include/c++/13/parallel/algo.h
/usr/include/c++/13/parallel/algobase.h
/usr/include/c++/13/parallel/algorithm
/usr/include/c++/13/parallel/algorithmfwd.h
/usr/include/c++/13/parallel/balanced_quicksort.h
/usr/include/c++/13/parallel/base.h
/usr/include/c++/13/parallel/basic_iterator.h
/usr/include/c++/13/parallel/checkers.h
/usr/include/c++/13/parallel/compatibility.h
/usr/include/c++/13/parallel/compiletime_settings.h
/usr/include/c++/13/parallel/equally_split.h
/usr/include/c++/13/parallel/features.h
/usr/include/c++/13/parallel/find.h
/usr/include/c++/13/parallel/find_selectors.h
/usr/include/c++/13/parallel/for_each.h
/usr/include/c++/13/parallel/for_each_selectors.h
/usr/include/c++/13/parallel/iterator.h
/usr/include/c++/13/parallel/list_partition.h
/usr/include/c++/13/parallel/losertree.h
/usr/include/c++/13/parallel/merge.h
/usr/include/c++/13/parallel/multiseq_selection.h
/usr/include/c++/13/parallel/multiway_merge.h
/usr/include/c++/13/parallel/multiway_mergesort.h
/usr/include/c++/13/parallel/numeric
/usr/include/c++/13/parallel/numericfwd.h
/usr/include/c++/13/parallel/omp_loop.h
/usr/include/c++/13/parallel/omp_loop_static.h
/usr/include/c++/13/parallel/par_loop.h
/usr/include/c++/13/parallel/parallel.h
/usr/include/c++/13/parallel/partial_sum.h
/usr/include/c++/13/parallel/partition.h
/usr/include/c++/13/parallel/queue.h
/usr/include/c++/13/parallel/quicksort.h
/usr/include/c++/13/parallel/random_number.h
/usr/include/c++/13/parallel/random_shuffle.h
/usr/include/c++/13/parallel/search.h
/usr/include/c++/13/parallel/set_operations.h
/usr/include/c++/13/parallel/settings.h
/usr/include/c++/13/parallel/sort.h
/usr/include/c++/13/parallel/tags.h
/usr/include/c++/13/parallel/types.h
/usr/include/c++/13/parallel/unique_copy.h
/usr/include/c++/13/parallel/workstealing.h
/usr/include/c++/13/pstl
/usr/include/c++/13/pstl/algorithm_fwd.h
/usr/include/c++/13/pstl/algorithm_impl.h
/usr/include/c++/13/pstl/execution_defs.h
/usr/include/c++/13/pstl/execution_impl.h
/usr/include/c++/13/pstl/glue_algorithm_defs.h
/usr/include/c++/13/pstl/glue_algorithm_impl.h
/usr/include/c++/13/pstl/glue_execution_defs.h
/usr/include/c++/13/pstl/glue_memory_defs.h
/usr/include/c++/13/pstl/glue_memory_impl.h
/usr/include/c++/13/pstl/glue_numeric_defs.h
/usr/include/c++/13/pstl/glue_numeric_impl.h
/usr/include/c++/13/pstl/memory_impl.h
/usr/include/c++/13/pstl/numeric_fwd.h
/usr/include/c++/13/pstl/numeric_impl.h
/usr/include/c++/13/pstl/parallel_backend.h
/usr/include/c++/13/pstl/parallel_backend_serial.h
/usr/include/c++/13/pstl/parallel_backend_tbb.h
/usr/include/c++/13/pstl/parallel_backend_utils.h
/usr/include/c++/13/pstl/parallel_impl.h
/usr/include/c++/13/pstl/pstl_config.h
/usr/include/c++/13/pstl/unseq_backend_simd.h
/usr/include/c++/13/pstl/utils.h
/usr/include/c++/13/queue
/usr/include/c++/13/random
/usr/include/c++/13/ranges
/usr/include/c++/13/ratio
/usr/include/c++/13/regex
/usr/include/c++/13/scoped_allocator
/usr/include/c++/13/semaphore
/usr/include/c++/13/set
/usr/include/c++/13/shared_mutex
/usr/include/c++/13/source_location
/usr/include/c++/13/span
/usr/include/c++/13/spanstream
/usr/include/c++/13/sstream
/usr/include/c++/13/stack
/usr/include/c++/13/stacktrace
/usr/include/c++/13/stdatomic.h
/usr/include/c++/13/stdexcept
/usr/include/c++/13/stdfloat
/usr/include/c++/13/stdlib.h
/usr/include/c++/13/stop_token
/usr/include/c++/13/streambuf
/usr/include/c++/13/string
/usr/include/c++/13/string_view
/usr/include/c++/13/syncstream
/usr/include/c++/13/system_error
/usr/include/c++/13/tgmath.h
/usr/include/c++/13/thread
/usr/include/c++/13/tr1
/usr/include/c++/13/tr1/array
/usr/include/c++/13/tr1/bessel_function.tcc
/usr/include/c++/13/tr1/beta_function.tcc
/usr/include/c++/13/tr1/ccomplex
/usr/include/c++/13/tr1/cctype
/usr/include/c++/13/tr1/cfenv
/usr/include/c++/13/tr1/cfloat
/usr/include/c++/13/tr1/cinttypes
/usr/include/c++/13/tr1/climits
/usr/include/c++/13/tr1/cmath
/usr/include/c++/13/tr1/complex
/usr/include/c++/13/tr1/complex.h
/usr/include/c++/13/tr1/cstdarg
/usr/include/c++/13/tr1/cstdbool
/usr/include/c++/13/tr1/cstdint
/usr/include/c++/13/tr1/cstdio
/usr/include/c++/13/tr1/cstdlib
/usr/include/c++/13/tr1/ctgmath
/usr/include/c++/13/tr1/ctime
/usr/include/c++/13/tr1/ctype.h
/usr/include/c++/13/tr1/cwchar
/usr/include/c++/13/tr1/cwctype
/usr/include/c++/13/tr1/ell_integral.tcc
/usr/include/c++/13/tr1/exp_integral.tcc
/usr/include/c++/13/tr1/fenv.h
/usr/include/c++/13/tr1/float.h
/usr/include/c++/13/tr1/functional
/usr/include/c++/13/tr1/functional_hash.h
/usr/include/c++/13/tr1/gamma.tcc
/usr/include/c++/13/tr1/hashtable.h
/usr/include/c++/13/tr1/hashtable_policy.h
/usr/include/c++/13/tr1/hypergeometric.tcc
/usr/include/c++/13/tr1/inttypes.h
/usr/include/c++/13/tr1/legendre_function.tcc
/usr/include/c++/13/tr1/limits.h
/usr/include/c++/13/tr1/math.h
/usr/include/c++/13/tr1/memory
/usr/include/c++/13/tr1/modified_bessel_func.tcc
/usr/include/c++/13/tr1/poly_hermite.tcc
/usr/include/c++/13/tr1/poly_laguerre.tcc
/usr/include/c++/13/tr1/random
/usr/include/c++/13/tr1/random.h
/usr/include/c++/13/tr1/random.tcc
/usr/include/c++/13/tr1/regex
/usr/include/c++/13/tr1/riemann_zeta.tcc
/usr/include/c++/13/tr1/shared_ptr.h
/usr/include/c++/13/tr1/special_function_util.h
/usr/include/c++/13/tr1/stdarg.h
/usr/include/c++/13/tr1/stdbool.h
/usr/include/c++/13/tr1/stdint.h
/usr/include/c++/13/tr1/stdio.h
/usr/include/c++/13/tr1/stdlib.h
/usr/include/c++/13/tr1/tgmath.h
/usr/include/c++/13/tr1/tuple
/usr/include/c++/13/tr1/type_traits
/usr/include/c++/13/tr1/unordered_map
/usr/include/c++/13/tr1/unordered_map.h
/usr/include/c++/13/tr1/unordered_set
/usr/include/c++/13/tr1/unordered_set.h
/usr/include/c++/13/tr1/utility
/usr/include/c++/13/tr1/wchar.h
/usr/include/c++/13/tr1/wctype.h
/usr/include/c++/13/tr2
/usr/include/c++/13/tr2/bool_set
/usr/include/c++/13/tr2/bool_set.tcc
/usr/include/c++/13/tr2/dynamic_bitset
/usr/include/c++/13/tr2/dynamic_bitset.tcc
/usr/include/c++/13/tr2/ratio
/usr/include/c++/13/tr2/type_traits
/usr/include/c++/13/tuple
/usr/include/c++/13/type_traits
/usr/include/c++/13/typeindex
/usr/include/c++/13/typeinfo
/usr/include/c++/13/unordered_map
/usr/include/c++/13/unordered_set
/usr/include/c++/13/utility
/usr/include/c++/13/valarray
/usr/include/c++/13/variant
/usr/include/c++/13/vector
/usr/include/c++/13/version
/usr/include/x86_64-linux-gnu
/usr/include/x86_64-linux-gnu/c++
/usr/include/x86_64-linux-gnu/c++/13
/usr/include/x86_64-linux-gnu/c++/13/bits
/usr/include/x86_64-linux-gnu/c++/13/bits/atomic_word.h
/usr/include/x86_64-linux-gnu/c++/13/bits/basic_file.h
/usr/include/x86_64-linux-gnu/c++/13/bits/c++allocator.h
/usr/include/x86_64-linux-gnu/c++/13/bits/c++config.h
/usr/include/x86_64-linux-gnu/c++/13/bits/c++io.h
/usr/include/x86_64-linux-gnu/c++/13/bits/c++locale.h
/usr/include/x86_64-linux-gnu/c++/13/bits/cpu_defines.h
/usr/include/x86_64-linux-gnu/c++/13/bits/ctype_base.h
/usr/include/x86_64-linux-gnu/c++/13/bits/ctype_inline.h
/usr/include/x86_64-linux-gnu/c++/13/bits/cxxabi_tweaks.h
/usr/include/x86_64-linux-gnu/c++/13/bits/error_constants.h
/usr/include/x86_64-linux-gnu/c++/13/bits/extc++.h
/usr/include/x86_64-linux-gnu/c++/13/bits/gthr-default.h
/usr/include/x86_64-linux-gnu/c++/13/bits/gthr-posix.h
/usr/include/x86_64-linux-gnu/c++/13/bits/gthr-single.h
/usr/include/x86_64-linux-gnu/c++/13/bits/gthr.h
/usr/include/x86_64-linux-gnu/c++/13/bits/messages_members.h
/usr/include/x86_64-linux-gnu/c++/13/bits/opt_random.h
/usr/include/x86_64-linux-gnu/c++/13/bits/os_defines.h
/usr/include/x86_64-linux-gnu/c++/13/bits/stdc++.h
/usr/include/x86_64-linux-gnu/c++/13/bits/stdtr1c++.h
/usr/include/x86_64-linux-gnu/c++/13/bits/time_members.h
/usr/include/x86_64-linux-gnu/c++/13/ext
/usr/include/x86_64-linux-gnu/c++/13/ext/opt_random.h
/usr/lib
/usr/lib/gcc
/usr/lib/gcc/x86_64-linux-gnu
/usr/lib/gcc/x86_64-linux-gnu/13
/usr/lib/gcc/x86_64-linux-gnu/13/libstdc++.a
/usr/lib/gcc/x86_64-linux-gnu/13/libstdc++exp.a
/usr/lib/gcc/x86_64-linux-gnu/13/libstdc++fs.a
/usr/lib/gcc/x86_64-linux-gnu/13/libsupc++.a
/usr/share
/usr/share/doc
/usr/share/doc/gcc-13-base
/usr/share/doc/gcc-13-base/C++
/usr/share/doc/gcc-13-base/C++/changelog.libstdc++.gz
/usr/lib/gcc/x86_64-linux-gnu/13/libstdc++.so
/usr/share/doc/libstdc++-13-dev



/usr/lib/gcc/x86_64-linux-gnu/13/libstdc++.a
/usr/lib/gcc/x86_64-linux-gnu/13/libstdc++exp.a
/usr/lib/gcc/x86_64-linux-gnu/13/libstdc++fs.a
/usr/lib/gcc/x86_64-linux-gnu/13/libsupc++.a
/usr/lib/gcc/x86_64-linux-gnu/13/libstdc++.so


在列出的文件中，每个文件都与GNU标准C++库（libstdc++）相关，它们分别有不同的用途：
1. `libstdc++.a`:
   - 这是一个静态库版本的libstdc++。静态库意味着当你编译程序时，链接器会将这个库中的所有需要的代码直接复制到最终的可执行文件中。使用静态库的好处是生成的可执行文件可以在没有安装相应动态库的情况下运行，但缺点是生成的可执行文件会比较大，并且如果库更新了，你需要重新编译程序才能获得更新。
2. `libstdc++exp.a`:
   - 这个文件名不是标准的libstdc++发行版的一部分，它可能是一个特定于某些环境或构建配置的扩展静态库。通常来说，这种命名可能是为了区分不同的特性集或者实验性的功能。具体的作用需要查看该特定环境下的文档或构建说明来确定。
3. `libstdc++fs.a`:
   - 这个库可能是指向C++文件系统库的静态版本，它是C++17标准引入的一个部分，提供了跨平台的文件系统操作功能。如果你的应用程序需要这些功能，并且你希望静态链接这些功能，那么你可能会用到这个库。
4. `libsupc++.a`:
   - 这个库包含了支持C++语言特性的底层实现，如异常处理、RTTI（Run-Time Type Information）、类的构造和析构等。它通常与libstdc++一起工作，提供完整的C++运行时支持。
5. `libstdc++.so`:
   - 这是libstdc++的共享库（动态链接库）。当你的程序使用动态链接方式编译时，这个库会在程序运行时被加载。这样做的好处是可以节省磁盘空间和内存，因为多个程序可以共享同一个库的实例。此外，当你更新这个库时，所有依赖它的程序都会自动受益于更新，而不需要重新编译这些程序。

对于`libstdc++exp.a`，由于这不是一个常见的文件名，其确切作用可能取决于具体的上下文或特殊的构建配置。如果你遇到这个文件，建议查阅相关的构建脚本或项目文档以了解更多信息。其他四个文件则是libstdc++的标准组成部分，分别用于不同的链接场景。[2]

```shell
dpkg -L libc6
/.
/etc
/etc/ld.so.conf.d
/etc/ld.so.conf.d/x86_64-linux-gnu.conf
/lib
/lib/x86_64-linux-gnu
/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
/lib/x86_64-linux-gnu/libBrokenLocale.so.1
/lib/x86_64-linux-gnu/libanl.so.1
/lib/x86_64-linux-gnu/libc.so.6
/lib/x86_64-linux-gnu/libc_malloc_debug.so.0
/lib/x86_64-linux-gnu/libdl.so.2
/lib/x86_64-linux-gnu/libm.so.6
/lib/x86_64-linux-gnu/libmemusage.so
/lib/x86_64-linux-gnu/libmvec.so.1
/lib/x86_64-linux-gnu/libnsl.so.1
/lib/x86_64-linux-gnu/libnss_compat.so.2
/lib/x86_64-linux-gnu/libnss_dns.so.2
/lib/x86_64-linux-gnu/libnss_files.so.2
/lib/x86_64-linux-gnu/libnss_hesiod.so.2
/lib/x86_64-linux-gnu/libpcprofile.so
/lib/x86_64-linux-gnu/libpthread.so.0
/lib/x86_64-linux-gnu/libresolv.so.2
/lib/x86_64-linux-gnu/librt.so.1
/lib/x86_64-linux-gnu/libthread_db.so.1
/lib/x86_64-linux-gnu/libutil.so.1
/lib64
/usr
/usr/lib
/usr/lib/x86_64-linux-gnu
/usr/lib/x86_64-linux-gnu/audit
/usr/lib/x86_64-linux-gnu/audit/sotruss-lib.so
/usr/lib/x86_64-linux-gnu/gconv
/usr/lib/x86_64-linux-gnu/gconv/ANSI_X3.110.so
/usr/lib/x86_64-linux-gnu/gconv/ARMSCII-8.so
/usr/lib/x86_64-linux-gnu/gconv/ASMO_449.so
/usr/lib/x86_64-linux-gnu/gconv/BIG5.so
/usr/lib/x86_64-linux-gnu/gconv/BIG5HKSCS.so
/usr/lib/x86_64-linux-gnu/gconv/BRF.so
/usr/lib/x86_64-linux-gnu/gconv/CP10007.so
/usr/lib/x86_64-linux-gnu/gconv/CP1125.so
/usr/lib/x86_64-linux-gnu/gconv/CP1250.so
/usr/lib/x86_64-linux-gnu/gconv/CP1251.so
/usr/lib/x86_64-linux-gnu/gconv/CP1252.so
/usr/lib/x86_64-linux-gnu/gconv/CP1253.so
/usr/lib/x86_64-linux-gnu/gconv/CP1254.so
/usr/lib/x86_64-linux-gnu/gconv/CP1255.so
/usr/lib/x86_64-linux-gnu/gconv/CP1256.so
/usr/lib/x86_64-linux-gnu/gconv/CP1257.so
/usr/lib/x86_64-linux-gnu/gconv/CP1258.so
/usr/lib/x86_64-linux-gnu/gconv/CP737.so
/usr/lib/x86_64-linux-gnu/gconv/CP770.so
/usr/lib/x86_64-linux-gnu/gconv/CP771.so
/usr/lib/x86_64-linux-gnu/gconv/CP772.so
/usr/lib/x86_64-linux-gnu/gconv/CP773.so
/usr/lib/x86_64-linux-gnu/gconv/CP774.so
/usr/lib/x86_64-linux-gnu/gconv/CP775.so
/usr/lib/x86_64-linux-gnu/gconv/CP932.so
/usr/lib/x86_64-linux-gnu/gconv/CSN_369103.so
/usr/lib/x86_64-linux-gnu/gconv/CWI.so
/usr/lib/x86_64-linux-gnu/gconv/DEC-MCS.so
/usr/lib/x86_64-linux-gnu/gconv/EBCDIC-AT-DE-A.so
/usr/lib/x86_64-linux-gnu/gconv/EBCDIC-AT-DE.so
/usr/lib/x86_64-linux-gnu/gconv/EBCDIC-CA-FR.so
/usr/lib/x86_64-linux-gnu/gconv/EBCDIC-DK-NO-A.so
/usr/lib/x86_64-linux-gnu/gconv/EBCDIC-DK-NO.so
/usr/lib/x86_64-linux-gnu/gconv/EBCDIC-ES-A.so
/usr/lib/x86_64-linux-gnu/gconv/EBCDIC-ES-S.so
/usr/lib/x86_64-linux-gnu/gconv/EBCDIC-ES.so
/usr/lib/x86_64-linux-gnu/gconv/EBCDIC-FI-SE-A.so
/usr/lib/x86_64-linux-gnu/gconv/EBCDIC-FI-SE.so
/usr/lib/x86_64-linux-gnu/gconv/EBCDIC-FR.so
/usr/lib/x86_64-linux-gnu/gconv/EBCDIC-IS-FRISS.so
/usr/lib/x86_64-linux-gnu/gconv/EBCDIC-IT.so
/usr/lib/x86_64-linux-gnu/gconv/EBCDIC-PT.so
/usr/lib/x86_64-linux-gnu/gconv/EBCDIC-UK.so
/usr/lib/x86_64-linux-gnu/gconv/EBCDIC-US.so
/usr/lib/x86_64-linux-gnu/gconv/ECMA-CYRILLIC.so
/usr/lib/x86_64-linux-gnu/gconv/EUC-CN.so
/usr/lib/x86_64-linux-gnu/gconv/EUC-JISX0213.so
/usr/lib/x86_64-linux-gnu/gconv/EUC-JP-MS.so
/usr/lib/x86_64-linux-gnu/gconv/EUC-JP.so
/usr/lib/x86_64-linux-gnu/gconv/EUC-KR.so
/usr/lib/x86_64-linux-gnu/gconv/EUC-TW.so
/usr/lib/x86_64-linux-gnu/gconv/GB18030.so
/usr/lib/x86_64-linux-gnu/gconv/GBBIG5.so
/usr/lib/x86_64-linux-gnu/gconv/GBGBK.so
/usr/lib/x86_64-linux-gnu/gconv/GBK.so
/usr/lib/x86_64-linux-gnu/gconv/GEORGIAN-ACADEMY.so
/usr/lib/x86_64-linux-gnu/gconv/GEORGIAN-PS.so
/usr/lib/x86_64-linux-gnu/gconv/GOST_19768-74.so
/usr/lib/x86_64-linux-gnu/gconv/GREEK-CCITT.so
/usr/lib/x86_64-linux-gnu/gconv/GREEK7-OLD.so
/usr/lib/x86_64-linux-gnu/gconv/GREEK7.so
/usr/lib/x86_64-linux-gnu/gconv/HP-GREEK8.so
/usr/lib/x86_64-linux-gnu/gconv/HP-ROMAN8.so
/usr/lib/x86_64-linux-gnu/gconv/HP-ROMAN9.so
/usr/lib/x86_64-linux-gnu/gconv/HP-THAI8.so
/usr/lib/x86_64-linux-gnu/gconv/HP-TURKISH8.so
/usr/lib/x86_64-linux-gnu/gconv/IBM037.so
/usr/lib/x86_64-linux-gnu/gconv/IBM038.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1004.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1008.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1008_420.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1025.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1026.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1046.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1047.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1097.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1112.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1122.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1123.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1124.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1129.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1130.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1132.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1133.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1137.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1140.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1141.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1142.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1143.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1144.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1145.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1146.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1147.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1148.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1149.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1153.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1154.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1155.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1156.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1157.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1158.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1160.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1161.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1162.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1163.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1164.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1166.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1167.so
/usr/lib/x86_64-linux-gnu/gconv/IBM12712.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1364.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1371.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1388.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1390.so
/usr/lib/x86_64-linux-gnu/gconv/IBM1399.so
/usr/lib/x86_64-linux-gnu/gconv/IBM16804.so
/usr/lib/x86_64-linux-gnu/gconv/IBM256.so
/usr/lib/x86_64-linux-gnu/gconv/IBM273.so
/usr/lib/x86_64-linux-gnu/gconv/IBM274.so
/usr/lib/x86_64-linux-gnu/gconv/IBM275.so
/usr/lib/x86_64-linux-gnu/gconv/IBM277.so
/usr/lib/x86_64-linux-gnu/gconv/IBM278.so
/usr/lib/x86_64-linux-gnu/gconv/IBM280.so
/usr/lib/x86_64-linux-gnu/gconv/IBM281.so
/usr/lib/x86_64-linux-gnu/gconv/IBM284.so
/usr/lib/x86_64-linux-gnu/gconv/IBM285.so
/usr/lib/x86_64-linux-gnu/gconv/IBM290.so
/usr/lib/x86_64-linux-gnu/gconv/IBM297.so
/usr/lib/x86_64-linux-gnu/gconv/IBM420.so
/usr/lib/x86_64-linux-gnu/gconv/IBM423.so
/usr/lib/x86_64-linux-gnu/gconv/IBM424.so
/usr/lib/x86_64-linux-gnu/gconv/IBM437.so
/usr/lib/x86_64-linux-gnu/gconv/IBM4517.so
/usr/lib/x86_64-linux-gnu/gconv/IBM4899.so
/usr/lib/x86_64-linux-gnu/gconv/IBM4909.so
/usr/lib/x86_64-linux-gnu/gconv/IBM4971.so
/usr/lib/x86_64-linux-gnu/gconv/IBM500.so
/usr/lib/x86_64-linux-gnu/gconv/IBM5347.so
/usr/lib/x86_64-linux-gnu/gconv/IBM803.so
/usr/lib/x86_64-linux-gnu/gconv/IBM850.so
/usr/lib/x86_64-linux-gnu/gconv/IBM851.so
/usr/lib/x86_64-linux-gnu/gconv/IBM852.so
/usr/lib/x86_64-linux-gnu/gconv/IBM855.so
/usr/lib/x86_64-linux-gnu/gconv/IBM856.so
/usr/lib/x86_64-linux-gnu/gconv/IBM857.so
/usr/lib/x86_64-linux-gnu/gconv/IBM858.so
/usr/lib/x86_64-linux-gnu/gconv/IBM860.so
/usr/lib/x86_64-linux-gnu/gconv/IBM861.so
/usr/lib/x86_64-linux-gnu/gconv/IBM862.so
/usr/lib/x86_64-linux-gnu/gconv/IBM863.so
/usr/lib/x86_64-linux-gnu/gconv/IBM864.so
/usr/lib/x86_64-linux-gnu/gconv/IBM865.so
/usr/lib/x86_64-linux-gnu/gconv/IBM866.so
/usr/lib/x86_64-linux-gnu/gconv/IBM866NAV.so
/usr/lib/x86_64-linux-gnu/gconv/IBM868.so
/usr/lib/x86_64-linux-gnu/gconv/IBM869.so
/usr/lib/x86_64-linux-gnu/gconv/IBM870.so
/usr/lib/x86_64-linux-gnu/gconv/IBM871.so
/usr/lib/x86_64-linux-gnu/gconv/IBM874.so
/usr/lib/x86_64-linux-gnu/gconv/IBM875.so
/usr/lib/x86_64-linux-gnu/gconv/IBM880.so
/usr/lib/x86_64-linux-gnu/gconv/IBM891.so
/usr/lib/x86_64-linux-gnu/gconv/IBM901.so
/usr/lib/x86_64-linux-gnu/gconv/IBM902.so
/usr/lib/x86_64-linux-gnu/gconv/IBM903.so
/usr/lib/x86_64-linux-gnu/gconv/IBM9030.so
/usr/lib/x86_64-linux-gnu/gconv/IBM904.so
/usr/lib/x86_64-linux-gnu/gconv/IBM905.so
/usr/lib/x86_64-linux-gnu/gconv/IBM9066.so
/usr/lib/x86_64-linux-gnu/gconv/IBM918.so
/usr/lib/x86_64-linux-gnu/gconv/IBM921.so
/usr/lib/x86_64-linux-gnu/gconv/IBM922.so
/usr/lib/x86_64-linux-gnu/gconv/IBM930.so
/usr/lib/x86_64-linux-gnu/gconv/IBM932.so
/usr/lib/x86_64-linux-gnu/gconv/IBM933.so
/usr/lib/x86_64-linux-gnu/gconv/IBM935.so
/usr/lib/x86_64-linux-gnu/gconv/IBM937.so
/usr/lib/x86_64-linux-gnu/gconv/IBM939.so
/usr/lib/x86_64-linux-gnu/gconv/IBM943.so
/usr/lib/x86_64-linux-gnu/gconv/IBM9448.so
/usr/lib/x86_64-linux-gnu/gconv/IEC_P27-1.so
/usr/lib/x86_64-linux-gnu/gconv/INIS-8.so
/usr/lib/x86_64-linux-gnu/gconv/INIS-CYRILLIC.so
/usr/lib/x86_64-linux-gnu/gconv/INIS.so
/usr/lib/x86_64-linux-gnu/gconv/ISIRI-3342.so
/usr/lib/x86_64-linux-gnu/gconv/ISO-2022-CN-EXT.so
/usr/lib/x86_64-linux-gnu/gconv/ISO-2022-CN.so
/usr/lib/x86_64-linux-gnu/gconv/ISO-2022-JP-3.so
/usr/lib/x86_64-linux-gnu/gconv/ISO-2022-JP.so
/usr/lib/x86_64-linux-gnu/gconv/ISO-2022-KR.so
/usr/lib/x86_64-linux-gnu/gconv/ISO-IR-197.so
/usr/lib/x86_64-linux-gnu/gconv/ISO-IR-209.so
/usr/lib/x86_64-linux-gnu/gconv/ISO646.so
/usr/lib/x86_64-linux-gnu/gconv/ISO8859-1.so
/usr/lib/x86_64-linux-gnu/gconv/ISO8859-10.so
/usr/lib/x86_64-linux-gnu/gconv/ISO8859-11.so
/usr/lib/x86_64-linux-gnu/gconv/ISO8859-13.so
/usr/lib/x86_64-linux-gnu/gconv/ISO8859-14.so
/usr/lib/x86_64-linux-gnu/gconv/ISO8859-15.so
/usr/lib/x86_64-linux-gnu/gconv/ISO8859-16.so
/usr/lib/x86_64-linux-gnu/gconv/ISO8859-2.so
/usr/lib/x86_64-linux-gnu/gconv/ISO8859-3.so
/usr/lib/x86_64-linux-gnu/gconv/ISO8859-4.so
/usr/lib/x86_64-linux-gnu/gconv/ISO8859-5.so
/usr/lib/x86_64-linux-gnu/gconv/ISO8859-6.so
/usr/lib/x86_64-linux-gnu/gconv/ISO8859-7.so
/usr/lib/x86_64-linux-gnu/gconv/ISO8859-8.so
/usr/lib/x86_64-linux-gnu/gconv/ISO8859-9.so
/usr/lib/x86_64-linux-gnu/gconv/ISO8859-9E.so
/usr/lib/x86_64-linux-gnu/gconv/ISO_10367-BOX.so
/usr/lib/x86_64-linux-gnu/gconv/ISO_11548-1.so
/usr/lib/x86_64-linux-gnu/gconv/ISO_2033.so
/usr/lib/x86_64-linux-gnu/gconv/ISO_5427-EXT.so
/usr/lib/x86_64-linux-gnu/gconv/ISO_5427.so
/usr/lib/x86_64-linux-gnu/gconv/ISO_5428.so
/usr/lib/x86_64-linux-gnu/gconv/ISO_6937-2.so
/usr/lib/x86_64-linux-gnu/gconv/ISO_6937.so
/usr/lib/x86_64-linux-gnu/gconv/JOHAB.so
/usr/lib/x86_64-linux-gnu/gconv/KOI-8.so
/usr/lib/x86_64-linux-gnu/gconv/KOI8-R.so
/usr/lib/x86_64-linux-gnu/gconv/KOI8-RU.so
/usr/lib/x86_64-linux-gnu/gconv/KOI8-T.so
/usr/lib/x86_64-linux-gnu/gconv/KOI8-U.so
/usr/lib/x86_64-linux-gnu/gconv/LATIN-GREEK-1.so
/usr/lib/x86_64-linux-gnu/gconv/LATIN-GREEK.so
/usr/lib/x86_64-linux-gnu/gconv/MAC-CENTRALEUROPE.so
/usr/lib/x86_64-linux-gnu/gconv/MAC-IS.so
/usr/lib/x86_64-linux-gnu/gconv/MAC-SAMI.so
/usr/lib/x86_64-linux-gnu/gconv/MAC-UK.so
/usr/lib/x86_64-linux-gnu/gconv/MACINTOSH.so
/usr/lib/x86_64-linux-gnu/gconv/MIK.so
/usr/lib/x86_64-linux-gnu/gconv/NATS-DANO.so
/usr/lib/x86_64-linux-gnu/gconv/NATS-SEFI.so
/usr/lib/x86_64-linux-gnu/gconv/PT154.so
/usr/lib/x86_64-linux-gnu/gconv/RK1048.so
/usr/lib/x86_64-linux-gnu/gconv/SAMI-WS2.so
/usr/lib/x86_64-linux-gnu/gconv/SHIFT_JISX0213.so
/usr/lib/x86_64-linux-gnu/gconv/SJIS.so
/usr/lib/x86_64-linux-gnu/gconv/T.61.so
/usr/lib/x86_64-linux-gnu/gconv/TCVN5712-1.so
/usr/lib/x86_64-linux-gnu/gconv/TIS-620.so
/usr/lib/x86_64-linux-gnu/gconv/TSCII.so
/usr/lib/x86_64-linux-gnu/gconv/UHC.so
/usr/lib/x86_64-linux-gnu/gconv/UNICODE.so
/usr/lib/x86_64-linux-gnu/gconv/UTF-16.so
/usr/lib/x86_64-linux-gnu/gconv/UTF-32.so
/usr/lib/x86_64-linux-gnu/gconv/UTF-7.so
/usr/lib/x86_64-linux-gnu/gconv/VISCII.so
/usr/lib/x86_64-linux-gnu/gconv/gconv-modules
/usr/lib/x86_64-linux-gnu/gconv/gconv-modules.cache
/usr/lib/x86_64-linux-gnu/gconv/gconv-modules.d
/usr/lib/x86_64-linux-gnu/gconv/gconv-modules.d/gconv-modules-extra.conf
/usr/lib/x86_64-linux-gnu/gconv/libCNS.so
/usr/lib/x86_64-linux-gnu/gconv/libGB.so
/usr/lib/x86_64-linux-gnu/gconv/libISOIR165.so
/usr/lib/x86_64-linux-gnu/gconv/libJIS.so
/usr/lib/x86_64-linux-gnu/gconv/libJISX0213.so
/usr/lib/x86_64-linux-gnu/gconv/libKSC.so
/usr/share
/usr/share/doc
/usr/share/doc/libc6
/usr/share/doc/libc6/NEWS.Debian.gz
/usr/share/doc/libc6/NEWS.gz
/usr/share/doc/libc6/README.Debian.gz
/usr/share/doc/libc6/README.hesiod.gz
/usr/share/doc/libc6/changelog.Debian.gz
/usr/share/doc/libc6/copyright
/usr/share/lintian
/usr/share/lintian/overrides
/usr/share/lintian/overrides/libc6
/lib64/ld-linux-x86-64.so.2
```

```
dpkg -L libc6-dev
/.
/usr
/usr/include
/usr/include/aio.h
/usr/include/aliases.h
/usr/include/alloca.h
/usr/include/ar.h
/usr/include/argp.h
/usr/include/argz.h
/usr/include/arpa
/usr/include/arpa/ftp.h
/usr/include/arpa/inet.h
/usr/include/arpa/nameser.h
/usr/include/arpa/nameser_compat.h
/usr/include/arpa/telnet.h
/usr/include/arpa/tftp.h
/usr/include/assert.h
/usr/include/byteswap.h
/usr/include/complex.h
/usr/include/cpio.h
/usr/include/ctype.h
/usr/include/dirent.h
/usr/include/dlfcn.h
/usr/include/elf.h
/usr/include/endian.h
/usr/include/envz.h
/usr/include/err.h
/usr/include/errno.h
/usr/include/error.h
/usr/include/execinfo.h
/usr/include/fcntl.h
/usr/include/features-time64.h
/usr/include/features.h
/usr/include/fenv.h
/usr/include/finclude
/usr/include/finclude/math-vector-fortran.h
/usr/include/fmtmsg.h
/usr/include/fnmatch.h
/usr/include/fstab.h
/usr/include/fts.h
/usr/include/ftw.h
/usr/include/gconv.h
/usr/include/getopt.h
/usr/include/glob.h
/usr/include/gnu-versions.h
/usr/include/grp.h
/usr/include/gshadow.h
/usr/include/iconv.h
/usr/include/ifaddrs.h
/usr/include/inttypes.h
/usr/include/langinfo.h
/usr/include/lastlog.h
/usr/include/libgen.h
/usr/include/libintl.h
/usr/include/limits.h
/usr/include/link.h
/usr/include/locale.h
/usr/include/malloc.h
/usr/include/math.h
/usr/include/mcheck.h
/usr/include/memory.h
/usr/include/mntent.h
/usr/include/monetary.h
/usr/include/mqueue.h
/usr/include/net
/usr/include/net/ethernet.h
/usr/include/net/if.h
/usr/include/net/if_arp.h
/usr/include/net/if_packet.h
/usr/include/net/if_ppp.h
/usr/include/net/if_shaper.h
/usr/include/net/if_slip.h
/usr/include/net/ppp-comp.h
/usr/include/net/ppp_defs.h
/usr/include/net/route.h
/usr/include/netash
/usr/include/netash/ash.h
/usr/include/netatalk
/usr/include/netatalk/at.h
/usr/include/netax25
/usr/include/netax25/ax25.h
/usr/include/netdb.h
/usr/include/neteconet
/usr/include/neteconet/ec.h
/usr/include/netinet
/usr/include/netinet/ether.h
/usr/include/netinet/icmp6.h
/usr/include/netinet/if_ether.h
/usr/include/netinet/if_fddi.h
/usr/include/netinet/if_tr.h
/usr/include/netinet/igmp.h
/usr/include/netinet/in.h
/usr/include/netinet/in_systm.h
/usr/include/netinet/ip.h
/usr/include/netinet/ip6.h
/usr/include/netinet/ip_icmp.h
/usr/include/netinet/tcp.h
/usr/include/netinet/udp.h
/usr/include/netipx
/usr/include/netipx/ipx.h
/usr/include/netiucv
/usr/include/netiucv/iucv.h
/usr/include/netpacket
/usr/include/netpacket/packet.h
/usr/include/netrom
/usr/include/netrom/netrom.h
/usr/include/netrose
/usr/include/netrose/rose.h
/usr/include/nfs
/usr/include/nfs/nfs.h
/usr/include/nl_types.h
/usr/include/nss.h
/usr/include/obstack.h
/usr/include/paths.h
/usr/include/poll.h
/usr/include/printf.h
/usr/include/proc_service.h
/usr/include/protocols
/usr/include/protocols/routed.h
/usr/include/protocols/rwhod.h
/usr/include/protocols/talkd.h
/usr/include/protocols/timed.h
/usr/include/pthread.h
/usr/include/pty.h
/usr/include/pwd.h
/usr/include/re_comp.h
/usr/include/regex.h
/usr/include/regexp.h
/usr/include/resolv.h
/usr/include/rpc
/usr/include/rpc/netdb.h
/usr/include/sched.h
/usr/include/scsi
/usr/include/scsi/scsi.h
/usr/include/scsi/scsi_ioctl.h
/usr/include/scsi/sg.h
/usr/include/search.h
/usr/include/semaphore.h
/usr/include/setjmp.h
/usr/include/sgtty.h
/usr/include/shadow.h
/usr/include/signal.h
/usr/include/spawn.h
/usr/include/stab.h
/usr/include/stdc-predef.h
/usr/include/stdint.h
/usr/include/stdio.h
/usr/include/stdio_ext.h
/usr/include/stdlib.h
/usr/include/string.h
/usr/include/strings.h
/usr/include/syscall.h
/usr/include/sysexits.h
/usr/include/syslog.h
/usr/include/tar.h
/usr/include/termio.h
/usr/include/termios.h
/usr/include/tgmath.h
/usr/include/thread_db.h
/usr/include/threads.h
/usr/include/time.h
/usr/include/ttyent.h
/usr/include/uchar.h
/usr/include/ucontext.h
/usr/include/ulimit.h
/usr/include/unistd.h
/usr/include/utime.h
/usr/include/utmp.h
/usr/include/utmpx.h
/usr/include/values.h
/usr/include/wait.h
/usr/include/wchar.h
/usr/include/wctype.h
/usr/include/wordexp.h
/usr/include/x86_64-linux-gnu
/usr/include/x86_64-linux-gnu/a.out.h
/usr/include/x86_64-linux-gnu/bits
/usr/include/x86_64-linux-gnu/bits/a.out.h
/usr/include/x86_64-linux-gnu/bits/argp-ldbl.h
/usr/include/x86_64-linux-gnu/bits/atomic_wide_counter.h
/usr/include/x86_64-linux-gnu/bits/byteswap.h
/usr/include/x86_64-linux-gnu/bits/cmathcalls.h
/usr/include/x86_64-linux-gnu/bits/confname.h
/usr/include/x86_64-linux-gnu/bits/cpu-set.h
/usr/include/x86_64-linux-gnu/bits/dirent.h
/usr/include/x86_64-linux-gnu/bits/dirent_ext.h
/usr/include/x86_64-linux-gnu/bits/dl_find_object.h
/usr/include/x86_64-linux-gnu/bits/dlfcn.h
/usr/include/x86_64-linux-gnu/bits/elfclass.h
/usr/include/x86_64-linux-gnu/bits/endian.h
/usr/include/x86_64-linux-gnu/bits/endianness.h
/usr/include/x86_64-linux-gnu/bits/environments.h
/usr/include/x86_64-linux-gnu/bits/epoll.h
/usr/include/x86_64-linux-gnu/bits/err-ldbl.h
/usr/include/x86_64-linux-gnu/bits/errno.h
/usr/include/x86_64-linux-gnu/bits/error-ldbl.h
/usr/include/x86_64-linux-gnu/bits/error.h
/usr/include/x86_64-linux-gnu/bits/eventfd.h
/usr/include/x86_64-linux-gnu/bits/fcntl-linux.h
/usr/include/x86_64-linux-gnu/bits/fcntl.h
/usr/include/x86_64-linux-gnu/bits/fcntl2.h
/usr/include/x86_64-linux-gnu/bits/fenv.h
/usr/include/x86_64-linux-gnu/bits/floatn-common.h
/usr/include/x86_64-linux-gnu/bits/floatn.h
/usr/include/x86_64-linux-gnu/bits/flt-eval-method.h
/usr/include/x86_64-linux-gnu/bits/fp-fast.h
/usr/include/x86_64-linux-gnu/bits/fp-logb.h
/usr/include/x86_64-linux-gnu/bits/getopt_core.h
/usr/include/x86_64-linux-gnu/bits/getopt_ext.h
/usr/include/x86_64-linux-gnu/bits/getopt_posix.h
/usr/include/x86_64-linux-gnu/bits/hwcap.h
/usr/include/x86_64-linux-gnu/bits/in.h
/usr/include/x86_64-linux-gnu/bits/indirect-return.h
/usr/include/x86_64-linux-gnu/bits/initspin.h
/usr/include/x86_64-linux-gnu/bits/inotify.h
/usr/include/x86_64-linux-gnu/bits/ioctl-types.h
/usr/include/x86_64-linux-gnu/bits/ioctls.h
/usr/include/x86_64-linux-gnu/bits/ipc-perm.h
/usr/include/x86_64-linux-gnu/bits/ipc.h
/usr/include/x86_64-linux-gnu/bits/ipctypes.h
/usr/include/x86_64-linux-gnu/bits/iscanonical.h
/usr/include/x86_64-linux-gnu/bits/libc-header-start.h
/usr/include/x86_64-linux-gnu/bits/libm-simd-decl-stubs.h
/usr/include/x86_64-linux-gnu/bits/link.h
/usr/include/x86_64-linux-gnu/bits/link_lavcurrent.h
/usr/include/x86_64-linux-gnu/bits/local_lim.h
/usr/include/x86_64-linux-gnu/bits/locale.h
/usr/include/x86_64-linux-gnu/bits/long-double.h
/usr/include/x86_64-linux-gnu/bits/math-vector.h
/usr/include/x86_64-linux-gnu/bits/mathcalls-helper-functions.h
/usr/include/x86_64-linux-gnu/bits/mathcalls-narrow.h
/usr/include/x86_64-linux-gnu/bits/mathcalls.h
/usr/include/x86_64-linux-gnu/bits/mathdef.h
/usr/include/x86_64-linux-gnu/bits/mman-linux.h
/usr/include/x86_64-linux-gnu/bits/mman-map-flags-generic.h
/usr/include/x86_64-linux-gnu/bits/mman-shared.h
/usr/include/x86_64-linux-gnu/bits/mman.h
/usr/include/x86_64-linux-gnu/bits/monetary-ldbl.h
/usr/include/x86_64-linux-gnu/bits/mqueue.h
/usr/include/x86_64-linux-gnu/bits/mqueue2.h
/usr/include/x86_64-linux-gnu/bits/msq.h
/usr/include/x86_64-linux-gnu/bits/netdb.h
/usr/include/x86_64-linux-gnu/bits/param.h
/usr/include/x86_64-linux-gnu/bits/platform
/usr/include/x86_64-linux-gnu/bits/platform/x86.h
/usr/include/x86_64-linux-gnu/bits/poll.h
/usr/include/x86_64-linux-gnu/bits/poll2.h
/usr/include/x86_64-linux-gnu/bits/posix1_lim.h
/usr/include/x86_64-linux-gnu/bits/posix2_lim.h
/usr/include/x86_64-linux-gnu/bits/posix_opt.h
/usr/include/x86_64-linux-gnu/bits/printf-ldbl.h
/usr/include/x86_64-linux-gnu/bits/procfs-extra.h
/usr/include/x86_64-linux-gnu/bits/procfs-id.h
/usr/include/x86_64-linux-gnu/bits/procfs-prregset.h
/usr/include/x86_64-linux-gnu/bits/procfs.h
/usr/include/x86_64-linux-gnu/bits/pthread_stack_min-dynamic.h
/usr/include/x86_64-linux-gnu/bits/pthread_stack_min.h
/usr/include/x86_64-linux-gnu/bits/pthreadtypes-arch.h
/usr/include/x86_64-linux-gnu/bits/pthreadtypes.h
/usr/include/x86_64-linux-gnu/bits/ptrace-shared.h
/usr/include/x86_64-linux-gnu/bits/resource.h
/usr/include/x86_64-linux-gnu/bits/rseq.h
/usr/include/x86_64-linux-gnu/bits/sched.h
/usr/include/x86_64-linux-gnu/bits/select.h
/usr/include/x86_64-linux-gnu/bits/select2.h
/usr/include/x86_64-linux-gnu/bits/sem.h
/usr/include/x86_64-linux-gnu/bits/semaphore.h
/usr/include/x86_64-linux-gnu/bits/setjmp.h
/usr/include/x86_64-linux-gnu/bits/setjmp2.h
/usr/include/x86_64-linux-gnu/bits/shm.h
/usr/include/x86_64-linux-gnu/bits/shmlba.h
/usr/include/x86_64-linux-gnu/bits/sigaction.h
/usr/include/x86_64-linux-gnu/bits/sigcontext.h
/usr/include/x86_64-linux-gnu/bits/sigevent-consts.h
/usr/include/x86_64-linux-gnu/bits/siginfo-arch.h
/usr/include/x86_64-linux-gnu/bits/siginfo-consts-arch.h
/usr/include/x86_64-linux-gnu/bits/siginfo-consts.h
/usr/include/x86_64-linux-gnu/bits/signal_ext.h
/usr/include/x86_64-linux-gnu/bits/signalfd.h
/usr/include/x86_64-linux-gnu/bits/signum-arch.h
/usr/include/x86_64-linux-gnu/bits/signum-generic.h
/usr/include/x86_64-linux-gnu/bits/sigstack.h
/usr/include/x86_64-linux-gnu/bits/sigstksz.h
/usr/include/x86_64-linux-gnu/bits/sigthread.h
/usr/include/x86_64-linux-gnu/bits/sockaddr.h
/usr/include/x86_64-linux-gnu/bits/socket-constants.h
/usr/include/x86_64-linux-gnu/bits/socket.h
/usr/include/x86_64-linux-gnu/bits/socket2.h
/usr/include/x86_64-linux-gnu/bits/socket_type.h
/usr/include/x86_64-linux-gnu/bits/ss_flags.h
/usr/include/x86_64-linux-gnu/bits/stab.def
/usr/include/x86_64-linux-gnu/bits/stat.h
/usr/include/x86_64-linux-gnu/bits/statfs.h
/usr/include/x86_64-linux-gnu/bits/statvfs.h
/usr/include/x86_64-linux-gnu/bits/statx-generic.h
/usr/include/x86_64-linux-gnu/bits/statx.h
/usr/include/x86_64-linux-gnu/bits/stdint-intn.h
/usr/include/x86_64-linux-gnu/bits/stdint-uintn.h
/usr/include/x86_64-linux-gnu/bits/stdio-ldbl.h
/usr/include/x86_64-linux-gnu/bits/stdio.h
/usr/include/x86_64-linux-gnu/bits/stdio2.h
/usr/include/x86_64-linux-gnu/bits/stdio_lim.h
/usr/include/x86_64-linux-gnu/bits/stdlib-bsearch.h
/usr/include/x86_64-linux-gnu/bits/stdlib-float.h
/usr/include/x86_64-linux-gnu/bits/stdlib-ldbl.h
/usr/include/x86_64-linux-gnu/bits/stdlib.h
/usr/include/x86_64-linux-gnu/bits/string_fortified.h
/usr/include/x86_64-linux-gnu/bits/strings_fortified.h
/usr/include/x86_64-linux-gnu/bits/struct_mutex.h
/usr/include/x86_64-linux-gnu/bits/struct_rwlock.h
/usr/include/x86_64-linux-gnu/bits/struct_stat.h
/usr/include/x86_64-linux-gnu/bits/struct_stat_time64_helper.h
/usr/include/x86_64-linux-gnu/bits/syscall.h
/usr/include/x86_64-linux-gnu/bits/syslog-ldbl.h
/usr/include/x86_64-linux-gnu/bits/syslog-path.h
/usr/include/x86_64-linux-gnu/bits/syslog.h
/usr/include/x86_64-linux-gnu/bits/sysmacros.h
/usr/include/x86_64-linux-gnu/bits/termios-baud.h
/usr/include/x86_64-linux-gnu/bits/termios-c_cc.h
/usr/include/x86_64-linux-gnu/bits/termios-c_cflag.h
/usr/include/x86_64-linux-gnu/bits/termios-c_iflag.h
/usr/include/x86_64-linux-gnu/bits/termios-c_lflag.h
/usr/include/x86_64-linux-gnu/bits/termios-c_oflag.h
/usr/include/x86_64-linux-gnu/bits/termios-misc.h
/usr/include/x86_64-linux-gnu/bits/termios-struct.h
/usr/include/x86_64-linux-gnu/bits/termios-tcflow.h
/usr/include/x86_64-linux-gnu/bits/termios.h
/usr/include/x86_64-linux-gnu/bits/thread-shared-types.h
/usr/include/x86_64-linux-gnu/bits/time.h
/usr/include/x86_64-linux-gnu/bits/time64.h
/usr/include/x86_64-linux-gnu/bits/timerfd.h
/usr/include/x86_64-linux-gnu/bits/timesize.h
/usr/include/x86_64-linux-gnu/bits/timex.h
/usr/include/x86_64-linux-gnu/bits/types
/usr/include/x86_64-linux-gnu/bits/types/FILE.h
/usr/include/x86_64-linux-gnu/bits/types/__FILE.h
/usr/include/x86_64-linux-gnu/bits/types/__fpos64_t.h
/usr/include/x86_64-linux-gnu/bits/types/__fpos_t.h
/usr/include/x86_64-linux-gnu/bits/types/__locale_t.h
/usr/include/x86_64-linux-gnu/bits/types/__mbstate_t.h
/usr/include/x86_64-linux-gnu/bits/types/__sigset_t.h
/usr/include/x86_64-linux-gnu/bits/types/__sigval_t.h
/usr/include/x86_64-linux-gnu/bits/types/clock_t.h
/usr/include/x86_64-linux-gnu/bits/types/clockid_t.h
/usr/include/x86_64-linux-gnu/bits/types/cookie_io_functions_t.h
/usr/include/x86_64-linux-gnu/bits/types/error_t.h
/usr/include/x86_64-linux-gnu/bits/types/locale_t.h
/usr/include/x86_64-linux-gnu/bits/types/mbstate_t.h
/usr/include/x86_64-linux-gnu/bits/types/res_state.h
/usr/include/x86_64-linux-gnu/bits/types/sig_atomic_t.h
/usr/include/x86_64-linux-gnu/bits/types/sigevent_t.h
/usr/include/x86_64-linux-gnu/bits/types/siginfo_t.h
/usr/include/x86_64-linux-gnu/bits/types/sigset_t.h
/usr/include/x86_64-linux-gnu/bits/types/sigval_t.h
/usr/include/x86_64-linux-gnu/bits/types/stack_t.h
/usr/include/x86_64-linux-gnu/bits/types/struct_FILE.h
/usr/include/x86_64-linux-gnu/bits/types/struct___jmp_buf_tag.h
/usr/include/x86_64-linux-gnu/bits/types/struct_iovec.h
/usr/include/x86_64-linux-gnu/bits/types/struct_itimerspec.h
/usr/include/x86_64-linux-gnu/bits/types/struct_msqid64_ds.h
/usr/include/x86_64-linux-gnu/bits/types/struct_msqid64_ds_helper.h
/usr/include/x86_64-linux-gnu/bits/types/struct_msqid_ds.h
/usr/include/x86_64-linux-gnu/bits/types/struct_osockaddr.h
/usr/include/x86_64-linux-gnu/bits/types/struct_rusage.h
/usr/include/x86_64-linux-gnu/bits/types/struct_sched_param.h
/usr/include/x86_64-linux-gnu/bits/types/struct_semid64_ds.h
/usr/include/x86_64-linux-gnu/bits/types/struct_semid64_ds_helper.h
/usr/include/x86_64-linux-gnu/bits/types/struct_semid_ds.h
/usr/include/x86_64-linux-gnu/bits/types/struct_shmid64_ds.h
/usr/include/x86_64-linux-gnu/bits/types/struct_shmid64_ds_helper.h
/usr/include/x86_64-linux-gnu/bits/types/struct_shmid_ds.h
/usr/include/x86_64-linux-gnu/bits/types/struct_sigstack.h
/usr/include/x86_64-linux-gnu/bits/types/struct_statx.h
/usr/include/x86_64-linux-gnu/bits/types/struct_statx_timestamp.h
/usr/include/x86_64-linux-gnu/bits/types/struct_timeb.h
/usr/include/x86_64-linux-gnu/bits/types/struct_timespec.h
/usr/include/x86_64-linux-gnu/bits/types/struct_timeval.h
/usr/include/x86_64-linux-gnu/bits/types/struct_tm.h
/usr/include/x86_64-linux-gnu/bits/types/time_t.h
/usr/include/x86_64-linux-gnu/bits/types/timer_t.h
/usr/include/x86_64-linux-gnu/bits/types/wint_t.h
/usr/include/x86_64-linux-gnu/bits/types.h
/usr/include/x86_64-linux-gnu/bits/typesizes.h
/usr/include/x86_64-linux-gnu/bits/uintn-identity.h
/usr/include/x86_64-linux-gnu/bits/uio-ext.h
/usr/include/x86_64-linux-gnu/bits/uio_lim.h
/usr/include/x86_64-linux-gnu/bits/unistd.h
/usr/include/x86_64-linux-gnu/bits/unistd_ext.h
/usr/include/x86_64-linux-gnu/bits/utmp.h
/usr/include/x86_64-linux-gnu/bits/utmpx.h
/usr/include/x86_64-linux-gnu/bits/utsname.h
/usr/include/x86_64-linux-gnu/bits/waitflags.h
/usr/include/x86_64-linux-gnu/bits/waitstatus.h
/usr/include/x86_64-linux-gnu/bits/wchar-ldbl.h
/usr/include/x86_64-linux-gnu/bits/wchar.h
/usr/include/x86_64-linux-gnu/bits/wchar2.h
/usr/include/x86_64-linux-gnu/bits/wctype-wchar.h
/usr/include/x86_64-linux-gnu/bits/wordsize.h
/usr/include/x86_64-linux-gnu/bits/xopen_lim.h
/usr/include/x86_64-linux-gnu/fpu_control.h
/usr/include/x86_64-linux-gnu/gnu
/usr/include/x86_64-linux-gnu/gnu/lib-names-64.h
/usr/include/x86_64-linux-gnu/gnu/lib-names.h
/usr/include/x86_64-linux-gnu/gnu/libc-version.h
/usr/include/x86_64-linux-gnu/gnu/stubs-64.h
/usr/include/x86_64-linux-gnu/gnu/stubs.h
/usr/include/x86_64-linux-gnu/ieee754.h
/usr/include/x86_64-linux-gnu/sys
/usr/include/x86_64-linux-gnu/sys/acct.h
/usr/include/x86_64-linux-gnu/sys/auxv.h
/usr/include/x86_64-linux-gnu/sys/bitypes.h
/usr/include/x86_64-linux-gnu/sys/cdefs.h
/usr/include/x86_64-linux-gnu/sys/debugreg.h
/usr/include/x86_64-linux-gnu/sys/dir.h
/usr/include/x86_64-linux-gnu/sys/elf.h
/usr/include/x86_64-linux-gnu/sys/epoll.h
/usr/include/x86_64-linux-gnu/sys/errno.h
/usr/include/x86_64-linux-gnu/sys/eventfd.h
/usr/include/x86_64-linux-gnu/sys/fanotify.h
/usr/include/x86_64-linux-gnu/sys/fcntl.h
/usr/include/x86_64-linux-gnu/sys/file.h
/usr/include/x86_64-linux-gnu/sys/fsuid.h
/usr/include/x86_64-linux-gnu/sys/gmon.h
/usr/include/x86_64-linux-gnu/sys/gmon_out.h
/usr/include/x86_64-linux-gnu/sys/inotify.h
/usr/include/x86_64-linux-gnu/sys/io.h
/usr/include/x86_64-linux-gnu/sys/ioctl.h
/usr/include/x86_64-linux-gnu/sys/ipc.h
/usr/include/x86_64-linux-gnu/sys/kd.h
/usr/include/x86_64-linux-gnu/sys/klog.h
/usr/include/x86_64-linux-gnu/sys/mman.h
/usr/include/x86_64-linux-gnu/sys/mount.h
/usr/include/x86_64-linux-gnu/sys/msg.h
/usr/include/x86_64-linux-gnu/sys/mtio.h
/usr/include/x86_64-linux-gnu/sys/param.h
/usr/include/x86_64-linux-gnu/sys/pci.h
/usr/include/x86_64-linux-gnu/sys/perm.h
/usr/include/x86_64-linux-gnu/sys/personality.h
/usr/include/x86_64-linux-gnu/sys/platform
/usr/include/x86_64-linux-gnu/sys/platform/x86.h
/usr/include/x86_64-linux-gnu/sys/poll.h
/usr/include/x86_64-linux-gnu/sys/prctl.h
/usr/include/x86_64-linux-gnu/sys/procfs.h
/usr/include/x86_64-linux-gnu/sys/profil.h
/usr/include/x86_64-linux-gnu/sys/ptrace.h
/usr/include/x86_64-linux-gnu/sys/queue.h
/usr/include/x86_64-linux-gnu/sys/quota.h
/usr/include/x86_64-linux-gnu/sys/random.h
/usr/include/x86_64-linux-gnu/sys/raw.h
/usr/include/x86_64-linux-gnu/sys/reboot.h
/usr/include/x86_64-linux-gnu/sys/reg.h
/usr/include/x86_64-linux-gnu/sys/resource.h
/usr/include/x86_64-linux-gnu/sys/rseq.h
/usr/include/x86_64-linux-gnu/sys/select.h
/usr/include/x86_64-linux-gnu/sys/sem.h
/usr/include/x86_64-linux-gnu/sys/sendfile.h
/usr/include/x86_64-linux-gnu/sys/shm.h
/usr/include/x86_64-linux-gnu/sys/signal.h
/usr/include/x86_64-linux-gnu/sys/signalfd.h
/usr/include/x86_64-linux-gnu/sys/single_threaded.h
/usr/include/x86_64-linux-gnu/sys/socket.h
/usr/include/x86_64-linux-gnu/sys/socketvar.h
/usr/include/x86_64-linux-gnu/sys/soundcard.h
/usr/include/x86_64-linux-gnu/sys/stat.h
/usr/include/x86_64-linux-gnu/sys/statfs.h
/usr/include/x86_64-linux-gnu/sys/statvfs.h
/usr/include/x86_64-linux-gnu/sys/swap.h
/usr/include/x86_64-linux-gnu/sys/syscall.h
/usr/include/x86_64-linux-gnu/sys/sysinfo.h
/usr/include/x86_64-linux-gnu/sys/syslog.h
/usr/include/x86_64-linux-gnu/sys/sysmacros.h
/usr/include/x86_64-linux-gnu/sys/termios.h
/usr/include/x86_64-linux-gnu/sys/time.h
/usr/include/x86_64-linux-gnu/sys/timeb.h
/usr/include/x86_64-linux-gnu/sys/timerfd.h
/usr/include/x86_64-linux-gnu/sys/times.h
/usr/include/x86_64-linux-gnu/sys/timex.h
/usr/include/x86_64-linux-gnu/sys/ttychars.h
/usr/include/x86_64-linux-gnu/sys/ttydefaults.h
/usr/include/x86_64-linux-gnu/sys/types.h
/usr/include/x86_64-linux-gnu/sys/ucontext.h
/usr/include/x86_64-linux-gnu/sys/uio.h
/usr/include/x86_64-linux-gnu/sys/un.h
/usr/include/x86_64-linux-gnu/sys/unistd.h
/usr/include/x86_64-linux-gnu/sys/user.h
/usr/include/x86_64-linux-gnu/sys/utsname.h
/usr/include/x86_64-linux-gnu/sys/vfs.h
/usr/include/x86_64-linux-gnu/sys/vlimit.h
/usr/include/x86_64-linux-gnu/sys/vm86.h
/usr/include/x86_64-linux-gnu/sys/vt.h
/usr/include/x86_64-linux-gnu/sys/wait.h
/usr/include/x86_64-linux-gnu/sys/xattr.h
/usr/lib
/usr/lib/x86_64-linux-gnu
/usr/lib/x86_64-linux-gnu/Mcrt1.o
/usr/lib/x86_64-linux-gnu/Scrt1.o
/usr/lib/x86_64-linux-gnu/crt1.o
/usr/lib/x86_64-linux-gnu/crti.o
/usr/lib/x86_64-linux-gnu/crtn.o
/usr/lib/x86_64-linux-gnu/gcrt1.o
/usr/lib/x86_64-linux-gnu/grcrt1.o
/usr/lib/x86_64-linux-gnu/libBrokenLocale.a
/usr/lib/x86_64-linux-gnu/libanl.a
/usr/lib/x86_64-linux-gnu/libc.a
/usr/lib/x86_64-linux-gnu/libc.so
/usr/lib/x86_64-linux-gnu/libc_nonshared.a
/usr/lib/x86_64-linux-gnu/libdl.a
/usr/lib/x86_64-linux-gnu/libg.a
/usr/lib/x86_64-linux-gnu/libm-2.35.a
/usr/lib/x86_64-linux-gnu/libm.a
/usr/lib/x86_64-linux-gnu/libm.so
/usr/lib/x86_64-linux-gnu/libmcheck.a
/usr/lib/x86_64-linux-gnu/libmvec.a
/usr/lib/x86_64-linux-gnu/libpthread.a
/usr/lib/x86_64-linux-gnu/libresolv.a
/usr/lib/x86_64-linux-gnu/librt.a
/usr/lib/x86_64-linux-gnu/libutil.a
/usr/lib/x86_64-linux-gnu/rcrt1.o
/usr/share
/usr/share/doc
/usr/share/doc/libc6-dev
/usr/share/doc/libc6-dev/copyright
/usr/share/gdb
/usr/share/gdb/auto-load
/usr/share/gdb/auto-load/lib
/usr/share/gdb/auto-load/lib/x86_64-linux-gnu
/usr/share/gdb/auto-load/lib/x86_64-linux-gnu/libpthread-2.35.so-gdb.py
/usr/share/lintian
/usr/share/lintian/overrides
/usr/share/lintian/overrides/libc6-dev
/usr/lib/x86_64-linux-gnu/libBrokenLocale.so
/usr/lib/x86_64-linux-gnu/libanl.so
/usr/lib/x86_64-linux-gnu/libc_malloc_debug.so
/usr/lib/x86_64-linux-gnu/libmvec.so
/usr/lib/x86_64-linux-gnu/libnss_compat.so
/usr/lib/x86_64-linux-gnu/libnss_hesiod.so
/usr/lib/x86_64-linux-gnu/libresolv.so
/usr/lib/x86_64-linux-gnu/libthread_db.so
/usr/share/doc/libc6-dev/changelog.Debian.gz
```

而C/C++编译器版本多于一个，并没有某个编译器占据了绝对统治地位。至少，intel的icc，微软的msvc，gnu的gcc，以及后起之秀clang，都各自有各自的地位，要协调多方意见制作大家认可的标准并不容易，改变起来自然更加耗时。

其实Windows还有一个由RAD Studio附带的bcc编译器，效率也很好

## releases/version/版本
### GNU GCC 15.2
2025-08-08

### GNU GCC 15.1
15.1已于2025年4月25日 10:52:00 GMT发布

### gcc 14.1
GCC 14.1 编译器计划在2024年5月7日左右发布
https://gcc.gnu.org/pipermail/gcc/2024-May/243921.html

### gcc 13.1.0
2023-04-26

### gcc 12.1.0
2022-05-06

### gcc-11.1.0
2021-04-27

### gcc 10.1.0
2020-05-07

https://mirror.linux-ia64.org/gnu/gcc/releases/

gcc-4.6.2/              2015-02-05 17:20
gcc-4.6.3/              2015-02-05 17:21
gcc-4.6.4/              2015-02-05 17:21
gcc-4.7.0/              2015-02-05 17:20
gcc-4.7.1/              2015-02-05 17:18
gcc-4.7.2/              2015-02-05 17:22
gcc-4.7.3/              2015-02-05 17:20
gcc-4.7.4/              2015-02-05 17:18
gcc-4.8.0/              2015-02-05 17:21
gcc-4.8.1/              2015-02-05 17:22
gcc-4.8.2/              2015-02-05 17:22
gcc-4.8.3/              2015-02-05 17:21
gcc-4.8.4/              2015-02-05 17:19
gcc-4.8.5/              2015-06-24 07:14
gcc-4.9.0/              2015-02-05 17:19
gcc-4.9.1/              2015-02-05 17:20
gcc-4.9.2/              2015-02-05 17:22
gcc-4.9.3/              2015-06-26 19:14
gcc-4.9.4/              2016-08-03 06:44
gcc-5.1.0/              2015-04-22 10:44
gcc-5.2.0/              2015-07-16 12:14
gcc-5.3.0/              2015-12-04 13:44
gcc-5.4.0/              2016-06-03 11:14
gcc-5.5.0/              2017-10-10 10:14
gcc-6.1.0/              2016-04-27 10:44
gcc-6.2.0/              2016-08-22 10:44
gcc-6.3.0/              2016-12-21 10:14
gcc-6.4.0/              2017-07-04 10:14
gcc-6.5.0/              2018-10-26 10:44
gcc-7.1.0/              2017-05-02 15:14
gcc-7.2.0/              2017-08-14 08:44
gcc-7.3.0/              2018-01-25 09:14
gcc-7.4.0/              2019-06-06 08:14
gcc-7.5.0/              2019-11-14 08:49
gcc-8.1.0/              2018-05-02 09:26
gcc-8.2.0/              2018-07-26 10:44
gcc-8.3.0/              2019-02-22 15:14
gcc-8.4.0/              2020-03-04 09:14
gcc-8.5.0/              2021-05-14 09:14
gcc-9.1.0/              2019-08-12 08:35
gcc-9.2.0/              2019-08-20 13:14
gcc-9.3.0/              2020-03-12 11:44
gcc-9.4.0/              2021-06-01 08:20
gcc-9.5.0/              2022-05-27 07:49
gcc-10.1.0/             2020-05-07 11:44
gcc-10.2.0/             2020-07-23 07:14
gcc-10.3.0/             2021-04-08 12:44
gcc-10.4.0/             2022-06-28 10:14
gcc-10.5.0/             2023-07-07 07:44
gcc-11.1.0/             2021-04-27 10:44
gcc-11.2.0/             2021-07-28 07:44
gcc-11.3.0/             2022-04-21 08:46
gcc-11.4.0/             2023-05-29 10:11
gcc-11.5.0/             2024-07-19 06:44
gcc-12.1.0/             2022-05-06 08:14
gcc-12.2.0/             2022-08-19 08:44
gcc-12.3.0/             2023-05-08 12:44
gcc-12.4.0/             2024-06-20 08:45
gcc-12.5.0/             2025-07-11 07:14
gcc-13.1.0/             2023-04-26 07:46
gcc-13.2.0/             2023-07-27 09:17
gcc-13.3.0/             2024-05-21 08:53
gcc-13.4.0/             2025-06-05 16:44
gcc-14.1.0/             2024-05-07 08:15
gcc-14.2.0/             2024-08-01 09:14
gcc-14.3.0/             2025-05-23 11:45
gcc-15.1.0/             2025-04-25 09:14
gcc-15.2.0/             2025-08-08 07:44

gcc 4.8编译gcc11不行吧？
g++ (GCC) 4.8.5 20150623 (Red Hat 4.8.5-44)
要在CentOS 7.9上编译GCC 11，您需要确保您的系统上安装了适当的GCC版本。GCC 11要求使用GCC 9或更高版本进行编译。因此，您需要安装GCC 9或更高版本。

编译openjdk 8，需要安装java7

sudo yum update
sudo yum groupinstall "Development Tools"
sudo yum install glibc-devel zlib-devel -y
wget https://mirror.linux-ia64.org/gnu/gcc/releases/gcc-11.4.0/gcc-11.4.0.tar.gz -O gcc-11.4.0.tar.gz 
--no-check-certificate
或者
wget https://ftp.gnu.org/gnu/gcc/gcc-11.4.0/gcc-11.4.0.tar.gz -O gcc-11.4.0.tar.gz --no-check-certificate
tar xzvf gcc-11.4.0.tar.gz

cd gcc-11.4.0

# 下载依赖
./contrib/download_prerequisites

# 配置。可以通过 prefix 参数设置编译完成的 GCC 的安装目录，如果不指定，会安装在 /usr/local下
# 可以配置为当前用户的某个目录
./configure --prefix=/home/wdidada/gcc11 --enable-threads=posix --disable-checking \
    --enable--long-long --with-system-zlib --enable-languages=c,c++ --enable-multilib

# 开始编译
make -j4

# 安装
# 编译产生物会安装到 configure --prefix 指定的目录中，或系统默认目录下
make install

# 修改环境变量
# 可以将下面的配置写到 .bashrc 或 .bash_profile 中，这样每次登录都会自动生效
export PATH=/home/wdidada/gcc11/bin:$PATH
export LD_LIBRARY_PATH=/home/wdidada/gcc11/lib64:$LD_LIBRARY_PATH
export CC=/home/wdidada/gcc11/bin/gcc
export CXX=/home/wdidada/gcc11/bin/g++

gnu compiler collection
可以编译多种语言

## centos
No CMAKE_CXX_COMPILER could be found.

这个错误提示表示在CMake中找不到CMAKE_CXX_COMPILER。要解决这个问题，你需要确保已经安装了C++编译器，并将其添加到系统的环境变量中。

对于Windows系统，你可以安装Visual Studio或MinGW等编译器。对于Linux系统，你可以安装g++或clang++等编译器。

安装完成后，重新运行CMake并指定编译器路径。例如，如果你使用的是g++，可以在CMake命令中添加`-DCMAKE_CXX_COMPILER=/usr/bin/g++`参数。

在 CentOS 7.9 上安装 g++，可以通过以下步骤进行：
1. 首先，更新系统软件包列表：
```
sudo yum update
```
2. 接下来，安装 GCC（GNU Compiler Collection）：
```
sudo yum groupinstall "Development Tools"
```
3. 安装完成后，你可以使用 `g++ --version` 命令来检查 g++ 是否已经成功安装。如果看到版本信息，说明安装成功。
g++ (GCC) 4.8.5 20150623 (Red Hat 4.8.5-44

GCC编译器插件的一个例子是GCC的VCG插件，该插件可以图形化GCC编译过程的内部数据结构，例如控制流图、函数调用图、支配图、Tree结构、Gimple结构、RTX结构、Pass列表等，方便开发人员分析应用程序。
GCC编译器插件还有用于动态安全分析、安全加固的功能，通过修改中间数据的能力，可以不用修改源代码就能添加新功能。这对于安全测试非常有用，可以通过动态插装来实现监控程序执行路径，但需要注意动态插装可能会对程序的运行性能产生影响，降低程序运行效率。
以上信息仅供参考，如有需要，建议咨询专业技术人员。

### gcc vs g++
gcc编译c代码
g++编译c++代码

### gcc代码如何组织
git
cmake

cc1plus
xg++

Killed signal terminated program
云服务器内存不够，导致gcc编译失败
https://www.jianshu.com/p/a4ad05a51456

https://www.zhihu.com/question/20940822

gcc手动安装最新版
更新动态库
#查看当前的动态库
strings /usr/lib64/libstdc++.so.6 | grep CXXABI
rm -f /usr/lib64/libstdc++.so.6
ln -s /usr/local/lib64/libstdc++.so.6.0.29 /usr/lib64/libstdc++.so.6
#查看更新后的动态库
strings /usr/lib64/libstdc++.so.6 | grep CXXABI

## 安装后的动态库会位于/usr/local/lib64目录下，
#其他版本在该目录下寻找对应的动态库libstdc++.so.6.X.XX

https://blog.csdn.net/qq_41054313/article/details/119453611

configure: error: Building GCC requires GMP 4.2+, MPFR 2.4.0+ and MPC 0.8.0+.
需要依赖 mpc，mpfr，gmp包，
GCC 源码里自带脚本可以轻松下载依赖包。
./contrib/download_prerequisites

以上软件各版本源码在https://ftp.gnu.org/gnu/链接中可下载

https://muzing.top/posts/16a16b69/

Redis里面有ruby脚本

gcc各版本历史
http://ftp.gnu.org/gnu/gcc/

libstdc++.so.6 'GLIBCXX 3.4.21'not found的问题
https://www.cnblogs.com/stelliformzm/p/12805826.html

http://ftp.tsukuba.wide.ad.jp/software/gcc/releases/　
tar -xvf gcc-5.4.0.tar.bz2
cd gcc-5.4.0
./contrib/download_prerequisits
mkdir build
cd build
../configure --enable-checking=release --enable-languages=c,c++ --disable-multlib
../configure --enable-checking=release --enable-languages=c,c++ --disable-multlib
../configure --enable-checking=release --enable-languages=c,c++ --disable-multlib
configure: error: I suspect your system does not have 32-bit development libraries (libc and headers). If you have them, rerun configure with --enable-multilib. If you do not have them, and want to build a 64-bit-only compiler, rerun configure with --disable-multilib.

安装autoconf和automake
yum -y install gcc automake autoconf libtool make

安装g++:
yum install gcc gcc-c++

yum install glibc-static libstdc++-static -y

sudo apt update
sudo apt install g++ -y

2020年5月7日发布 GCC 10.1.1
clang 12

```shell
yum install gcc-c++
Dependencies Resolved

=========================================================
 Package     Arch       Version           Repository
                                                    Size
=========================================================
Installing:
 gcc-c++     x86_64     4.8.5-44.el7      base     7.2 M
Installing for dependencies:
 cpp         x86_64     4.8.5-44.el7      base     5.9 M
 gcc         x86_64     4.8.5-44.el7      base      16 M

Transaction Summary
=========================================================
Install  1 Package (+2 Dependent packages)

Total download size: 29 M
Installed size: 69 M
Is this ok [y/d/N]:
```

UNIX系统的内核主要由C语言编写
在AIX下进行C编程，最通用的编辑器为vi/vim
选择编译器：常用的是GNU C/C++编译器 GCC (开源的跨平台编译器套件)；XLC(AIX的商业版本编译器)
选择调试器：应用最广泛的调试器是gdb (UNIX下用dbx）
程序维护工具：make是Linux/Unix下常用的程序维护工具
AIX需要首先安装Linux RPM格式支持，才能安装gccRPM for AIX软件包

xlc++ 和 g++
AIX上使用的是xlc++编译器，Linux上使用的是g++编译器。

对C标准中没有严格定义的行为，两个编译器的处理方式不一定相同，代码在两个平台运行会有不一样的表现。导致在一个平台运行正常，另一个平台可能就是bug了。
https://www.bilibili.com/read/cv7849739/

https://blog.csdn.net/tglg/article/details/4041019

https://cbs.centos.org/koji/buildinfo?buildID=31753

sudo yum install centos-release-scl
sudo yum install devtoolset-8

devtoolset-9

```shell
rpm -qa | grep gcc
devtoolset-7-gcc-7.3.1-5.16.el7.x86_64
libgcc-4.8.5-44.el7.i686
gcc-4.8.5-44.el7.x86_64
devtoolset-8-gcc-8.3.1-3.2.el7.x86_64
devtoolset-9-gcc-c++-9.1.1-2.6.el7.x86_64
gcc-gfortran-4.8.5-44.el7.x86_64
devtoolset-9-gcc-gfortran-9.1.1-2.6.el7.x86_64
devtoolset-8-gcc-c++-8.3.1-3.2.el7.x86_64
gcc-c++-4.8.5-44.el7.x86_64
devtoolset-9-gcc-9.1.1-2.6.el7.x86_64
libgcc-4.8.5-44.el7.x86_64
devtoolset-7-gcc-c++-7.3.1-5.16.el7.x86_64
```

[install gcc 8 on centos](https://stackoverflow.com/questions/55345373/how-to-install-gcc-g-8-on-centos)

```c
yum install devtoolset-8-gcc devtoolset-8-gcc-c++
```

腾讯个人云主机

gcc 4.8 8.3 9.1

公司会自建centos repo镜像

--disable-multilib

gcc编译参数

addtion on:gcc-multilib 

如何查看gcc是否支持

multilib是同时生成多个平台的代码，比如：64bit机器，同时可以产生32和64两种格式，不是研究这个的，仅供参考。

是gcc的一个选项

scl enable devtoolset-8 -- bash
source /opt/rh/devtoolset-8/enable

scl enable devtoolset-9 -- bash
source /opt/rh/devtoolset-9/enable

切换bash gcc版本

https://cloud.tencent.com/developer/article/1430839

 默认情况下，GCC/G++链接时优先链接动态库，如果没有动态库，则链接相应的静态库。同时，GCC/G++也提供了链接选项 -Wl,-Bstatic 和 -Wl,-Bdynamic 供用户指定链接动态库或者静态库。

  -Wl,-Bstatic指示跟在后面的-lxxx选项链接的都是静态库，-Wl,-Bdynamic指示跟在后面的-lxxx选项链接的都是动态库。

被依赖的在后面，依赖其他的在前面

[GCC/G++选项 -Wl,-Bstatic和-Wl,-Bdynamic](https://blog.csdn.net/weixin_34257076/article/details/91871190)

https://www.jianshu.com/p/fdd516337c76

c++ 静态库 动态库 未定义的引用

https://www.runoob.com/w3cnote/cpp-static-library-and-dynamic-library.html

http://asrman.blogspot.com/2018/11/cc-so.html

https://gcc.gnu.org/

## centos 7编译安装
编译安装gcc
```shell
sudo yum update
sudo yum groupinstall "Development Tools"
sudo yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
wget https://ftp.gnu.org/gnu/gcc/gcc-11.2.0/gcc-11.2.0.tar.gz
ls -la gcc-11.2.0.tar.gz
tar -zxvf gcc-11.2.0.tar.gz
cd gcc-11.2.0
./contrib/download_prerequisites
./configure --enable-languages=c,c++ --disable-multilib --with-system-zlib --with-system-bzlib --with-system-readline --with-system-sqlite --with-system-ncurses --with-system-libffi --with-plugindir=/usr/lib64/gcc/plugin --with-pkgversion="CentOS 7.9" --with-bugurl="https://bugs.centos.org/taskman" --enable-shared --enable-static --enable-threads=posix --enable-checking=release --enable-optimizations --enable-lto-plugin --enable-libstdcxx-pch --enable-default-pie --enable-default-ssp --enable-libssp --enable-libgomp --enable-libquadmath --enable-libmpx --enable-libunwind --enable-libsanitizer=address,undefined CC=gcc CXX=g++
make all-gcc all-target-libgcc
sudo make install-gcc install-target-libgcc
```

以上 gcc、g++、cpp 都叫做 compiler driver 。这些都不负责编译代码，只负责调用真正的编译器（compiler proper）。gcc 这个项目中，真正负责编译 C 代码的程序叫做 cc1，负责编译 C++ 代码的程序叫做 cc1plus 。
