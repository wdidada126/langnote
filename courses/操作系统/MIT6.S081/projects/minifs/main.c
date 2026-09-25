/* main.c — minifs 演示：基本操作 + 两种崩溃时机 + 批提交（L06/L07/L08/L14） */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "minifs.h"

static Mfs m;

static unsigned char wbuf[3 * BS], rbuf[3 * BS];

static void list_cb(const char *name, int inum, int type, int size)
{
    printf("    %-14s ino=%2d type=%s size=%d\n", name, inum,
           type == I_DIR ? "dir " : "file", size);
}

static void fresh_fs(void)
{
    fs_mkfs(&m);
    fs_mount(&m);
}

static void basics(void)
{
    int fd, i, n;
    puts("== 基本：mkdir / create / write / read / ls / unlink ==");
    for (i = 0; i < 3 * BS; i++) wbuf[i] = (unsigned char)(i * 7 + 1);
    if (fs_mkdir(&m, "/doc") != 0) { printf("mkdir failed\n"); return; }
    if (fs_create(&m, "/doc/a") != 0) { printf("create failed\n"); return; }
    fd = fs_open(&m, "/doc/a", 1);
    n = fs_write(&m, fd, wbuf, 3 * BS);
    printf("wrote %d/%d bytes\n", n, 3 * BS);
    fs_close(&m, fd);
    fd = fs_open(&m, "/doc/a", 0);
    n = fs_read(&m, fd, rbuf, 3 * BS);
    fs_close(&m, fd);
    printf("read %d bytes, match=%s, size=%d\n", n,
           memcmp(wbuf, rbuf, (size_t)3 * BS) == 0 ? "YES" : "NO",
           fs_stat_size(&m, "/doc/a"));
    puts("  ls /doc:");
    fs_ls(&m, "/doc", list_cb);
    fs_unlink(&m, "/doc/a");
    puts("  after unlink:");
    fs_ls(&m, "/doc", list_cb);
    fs_dump_stats(&m, "basics");
}

static void crash_final_phase(void)
{
    int fd, i, r;
    puts("== 崩溃时机 A：commit 已写日志头，回写目标块中途（应重放补齐） ==");
    fresh_fs();
    fs_create(&m, "/x");
    /* 事务含 3 块：日志区 3 写 + 头 1 写 + 回写 3 次。在第 6 次物理写下盘后"断电" */
    fd = fs_open(&m, "/x", 1);
    { unsigned char big[2 * BS];
      for (i = 0; i < 2 * BS; i++) big[i] = (unsigned char)(i + 65);
      fs_set_crash_at(&m, 7);
      r = fs_write(&m, fd, big, 2 * BS);
      fs_set_crash_at(&m, 0);
      printf("write returned %d (-2 = crashed)\n", r); }
    fs_dump_stats(&m, "after crash A");
    fs_mount(&m);                       /* "重启"：重放 */
    fd = fs_open(&m, "/x", 0);
    if (fd >= 0) {
        unsigned char chk[2 * BS];
        int n = fs_read(&m, fd, chk, 2 * BS);
        int ok = (n == 2 * BS);
        for (i = 0; ok && i < n; i++) if (chk[i] != (unsigned char)(i + 65)) ok = 0;
        printf("recovered file size=%d verify=%s\n", n, ok ? "OK" : "TORN");
        fs_close(&m, fd);
    } else {
        printf("file /x missing after recovery (transaction lost)\n");
    }
}

static void crash_log_phase(void)
{
    int fd, i, r;
    puts("== 崩溃时机 B：日志内容写到一半（头未写 → 事务应整体作废） ==");
    fresh_fs();
    fs_create(&m, "/y");
    fd = fs_open(&m, "/y", 1);
    { unsigned char big[BS];
      for (i = 0; i < BS; i++) big[i] = (unsigned char)'z';
      fs_set_crash_at(&m, 2);           /* 第 2 次物理写后崩：头还没落盘 */
      r = fs_write(&m, fd, big, BS);
      fs_set_crash_at(&m, 0);
      printf("write returned %d\n", r); }
    fs_mount(&m);
    printf("size(/y) after recovery = %d（0 = 干净回滚，无半块数据）\n",
           fs_stat_size(&m, "/y"));
}

static void batching(void)
{
    int i, before;
    char path[16];
    puts("== fssched 式批提交：batch=1 vs batch=8 的 IO/commit 对比 ==");
    fresh_fs();
    before = (int)m.n_pwrite;
    for (i = 0; i < 8; i++) { sprintf(path, "/f%d", i); fs_create(&m, path); }
    printf("batch=1: %d pwrites, %ld commits\n", (int)m.n_pwrite - before, m.n_commit);
    fresh_fs();
    m.batch = 8;
    before = (int)m.n_pwrite;
    for (i = 0; i < 8; i++) { sprintf(path, "/g%d", i); fs_create(&m, path); }
    fs_commit(&m);
    printf("batch=8: %d pwrites, %ld commits（攒批摊薄每事务固定开销）\n",
           (int)m.n_pwrite - before, m.n_commit);
    m.batch = 1;
}

int main(void)
{
    puts("minifs demo — 6.1810 L06/L07/L08/L14 (xv6 fs+log 复刻)");
    basics();
    crash_final_phase();
    crash_log_phase();
    batching();
    puts("done.");
    return 0;
}
