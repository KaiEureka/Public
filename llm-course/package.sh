#!/bin/bash
# Bundle the finished book, its sources and the experiment code (fonts and build/ are left out).
set -e
cd "$(dirname "$0")"
OUT="从零造一个前沿大模型_源文件与代码.zip"
rm -f "$OUT"
find code figs -name __pycache__ -prune -exec rm -rf {} +
zip -qr "$OUT" "从零造一个前沿大模型.pdf" README.md src figs code book.css template.html render.js \
    build.py fill_appC.py appC.template.md repro_verdict.txt package.sh INDEX.md make_index.py -x "*.DS_Store"
ls -la "$OUT"
