#!/bin/bash

# 刷酸医美电子书部署脚本
# 用于启动MkDocs开发服务器并进行必要的检查

echo "🚀 开始部署刷酸医美电子书..."

# 检查当前目录
if [ ! -f "mkdocs.yml" ]; then
    echo "❌ 错误：未找到 mkdocs.yml 文件，请确保在项目根目录运行此脚本"
    exit 1
fi

# 检查Python和pip
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 python3，请先安装Python 3.7+"
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "❌ 错误：未找到 pip3，请先安装pip"
    exit 1
fi

# 检查并安装依赖
echo "📦 检查依赖..."
if ! python3 -c "import mkdocs" 2>/dev/null; then
    echo "📥 安装MkDocs依赖..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败，请检查网络连接或权限"
        exit 1
    fi
else
    echo "✅ 依赖已安装"
fi

# 检查关键文件
echo "🔍 检查关键文件..."

# 检查docs目录结构
required_dirs=("docs" "docs/chapters" "docs/images" "docs/stylesheets" "docs/javascripts" "docs/appendix" "docs/about")
for dir in "${required_dirs[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "❌ 缺少目录: $dir"
        exit 1
    fi
done

# 检查关键文件
required_files=("docs/index.md" "docs/stylesheets/extra.css" "mkdocs.yml")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ 缺少文件: $file"
        exit 1
    fi
done

# 检查图片文件
image_count=$(find docs/images -name "*.svg" | wc -l)
if [ "$image_count" -lt 10 ]; then
    echo "⚠️  警告：图片文件数量较少 ($image_count 个)，可能影响显示效果"
else
    echo "✅ 图片文件检查通过 ($image_count 个SVG文件)"
fi

# 检查章节文件
chapter_count=$(find docs/chapters -name "*.md" | wc -l)
if [ "$chapter_count" -lt 10 ]; then
    echo "⚠️  警告：章节文件数量较少 ($chapter_count 个)"
else
    echo "✅ 章节文件检查通过 ($chapter_count 个章节)"
fi

# 运行图片修复脚本（如果存在）
if [ -f "fix_images.py" ]; then
    echo "🔧 运行图片修复脚本..."
    python3 fix_images.py
fi

# 检查端口占用
PORT=8000
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  端口 $PORT 已被占用，尝试终止现有进程..."
    pkill -f "mkdocs serve"
    sleep 2
fi

# 构建静态文件（可选）
if [ "$1" = "--build" ]; then
    echo "🏗️  构建静态文件..."
    mkdocs build
    if [ $? -eq 0 ]; then
        echo "✅ 静态文件构建完成，输出目录: site/"
        echo "📁 可以将 site/ 目录部署到任何静态文件服务器"
    else
        echo "❌ 构建失败"
        exit 1
    fi
    exit 0
fi

# 启动开发服务器
echo "🌐 启动MkDocs开发服务器..."
echo "📍 服务地址: http://localhost:$PORT"
echo "📍 服务地址: http://127.0.0.1:$PORT"
echo ""
echo "💡 使用说明:"
echo "   - 按 Ctrl+C 停止服务器"
echo "   - 修改文件后会自动重新加载"
echo "   - 使用 --build 参数构建静态文件"
echo ""
echo "🎉 电子书部署完成，开始享受阅读吧！"
echo ""

# 启动服务器
mkdocs serve --dev-addr=0.0.0.0:$PORT

# 如果服务器意外停止
echo ""
echo "📴 服务器已停止"
