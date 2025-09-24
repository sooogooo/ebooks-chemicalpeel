#!/bin/bash

echo "🚀 开始自动优化..."

# 1. 优化SVG图片
echo "📊 优化SVG图片..."
python3 scripts/optimize-images.py

# 2. 检查Markdown文件
echo "📝 检查Markdown文件..."
if [ -f "check_and_fix.py" ]; then
    python3 check_and_fix.py
fi

# 3. 构建项目
echo "🔨 构建项目..."
mkdocs build --clean

# 4. 压缩静态文件
echo "📦 压缩静态文件..."
if command -v gzip &> /dev/null; then
    find site/ -name "*.html" -o -name "*.css" -o -name "*.js" | xargs gzip -k
fi

echo "✅ 优化完成！"
