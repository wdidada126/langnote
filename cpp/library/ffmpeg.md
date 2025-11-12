# ffmpeg

## win 编译好的库文件
https://github.com/BtbN/FFmpeg-Builds/releases

ffmpeg-n7.1.1-2-g68b5db2464-win64-lgpl-shared-7.1.zip

[Environment]::SetEnvironmentVariable("FFmpeg_LIBRARIES", "D:\develops\ffmpeg-n7.1.1-2-g68b5db2464-win64-lgpl-shared-7.1\include", "User")
#### 设置用户级环境变量
[Environment]::SetEnvironmentVariable("FFmpeg_LIBRARIES", "D:\develops\ffmpeg-n7.1.1-2-g68b5db2464-win64-lgpl-shared-7.1\lib", "User")
#### 设置系统级环境变量

## win编译好的可执行文件
```
choco install ffmpeg
choco install ffmpeg-full
```

The following builds are also available through package managers:
release essentials: choco install ffmpeg winget install "FFmpeg (Essentials Build)"
release full: choco install ffmpeg-full scoop install ffmpeg winget install ffmpeg
release full shared: scoop install ffmpeg-shared winget install "FFmpeg (Shared)"
git master: scoop install ffmpeg-gyan-nightly

cmake
支持跨平台编译
android

## ubuntu 上编译ffmpeg
https://ffmpeg.org/

https://github.com/FFmpeg/FFmpeg

c语言写的
c/ffmpeg

make组织的

https://github.com/edidada/FFmpeg4Android
https://github.com/edidada/testffmpeg

vcpkg

```shell
-- Building Options: --toolchain=msvc --enable-pic --disable-doc --enable-debug --enable-runtime-cpudetect --disable-autodetect --target-os=win32 --enable-w32threads --enable-d3d11
va --enable-d3d12va --enable-dxva2 --enable-mediafoundation --disable-inline-asm --cc=cl.exe --host_cc=cl.exe --cxx=cl.exe --windres=rc.exe --ld=link.exe --ar='ar-lib lib.exe' --ra
nlib=: --disable-ffmpeg --disable-ffplay --disable-ffprobe --enable-avcodec --enable-avdevice --enable-avformat --enable-avfilter --disable-postproc --enable-swresample --enable-sw
scale --disable-alsa --disable-amf --disable-libaom --disable-libass --disable-avisynth --disable-bzlib --disable-libdav1d --disable-libfdk-aac --disable-libfontconfig --disable-li
bharfbuzz --disable-libfreetype --disable-libfribidi --disable-iconv --disable-libilbc --disable-lzma --disable-libmp3lame --disable-libmodplug --disable-cuda --disable-nvenc --dis
able-nvdec  --disable-cuvid --disable-ffnvcodec --disable-opencl --disable-opengl --disable-libopenh264 --disable-libopenjpeg --disable-libopenmpt --disable-openssl --enable-schann
el --disable-libopus --disable-sdl2 --disable-libsnappy --disable-libsoxr --disable-libspeex --disable-libssh --disable-libtensorflow --disable-libtesseract --disable-libtheora --d
isable-libvorbis --disable-libvpx --disable-libwebp --disable-libx264 --disable-libx265 --disable-libxml2 --disable-zlib --disable-libsrt --disable-libmfx --enable-cross-compile --disable-static --enable-shared --extra-cflags=-DHAVE_UNISTD_H=0 --pkg-config="D:/develops/tools/vcpkg/downloads/tools/msys2/21caed2f81ec917b/mingw64/bin/pkg-config.exe"
```
## 编程语言
c
## 源代码
https://git.ffmpeg.org/ffmpeg.git
https://github.com/FFmpeg/FFmpeg.git

## 版本version
https://github.com/FFmpeg/FFmpeg/tags

8.0，2025 Aug 22