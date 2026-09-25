#!/usr/bin/env bash
# 语法自检：python3 -m py_compile chat_tcp.py chat_udp.py
set -e
cd "$(dirname "$0")"
python3 -m py_compile chat_tcp.py chat_udp.py
case "${1:-server}" in
  server) python3 chat_tcp.py --server ;;
  client) python3 chat_tcp.py --name "${2:-guest}" ;;
  udp-server) python3 chat_udp.py --server ;;
  udp-client) python3 chat_udp.py --name "${2:-guest}" ;;
  *) echo "usage: $0 [server|client <name>|udp-server|udp-client <name>]"; exit 2 ;;
esac
