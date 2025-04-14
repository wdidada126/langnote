# meson

## clion 2024支持meson
meson.build
ninja


## comand
meson setup build --native-file=D:\develops\tools\vcpkg\scripts\buildsystems\vcpkg.cmake
cd build
meson compile -j 6 --native-file=D:\develops\tools\vcpkg\scripts\buildsystems\vcpkg.cmake
meson install
meson test


https://github.com/cisco/openh264
openh264用meson构建
python写的

https://mesonbuild.com/Getting-meson_zh.html

pip3 install meson
choco install meson

C:\Users\edida\AppData\Local\Temp\chocolatey\meson\1.5.1\meson-1.5.1-64.msi

eclipse mac版本支持meson

meson.build

### meson的项目
https://github.com/pistacheio/pistache/tree/0.0.5

```shell
$ cd pistache
$ meson setup build \
    --buildtype=release \
    -DPISTACHE_USE_SSL=true \
    -DPISTACHE_BUILD_EXAMPLES=true \
    -DPISTACHE_BUILD_TESTS=true \
    -DPISTACHE_BUILD_DOCS=false \
    --prefix="/usr"
$ meson compile -C build
$ meson compile
$ meson install -C build
```

## 安装
sudo yum install meson -y

https://mesonbuild.com/

https://gitee.com/edidada/tutorial

### win
pip3 install meson命令安装，如果在root环境下，它会在系统范围内安装。
相反,你也可以使用 pip3 install --user meson命令来为user用户单独安装

glib

https://gitlab.gnome.org/GNOME/glib/-/releases

就是用meson组织的

### pistache

```shell
cd pistache
meson setup build \
    --buildtype=release \
    -DPISTACHE_USE_SSL=true \
    -DPISTACHE_BUILD_EXAMPLES=true \
    -DPISTACHE_BUILD_TESTS=true \
    -DPISTACHE_BUILD_DOCS=true \
    --prefix="$PWD/prefix"
meson install -C build
```
### cpp-httplib
meson_options.txt


meson setup -h
usage: meson setup [-h] [--prefix PREFIX] [--bindir BINDIR] [--datadir DATADIR] [--includedir INCLUDEDIR] [--infodir INFODIR] [--libdir LIBDIR]
                   [--licensedir LICENSEDIR] [--libexecdir LIBEXECDIR] [--localedir LOCALEDIR] [--localstatedir LOCALSTATEDIR] [--mandir MANDIR]
                   [--sbindir SBINDIR] [--sharedstatedir SHAREDSTATEDIR] [--sysconfdir SYSCONFDIR] [--auto-features {enabled,disabled,auto}]
                   [--backend {ninja,vs,vs2010,vs2012,vs2013,vs2015,vs2017,vs2019,vs2022,xcode,none}] [--genvslite {vs2022}]
                   [--buildtype {plain,debug,debugoptimized,release,minsize,custom}] [--debug] [--default-library {shared,static,both}]
                   [--default-both-libraries {shared,static,auto}] [--errorlogs] [--install-umask INSTALL_UMASK] [--layout {mirror,flat}]
                   [--optimization {plain,0,g,1,2,3,s}] [--prefer-static] [--stdsplit] [--strip] [--unity {on,off,subprojects}] [--unity-size UNITY_SIZE]        
                   [--warnlevel {0,1,2,3,everything}] [--werror] [--wrap-mode {default,nofallback,nodownload,forcefallback,nopromote}]
                   [--force-fallback-for FORCE_FALLBACK_FOR] [--vsenv] [--pkgconfig.relocatable] [--python.bytecompile PYTHON.BYTECOMPILE]
                   [--python.install-env {auto,prefix,system,venv}] [--python.platlibdir PYTHON.PLATLIBDIR] [--python.purelibdir PYTHON.PURELIBDIR]
                   [--python.allow-limited-api] [--pkg-config-path PKG_CONFIG_PATH] [--build.pkg-config-path BUILD.PKG_CONFIG_PATH]
                   [--cmake-prefix-path CMAKE_PREFIX_PATH] [--build.cmake-prefix-path BUILD.CMAKE_PREFIX_PATH] [-D option] [--native-file NATIVE_FILE]
                   [--cross-file CROSS_FILE] [-v] [--fatal-meson-warnings] [--reconfigure] [--wipe] [--clearcache]
                   [builddir] [sourcedir]

positional arguments:
  builddir
  sourcedir

options:
  -h, --help                                                                    show this help message and exit
  --prefix PREFIX                                                               Installation prefix (default: c:/).
  --bindir BINDIR                                                               Executable directory (default: bin).
  --datadir DATADIR                                                             Data file directory (default: share).
  --includedir INCLUDEDIR                                                       Header file directory (default: include).
  --infodir INFODIR                                                             Info page directory (default: share/info).
  --libdir LIBDIR                                                               Library directory (default: lib).
  --licensedir LICENSEDIR                                                       Licenses directory (default: ).
  --libexecdir LIBEXECDIR                                                       Library executable directory (default: libexec).
  --localedir LOCALEDIR                                                         Locale data directory (default: share/locale).
  --localstatedir LOCALSTATEDIR                                                 Localstate data directory (default: var).
  --mandir MANDIR                                                               Manual page directory (default: share/man).
  --sbindir SBINDIR                                                             System executable directory (default: sbin).
  --sharedstatedir SHAREDSTATEDIR                                               Architecture-independent data directory (default: com).
  --sysconfdir SYSCONFDIR                                                       Sysconf data directory (default: etc).
  --auto-features {enabled,disabled,auto}                                       Override value of all 'auto' features (default: auto).
  --backend {ninja,vs,vs2010,vs2012,vs2013,vs2015,vs2017,vs2019,vs2022,xcode,none}
                                                                                Backend to use (default: ninja).
  --genvslite {vs2022}                                                          Setup multiple buildtype-suffixed ninja-backend build directories, and a
                                                                                [builddir]_vs containing a Visual Studio meta-backend with multiple
                                                                                configurations that calls into them (default: vs2022).
  --buildtype {plain,debug,debugoptimized,release,minsize,custom}               Build type to use (default: debug).
  --debug                                                                       Enable debug symbols and other information
  --default-library {shared,static,both}                                        Default library type (default: shared).
  --default-both-libraries {shared,static,auto}                                 Default library type for both_libraries (default: shared).
  --errorlogs                                                                   Whether to print the logs from failing tests
  --install-umask INSTALL_UMASK                                                 Default umask to apply on permissions of installed files (default: 022).
  --layout {mirror,flat}                                                        Build directory layout (default: mirror).
  --optimization {plain,0,g,1,2,3,s}                                            Optimization level (default: 0).
  --prefer-static                                                               Whether to try static linking before shared linking
  --stdsplit                                                                    Split stdout and stderr in test logs
  --strip                                                                       Strip targets on install
  --unity {on,off,subprojects}                                                  Unity build (default: off).
  --unity-size UNITY_SIZE                                                       Unity block size (default: (2, None, 4)).
  --warnlevel {0,1,2,3,everything}                                              Compiler warning level to use (default: 1).
  --werror                                                                      Treat warnings as errors
  --wrap-mode {default,nofallback,nodownload,forcefallback,nopromote}           Wrap mode (default: default).
  --force-fallback-for FORCE_FALLBACK_FOR                                       Force fallback for those subprojects (default: []).
  --vsenv                                                                       Activate Visual Studio environment
  --pkgconfig.relocatable                                                       Generate pkgconfig files as relocatable
  --python.bytecompile PYTHON.BYTECOMPILE                                       Whether to compile bytecode (default: (-1, 2, 0)).
  --python.install-env {auto,prefix,system,venv}                                Which python environment to install to (default: prefix).
  --python.platlibdir PYTHON.PLATLIBDIR                                         Directory for site-specific, platform-specific files (default: ).
  --python.purelibdir PYTHON.PURELIBDIR                                         Directory for site-specific, non-platform-specific files (default: ).
  --python.allow-limited-api                                                    Whether to allow use of the Python Limited API
  --pkg-config-path PKG_CONFIG_PATH                                             List of additional paths for pkg-config to search (default: []). (just for host  
                                                                                machine)
  --build.pkg-config-path BUILD.PKG_CONFIG_PATH                                 List of additional paths for pkg-config to search (default: []). (just for build 
                                                                                machine)
  --cmake-prefix-path CMAKE_PREFIX_PATH                                         List of additional prefixes for cmake to search (default: []). (just for host    
                                                                                machine)
  --build.cmake-prefix-path BUILD.CMAKE_PREFIX_PATH                             List of additional prefixes for cmake to search (default: []). (just for build   
                                                                                machine)
  -D option                                                                     Set the value of an option, can be used several times to set multiple options.   
  --native-file NATIVE_FILE                                                     File containing overrides for native compilation environment.
  --cross-file CROSS_FILE                                                       File describing cross compilation environment.
  -v, --version                                                                 show program's version number and exit
  --fatal-meson-warnings                                                        Make all Meson warnings fatal
  --reconfigure                                                                 Set options and reconfigure the project. Useful when new options have been added 
                                                                                to the project and the default value is not working.
  --wipe                                                                        Wipe build directory and reconfigure using previous command line options. Useful 
                                                                                when build directory got corrupted, or when rebuilding with a newer version of   
                                                                                meson.
  --clearcache                                                                  Clear cached state (e.g. found dependencies). Since 1.3.0.
PS D:\develops\git\github\cpp-httplib-0.18.7> 
