# 《刷酸医美：刷出好气色》部署指南

## 📦 发布包说明

**文件名**: `release.zip`
**大小**: 1.8 MB
**包含**: 完整的静态网站文件 (152个文件)

## 🚀 快速部署

### 方法一：Web服务器部署

1.**下载并解压**
   ```bash
   unzip release.zip
   cd site/
   ```

2.**配置Web服务器**
   -**Nginx**: 将 `site/` 目录设为网站根目录
   -**Apache**: 将 `site/` 目录设为 DocumentRoot
   -**IIS**: 将 `site/` 目录设为网站物理路径

3.**访问网站**
   - 通过浏览器访问配置的域名或IP地址

### 方法二：本地预览

```bash
# 解压文件
unzip release.zip
cd site/

# 使用Python启动本地服务器
python3 -m http.server 8000

# 或使用PHP
php -S localhost:8000

# 或使用Node.js
npx serve . -p 8000
```

然后访问 `http://localhost:8000`

## 📱 网站特性

- ✅**响应式设计**: 完美支持手机、平板、电脑
- ✅**全文搜索**: 支持中文搜索，快速定位内容
- ✅**主题切换**: 明暗主题自由切换
- ✅**导航便捷**: 多级导航，章节目录
- ✅**打印友好**: 优化的打印样式
- ✅**离线可用**: 无需网络连接即可使用
- ✅**SEO优化**: 搜索引擎友好

## 🎨 定制说明

### Logo和Favicon
-**Logo**: `images/branding/logo.png`
-**Favicon**: `images/branding/favicon.png`
- 已使用指定的 https://docs.bccsw.cn/ 资源

### 样式定制
- 主样式文件: `stylesheets/extra.css`
- 主题色: Teal (青色)
- 字体: Noto Sans SC (中文)

### 内容更新
- 所有Markdown源文件已编译为HTML
- 如需更新内容，需要重新构建

## 📊 内容统计

-**总字数**: 118,554字
-**完成度**: 98.8% (接近12万字目标)
-**章节数**: 14个主要章节
-**附录数**: 4个实用附录
-**图表数**: 18个SVG专业图表

## 🔧 技术规格

-**生成工具**: MkDocs + Material主题
-**兼容性**: 支持所有现代浏览器
-**移动端**: 完全响应式设计
-**搜索**: 客户端JavaScript搜索
-**加载速度**: 优化的静态文件，快速加载

## 📄 文件结构

```
site/
├── index.html              # 首页
├── search/                 # 搜索功能
├── chapters/               # 章节页面
├── appendix/               # 附录页面
├── about/                  # 关于页面
├── images/                 # 图片资源
├── stylesheets/            # 样式文件
├── javascripts/            # JavaScript文件
└── README.md              # 说明文档
```

## 🌐 服务器配置建议

### Nginx配置示例
```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/site;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # 启用gzip压缩
    gzip on;
    gzip_types text/css application/javascript text/html;
}
```

### Apache配置示例
```apache
<VirtualHost *:80>
    ServerName your-domain.com
    DocumentRoot /path/to/site
    
    # 启用压缩
    LoadModule deflate_module modules/mod_deflate.so
    <Location />
        SetOutputFilter DEFLATE
    </Location>
</VirtualHost>
```

## 🔒 安全建议

1. **HTTPS**: 建议使用SSL证书启用HTTPS
2.**访问控制**: 根据需要设置访问权限
3.**备份**: 定期备份网站文件
4.**更新**: 保持服务器软件更新

## 📞 技术支持

如遇到部署问题，请检查：
1. Web服务器是否正确配置
2. 文件权限是否正确
3. 浏览器是否支持现代Web标准

---

**部署完成后，您将拥有一个专业的刷酸医美知识网站！** 🎉
