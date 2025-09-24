#!/bin/bash

# 快速启动脚本
echo "🚀 启动《刷酸医美：输出好气色》电子书..."

# 检查是否在正确目录
if [ ! -f "mkdocs.yml" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

# 检查Python和MkDocs
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要安装Python3"
    exit 1
fi

# 尝试启动MkDocs
if command -v mkdocs &> /dev/null; then
    echo "✅ 找到MkDocs，启动服务器..."
    echo "📖 电子书地址: http://127.0.0.1:8000"
    echo "🔄 按 Ctrl+C 停止服务器"
    echo ""
    mkdocs serve
else
    echo "📦 MkDocs未安装，正在安装依赖..."
    pip3 install mkdocs mkdocs-material pymdown-extensions
    
    if [ $? -eq 0 ]; then
        echo "✅ 依赖安装完成，启动服务器..."
        echo "📖 电子书地址: http://127.0.0.1:8000"
        echo "🔄 按 Ctrl+C 停止服务器"
        echo ""
        mkdocs serve
    else
        echo "❌ 依赖安装失败，请手动安装：pip3 install -r requirements.txt"
        exit 1
    fi
fi
