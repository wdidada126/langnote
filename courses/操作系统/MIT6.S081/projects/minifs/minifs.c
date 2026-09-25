/* minifs.c — 单用户文件系统 + redo 日志 + 崩溃模拟（xv6 fs.c/bio.c/log.c 的教学复刻）
 * bread/bwrite ↔ 缓冲缓存；log_write/commit ↔ 写前日志；fs_mount ↔ 崩溃后重放。 */
#include <stdio.h>
#include <string.h>
#include "minifs.h"

/* ---------- 小端序列化 ---------- */
static void put16(unsigned char *p, unsigned v) { p[0] = (unsigned char)v; p[1] = (unsigned char)(v >> 8); }
static void put32(unsigned char *p, unsigned long v)
{ p[0] = (unsigned char)v; p[1] = (unsigned char)(v >> 8); p[2] = (unsigned char)(v >> 16); p[3] = (unsigned char)(v >> 24); }
static unsigned int get16(const unsigned char *p) { return (unsigned)(p[0] | (p[1] << 8)); }
static unsigned long get32(const unsigned char *p)
{ return (unsigned long)p[0] | ((unsigned long)p[1] << 8) | ((unsigned long)p[2] << 16) | ((unsigned long)p[3] << 24); }

typedef struct { int type; unsigned int size; unsigned short a[NADDR]; } INode;

/* ---------- 物理层："下盘"带崩溃计点 ---------- */
static int pwrite_blk(Mfs *m, int bno, const unsigned char *src)
{
    if (m->crashed) return 0;
    memcpy(m->disk + (size_t)bno * BS, src, BS);
    m->n_pwrite++;
    m->ops_done++;
    if (m->crash_at && m->ops_done >= m->crash_at) m->crashed = 1;
    return !m->crashed;
}

/* ---------- 缓冲缓存（bio.c） ---------- */
static Buf *bfind(Mfs *m, int bno)
{
    int i;
    for (i = 0; i < CACHE_N; i++)
        if (m->cache[i].valid && m->cache[i].bno == bno) return &m->cache[i];
    return 0;
}

static int commit(Mfs *m);

static Buf *bread(Mfs *m, int bno)
{
    Buf *b = bfind(m, bno);
    int i;
    m->n_bread++;
    if (b) return b;
    for (i = 0; i < CACHE_N; i++)
        if (!m->cache[i].valid) {
            b = &m->cache[i];
            b->bno = bno; b->valid = 1; b->dirty = 0;
            memcpy(b->data, m->disk + (size_t)bno * BS, BS);
            return b;
        }
    /* 缓存满但还有脏块：事务过大，先提交（xv6 会 panic，这里宽容处理） */
    if (commit(m) != 0) return 0;
    b = &m->cache[0];
    b->bno = bno; b->valid = 1; b->dirty = 0;
    memcpy(b->data, m->disk + (size_t)bno * BS, BS);
    return b;
}

/* ---------- 日志（log.c） ---------- */
static void log_write(Mfs *m, Buf *b)
{
    int i;
    b->dirty = 1;
    for (i = 0; i < m->log_n; i++)
        if (m->log_bno[i] == b->bno) { memcpy(m->log_data[i], b->data, BS); return; }
    if (m->log_n >= LOG_SLOTS) { printf("minifs: transaction full\n"); return; }
    m->log_bno[m->log_n] = b->bno;
    memcpy(m->log_data[m->log_n], b->data, BS);
    m->log_n++;
}

static int commit(Mfs *m)
{
    unsigned char hdr[BS];
    int i;
    if (m->log_n == 0) return 0;
    if (m->crashed) { m->log_n = 0; return -1; }
    /* 1. 日志内容写入日志区（崩溃在此前/中 → 头无效 → 整个事务作废） */
    for (i = 0; i < m->log_n; i++)
        if (!pwrite_blk(m, LOG_SLOT0 + i, m->log_data[i])) { m->log_n = 0; return -1; }
    /* 2. 日志头：magic + count + 目标块表（"屏障"= 之前都已落盘） */
    memset(hdr, 0, sizeof hdr);
    put32(hdr, LOG_MAGIC);
    put16(hdr + 4, (unsigned)m->log_n);
    for (i = 0; i < m->log_n; i++) put16(hdr + 8 + 2 * i, (unsigned)m->log_bno[i]);
    if (!pwrite_blk(m, LOG_HDR, hdr)) { m->log_n = 0; return -1; }
    /* 3. 拷回目标块（崩溃在此之间 → 重放补齐，redo-all 幂等） */
    for (i = 0; i < CACHE_N; i++)
        if (m->cache[i].valid && m->cache[i].dirty)
            if (!pwrite_blk(m, m->cache[i].bno, m->cache[i].data)) { m->log_n = 0; return -1; }
    /* 4. 清头 = 事务完成 */
    memset(hdr, 0, sizeof hdr);
    pwrite_blk(m, LOG_HDR, hdr);
    for (i = 0; i < CACHE_N; i++) m->cache[i].dirty = 0;
    m->n_commit++;
    m->log_n = 0;
    return 0;
}

void fs_set_crash_at(Mfs *m, int op) { m->crash_at = op; m->ops_done = 0; m->crashed = 0; }
int  fs_crashed(Mfs *m) { return m->crashed; }
int  fs_commit(Mfs *m) { return commit(m); }

/* ---------- inode / 位图 ---------- */
static int rd_ino(Mfs *m, int inum, INode *n)
{
    Buf *b; unsigned char *p; int i;
    if (inum < 0 || inum >= NINODE) return -1;
    b = bread(m, INO_START + inum / INO_PER);
    if (!b) return -1;
    p = b->data + (inum % INO_PER) * 32;
    n->type = p[0];
    n->size = (unsigned)get32(p + 4);
    for (i = 0; i < NADDR; i++) n->a[i] = (unsigned short)get16(p + 8 + 2 * i);
    return 0;
}

static int wr_ino(Mfs *m, int inum, const INode *n)
{
    Buf *b; unsigned char *p; int i;
    b = bread(m, INO_START + inum / INO_PER);
    if (!b) return -1;
    p = b->data + (inum % INO_PER) * 32;
    memset(p, 0, 32);
    p[0] = (unsigned char)n->type;
    put32(p + 4, n->size);
    for (i = 0; i < NADDR; i++) put16(p + 8 + 2 * i, n->a[i]);
    log_write(m, b);
    return 0;
}

static void bmp_set(Mfs *m, int base, int idx, int v)
{
    Buf *b = bread(m, BMP_BNO);
    if (!b) return;
    if (v) b->data[base + idx / 8] |= (unsigned char)(1u << (idx % 8));
    else   b->data[base + idx / 8] &= (unsigned char)~(1u << (idx % 8));
    log_write(m, b);
}
static int bmp_get(Mfs *m, int base, int idx)
{
    Buf *b = bread(m, BMP_BNO);
    if (!b) return 1;
    return (b->data[base + idx / 8] >> (idx % 8)) & 1;
}

static int balloc(Mfs *m)
{
    int i;
    for (i = DATA_START; i < NB; i++) if (!bmp_get(m, 0, i)) { bmp_set(m, 0, i, 1); return i; }
    return -1;
}
static void bfree(Mfs *m, int bno) { if (bno > 0) bmp_set(m, 0, bno, 0); }

static int ialloc(Mfs *m)
{
    int i;
    for (i = 1; i < NINODE; i++) if (!bmp_get(m, 40, i)) { bmp_set(m, 40, i, 1); return i; }
    return -1;
}
static void ifree(Mfs *m, int inum) { bmp_set(m, 40, inum, 0); }

/* ---------- 目录：16B 条目 = inum(2) + name[14] ---------- */
#define DENT 16

static int dir_find(Mfs *m, int dir, const char *name)
{
    INode n; int blk, k;
    if (rd_ino(m, dir, &n)) return -1;
    for (blk = 0; blk < NADDR; blk++) {
        Buf *b;
        if (!n.a[blk]) continue;
        b = bread(m, n.a[blk]);
        if (!b) return -1;
        for (k = 0; k < BS / DENT; k++) {
            unsigned char *e = b->data + k * DENT;
            if (get16(e) != 0 && strncmp((const char *)e + 2, name, 13) == 0)
                return (int)get16(e);
        }
    }
    return -1;
}

static int dir_add(Mfs *m, int dir, const char *name, int inum)
{
    INode n; int blk;
    if (rd_ino(m, dir, &n)) return -1;
    for (blk = 0; blk < NADDR; blk++) {
        Buf *b;
        if (!n.a[blk]) {
            int nb = balloc(m);
            if (nb < 0) return -1;
            n.a[blk] = (unsigned short)nb;
            b = bread(m, nb);
            if (!b) return -1;
            memset(b->data, 0, BS);
            log_write(m, b);
        } else {
            b = bread(m, n.a[blk]);
            if (!b) return -1;
        }
        { int k;
          for (k = 0; k < BS / DENT; k++) {
              unsigned char *e = b->data + k * DENT;
              if (get16(e) == 0) {
                  put16(e, (unsigned)inum);
                  strncpy((char *)e + 2, name, 13);
                  e[15] = 0;
                  log_write(m, b);
                  return 0;
              }
          } }
    }
    return -1; /* 目录满或文件过大 */
}

static int dir_del(Mfs *m, int dir, const char *name)
{
    INode n; int blk, k;
    if (rd_ino(m, dir, &n)) return -1;
    for (blk = 0; blk < NADDR; blk++) {
        Buf *b;
        if (!n.a[blk]) continue;
        b = bread(m, n.a[blk]);
        if (!b) return -1;
        for (k = 0; k < BS / DENT; k++) {
            unsigned char *e = b->data + k * DENT;
            if (get16(e) != 0 && strncmp((const char *)e + 2, name, 13) == 0) {
                put16(e, 0);
                log_write(m, b);
                return 0;
            }
        }
    }
    return -1;
}

/* namei："a/b/c" → 返回值=目标 inum（存在）；
 * 不存在返回 -1 且 *parent/last 给出父目录与末段名；路径断裂返回 -2。 */
static int namei(Mfs *m, const char *path, char *last, int *parent)
{
    char comp[16];
    const char *p = path;
    int cur = 0;
    if (last) last[0] = 0;
    if (parent) *parent = -1;
    while (*p == '/') p++;
    if (!*p) return 0; /* 根 */
    for (;;) {
        const char *s = p;
        size_t len;
        int next;
        INode n;
        while (*p && *p != '/') p++;
        len = (size_t)(p - s);
        if (len == 0 || len >= sizeof comp) return -2;
        memcpy(comp, s, len);
        comp[len] = 0;
        while (*p == '/') p++;
        next = dir_find(m, cur, comp);
        if (!*p) { /* comp 是最后一段 */
            if (last) strcpy(last, comp);
            if (parent) *parent = cur;
            return next;
        }
        if (next < 0) return -2;
        if (rd_ino(m, next, &n) || n.type != I_DIR) return -2;
        cur = next;
    }
}

static FOpen ofiles[16];

/* ---------- 事务壳子 ---------- */
static int tx_begin(Mfs *m) { return m->crashed ? -2 : 0; }
static int tx_end(Mfs *m)
{
    if (m->crashed) return -2;
    if (m->batch > 1) return 0; /* 批提交模式（fssched 式）：攒够一起 commit */
    return commit(m) == 0 ? 0 : -2;
}

/* ---------- 对外 API ---------- */
int fs_mkfs(Mfs *m)
{
    unsigned char blk[BS];
    int i;
    memset(m->disk, 0, sizeof m->disk);
    memset(blk, 0, BS);
    put32(blk, FS_MAGIC);
    put16(blk + 4, NB);
    put16(blk + 6, NINODE);
    memcpy(m->disk + (size_t)SB_BNO * BS, blk, BS);
    memset(blk, 0, BS);
    for (i = 0; i < DATA_START; i++) blk[i / 8] |= (unsigned char)(1u << (i % 8));
    memcpy(m->disk + (size_t)BMP_BNO * BS, blk, BS);
    { INode n; /* 根目录：type=DIR，手写进 inode 区（格式化绕过日志） */
      unsigned char *p = m->disk + (size_t)INO_START * BS;
      memset(&n, 0, sizeof n);
      n.type = I_DIR;
      p[0] = (unsigned char)n.type;
      put32(p + 4, 0);
      memset(m->cache, 0, sizeof m->cache);
      memset(ofiles, 0, sizeof ofiles); }
    m->log_n = 0; m->crashed = 0; m->crash_at = 0;
    m->n_pwrite = m->n_bread = m->n_commit = 0;
    m->batch = 1;
    return 0;
}

int fs_mount(Mfs *m)
{
    unsigned char *hdr = m->disk + (size_t)LOG_HDR * BS;
    if (get32(hdr) == LOG_MAGIC) { /* redo 重放：幂等，全量再拷一遍 */
        int count = (int)get16(hdr + 4), i, keep = m->crash_at;
        m->crash_at = 0; /* 恢复期间不许再"崩" */
        for (i = 0; i < count && i < LOG_SLOTS; i++) {
            int target = (int)get16(hdr + 8 + 2 * i);
            memcpy(m->disk + (size_t)target * BS,
                   m->disk + (size_t)(LOG_SLOT0 + i) * BS, BS);
        }
        memset(m->disk + (size_t)LOG_HDR * BS, 0, BS);
        m->crash_at = keep;
        printf("minifs: log replayed (%d blocks)\n", count);
    }
    memset(m->cache, 0, sizeof m->cache); /* 内存态全丢 = 未提交事务自动消失 */
    memset(ofiles, 0, sizeof ofiles);
    m->log_n = 0;
    m->crashed = 0;   /* "重启"抹平一切 */
    m->mounted = 1;
    return 0;
}

int fs_create(Mfs *m, const char *path)
{
    char name[16]; int parent, r, inum;
    INode n;
    if (tx_begin(m)) return -2;
    r = namei(m, path, name, &parent);
    if (r >= 0) { tx_end(m); return -1; }        /* 已存在 */
    if (r != -1 || parent < 0) { tx_end(m); return -1; }
    inum = ialloc(m);
    if (inum < 0) { tx_end(m); return -1; }
    memset(&n, 0, sizeof n); n.type = I_FILE;
    wr_ino(m, inum, &n);
    if (dir_add(m, parent, name, inum) < 0) { ifree(m, inum); tx_end(m); return -1; }
    return tx_end(m);
}

int fs_mkdir(Mfs *m, const char *path)
{
    char name[16]; int parent, r, inum;
    INode n;
    if (tx_begin(m)) return -2;
    r = namei(m, path, name, &parent);
    if (r >= 0 || r != -1 || parent < 0) { tx_end(m); return -1; }
    inum = ialloc(m);
    if (inum < 0) { tx_end(m); return -1; }
    memset(&n, 0, sizeof n); n.type = I_DIR;
    wr_ino(m, inum, &n);
    if (dir_add(m, parent, name, inum) < 0) { ifree(m, inum); tx_end(m); return -1; }
    return tx_end(m);
}

int fs_open(Mfs *m, const char *path, int writable)
{
    char name[16]; int parent, in;
    INode n;
    int i;
    (void)name; (void)parent;
    in = namei(m, path, name, &parent);
    if (in < 0) return -1;
    if (rd_ino(m, in, &n) || n.type != I_FILE) return -1;
    for (i = 0; i < 16; i++)
        if (!ofiles[i].in_use) {
            ofiles[i].in_use = 1; ofiles[i].inum = in;
            ofiles[i].off = writable ? (int)n.size : 0;
            ofiles[i].writable = writable;
            return i;
        }
    return -1;
}

int fs_write(Mfs *m, int fd, const void *data, int n)
{
    FOpen *o;
    INode in;
    const unsigned char *p = (const unsigned char *)data;
    int done = 0;
    if (fd < 0 || fd >= 16 || !ofiles[fd].in_use) return -1;
    if (tx_begin(m)) return -2;
    o = &ofiles[fd];
    if (rd_ino(m, o->inum, &in)) { tx_end(m); return -1; }
    while (done < n) {
        int bidx = o->off / BS, boff = o->off % BS;
        int cnt = BS - boff;
        Buf *b;
        if (cnt > n - done) cnt = n - done;
        if (bidx >= NADDR) { printf("minifs: file too big (no indirect blocks)\n"); break; }
        if (!in.a[bidx]) {
            int nb = balloc(m);
            if (nb < 0) break;
            in.a[bidx] = (unsigned short)nb;
        }
        b = bread(m, in.a[bidx]);
        if (!b) break;
        memcpy(b->data + boff, p + done, (size_t)cnt);
        log_write(m, b);
        o->off += cnt; done += cnt;
        if ((unsigned)o->off > in.size) in.size = (unsigned)o->off;
    }
    wr_ino(m, o->inum, &in);
    if (tx_end(m) == -2) return -2;
    return done;
}

int fs_read(Mfs *m, int fd, void *data, int n)
{
    FOpen *o;
    INode in;
    unsigned char *p = (unsigned char *)data;
    int done = 0;
    if (fd < 0 || fd >= 16 || !ofiles[fd].in_use) return -1;
    o = &ofiles[fd];
    if (rd_ino(m, o->inum, &in)) return -1;
    while (done < n && o->off < (int)in.size) {
        int bidx = o->off / BS, boff = o->off % BS;
        int cnt = BS - boff, avail = (int)in.size - o->off;
        Buf *b;
        if (cnt > n - done) cnt = n - done;
        if (cnt > avail) cnt = avail;
        b = bread(m, in.a[bidx]);
        if (!b) break;
        memcpy(p + done, b->data + boff, (size_t)cnt);
        o->off += cnt; done += cnt;
    }
    return done;
}

int fs_close(Mfs *m, int fd)
{
    if (fd < 0 || fd >= 16) return -1;
    ofiles[fd].in_use = 0;
    (void)m;
    return 0;
}

int fs_unlink(Mfs *m, const char *path)
{
    char name[16]; int parent, r, in, i;
    INode n;
    if (tx_begin(m)) return -2;
    r = namei(m, path, name, &parent);
    in = r;
    if (in < 0) { tx_end(m); return -1; }
    dir_del(m, parent, name);
    if (rd_ino(m, in, &n) == 0) {
        for (i = 0; i < NADDR; i++) if (n.a[i]) bfree(m, n.a[i]);
        memset(&n, 0, sizeof n);
        wr_ino(m, in, &n);
    }
    ifree(m, in);
    return tx_end(m);
}

int fs_stat_size(Mfs *m, const char *path)
{
    char name[16]; int parent, in;
    INode n;
    (void)name; (void)parent;
    in = namei(m, path, name, &parent);
    if (in < 0 || rd_ino(m, in, &n)) return -1;
    return (int)n.size;
}

void fs_ls(Mfs *m, const char *path, void (*cb)(const char *, int, int, int))
{
    INode n;
    int in, blk, k;
    char name[16]; int parent;
    (void)name; (void)parent;
    in = namei(m, path, name, &parent);
    if (in < 0 || rd_ino(m, in, &n) || n.type != I_DIR) return;
    for (blk = 0; blk < NADDR; blk++) {
        Buf *b;
        if (!n.a[blk]) continue;
        b = bread(m, n.a[blk]);
        if (!b) return;
        for (k = 0; k < BS / DENT; k++) {
            unsigned char *e = b->data + k * DENT;
            int ino = (int)get16(e);
            INode cn;
            if (!ino) continue;
            if (rd_ino(m, ino, &cn) == 0)
                cb((const char *)e + 2, ino, cn.type, (int)cn.size);
        }
    }
}

void fs_dump_stats(Mfs *m, const char *tag)
{
    printf("[minifs %s] pwrites=%ld breads=%ld commits=%ld batch=%d %s\n",
           tag, m->n_pwrite, m->n_bread, m->n_commit, m->batch,
           m->crashed ? "*** CRASHED: remount to recover ***" : "");
}
