#!/usr/bin/env bash
# courses 配套代码聚合编译脚本 — Ubuntu 24.04+ (latest)
#
# 用法:
#   ./build-all-ubuntu.sh              # 编译全部核心课项目
#   ./build-all-ubuntu.sh --deps       # 先 apt 安装所需工具链，再编译
#   ./build-all-ubuntu.sh --check      # 只做语法级检查(py_compile/编译 -fsyntax-only)
#   ./build-all-ubuntu.sh <课程路径>    # 限定单课，如: 计算机系统基础/CSAPP
#
# 工具链: gcc/g++ build-essential · python3 · default-jdk(17+) · golang · iverilog

set -uo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
LOGDIR="$ROOT/.build-logs"
CHECK=0; ONLY=""

for arg in "$@"; do
  case "$arg" in
    --check) CHECK=1 ;;
    --deps)
      echo "== 安装工具链 (需要 sudo) =="
      sudo apt-get update
      sudo apt-get install -y build-essential python3 default-jdk golang-go iverilog
      ;;
    *) ONLY="$ROOT/${arg#./}" ;;
  esac
done

command -v gcc   >/dev/null || { echo "缺少 gcc（或先跑 --deps）"; exit 1; }
command -v g++   >/dev/null || { echo "缺少 g++"; exit 1; }
command -v python3 >/dev/null || { echo "缺少 python3"; exit 1; }

mkdir -p "$LOGDIR"
PASS=0; FAIL=0; SKIP=0
FAILED=()

run() { # <proj> <desc> <cmd...>
  local proj="$1"; shift
  local desc="$1"; shift
  local rel="${proj#"$ROOT"/}"
  echo "==> [$desc] $rel"
  # 单项目硬超时 240s：仿真/REPL 类挂死记为 FAIL，不再拖满整条 CI。
  if ( cd "$proj" && timeout -k 10 240 "$@" ) >"$LOGDIR/$(echo "$rel" | tr '/' '_').log" 2>&1; then
    PASS=$((PASS+1))
  else
    FAIL=$((FAIL+1)); FAILED+=("$rel [$desc]")
    tail -n 15 "$LOGDIR/$(echo "$rel" | tr '/' '_').log" | sed 's/^/    /'
  fi
}

for proj in "$ROOT"/*/*/projects/* "$ROOT"/*/*/*/projects/* "$ROOT"/*/*/*/*/projects/*; do
  [ -d "$proj" ] || continue
  if [ -n "$ONLY" ]; then
    case "$proj" in "$ONLY"/*) : ;; *) continue ;; esac
  fi
  rel="${proj#"$ROOT"/}"

  # 优先使用项目自带 build.sh
  if [ -f "$proj/build.sh" ]; then
    run "$proj" build.sh bash build.sh
    continue
  fi

  # 按语言自动识别
  if compgen -G "$proj/*.py" >/dev/null; then
    run "$proj" "python py_compile" python3 -m compileall -q "$proj"
  elif compgen -G "$proj/*.go" >/dev/null || [ -f "$proj/go.mod" ]; then
    command -v go >/dev/null && run "$proj" go go build ./... || SKIP=$((SKIP+1))
  elif compgen -G "$proj/*.java" >/dev/null; then
    command -v javac >/dev/null && {
      srcs=$(find "$proj" -name '*.java')
      run "$proj" javac javac -d "$proj/out" $srcs
    } || SKIP=$((SKIP+1))
  elif compgen -G "$proj/*.cpp" >/dev/null; then
    srcs=$(find "$proj" -name '*.cpp')
    if [ "$CHECK" -eq 1 ]; then
      run "$proj" g++-check g++ -std=c++17 -fsyntax-only $srcs
    else
      run "$proj" g++ g++ -std=c++17 -pthread $srcs -o "$proj/out_bin"
    fi
  elif compgen -G "$proj/*.c" >/dev/null; then
    srcs=$(find "$proj" -name '*.c')
    if [ "$CHECK" -eq 1 ]; then
      run "$proj" gcc-check gcc -std=c11 -fsyntax-only $srcs
    else
      run "$proj" gcc gcc -std=c11 -pthread $srcs -o "$proj/out_bin"
    fi
  elif compgen -G "$proj/*.v" >/dev/null; then
    command -v iverilog >/dev/null && {
      srcs=$(find "$proj" -name '*.v')
      run "$proj" iverilog iverilog -g2005 -o "$proj/out_sim" $srcs
    } || SKIP=$((SKIP+1))
  else
    SKIP=$((SKIP+1))
  fi
done

echo
echo "结果: PASS=$PASS FAIL=$FAIL SKIP=$SKIP  (日志: $LOGDIR)"
for f in "${FAILED[@]:-}"; do [ -n "$f" ] && echo "  FAIL: $f"; done
[ "$FAIL" -eq 0 ]
