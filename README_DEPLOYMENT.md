# 静态网站部署说明

## 快速部署

1. 解压 `cp0921.zip` 文件
2. 将解压后的 `site` 文件夹内容上传到您的Web服务器
3. 访问 `index.html` 即可查看网站

## 部署方式

### 方式一：直接解压部署
```bash
unzip cp0921.zip
# 将 site/ 目录下的所有文件复制到Web服务器根目录
```

### 方式二：本地测试
```bash
unzip cp0921.zip
cd site
python3 -m http.server 8000
# 访问 http://localhost:8000
```

### 方式三：Nginx部署
```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/site;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

## 文件结构

```
site/
├── index.html          # 首页
├── chapters/           # 章节页面
├── appendix/           # 附录页面
├── about/              # 关于页面
├── images/             # 图片资源
├── assets/             # CSS/JS资源
├── stylesheets/        # 样式文件
├── javascripts/        # 脚本文件
└── search/             # 搜索功能
```

## 特性

- ✅ 完全静态化，无需数据库
- ✅ 响应式设计，支持移动端
- ✅ 内置搜索功能
- ✅ 离线可用（PWA支持）
- ✅ SEO友好

## 系统要求

- 任何支持HTML5的Web服务器
- 无需PHP、数据库等后端支持
- 建议使用HTTPS协议

## 注意事项

- 确保Web服务器支持SVG文件类型
- 建议启用gzip压缩以提高加载速度
- 可配置CDN加速静态资源加载
