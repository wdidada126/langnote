/* minifs.h — 单用户迷你文件系统（对应 6.1810 L06/L07/L08/L14）
 * 磁盘 = 内存数组；缓冲缓存/日志/崩溃恢复全部按 xv6 bio.c + log.c 建模。 */
#ifndef MINIFS_H
#define MINIFS_H

#define BS        512            /* 块大小 */
#define NB        256            /* 块数（镜像 128KiB） */
#define SB_BNO    0              /* superblock */
#define BMP_BNO   1              /* 块位图 + inode 位图 */
#define INO_START 2              /* inode 区起始（2 块 = 32 个 inode） */
#define INO_PER   16
#define NINODE    32
#define LOG_HDR   8              /* 日志头块 */
#define LOG_SLOT0 9              /* 日志数据槽起始 */
#define LOG_SLOTS 19
#define DATA_START 32            /* 数据块起点 */
#define NADDR     8              /* 每 inode 直接块数（无间接：单文件上限 4KiB） */
#define CACHE_N   16

#define FS_MAGIC  0x4d465331u    /* "MFS1" */
#define LOG_MAGIC 0x4c4f4731u

enum { I_FREE = 0, I_FILE = 1, I_DIR = 2 };

typedef struct { int bno, valid; unsigned char data[BS]; int dirty; } Buf;

typedef struct {
    int in_use, inum, off, writable;
} FOpen;

typedef struct Mfs {
    unsigned char disk[NB * BS];  /* "物理磁盘" */
    Buf cache[CACHE_N];
    /* 当前事务 */
    int log_n;                    /* 日志中的块数 */
    int log_bno[LOG_SLOTS];       /* 目标块号 */
    unsigned char log_data[LOG_SLOTS][BS];
    int crashed;                  /* 本进程周期内已"崩溃"（abort） */
    /* 崩溃模拟：第 n 次物理写时挂掉 */
    int crash_at, ops_done;
    /* 统计 */
    long n_pwrite, n_bread, n_commit, n_commit_io;
    int batch;                    /* >1 时 syscall 不自动 commit（fssched 式批提交） */
    int mounted;
} Mfs;

int  fs_mkfs(Mfs *m);
int  fs_mount(Mfs *m);             /* 含日志重放恢复 */
int  fs_crashed(Mfs *m);
int  fs_commit(Mfs *m);            /* 批提交模式下的显式提交 */

int  fs_create(Mfs *m, const char *path);
int  fs_open(Mfs *m, const char *path, int writable);   /* 返回 fd 或 -1 */
int  fs_mkdir(Mfs *m, const char *path);
int  fs_unlink(Mfs *m, const char *path);
int  fs_write(Mfs *m, int fd, const void *data, int n); /* 返回写入字节或 -2=崩 */
int  fs_read(Mfs *m, int fd, void *data, int n);
int  fs_close(Mfs *m, int fd);
int  fs_stat_size(Mfs *m, const char *path);
/* 遍历：回调 name,inum,type,size */
void fs_ls(Mfs *m, const char *path,
           void (*cb)(const char *, int, int, int));
void fs_dump_stats(Mfs *m, const char *tag);
void fs_set_crash_at(Mfs *m, int op);   /* 0=关闭 */

#endif
