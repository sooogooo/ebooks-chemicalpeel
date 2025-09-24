#!/bin/bash

# MkDocs服务管理脚本
MKDOCS_PORT=9112
MKDOCS_PID_FILE="mkdocs.pid"
MKDOCS_LOG_FILE="mkdocs_9112.log"
PROJECT_DIR="/home/sooogooo/AmazonQ/ebooks/ChemicalPell"

start_mkdocs() {
    echo "🚀 启动MkDocs服务在端口 $MKDOCS_PORT..."
    cd "$PROJECT_DIR"
    
    # 检查是否已经在运行
    if [ -f "$MKDOCS_PID_FILE" ] && kill -0 $(cat "$MKDOCS_PID_FILE") 2>/dev/null; then
        echo "⚠️  MkDocs服务已在运行 (PID: $(cat $MKDOCS_PID_FILE))"
        return 1
    fi
    
    # 启动服务
    nohup python3 -m mkdocs serve --dev-addr=0.0.0.0:$MKDOCS_PORT > "$MKDOCS_LOG_FILE" 2>&1 &
    echo $! > "$MKDOCS_PID_FILE"
    
    sleep 3
    
    # 验证启动
    if kill -0 $(cat "$MKDOCS_PID_FILE") 2>/dev/null; then
        echo "✅ MkDocs服务启动成功!"
        echo "📍 访问地址: http://localhost:$MKDOCS_PORT"
        echo "📄 日志文件: $MKDOCS_LOG_FILE"
        echo "🆔 进程ID: $(cat $MKDOCS_PID_FILE)"
    else
        echo "❌ MkDocs服务启动失败"
        rm -f "$MKDOCS_PID_FILE"
        return 1
    fi
}

stop_mkdocs() {
    echo "🛑 停止MkDocs服务..."
    
    if [ -f "$MKDOCS_PID_FILE" ]; then
        PID=$(cat "$MKDOCS_PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            kill "$PID"
            echo "✅ MkDocs服务已停止 (PID: $PID)"
        else
            echo "⚠️  进程不存在 (PID: $PID)"
        fi
        rm -f "$MKDOCS_PID_FILE"
    else
        echo "⚠️  未找到PID文件，尝试强制停止..."
        pkill -f "mkdocs.*$MKDOCS_PORT"
        echo "✅ 强制停止完成"
    fi
}

status_mkdocs() {
    echo "📊 MkDocs服务状态检查..."
    
    if [ -f "$MKDOCS_PID_FILE" ]; then
        PID=$(cat "$MKDOCS_PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            echo "✅ 服务运行中 (PID: $PID)"
            echo "📍 端口: $MKDOCS_PORT"
            echo "📄 日志: $MKDOCS_LOG_FILE"
            
            # 检查端口监听
            if ss -tlnp | grep ":$MKDOCS_PORT" > /dev/null; then
                echo "🌐 端口监听正常"
            else
                echo "⚠️  端口未监听"
            fi
        else
            echo "❌ 服务未运行 (PID文件存在但进程不存在)"
            rm -f "$MKDOCS_PID_FILE"
        fi
    else
        echo "❌ 服务未运行 (无PID文件)"
    fi
}

restart_mkdocs() {
    echo "🔄 重启MkDocs服务..."
    stop_mkdocs
    sleep 2
    start_mkdocs
}

show_logs() {
    echo "📄 显示MkDocs服务日志..."
    if [ -f "$MKDOCS_LOG_FILE" ]; then
        tail -f "$MKDOCS_LOG_FILE"
    else
        echo "❌ 日志文件不存在: $MKDOCS_LOG_FILE"
    fi
}

case "$1" in
    start)
        start_mkdocs
        ;;
    stop)
        stop_mkdocs
        ;;
    status)
        status_mkdocs
        ;;
    restart)
        restart_mkdocs
        ;;
    logs)
        show_logs
        ;;
    *)
        echo "使用方法: $0 {start|stop|status|restart|logs}"
        echo ""
        echo "命令说明:"
        echo "  start   - 启动MkDocs服务"
        echo "  stop    - 停止MkDocs服务"
        echo "  status  - 检查服务状态"
        echo "  restart - 重启服务"
        echo "  logs    - 查看服务日志"
        exit 1
        ;;
esac
