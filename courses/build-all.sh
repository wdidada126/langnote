#!/usr/bin/env bash
# courses 聚合编译/检查脚本（集中验证用；本轮开发时只写未执行）
#
# 用法：
#   ./build-all.sh            # 依次执行各课程 projects 下的 build.sh（C/C++/Java/Verilog/Go）
#   ./build-all.sh --check    # 不编译，只做语法级检查（python -m py_compile / javac -Xlint:none 可选关闭）
#   ./build-all.sh <课程路径>  # 只处理指定课程，如 计算机系统基础/CSAPP
#
# 语言覆盖：
#   - 有 build.sh 的项目：直接 bash build.sh（内部为 gcc/g++/javac/iverilog/go build 等）
#   - 无 build.sh 的 Python 项目：py_compile 语法检查
#   - 有 run.sh 的 Python 项目：仅提示，不自动运行（需人工确认）

set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"
CHECK=0
ONLY=""
for arg in "$@"; do
  case "$arg" in
    --check) CHECK=1 ;;
    *) ONLY="$ROOT/${arg#./}" ;;
  esac
done

PASS=0; FAIL=0; SKIP=0
FAILED_LIST=()

for proj in "$ROOT"/*/*/projects/* "$ROOT"/*/*/*/projects/*; do
  [ -d "$proj" ] || continue
  rel="${proj#"$ROOT"/}"
  if [ -n "$ONLY" ]; then
    case "$proj" in
      "$ONLY"/*) : ;;
      *) continue ;;
    esac
  fi
  if [ -f "$proj/build.sh" ]; then
    echo "==> [build] $rel"
    if (cd "$proj" && bash build.sh >/tmp/buildall.log 2>&1); then
      PASS=$((PASS+1))
    else
      FAIL=$((FAIL+1)); FAILED_LIST+=("$rel")
      tail -n 20 /tmp/buildall.log
    fi
  elif [ -f "$proj/run.sh" ] && [ "$CHECK" -eq 1 ]; then
    pys=$(find "$proj" -name "*.py")
    if [ -n "$pys" ]; then
      echo "==> [check] $rel (python)"
      if python3 -m py_compile $pys 2>/tmp/buildall.log; then
        PASS=$((PASS+1))
      else
        FAIL=$((FAIL+1)); FAILED_LIST+=("$rel"); tail -n 20 /tmp/buildall.log
      fi
    else
      SKIP=$((SKIP+1))
    fi
  else
    SKIP=$((SKIP+1))
  fi
done

echo
echo "结果: PASS=$PASS FAIL=$FAIL SKIP=$SKIP"
for f in "${FAILED_LIST[@]:-}"; do [ -n "$f" ] && echo "  FAIL: $f"; done
[ "$FAIL" -eq 0 ]
