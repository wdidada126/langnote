#include <stdio.h>
#include <stdlib.h>

/* L13：运行期显式装载共享库。
 * POSIX: dlopen/dlsym/dlclose（-ldl）
 * Windows: LoadLibraryA / GetProcAddress / FreeLibrary
 * 可观察对比：把 libdyn 从链接命令去掉、改用本程序装载 → 磁盘符号表何时被查。 */
#ifdef _WIN32
#include <windows.h>

int main(void)
{
    HMODULE h;
    void (*greet)(const char *);

    h = LoadLibraryA("dyn.dll");            /* 注意：DLL 须与 exe 同目录或在 PATH */
    if (!h) {
        fprintf(stderr, "LoadLibrary failed: %lu (先运行 build.bat 生成 dyn.dll)\n",
                (unsigned long)GetLastError());
        return 1;
    }
    greet = (void (*)(const char *))GetProcAddress(h, "dyn_greet");
    if (!greet) {
        fprintf(stderr, "GetProcAddress failed\n");
        FreeLibrary(h);
        return 1;
    }
    greet("CSAPP");
    FreeLibrary(h);
    return 0;
}

#else  /* POSIX */
#include <dlfcn.h>

int main(void)
{
    void *h;
    void (*greet)(const char *);

    h = dlopen("./libdyn.so", RTLD_NOW);    /* 当前目录显式路径；系统目录可给 "libdyn.so" */
    if (!h) {
        fprintf(stderr, "dlopen: %s (先 make dyn 生成 libdyn.so)\n", dlerror());
        return 1;
    }
    *(void **)(&greet) = dlsym(h, "dyn_greet");
    if (!greet) {
        fprintf(stderr, "dlsym: %s\n", dlerror());
        dlclose(h);
        return 1;
    }
    greet("CSAPP");
    dlclose(h);
    return 0;
}
#endif
