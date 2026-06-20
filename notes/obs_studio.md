# obs_studio

win/mac编译，有维护的依赖库


编译obs studio，cmake组织的，CMakePresets.json，编译类型，RelWithDebInfo

```shell
PS D:\develops\git\github\obs-studio> cmake --build --preset windows-x64
Error: D:/develops/git/github/obs-studio/build_x64 is not a directory
PS D:\develops\git\github\obs-studio> cmake --preset windows-x64
Preset CMake variables:

  ENABLE_BROWSER:BOOL="TRUE"
  GPU_PRIORITY_VAL:STRING=""
  RESTREAM_CLIENTID:STRING=""
  RESTREAM_HASH:STRING=""
  TWITCH_CLIENTID:STRING=""
  TWITCH_HASH:STRING=""
  VIRTUALCAM_GUID:STRING="A3FCE0F5-3493-419F-958A-ABA1250EC20B"
  YOUTUBE_CLIENTID:STRING=""
  YOUTUBE_CLIENTID_HASH:STRING=""
  YOUTUBE_SECRET:STRING=""
  YOUTUBE_SECRET_HASH:STRING=""

-- Selecting Windows SDK version 10.0.22621.0 to target Windows 10.0.26100.
-- The C compiler identification is MSVC 19.38.33144.0
-- The CXX compiler identification is MSVC 19.38.33144.0
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: C:/Program Files/Microsoft Visual Studio/2022/Enterprise/VC/Tools/MSVC/14.38.33130/bin/Hostx64/x64/cl.exe - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: C:/Program Files/Microsoft Visual Studio/2022/Enterprise/VC/Tools/MSVC/14.38.33130/bin/Hostx64/x64/cl.exe - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Selecting Windows SDK version 10.0.22621.0 to target Windows 10.0.26100.
-- The C compiler identification is MSVC 19.38.33144.0
-- The CXX compiler identification is MSVC 19.38.33144.0
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: C:/Program Files/Microsoft Visual Studio/2022/Enterprise/VC/Tools/MSVC/14.38.33130/bin/Hostx64/x86/cl.exe - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: C:/Program Files/Microsoft Visual Studio/2022/Enterprise/VC/Tools/MSVC/14.38.33130/bin/Hostx64/x86/cl.exe - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Setting up Pre-Built obs-deps (x86)
-- Setting up Pre-Built obs-deps (x86) - done
CMake Warning (dev) at cmake/finders/FindDetours.cmake:65 (message):
  Failed to find detours version.
Call Stack (most recent call first):
  plugins/win-capture/graphics-hook/CMakeLists.txt:3 (find_package)
This warning is for project developers.  Use -Wno-dev to suppress it.

-- Found Detours: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x86/lib/detours.lib (found version "0.0.0")
-- Found Vulkan: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x86/lib/vulkan-1.lib (found version "1.3.216")  missing components: glslc glslangValidator
-- Configuring done (5.8s)
-- Generating done (0.1s)
-- Build files have been written to: D:/develops/git/github/obs-studio/build_x86
-- Setting up Pre-Built obs-deps (x64)
-- Setting up Pre-Built obs-deps (x64) - done
-- Setting up Pre-Built Qt6 (x64)
-- Setting up Pre-Built Qt6 (x64) - done
-- Setting up Chromium Embedded Framework (x64)
-- Setting up Chromium Embedded Framework (x64) - done
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Failed
-- Looking for pthread_create in pthreads
-- Looking for pthread_create in pthreads - not found
-- Looking for pthread_create in pthread
-- Looking for pthread_create in pthread - not found
-- Found Threads: TRUE
-- Found FFmpeg: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avformat-61.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avutil-59.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/swscale-8.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/swresample-5.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avcodec-61.dll (found suitable version "7.0", minimum required is "6.1") found components: avformat avutil swscale swresample avcodec
-- Found ZLIB: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/lib/zlib.lib (found version "1.3.1")
-- Found Uthash: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/include (found version "2.3.0")
-- Performing Test HAVE_STDATOMIC
-- Performing Test HAVE_STDATOMIC - Success
-- Found WrapAtomic: TRUE
-- Found jansson: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/lib/jansson.lib (found version "2.14")
-- Performing Test COMPILER_HAS_DEPRECATED_ATTR
-- Performing Test COMPILER_HAS_DEPRECATED_ATTR - Failed
-- Performing Test COMPILER_HAS_DEPRECATED
-- Performing Test COMPILER_HAS_DEPRECATED - Success
-- Found OpenGL: opengl32
-- aja: Using new libajantv2 library
CMake Warning (dev) at cmake/finders/FindLibAJANTV2.cmake:100 (message):
  Failed to find LibAJANTV2 version.
Call Stack (most recent call first):
  plugins/aja/CMakeLists.txt:10 (find_package)
This warning is for project developers.  Use -Wno-dev to suppress it.

-- Found LibAJANTV2: optimized;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/lib/ajantv2.lib;debug;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/lib/ajantv2d.lib (found version "0.0.0")
-- Found CEF: D:/develops/git/github/obs-studio/.deps/cef_binary_6533_windows_x64/Release/libcef.dll (found suitable version "127.145.7", minimum required is "95")
-- Found nlohmann_json: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/share/cmake/nlohmann_json/nlohmann_jsonConfig.cmake (found suitable version "3.11.3", minimum required is "3.11")
-- Found FFmpeg: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avcodec-61.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avfilter-10.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avdevice-61.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avutil-59.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/swscale-8.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avformat-61.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/swresample-5.dll (found suitable version "7.0", minimum required is "6.1") found components: avcodec avfilter avdevice avutil swscale avformat swresample
-- Found FFmpeg: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avcodec-61.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avfilter-10.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avdevice-61.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avutil-59.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/swscale-8.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avformat-61.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/swresample-5.dll (found version "7.0") found components: avcodec avdevice avutil avformat
-- Found AMF: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/include (found suitable version "1.4.34", minimum required is "1.4.29")
-- Found FFmpeg: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avcodec-61.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avfilter-10.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avdevice-61.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avutil-59.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/swscale-8.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avformat-61.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/swresample-5.dll (found version "7.0") found components: avcodec avutil avformat
CMake Warning (dev) at cmake/finders/FindLibspeexdsp.cmake:87 (message):
  Failed to find Libspeexdsp version.
Call Stack (most recent call first):
  plugins/obs-filters/cmake/speexdsp.cmake:4 (find_package)
  plugins/obs-filters/CMakeLists.txt:34 (include)
This warning is for project developers.  Use -Wno-dev to suppress it.

-- Found Libspeexdsp: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/lib/speexdsp.lib (found version "0.0.0")
CMake Warning (dev) at cmake/finders/FindLibrnnoise.cmake:87 (message):
  Failed to find Librnnoise version.
Call Stack (most recent call first):
  plugins/obs-filters/cmake/rnnoise.cmake:5 (find_package)
  plugins/obs-filters/CMakeLists.txt:35 (include)
This warning is for project developers.  Use -Wno-dev to suppress it.

-- Found Librnnoise: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/lib/rnnoise.lib (found version "0.0.0")
-- Found FFnvcodec: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/include (found suitable version "12.2", minimum required is "12")
-- Found MbedTLS: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/lib/mbedtls.lib (found version "3.4.1")
-- Found VPL: optimized;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/lib/vpl.lib;debug;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/lib/vpld.lib (Required is at least version "2.9")
-- Found VPL: optimized;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/lib/vpl.lib;debug;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/lib/vpld.lib (found suitable version "2.12", minimum required is "2.9")
-- Found CURL: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/lib/cmake/CURL/CURLConfig.cmake (found version "8.9.1-DEV")
-- Found nlohmann_json: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/share/cmake/nlohmann_json/nlohmann_jsonConfig.cmake (found suitable version "3.11.3", minimum required is "3")
-- Found Websocketpp: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/include (found suitable version "0.8.2", minimum required is "0.8")
-- Found Asio: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/include (found suitable version "1.31.0", minimum required is "1.12.1")
-- Found Libx264: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/libx264-164.dll (found version "0.164.3106")
-- Found Freetype: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/lib/freetype.lib (found version "2.13.3")
CMake Warning (dev) at cmake/finders/FindDetours.cmake:65 (message):
  Failed to find detours version.
Call Stack (most recent call first):
  plugins/win-capture/graphics-hook/CMakeLists.txt:3 (find_package)
This warning is for project developers.  Use -Wno-dev to suppress it.

-- Found Detours: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/lib/detours.lib (found version "0.0.0")
-- Found Vulkan: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/lib/vulkan-1.lib (found version "1.3.216")  missing components: glslc glslangValidator
-- Found FFmpeg: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avcodec-61.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avutil-59.dll (found version "7.0") found components: avcodec avutil
-- Found FFmpeg: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avcodec-61.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avutil-59.dll;D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/avformat-61.dll (found version "7.0") found components: avcodec avutil avformat
-- aja: Using new libajantv2 library
CMake Warning (dev) at cmake/finders/FindLibAJANTV2.cmake:100 (message):
  Failed to find LibAJANTV2 version.
Call Stack (most recent call first):
  UI/frontend-plugins/aja-output-ui/CMakeLists.txt:8 (find_package)
This warning is for project developers.  Use -Wno-dev to suppress it.

-- Found SWIG: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/bin/swig.exe (found suitable version "4.1.0", minimum required is "4")
-- Found Luajit: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/lib/lua51.lib (found version "2.1.1724512491")
-- Found Python: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/lib/python3.lib (found suitable version "3.8.10", required range is "3.8...<3.12")
CMake Warning (dev) at cmake/finders/FindDetours.cmake:65 (message):
  Failed to find detours version.
Call Stack (most recent call first):
  UI/cmake/os-windows.cmake:12 (find_package)
  UI/CMakeLists.txt:109 (include)
This warning is for project developers.  Use -Wno-dev to suppress it.

-- Found nlohmann_json: D:/develops/git/github/obs-studio/.deps/obs-deps-2024-09-12-x64/share/cmake/nlohmann_json/nlohmann_jsonConfig.cmake (found suitable version "3.11.3", minimum required is "3.11")
                      _                   _             _ _
                 ___ | |__  ___       ___| |_ _   _  __| (_) ___
                / _ \| '_ \/ __|_____/ __| __| | | |/ _` | |/ _ \
               | (_) | |_) \__ \_____\__ \ |_| |_| | (_| | | (_) |
                \___/|_.__/|___/     |___/\__|\__,_|\__,_|_|\___/

OBS:  Application Version: 31.0.2-modified - Build Number: 35
==================================================================================


------------------------       Enabled Features           ------------------------
 - Browser panels
 - Direct3D 11 renderer
 - NVIDIA Audio FX support
 - NVIDIA Video FX support
 - OpenGL renderer
 - Plugin Support
 - RNNoise noise suppression
 - Scripting Support (Frontend)
 - Scripting support
 - SpeexDSP noise suppression
 - User Interface
 - What's New panel
------------------------       Disabled Features          ------------------------
 - Restream API connection
 - Twitch API connection
 - YouTube API connection
------------------------        Enabled Modules           ------------------------
 - aja
 - aja-output-ui
 - coreaudio-encoder
 - decklink
 - decklink-captions
 - decklink-output-ui
 - frontend-tools
 - graphics-hook
 - image-source
 - libobs-d3d11
 - libobs-winrt
 - nv-filters
 - obs-browser
 - obs-ffmpeg
 - obs-filters
 - obs-nvenc
 - obs-outputs
 - obs-qsv11
 - obs-text
 - obs-transitions
 - obs-virtualcam-module
 - obs-vst
 - obs-webrtc
 - obs-websocket
 - obs-x264
 - obslua
 - obspython
 - rtmp-services
 - text-freetype2
 - vlc-video
 - win-capture
 - win-dshow
 - win-wasapi
------------------------        Disabled Modules          ------------------------
 - obs-libfdk
 - test-input
----------------------------------------------------------------------------------
-- Configuring done (21.9s)
-- Generating done (8.8s)
-- Build files have been written to: D:/develops/git/github/obs-studio/build_x64
PS D:\develops\git\github\obs-studio>
```

