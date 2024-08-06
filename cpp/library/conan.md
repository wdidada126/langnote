# conan

conan install libmysql报错，需要
brew unlink boost

-DCMAKE_PROJECT_TOP_LEVEL_INCLUDES="conan_provider.cmake" -DCONAN_COMMAND="D:\dev_tools\Conan\conan\conan.exe" -DCMAKE_TOOLCHAIN_FILE="D:\git\github\rest_poco\cmake-build-debug-visual-studio-64\conan\build\Debug\generators\conan_toolchain.cmake"

-DCMAKE_PROJECT_TOP_LEVEL_INCLUDES="conan_provider.cmake" -DCONAN_COMMAND="/usr/local/bin/conan" -DCMAKE_TOOLCHAIN_FILE="~/Develop/git/github/rest_poco/cmake-build-debug/conan/build/Debug/generators/conan_toolchain.cmake"

-DCMAKE_TOOLCHAIN_FILE="D:\git\github\rest_poco\cmake-build-debug\conan\build\Debug\generators\conan_toolchain.cmake"

上面的不一定对，
CMake Error at conan_provider.cmake:247 (message):
CMake-Conan: unable to map MSVC runtime:
$<$<CONFIG:Debug>:MultiThreadedDebugDLL> to Conan settings

cmake --pretest 命令是对的，cLion的话，换一个cmake配置项

而且另外一个讨厌的问题是C++没有包管理器，好不容易有个conan挺好用的大家又不爱用，导致小功能全都自己搓轮子

wdidada@10-23-29-39:~/myqt6app$ sudo conan install -u ./ --build=missing
ERROR: Ambiguous command, both conanfile.py and conanfile.txt exist

https://blog.conan.io/introducing-new-conan-clion-plugin/

## conan设置build type为Debug
conan2
新建或者更改profile

## conan2 python api
https://docs.conan.io/2.0/reference/extensions/python_api.html#reference-python-api

## conan1
SET(CONAN_DISABLE_CHECK_COMPILER true)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

opengl/system: WARN: System requirements: 'libgl-dev' are missing but can't install because tools.system.package_manager:mode is 'check'.Please update packages manually or set 'tools.system.package_manager:mode' to 'install' in the [conf] section of the profile, or in the command line using '-c tools.system.package_manager:mode=install'

/home/codespace/.conan/conan.conf

文档

案例
例子
qt
opencv
Poco
Zlib
Grpc conan的例子

Conan 1.52使用本地缓存来存储下载的库文件和构建的二进制文件。这些缓存文件根据不同的规则进行组织，以便于管理和查找。
在Conan 1.52中，本地缓存的组织方式如下：
分版本：Conan将每个库的每个版本存储在本地缓存中。这样，当你需要构建特定版本的库时，Conan可以在本地缓存中找到对应的版本，避免了重新下载和构建的过程。
分编译器：Conan根据不同的编译器对库进行分类。这意味着，如果你使用不同的编译器构建同一个库，Conan将在本地缓存中为每个编译器保存一个独立的版本。这样可以确保不同编译器之间的兼容性和正确性。
分配置：Conan还根据不同的构建配置对库进行分类。构建配置可以包括不同的优化选项、警告级别等。Conan在本地缓存中为每个配置保存一个独立的版本，以便于进行定制化的构建和测试。
分平台：对于跨平台的库，Conan将根据不同的操作系统和架构对库进行分类。这样可以确保不同平台之间的兼容性和正确性。
在Conan 1.52中，本地缓存的文件结构大致如下：
```bash
conan_cache/
├── packages/
│   ├── <package_name>/
│   │   ├── <version>/
│   │   │   ├── <os>/
│   │   │   │   ├── <arch>/
│   │   │   │   │   ├── <compiler>/
│   │   │   │   │   │   ├── <build_type>/
│   │   │   │   │   │   │   ├── <package_id>.conan
│   │   │   │   │   │   └── <package_id>.info
│   │   │   │   └── <package_id>.conan
│   │   └── <package_id>.info
└── binaries/
    ├── <package_name>/
    │   ├── <version>/
    │   │   ├── <os>/
    │   │   │   ├── <arch>/
    │   │   │   └── <compiler>/
    │   └── <package_id>.info
    └── <package_name>.info
```
上述文件结构中，<package_name>表示库的名称，<version>表示库的版本，<os>表示操作系统，<arch>表示架构，<compiler>表示编译器，<build_type>表示构建类型，<package_id>表示库的唯一标识符。
通过这种方式，Conan可以在本地缓存中快速找到所需的库文件，并确保正确性和一致性。这大大减少了重新下载和构建的时间，提高了开发效率。


conan可以直接使用make gcc，不使用cmake等构件工具吗？

是的，Conan可以用来直接调用gcc或其他编译器进行构建，而不需要使用CMake等构建工具。Conan提供了一种简单的方式来管理依赖关系和构建配置，它能够根据不同的编译器和配置生成相应的构建文件，并在构建过程中进行适当的配置和调整。
Conan的构建脚本可以指定要使用的编译器和其版本，以及相关的编译标志和选项。通过在Conan配置文件中指定这些信息，Conan可以生成适合特定编译器和构建需求的构建文件（例如Makefile或Visual Studio项目文件）。
一旦Conan生成了适合的构建文件，您可以使用常规的构建命令（如make、nmake或msbuild）来执行构建过程。这将直接调用指定的编译器，并根据构建文件的指示进行编译和链接。
因此，使用Conan可以简化构建过程，减少对外部构建工具的依赖，并为您提供更灵活的方式来管理依赖关系和构建配置。

  ```shell
conan graph info  .

======== Computing dependency graph ========
Graph root
    conanfile.txt: /workspaces/myqt6app/conanfile.txt
Requirements
    brotli/1.1.0#d56d7bb9ca722942aba17369cb5c0519 - Cache
    bzip2/1.0.8#457c272f7da34cb9c67456dd217d36c4 - Cache
    freetype/2.13.2#c9ee90dc6f88356febac6fcdba0b2249 - Cache
    libpng/1.6.40#06f726bd4bfd83f5cdc10587826093f0 - Cache
    qt/6.4.1#37219eaac385e2969ded4b47563c71c2 - Cache
    zlib/1.3.1#af8f2ef3d8e0fddf1975281d7fe43bf6 - Cache
Resolved version ranges
    freetype/[>=2.13.2]: freetype/2.13.2
    zlib/[>=1.2.11 <2]: zlib/1.3.1
Graph error
    Version conflict: qt/6.4.1->zlib/1.2.13, None->zlib/1.3.1.

======== Basic graph information ========
conanfile:
  ref: conanfile
  id: 0
  recipe: Consumer
  package_id: None
  prev: None
  build_id: None
  binary: None
  invalid_build: False
  info_invalid: None
  name: None
  user: None
  channel: None
  url: None
  license: None
  author: None
  description: None
  homepage: None
  build_policy: None
  upload_policy: None
  revision_mode: hash
  provides: None
  deprecated: None
  win_bash: None
  win_bash_run: None
  default_options: None
  options_description: None
  version: None
  topics: None
  package_type: unknown
  settings:
    os: Linux
    arch: x86_64
    compiler: gcc
    compiler.cppstd: gnu17
    compiler.libcxx: libstdc++11
    compiler.version: 9
    build_type: Release
  options:
  options_definitions:
  generators: ['CMakeDeps']
  system_requires:
  recipe_folder: None
  source_folder: None
  build_folder: None
  generators_folder: None
  package_folder: None
  cpp_info:
    root:
      includedirs: ['include']
      srcdirs: None
      libdirs: ['lib']
      resdirs: None
      bindirs: ['bin']
      builddirs: None
      frameworkdirs: None
      system_libs: None
      frameworks: None
      libs: None
      defines: None
      cflags: None
      cxxflags: None
      sharedlinkflags: None
      exelinkflags: None
      objects: None
      sysroot: None
      requires: None
      properties: None
  label: conanfile.txt
  dependencies:
    1:
      ref: freetype/2.13.2
      run: False
      libs: True
      skip: False
      test: False
      force: False
      direct: True
      build: False
      transitive_headers: None
      transitive_libs: None
      headers: True
      package_id_mode: None
      visible: True
    2:
      ref: libpng/1.6.40
      run: False
      libs: True
      skip: False
      test: False
      force: False
      direct: False
      build: False
      transitive_headers: None
      transitive_libs: None
      headers: False
      package_id_mode: None
      visible: True
    3:
      ref: zlib/1.3.1
      run: False
      libs: True
      skip: False
      test: False
      force: False
      direct: False
      build: False
      transitive_headers: None
      transitive_libs: None
      headers: False
      package_id_mode: None
      visible: True
    4:
      ref: bzip2/1.0.8
      run: False
      libs: True
      skip: False
      test: False
      force: False
      direct: False
      build: False
      transitive_headers: None
      transitive_libs: None
      headers: False
      package_id_mode: None
      visible: True
    5:
      ref: brotli/1.1.0
      run: False
      libs: True
      skip: False
      test: False
      force: False
      direct: True
      build: False
      transitive_headers: None
      transitive_libs: None
      headers: True
      package_id_mode: None
      visible: True
    6:
      ref: qt/6.4.1
      run: False
      libs: True
      skip: False
      test: False
      force: False
      direct: True
      build: False
      transitive_headers: None
      transitive_libs: None
      headers: True
      package_id_mode: None
      visible: True
  context: host
  test: False
freetype/2.13.2#c9ee90dc6f88356febac6fcdba0b2249:
  ref: freetype/2.13.2#c9ee90dc6f88356febac6fcdba0b2249
  id: 1
  recipe: Cache
  package_id: None
  prev: None
  build_id: None
  binary: None
  invalid_build: False
  info_invalid: None
  name: freetype
  user: None
  channel: None
  url: https://github.com/conan-io/conan-center-index
  license: FTL
  author: None
  description: FreeType is a freely available software library to render fonts.
  homepage: https://www.freetype.org
  build_policy: None
  upload_policy: None
  revision_mode: hash
  provides: None
  deprecated: None
  win_bash: None
  win_bash_run: None
  default_options:
    shared: False
    fPIC: True
    with_png: True
    with_zlib: True
    with_bzip2: True
    with_brotli: True
    subpixel: False
  options_description: None
  version: 2.13.2
  topics: ['freetype', 'fonts']
  package_type: static-library
  settings:
    os: Linux
    arch: x86_64
    compiler: gcc
    compiler.version: 9
    build_type: Release
  options:
    fPIC: True
    shared: False
    subpixel: False
    with_brotli: True
    with_bzip2: True
    with_png: True
    with_zlib: True
  options_definitions:
    shared: ['True', 'False']
    fPIC: ['True', 'False']
    with_png: ['True', 'False']
    with_zlib: ['True', 'False']
    with_bzip2: ['True', 'False']
    with_brotli: ['True', 'False']
    subpixel: ['True', 'False']
  generators: []
  system_requires:
  recipe_folder: /home/codespace/.conan2/p/freetdf27971e4a016/e
  source_folder: None
  build_folder: None
  generators_folder: None
  package_folder: None
  cpp_info:
    root:
      includedirs: ['include']
      srcdirs: None
      libdirs: ['lib']
      resdirs: None
      bindirs: ['bin']
      builddirs: None
      frameworkdirs: None
      system_libs: None
      frameworks: None
      libs: None
      defines: None
      cflags: None
      cxxflags: None
      sharedlinkflags: None
      exelinkflags: None
      objects: None
      sysroot: None
      requires: None
      properties: None
  label: freetype/2.13.2
  dependencies:
    2:
      ref: libpng/1.6.40
      run: False
      libs: True
      skip: False
      test: False
      force: False
      direct: True
      build: False
      transitive_headers: None
      transitive_libs: None
      headers: True
      package_id_mode: None
      visible: True
    3:
      ref: zlib/1.3.1
      run: False
      libs: True
      skip: False
      test: False
      force: False
      direct: True
      build: False
      transitive_headers: None
      transitive_libs: None
      headers: True
      package_id_mode: None
      visible: True
    4:
      ref: bzip2/1.0.8
      run: False
      libs: True
      skip: False
      test: False
      force: False
      direct: True
      build: False
      transitive_headers: None
      transitive_libs: None
      headers: True
      package_id_mode: None
      visible: True
    5:
      ref: brotli/1.1.0
      run: False
      libs: True
      skip: False
      test: False
      force: False
      direct: True
      build: False
      transitive_headers: None
      transitive_libs: None
      headers: True
      package_id_mode: None
      visible: True
  context: host
  test: False
libpng/1.6.40#06f726bd4bfd83f5cdc10587826093f0:
  ref: libpng/1.6.40#06f726bd4bfd83f5cdc10587826093f0
  id: 2
  recipe: Cache
  package_id: None
  prev: None
  build_id: None
  binary: None
  invalid_build: False
  info_invalid: None
  name: libpng
  user: None
  channel: None
  url: https://github.com/conan-io/conan-center-index
  license: libpng-2.0
  author: None
  description: libpng is the official PNG file format reference library.
  homepage: http://www.libpng.org
  build_policy: None
  upload_policy: None
  revision_mode: hash
  provides: None
  deprecated: None
  win_bash: None
  win_bash_run: None
  default_options:
    shared: False
    fPIC: True
    neon: True
    msa: True
    sse: True
    vsx: True
    api_prefix: 
  options_description: None
  version: 1.6.40
  topics: ['png', 'graphics', 'image']
  package_type: static-library
  settings:
    os: Linux
    arch: x86_64
    compiler: gcc
    compiler.version: 9
    build_type: Release
  options:
    api_prefix: 
    fPIC: True
    shared: False
    sse: True
  options_definitions:
    shared: ['True', 'False']
    fPIC: ['True', 'False']
    sse: ['True', 'False']
    api_prefix: ['ANY']
  generators: []
  system_requires:
  recipe_folder: /home/codespace/.conan2/p/libpncf17c2d1c5008/e
  source_folder: None
  build_folder: None
  generators_folder: None
  package_folder: None
  cpp_info:
    root:
      includedirs: ['include']
      srcdirs: None
      libdirs: ['lib']
      resdirs: None
      bindirs: ['bin']
      builddirs: None
      frameworkdirs: None
      system_libs: None
      frameworks: None
      libs: None
      defines: None
      cflags: None
      cxxflags: None
      sharedlinkflags: None
      exelinkflags: None
      objects: None
      sysroot: None
      requires: None
      properties: None
  label: libpng/1.6.40
  dependencies:
    3:
      ref: zlib/1.3.1
      run: False
      libs: True
      skip: False
      test: False
      force: False
      direct: True
      build: False
      transitive_headers: None
      transitive_libs: None
      headers: True
      package_id_mode: None
      visible: True
  context: host
  test: False
zlib/1.3.1#af8f2ef3d8e0fddf1975281d7fe43bf6:
  ref: zlib/1.3.1#af8f2ef3d8e0fddf1975281d7fe43bf6
  id: 3
  recipe: Cache
  package_id: None
  prev: None
  build_id: None
  binary: None
  invalid_build: False
  info_invalid: None
  name: zlib
  user: None
  channel: None
  url: https://github.com/conan-io/conan-center-index
  license: Zlib
  author: None
  description: A Massively Spiffy Yet Delicately Unobtrusive Compression Library (Also Free, Not to Mention Unencumbered by Patents)
  homepage: https://zlib.net
  build_policy: None
  upload_policy: None
  revision_mode: hash
  provides: None
  deprecated: None
  win_bash: None
  win_bash_run: None
  default_options:
    shared: False
    fPIC: True
  options_description: None
  version: 1.3.1
  topics: ['zlib', 'compression']
  package_type: static-library
  settings:
    os: Linux
    arch: x86_64
    compiler: gcc
    compiler.version: 9
    build_type: Release
  options:
    fPIC: True
    shared: False
  options_definitions:
    shared: ['True', 'False']
    fPIC: ['True', 'False']
  generators: []
  system_requires:
  recipe_folder: /home/codespace/.conan2/p/zlib7bf0f3bfff70f/e
  source_folder: None
  build_folder: None
  generators_folder: None
  package_folder: None
  cpp_info:
    root:
      includedirs: ['include']
      srcdirs: None
      libdirs: ['lib']
      resdirs: None
      bindirs: ['bin']
      builddirs: None
      frameworkdirs: None
      system_libs: None
      frameworks: None
      libs: None
      defines: None
      cflags: None
      cxxflags: None
      sharedlinkflags: None
      exelinkflags: None
      objects: None
      sysroot: None
      requires: None
      properties: None
  label: zlib/1.3.1
  dependencies:
  context: host
  test: False
bzip2/1.0.8#457c272f7da34cb9c67456dd217d36c4:
  ref: bzip2/1.0.8#457c272f7da34cb9c67456dd217d36c4
  id: 4
  recipe: Cache
  package_id: None
  prev: None
  build_id: None
  binary: None
  invalid_build: False
  info_invalid: None
  name: bzip2
  user: None
  channel: None
  url: https://github.com/conan-io/conan-center-index
  license: bzip2-1.0.8
  author: None
  description: bzip2 is a free and open-source file compression program that uses the Burrows Wheeler algorithm.
  homepage: https://sourceware.org/bzip2
  build_policy: None
  upload_policy: None
  revision_mode: hash
  provides: None
  deprecated: None
  win_bash: None
  win_bash_run: None
  default_options:
    shared: False
    fPIC: True
    build_executable: True
  options_description: None
  version: 1.0.8
  topics: ['data-compressor', 'file-compression']
  package_type: static-library
  settings:
    os: Linux
    arch: x86_64
    compiler: gcc
    compiler.version: 9
    build_type: Release
  options:
    build_executable: True
    fPIC: True
    shared: False
  options_definitions:
    shared: ['True', 'False']
    fPIC: ['True', 'False']
    build_executable: ['True', 'False']
  generators: []
  system_requires:
  recipe_folder: /home/codespace/.conan2/p/bzip232e122e5f0e0b/e
  source_folder: None
  build_folder: None
  generators_folder: None
  package_folder: None
  cpp_info:
    root:
      includedirs: ['include']
      srcdirs: None
      libdirs: ['lib']
      resdirs: None
      bindirs: ['bin']
      builddirs: None
      frameworkdirs: None
      system_libs: None
      frameworks: None
      libs: None
      defines: None
      cflags: None
      cxxflags: None
      sharedlinkflags: None
      exelinkflags: None
      objects: None
      sysroot: None
      requires: None
      properties: None
  label: bzip2/1.0.8
  dependencies:
  context: host
  test: False
brotli/1.1.0#d56d7bb9ca722942aba17369cb5c0519:
  ref: brotli/1.1.0#d56d7bb9ca722942aba17369cb5c0519
  id: 5
  recipe: Cache
  package_id: None
  prev: None
  build_id: None
  binary: None
  invalid_build: False
  info_invalid: None
  name: brotli
  user: None
  channel: None
  url: https://github.com/conan-io/conan-center-index
  license: ['MIT']
  author: None
  description: Brotli compression format
  homepage: https://github.com/google/brotli
  build_policy: None
  upload_policy: None
  revision_mode: hash
  provides: None
  deprecated: None
  win_bash: None
  win_bash_run: None
  default_options:
    shared: False
    fPIC: True
    target_bits: None
    endianness: None
    enable_portable: False
    enable_rbit: True
    enable_debug: False
    enable_log: False
  options_description: None
  version: 1.1.0
  topics: ['brotli', 'compression']
  package_type: static-library
  settings:
    os: Linux
    arch: x86_64
    compiler: gcc
    compiler.version: 9
    build_type: Release
  options:
    enable_debug: False
    enable_log: False
    enable_portable: False
    enable_rbit: True
    endianness: None
    fPIC: True
    shared: False
    target_bits: None
  options_definitions:
    shared: ['True', 'False']
    fPIC: ['True', 'False']
    target_bits: ['64', '32', None]
    endianness: ['big', 'little', 'neutral', None]
    enable_portable: ['True', 'False']
    enable_rbit: ['True', 'False']
    enable_debug: ['True', 'False']
    enable_log: ['True', 'False']
  generators: []
  system_requires:
  recipe_folder: /home/codespace/.conan2/p/brotl01cfbaf421d56/e
  source_folder: None
  build_folder: None
  generators_folder: None
  package_folder: None
  cpp_info:
    root:
      includedirs: ['include']
      srcdirs: None
      libdirs: ['lib']
      resdirs: None
      bindirs: ['bin']
      builddirs: None
      frameworkdirs: None
      system_libs: None
      frameworks: None
      libs: None
      defines: None
      cflags: None
      cxxflags: None
      sharedlinkflags: None
      exelinkflags: None
      objects: None
      sysroot: None
      requires: None
      properties: None
  label: brotli/1.1.0
  dependencies:
  context: host
  test: False
qt/6.4.1#37219eaac385e2969ded4b47563c71c2:
  ref: qt/6.4.1#37219eaac385e2969ded4b47563c71c2
  id: 6
  recipe: Cache
  package_id: None
  prev: None
  build_id: None
  binary: None
  invalid_build: False
  info_invalid: None
  name: qt
  user: None
  channel: None
  url: https://github.com/conan-io/conan-center-index
  license: LGPL-3.0-only
  author: None
  description: Qt is a cross-platform framework for graphical user interfaces.
  homepage: https://www.qt.io
  build_policy: None
  upload_policy: None
  revision_mode: hash
  provides: None
  deprecated: None
  win_bash: None
  win_bash_run: None
  default_options:
    shared: False
    opengl: desktop
    with_vulkan: False
    openssl: True
    with_pcre2: True
    with_glib: False
    with_doubleconversion: True
    with_freetype: True
    with_fontconfig: True
    with_icu: True
    with_harfbuzz: True
    with_libjpeg: False
    with_libpng: True
    with_sqlite3: True
    with_mysql: False
    with_pq: True
    with_odbc: True
    with_zstd: False
    with_brotli: True
    with_dbus: False
    with_libalsa: False
    with_openal: True
    with_gstreamer: False
    with_pulseaudio: False
    with_gssapi: False
    with_md4c: True
    with_x11: True
    gui: True
    widgets: True
    device: None
    cross_compile: None
    sysroot: None
    multiconfiguration: False
    disabled_features: 
    qtsvg: False
    qtdeclarative: False
    qttools: False
    qttranslations: False
    qtdoc: False
    qtwayland: False
    qtquickcontrols2: False
    qtquicktimeline: False
    qtquick3d: False
    qtshadertools: False
    qt5compat: False
    qtactiveqt: False
    qtcharts: False
    qtdatavis3d: False
    qtlottie: False
    qtscxml: False
    qtvirtualkeyboard: False
    qt3d: False
    qtimageformats: False
    qtnetworkauth: False
    qtcoap: False
    qtmqtt: False
    qtopcua: False
    qtmultimedia: False
    qtlocation: False
    qtsensors: False
    qtconnectivity: False
    qtserialbus: False
    qtserialport: False
    qtwebsockets: False
    qtwebchannel: False
    qtwebengine: False
    qtwebview: False
    qtremoteobjects: False
    qtpositioning: False
    qtlanguageserver: False
    qtspeech: False
    qthttpserver: False
    qtquick3dphysics: False
    qtgrpc: False
    qtquickeffectmaker: False
  options_description: None
  version: 6.4.1
  topics: ['framework', 'ui']
  package_type: static-library
  settings:
    os: Linux
    arch: x86_64
    compiler: gcc
    compiler.cppstd: gnu17
    compiler.libcxx: libstdc++11
    compiler.version: 9
    build_type: Release
  options:
    cross_compile: None
    device: None
    disabled_features: 
    gui: True
    multiconfiguration: False
    opengl: desktop
    openssl: True
    qt3d: False
    qt5compat: False
    qtactiveqt: False
    qtcharts: False
    qtcoap: False
    qtconnectivity: False
    qtdatavis3d: False
    qtdeclarative: False
    qtdoc: False
    qthttpserver: False
    qtimageformats: False
    qtlanguageserver: False
    qtlottie: False
    qtmqtt: False
    qtmultimedia: False
    qtnetworkauth: False
    qtopcua: False
    qtpositioning: False
    qtquick3d: False
    qtquick3dphysics: False
    qtquicktimeline: False
    qtremoteobjects: False
    qtscxml: False
    qtsensors: False
    qtserialbus: False
    qtserialport: False
    qtshadertools: False
    qtspeech: False
    qtsvg: False
    qttools: False
    qttranslations: False
    qtvirtualkeyboard: False
    qtwayland: False
    qtwebchannel: False
    qtwebengine: False
    qtwebsockets: False
    qtwebview: False
    shared: False
    sysroot: None
    widgets: True
    with_brotli: True
    with_dbus: False
    with_doubleconversion: True
    with_fontconfig: True
    with_freetype: True
    with_glib: False
    with_gssapi: False
    with_harfbuzz: True
    with_icu: True
    with_libjpeg: False
    with_libpng: True
    with_md4c: True
    with_mysql: False
    with_odbc: True
    with_pcre2: True
    with_pq: True
    with_sqlite3: True
    with_vulkan: False
    with_x11: True
    with_zstd: False
  options_definitions:
    shared: ['True', 'False']
    opengl: ['no', 'desktop', 'dynamic']
    with_vulkan: ['True', 'False']
    openssl: ['True', 'False']
    with_pcre2: ['True', 'False']
    with_glib: ['True', 'False']
    with_doubleconversion: ['True', 'False']
    with_freetype: ['True', 'False']
    with_fontconfig: ['True', 'False']
    with_icu: ['True', 'False']
    with_harfbuzz: ['True', 'False']
    with_libjpeg: ['libjpeg', 'libjpeg-turbo', 'False']
    with_libpng: ['True', 'False']
    with_sqlite3: ['True', 'False']
    with_mysql: ['True', 'False']
    with_pq: ['True', 'False']
    with_odbc: ['True', 'False']
    with_zstd: ['True', 'False']
    with_brotli: ['True', 'False']
    with_dbus: ['True', 'False']
    with_gssapi: ['True', 'False']
    with_md4c: ['True', 'False']
    with_x11: ['True', 'False']
    gui: ['True', 'False']
    widgets: ['True', 'False']
    device: [None, 'ANY']
    cross_compile: [None, 'ANY']
    sysroot: [None, 'ANY']
    multiconfiguration: ['True', 'False']
    disabled_features: [None, 'ANY']
    qtsvg: ['True', 'False']
    qtdeclarative: ['True', 'False']
    qttools: ['True', 'False']
    qttranslations: ['True', 'False']
    qtdoc: ['True', 'False']
    qtwayland: ['True', 'False']
    qtquicktimeline: ['True', 'False']
    qtquick3d: ['True', 'False']
    qtshadertools: ['True', 'False']
    qt5compat: ['True', 'False']
    qtactiveqt: ['True', 'False']
    qtcharts: ['True', 'False']
    qtdatavis3d: ['True', 'False']
    qtlottie: ['True', 'False']
    qtscxml: ['True', 'False']
    qtvirtualkeyboard: ['True', 'False']
    qt3d: ['True', 'False']
    qtimageformats: ['True', 'False']
    qtnetworkauth: ['True', 'False']
    qtcoap: ['True', 'False']
    qtmqtt: ['True', 'False']
    qtopcua: ['True', 'False']
    qtmultimedia: ['True', 'False']
    qtsensors: ['True', 'False']
    qtconnectivity: ['True', 'False']
    qtserialbus: ['True', 'False']
    qtserialport: ['True', 'False']
    qtwebsockets: ['True', 'False']
    qtwebchannel: ['True', 'False']
    qtwebengine: ['True', 'False']
    qtwebview: ['True', 'False']
    qtremoteobjects: ['True', 'False']
    qtpositioning: ['True', 'False']
    qtlanguageserver: ['True', 'False']
    qtspeech: ['True', 'False']
    qthttpserver: ['True', 'False']
    qtquick3dphysics: ['True', 'False']
  generators: []
  system_requires:
  recipe_folder: /home/codespace/.conan2/p/qtc38dc2f86b9ea/e
  source_folder: None
  build_folder: None
  generators_folder: None
  package_folder: None
  cpp_info:
    root:
      includedirs: ['include']
      srcdirs: None
      libdirs: ['lib']
      resdirs: None
      bindirs: ['bin']
      builddirs: None
      frameworkdirs: None
      system_libs: None
      frameworks: None
      libs: None
      defines: None
      cflags: None
      cxxflags: None
      sharedlinkflags: None
      exelinkflags: None
      objects: None
      sysroot: None
      requires: None
      properties: None
  label: qt/6.4.1
  dependencies:
  context: host
  test: False

  ```

Conan是C/C++的包管理器，用于构建和管理C/C++的软件包。Conan flow是Conan的自动化构建和部署工具，用于自动化构建、测试、发布和部署C/C++的软件包。它可以帮助开发人员快速构建和发布软件包，并确保软件包的质量和稳定性。


在Conan中，-s 参数用于指定构建系统的配置。例如，您可以使用以下命令指定要使用的编译器：
```bash
conan create -s "compiler.version=14"
```
在这里，compiler.version=14 指定了要使用的编译器版本为14。您可以使用其他配置选项来指定构建系统的其他方面，例如平台、工具链等。
-t 参数用于指定要使用的测试套件。例如，您可以使用以下命令指定要使用的测试套件：
```bash
conan create -t my_test_suite
```
在这里，my_test_suite 是要使用的测试套件的名称。您可以根据需要选择适合您项目的测试套件。
所以，conan create -s -t 命令将使用指定的构建系统配置和测试套件来创建软件包。

Conan的source函数用于源代码的拉取和准备，例如对源码进行一些修改。这是Conan构建流程的一部分，确保源代码是正确的版本，并且已经准备好进行构建。

conan需要c标准库 cpp标准库 nasm库

查看它的包描述。
$ conan inspect poco/1.9.4
 conan profile new default --detect  # Generates default profile detecting > GCC and sets old ABI
$ conan profile update settings.compiler.libcxx=libstdc++11 default  # Sets libcxx to C++11 ABI

如果特定配置的二进制包不存在conan将会抛出一个错误。
使用conan install .. --build=missing来从源码构建你需要的二进制包，当然这需要你要的二进制配置被包的说明文件所支持。

https://ccup.github.io/conan-docs-zh/05-creating-packages.html

## conan generators

https://docs.conan.io/en/latest/reference/generators.html#generators-reference


conan new会在当前文件夹下生成conanfile.py
如果开发人员要作为生产者角色(producer),把自己的项目也封装成conan包上传到conan服务器供第三方使用，conanfile.txt是不能满足要求的，必须使用全能的confile.py脚本来定义包的配置,事实上conan在分发包时就是基于python脚本的灵活性通过conanfile.py来定义包的全部配置的。所以当我们执行conan new命令创建一个新的conan配置时，自动生成的是conanfile.py脚本。
https://docs.conan.io/1/reference/conanfile.html

Options
我们看到在执行conan install的时候可以指定配置。例如conan install .. -s build_type=Debug。这里指定的一般都是客户机器上的项目级别的配置，一般没法在包配置中指定默认值。例如，在包配置中指定使用“Visual Studio”作为默认编译期就不合理，因为类似这些配置最好由最终用户指定，否则对于在linux工作上的用户就不友好。

但是包配置中的[options]最好用于指定包普遍适用的配置，以及指定默认值。例如一个包可以指定默认为静态链接，这样用户一般情况就不用再指定了。

可以使用类似conan get poco/1.9.4@的命令查看指定包的的options。也可以通过conan inspect命令，如下：

$ conan inspect poco/1.9.4@ -a=options
$ conan inspect poco/1.9.4@ -a=default_options

## conan profiles
https://ccup.github.io/conan-docs-zh/04-using-package.html#%E4%BD%BF%E7%94%A8profiles

https://docs.conan.io/1/reference/profiles.html


cat .conan2/profiles/default
[settings]
arch=x86_64
build_type=Release
compiler=gcc
compiler.cppstd=gnu14
compiler.libcxx=libstdc++11
compiler.version=9
os=Linux

`libstdc++` 是 GNU C++ 标准库的实现，它提供了 C++ 标准库的各种功能和特性。而 `libstdc++11`、`libstdc++14`、`libstdc++17` 是 `libstdc++` 的不同版本，它们对应于不同的 C++ 标准。
下面是它们之间的区别：
1. `libstdc++11`：这是对应 C++11 标准的 `libstdc++` 版本。C++11 是 C++ 标准的一个重要版本，引入了许多新的语言功能和库特性，如 lambda 表达式、右值引用、线程支持等。`libstdc++11` 包含了 C++11 标准库的实现。
2. `libstdc++14`：这是对应 C++14 标准的 `libstdc++` 版本。C++14 是 C++ 标准的下一个版本，对 C++11 进行了一些扩展和改进。它添加了一些新功能，如二进制字面量、泛型 lambda 表达式、`constexpr` 函数的放宽要求等。`libstdc++14` 包含了 C++14 标准库的实现。
3. `libstdc++17`：这是对应 C++17 标准的 `libstdc++` 版本。C++17 是 C++ 标准的下一个版本，引入了一系列新功能和改进，如结构化绑定、`if constexpr`、折叠表达式等。`libstdc++17` 包含了 C++17 标准库的实现。
每个版本的 `libstdc++` 实现了相应版本的 C++ 标准，并提供了相应的功能和特性。因此，选择使用哪个版本取决于您的项目需求和目标平台的支持情况。通常情况下，您应该选择与您的编译器和目标平台兼容的版本。

需要注意的是，不同的编译器可能具有不同的命名约定和默认版本。因此，确保在编译代码时正确配置编译器选项，以便使用所需的 `libstdc++` 版本。
ERROR: Invalid setting 'libstdc++17' is not a valid 'settings.compiler.libcxx' value.
Possible values are ['libstdc++', 'libstdc++11']

conan 需要python文件去定义
xmake 需要lua文件去定义

## template
templates: basic,
cmake_lib, cmake_exe, meson_lib, meson_exe,
msbuild_lib, msbuild_exe, bazel_lib, bazel_exe,
autotools_lib, autotools_exe. E.g. 'conan new
cmake_lib -d name=hello -d version=0.1'. You can
define your own templates too by inputting an absolute
path as your template, or a path relative to your
conan home folder.
## 安装特定版本的conan
pip3 install conan==1.62.0
pip3 install --user conan==2.0.6
pip3 install conan==2.0.6
conan server
virtual = local + remote
local仅仅是本地的
remote是远程的
这个跟maven不一样
https://blog.51cto.com/u_15926338/5979962

https://github.com/conan-io/conan

Decentralized, open-source (MIT), C/C++ package manager.

Homepage: https://conan.io/
Github: https://github.com/conan-io/conan
Docs: https://docs.conan.io
Slack: https://cpplang.slack.com (#conan channel. Please, click here to get an invitation)
Twitter: https://twitter.com/conan_io

https://conan.io/center

Conan是一款免费开源的C/C++语言的依赖项和包管理器，适用于所有平台，包括Windows、Linux、OSX、FreeBSD、Solaris等。它集成了所有构建系统，例如：CMake、Visual Studio（MSBuild）、Makefiles、SCons等。

## conan server

JFrog Artifactory Community Edition

bintray.com/conan是一个用于存储和分发C/C++语言依赖项和包的在线平台，它由Bincrafters团队维护并开放给OSS社区使用。你可以把它想象为一个仓库，这里包含了大量由贡献者创建的各种各样的Conan包。
Conan本身是一款免费开源的依赖项和包管理器，适用于所有平台，包括Windows，Linux，OSX，FreeBSD，Solaris等。它使用起来非常灵活，可以应用于各种开发目标，包括嵌入式、移动（iOS，Android）和裸机。此外，它还与所有build系统集成，如CMake，Visual Studio（MSBuild），Makefiles，SCons等，以及其他专有系统。
在分布式的架构中，Conan遵循客户端-服务器模式。在这种模式下，客户端可以从不同的远端服务器上获取或上传包。服务端主要负责包的存储，并不负责包的构建和生成。实际上，包的构建和生成都在客户端完成。

JFrog，现更名为捷蛙科技（北京）有限公司，是一家全球领先的软件分发和管理解决方案提供商。公司成立十多年以来，在全球拥有成千上万的客户和数百万用户，已成为DevOps数据库与版本和更新管理领域不可忽视的标准。

其主要产品包括JFrog Artifactory企业制品库和JFrog Platform混合DevOps平台。JFrog Artifactory支持所有开发语言，是整个DevOps流水线中所有软件包、容器映像和Helm图表的单一数据源。它具备丰富的元数据和资产可见性，可以自动化开发生命周期。而JFrog Platform则是一个通用的、端到端的混合DevOps平台，通过二进制文件管理、CI/CD流水线和DevSecOps工具自动执行从构建到生产的软件升级。

这些产品和服务的核心目标是实现“流式软件”的愿景，即允许二进制制品从开发端无缝、安全地流向边缘应用节点。

Conan是一个开源的、跨平台的、去中心化的C++包管理器，它允许您安装、解决构建依赖，更重要的是可以直接集成到Build System中使用。同时，它也支持私有仓库的搭建，以满足私有项目的需求。

要搭建Conan私有仓库，首先需要在服务器上安装Conan。然后，可以使用以下命令创建一个新的私有仓库：

```bash
conan create . user/channel
```

其中，`.`表示要将新仓库创建在当前目录下，`user`是用户名，`channel`是频道名称。您可以根据实际需求自行更改这些值。
此外，如果您正在使用Artifactory，也可以快速方便地搭建Conan私有仓库。具体来说，可以参考JFrog官网上的文档来进行设置和配置。
在NVD（美国国家漏洞数据库）提供的CVE（公共漏洞和暴露）的基础上，JFrog还提供了VulnDB这一商业漏洞数据库。而VulnDB提供了更大范围的安全漏洞数据


https://blog.csdn.net/qqqq123qqqqqqq/article/details/79421686

https://blog.csdn.net/h511555/article/details/8904143

## 官网
https://conan.io/

通用的 C++ 软件包管理器

https://www.infoq.cn/article/does-cpp-need-a-universal-package-manager

C++ 在软件包管理器上并不存在短板。当前有大量的工具可用，例如
[buckaroo](https://www.buckaroo.pm/)、
[cget](http://cget.readthedocs.io/en/latest/)、
[conan](https://conan.io/)、
[conda](https://conda.io/docs/)、
[cpm](http://www.cpm.rocks/)、
[cppan](https://cppan.org/)、
[hunter](https://docs.hunter.sh/en/latest/)
等等，不胜枚举。

https://github.com/LoopPerfect/buckaroo/

https://bintray.com/conan/conan-center

官网搜索
搜索库
maven 在官方仓库搜索，根据group arfitfect搜索
conan search grpc
xrepo search grpc
用'conan search mysql'搜索不出来

pistache 只支持Linux目前

pistache/d5608a1@conan/stable: Downloaded recipe revision 0
ERROR: pistache/d5608a1@conan/stable: Error in configure() method, line 24
        raise ConanException("Only Linux supported")
        ConanException: Only Linux supported

conan找不到mysqlclient

folly

Pistache

有Poco

https://github.com/conan-io/conan

油管博主 @Lötwig Fusel
https://www.youtube.com/watch?v=T6RZ5On3xz8
https://zhuanlan.zhihu.com/p/613174589

合肥某车企weilai，招聘conan ci/cd工程师

conan支持企业内部自建库管理，conan下载一个库，先编写conanfile文件，然后下载到本地文件夹

Conan是一个开源的C++包管理器，它主要用于方便地安装、管理和使用C++开发中的各种库和工具。它并不直接提供搭建公司内部仓库的功能，但是可以作为公司内部仓库的一个组成部分。
要搭建公司内部的Conan仓库，可以按照以下步骤进行：
在公司内部服务器上安装Conan服务端。
Conan服务端是一个基于Python的Web应用程序，它提供了Conan仓库的存储和管理功能。安装Conan服务端时，需要确保服务器上已经安装了Python和相关的依赖库。
配置Conan服务端。
安装完成后，需要对Conan服务端进行配置。配置内容包括设置仓库名称、设置仓库中保存的包信息、设置用户和权限等。
部署Conan客户端。
Conan客户端是用于与Conan服务端进行 交互的工具。在公司内部，需要为每个开发人员部署Conan客户端，并确保他们使用相同的配置。
上传包到Conan仓库。
当开发人员完成了C++库的开发后，可以使用Conan客户端将库文件上传到Conan服务端。上传时需要指定包的名称、版本号和相关信息。
配置其他开发工具使用内部仓库。
最后，需要配置其他开发工具（如Visual Studio、Eclipse等）使用公司内部的Conan仓库。配置方法因开发工具而异，一般需要在开发工具的选项中指定Conan仓库的地址和凭据信息。
综上所述，Conan本身并不提供完整的公司内部仓库搭建功能，但可以作为公司内部仓库的一个组成部分，方便开发人员管理和使用C++库和工具。如需搭建公司内部仓库，可以结合使用其他工具和方法来实现。

可以按照以下步骤在CentOS 7.2上安装Conan Server：

安装Conan Server
在CentOS 7.2上安装Conan Server需要先安装Python和一些Python依赖库。首先，使用以下命令安装Python：

```shell
sudo yum install -y python
```
然后，使用以下命令安装pip（Python包管理工具）：

```shell
sudo yum install -y python-pip
```
接下来，使用pip安装Conan Server：

```shell
    sudo pip install conanserver
```
安装完成后，您可以使用以下命令启动Conan Server：

```shell
sudo conanserver start
```
配置Conan Server
Conan Server的配置文件位于~/.conan/server.conf。您可以使用文本编辑器打开该文件，根据您的需求进行配置。例如，您可以设置管理员权限、禁用PVP等。
3. 设置虚拟环境

为了使用Conan Server，您需要创建一个虚拟环境。可以使用以下命令创建一个新的虚拟环境：

```shell
sudo conan env create --file=conans/myenv.yml
```
其中，conans/myenv.yml是包含虚拟环境配置的文件。您可以根据您的需求修改该文件中的内容。然后，使用以下命令激活虚拟环境：

```shell
sudo conan env activate myenv
```
创建和管理Conan仓库
Conan Server可以用于创建和管理Conan仓库。您可以使用以下命令创建一个新的Conan仓库：

```shell
sudo conan new myrepo/1.0.0 -g=BASIC -u=myusername -p=mypassword --url=https://myrepo.com
```
其中，myrepo是您为仓库取的名称，1.0.0是您为仓库设置的版本号。-g=BASIC表示使用基本认证方式，-u=myusername和-p=mypassword表示设置用户名和密码，--url=https://myrepo.com表示设置仓库的URL。您需要将myrepo、1.0.0、myusername、mypassword和https://myrepo.com替换为您自己的值。然后，使用以下命令激活虚拟环境：source activate myenv。

conan可以支持cmake autotools
qmake
msbuild
跨平台

nget支持windows

### 例子
Conan_examples
https://github.com/conan-io/examples

https://gitee.com/edidada/testconan
https://github.com/edidada/conan2prjs

pip install conan
pip3 install conan

https://docs.conan.io/en/latest/installation.html

要求python3吗？

conan search grpc -r conancenter


默认远程地址 conancenter

默认配置文件
~/.conan/conan.conf
编译

conan install .

conan install -c conxxx.txt
conanfile.txt
```
[requires]
# gtest/1.8.0@lasote/stable
# zlib/1.2.11@conan/stable
# Poco/1.8.1@pocoproject/stable
pistache/d5608a1@conan/stable
# opencv/3.4.1@garrick/stable

[generators]
cmake

[options]
# opencv:shared=True
```

conan remote add/remove xxx

安装

conan inspect poco/1.9.4

`conan install cjson/1.7.13@`
`conan install packagename/1.0@`
@很重要，有这个后缀才conan install才会把输入参数当做一个包名，如果没有@,conan install 会把 cjson/1.7.13当做一个路径

PS D:\git\github\career> conan install cjson/1.7.13@
ERROR: Conanfile not found at D:\git\github\career\cjson\1.7.13@


************************* WARNING: GCC OLD ABI COMPATIBILITY ***********************
 
Conan detected a GCC version > 5 but has adjusted the 'compiler.libcxx' setting to
'libstdc++' for backwards compatibility.
Your compiler is likely using the new CXX11 ABI by default (libstdc++11).
If you want Conan to use the new ABI for the default profile, run:
    $ conan profile update settings.compiler.libcxx=libstdc++11 default
Or edit '/home/wdidada/.conan/profiles/default' and set compiler.libcxx=libstdc++11
************************************************************************************

conan profile update settings.compiler.libcxx=libstdc++11 default


## conan 添加自定义的库
创建包
https://blog.csdn.net/hezhanran/article/details/112170151

## conan 2

```shell
conan version
version: 2.0.14
python
  version: 3.10.13
  sys_version: 3.10.13 (main, Nov 16 2023, 19:48:55) [GCC 9.4.0]
```

~/.conan/profiles/default

~/.conan2/profiles/default

## vcpkg和conan
conan支持选择库版本，vcpkg默认安装最新版本
apt yum也是安装特定版本

## conan2
conan new cmake_exe -d name=mypkg -d version=0.1 -f

conan graph info  .

conan new cmake_exe -d name=conan2opencvtest -d version=0.1 -f

conan new cmake_exe -d name=conan2grpctest -d version=0.1 -f

conan new cmake_exe -d name=conan2thrifttest -d version=0.1 -f

conan new cmake_exe -d name=conan2pocotest -d version=0.1 -f
conan new cmake_exe -d name=conan2zlibtest -d version=0.1 -f
conan new cmake_exe -d name=conan2leveldbtest -d version=0.1 -f


cmake > 3.23

cmake --preset conan-release
cmake --preset conan-debug

cmake <path> -G "Unix Makefiles" -DCMAKE_TOOLCHAIN_FILE=/Users/ibqo/Develop/git/github/conan2prjs/conan2grpctest/build/Release/generators/conan_toolchain.cmake -DCMAKE_POLICY_DEFAULT_CMP0091=NEW -DCMAKE_BUILD_TYPE=Release

conan install -u ../ --build=missing
conan install -u ./ --build=missing
cmake --build .


-DCMAKE_TOOLCHAIN_FILE=/Users/ibqo/Develop/git/github/conan2prjs/conan2zlibtest/build/Release/generators/conan_toolchain.cmake -DCMAKE_POLICY_DEFAULT_CMP0091=NEW -DCMAKE_BUILD_TYPE=Release


-DCMAKE_TOOLCHAIN_FILE=/Users/ibqo/Develop/git/github/conan2prjs/conan2pocotest/build/Release/generators/conan_toolchain.cmake -DCMAKE_POLICY_DEFAULT_CMP0091=NEW -DCMAKE_BUILD_TYPE=Release

-DCMAKE_TOOLCHAIN_FILE=/Users/ibqo/Develop/git/github/myqt6app/build/Release/generators/conan_toolchain.cmake -DCMAKE_POLICY_DEFAULT_CMP0091=NEW -DCMAKE_BUILD_TYPE=Release


conan install -u ./ --build=missing -pr=default_debug
conan profile show -pr default_debug
conan profile detect --name default_debug2
conan create . -pr=default_debug2


设置成debug模式
conan install -u ./ --build=missing -pr:a=default_debug
conan install --help

## clion conan插件

Debug模式下可以自动下载依赖

https://blog.conan.io/introducing-new-conan-clion-plugin/
https://github.com/conan-io/conan-clion-plugin

真的好用
conan_provider.cmake
https://github.com/conan-io/cmake-conan/blob/develop2/conan_provider.cmake

-DCMAKE_PROJECT_TOP_LEVEL_INCLUDES="conan_provider.cmake" -DCONAN_COMMAND="D:\dev_tools\Conan\conan\conan.exe"
