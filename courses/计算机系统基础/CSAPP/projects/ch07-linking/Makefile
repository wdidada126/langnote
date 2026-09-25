# ch07-linking —— 静态库 / 动态库 / 符号解析演示（Linux/macOS + gcc）
# Windows 请用 build.bat（cl）。
CC      ?= gcc
CFLAGS  ?= -std=c99 -Wall -Wextra -O1
OBJDIR  := obj
BINDIR  := bin

OBJS := $(OBJDIR)/main.o $(OBJDIR)/vec.o $(OBJDIR)/weakdemo.o \
        $(OBJDIR)/strongdef.o $(OBJDIR)/foo.o $(OBJDIR)/bar.o

.PHONY: all dirs static order dyn run weak_demo clean

all: static order dyn

dirs:
	@mkdir -p $(OBJDIR) $(BINDIR)

$(OBJDIR)/%.o: src/%.c src/common.h | dirs
	$(CC) $(CFLAGS) -c $< -o $@

# ① 静态库：ar 归档 + 链接（依赖放在使用方之后）
$(BINDIR)/libvec.a: $(OBJDIR)/vec.o | dirs
	ar rcs $@ $^

static: $(BINDIR)/static_demo
$(BINDIR)/static_demo: $(OBJDIR)/main.o $(OBJDIR)/weakdemo.o $(OBJDIR)/foo.o \
                       $(BINDIR)/libvec.a $(BINDIR)/libb.a | dirs
	$(CC) $(CFLAGS) -o $@ $(OBJDIR)/main.o $(OBJDIR)/weakdemo.o \
	      $(OBJDIR)/foo.o $(BINDIR)/libb.a $(BINDIR)/libvec.a
	@echo "静态示例 → $(BINDIR)/static_demo （ar 只抽取被引用到的成员）"

# ② 链接顺序：正确（liba 在前、被依赖的 libb 在后）
$(BINDIR)/liba.a: $(OBJDIR)/foo.o | dirs
	ar rcs $@ $^
$(BINDIR)/libb.a: $(OBJDIR)/bar.o | dirs
	ar rcs $@ $^
order: $(BINDIR)/order_ok
$(BINDIR)/order_ok: $(OBJDIR)/main.o $(OBJDIR)/weakdemo.o \
                    $(BINDIR)/liba.a $(BINDIR)/libb.a $(BINDIR)/libvec.a | dirs
	$(CC) $(CFLAGS) -o $@ $(OBJDIR)/main.o $(OBJDIR)/weakdemo.o \
	      $(BINDIR)/liba.a $(BINDIR)/libb.a $(BINDIR)/libvec.a
	@echo "make order_bad 观察反序失败；两库互换后链接器一次扫描即弃"

order_bad: | dirs
	-$(CC) $(CFLAGS) -o $(BINDIR)/order_err $(OBJDIR)/main.o $(OBJDIR)/weakdemo.o \
	      $(BINDIR)/libb.a $(BINDIR)/liba.a $(BINDIR)/libvec.a
	@echo "^ 上一步【预期失败】：处理 libb 时无人引用 bar → 丢弃 → foo 未定义"

# ③ 弱/强符号实验：strongdef.o 以 -fcommon 链入 → 强胜弱(100)；
#    去掉 -fcommon（GCC≥10 默认）→ multiple definition 错误（规则 1）
weak_demo: $(OBJDIR)/main.o $(OBJDIR)/weakdemo.o $(OBJDIR)/strongdef.o \
           $(OBJDIR)/vec.o $(OBJDIR)/foo.o $(OBJDIR)/bar.o | dirs
	$(CC) $(CFLAGS) -fcommon -o $(BINDIR)/weak_demo $^
	@echo "运行 $(BINDIR)/weak_demo → shared_counter=100（强胜弱）"
	$(CC) $(CFLAGS) -o $(BINDIR)/weak_dup $^ 2>/dev/null || \
	  echo "不带 -fcommon 时链接失败：正是现代工具链对规则3的收紧"

# ④ 共享库 + dlopen
dyn: $(BINDIR)/dynload $(BINDIR)/libdyn.so
$(BINDIR)/libdyn.so: src/dynlib.c | dirs
	$(CC) $(CFLAGS) -fPIC -shared -o $@ $<
$(BINDIR)/dynload: src/dynload.c | dirs
	$(CC) $(CFLAGS) -o $@ $< -ldl

run: all
	cd $(BINDIR) && ./static_demo && ./order_ok && ./dynload

clean:
	rm -rf $(OBJDIR) $(BINDIR)
