@echo off
rem ch07-linking 构建脚本（MSVC cl/lib/link）
rem 需先 call vcvarsall.bat x64（或于 x64 Native Tools 命令行中运行）
setlocal
if not exist obj mkdir obj
if not exist bin mkdir bin

rem ---- 编译目标文件 ----
cl /nologo /W3 /O2 /c /Fobs\ src\main.c src\vec.c src\weakdemo.c src\strongdef.c src\foo.c src\bar.c

rem ---- ① 静态库 lib + link ----
lib /nologo /OUT:bin\libvec.lib bs\vec.obj
lib /nologo /OUT:bin\liba.lib  bs\foo.obj
lib /nologo /OUT:bin\libb.lib  bs\bar.obj
link /nologo /OUT:bin\static_demo.exe bs\main.obj bs\weakdemo.obj ^
     bin\libvec.lib bin\liba.lib bin\libb.lib

rem 注意：MSVC 的 .lib 静态库不做"按需抽取依赖扫描"，
rem 但成员 .obj 仍按引用抽取；演示 foo 依赖 bar 时顺序同样重要。

rem ---- ② 动态库 /LD ----
cl /nologo /W3 /O2 /LD /Fe:bin\dyn.dll src\dynlib.c
cl /nologo /W3 /O2 /Fe:bin\dynload.exe src\dynload.c

rem ---- 运行 ----
pushd bin
static_demo.exe
dynload.exe
popd
echo 完成：bin\ 下有 static_demo.exe / dyn.dll / dynload.exe
