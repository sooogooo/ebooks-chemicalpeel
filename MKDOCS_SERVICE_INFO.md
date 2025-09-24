# MkDocs服务运行信息

## 🚀 服务状态

**✅ 服务已成功启动并在后台运行**

-**端口**: 9112
-**访问地址**: http://localhost:9112 或 http://0.0.0.0:9112
-**进程ID**: 7504
-**日志文件**: mkdocs_9112.log
-**启动方式**: nohup (不会因终端退出而停止)

## 📋 服务管理

### 使用管理脚本
```bash
# 检查服务状态
./manage_mkdocs.sh status

# 停止服务
./manage_mkdocs.sh stop

# 启动服务
./manage_mkdocs.sh start

# 重启服务
./manage_mkdocs.sh restart

# 查看实时日志
./manage_mkdocs.sh logs
```

### 手动管理命令
```bash
# 查看运行进程
ps aux | grep mkdocs | grep -v grep

# 检查端口监听
ss -tlnp | grep :9112

# 查看日志
tail -f mkdocs_9112.log

# 手动停止服务
kill 7504
# 或强制停止
pkill -f "mkdocs.*9112"
```

## 🔧 服务特性

### 后台运行保障
- ✅ 使用 `nohup` 启动，不受终端退出影响
- ✅ 进程独立运行，系统重启前持续服务
- ✅ 日志输出重定向到文件，便于调试

### 自动重载
- ✅ 监控 `docs/` 目录和 `mkdocs.yml` 文件变化
- ✅ 文件修改后自动重新构建
- ✅ 浏览器自动刷新显示最新内容

### 网络访问
- ✅ 绑定到 0.0.0.0:9112，支持外部访问
- ✅ 支持本地访问 http://localhost:9112
- ✅ 支持局域网访问 http://[服务器IP]:9112

## 📊 服务监控

### 健康检查
```bash
# 检查服务是否响应
curl -I http://localhost:9112

# 检查进程状态
kill -0 7504 && echo "服务运行中" || echo "服务已停止"

# 检查端口占用
lsof -i :9112 2>/dev/null || ss -tlnp | grep :9112
```

### 日志监控
```bash
# 查看最新日志
tail -20 mkdocs_9112.log

# 实时监控日志
tail -f mkdocs_9112.log

# 搜索错误日志
grep -i error mkdocs_9112.log
```

## 🛠️ 故障排除

### 常见问题

**1. 端口被占用**
```bash
# 查找占用端口的进程
ss -tlnp | grep :9112
# 停止占用进程
kill [PID]
```

**2. 服务无法启动**
```bash
# 检查日志错误
tail -50 mkdocs_9112.log
# 检查配置文件
python3 -m mkdocs build --verbose
```

**3. 页面无法访问**
```bash
# 检查防火墙设置
sudo ufw status
# 检查服务绑定地址
ss -tlnp | grep :9112
```

### 重新部署
```bash
# 完全重启服务
./manage_mkdocs.sh stop
./manage_mkdocs.sh start

# 清理并重新构建
rm -rf site/
python3 -m mkdocs build
./manage_mkdocs.sh restart
```

## 📈 性能优化

### 资源使用
-**内存使用**: 约64MB
-**CPU使用**: 低负载时 < 1%
-**磁盘IO**: 文件变化时短暂增加

### 优化建议
- 大文件修改时可能需要等待重新构建
- 图片较多时构建时间会增加
- 可考虑使用 `mkdocs build` 生成静态文件部署

## 🔒 安全注意事项

### 网络安全
- 服务绑定到 0.0.0.0，外部可访问
- 建议在生产环境中配置防火墙
- 考虑使用反向代理添加认证

### 文件安全
- 服务具有读取项目文件的权限
- 日志文件包含访问记录
- 定期清理日志文件避免占用过多空间

---

**服务启动时间**: 2025-08-14 20:05 UTC  
**当前状态**: ✅ 运行中  
**管理员**: Amazon Q  
**维护模式**: 自动化管理
