# meson
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

sudo yum install meson -y

https://mesonbuild.com/

https://gitee.com/edidada/tutorial



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
