#!/usr/bin/env python3
"""
电子书内容检查和修复脚本
检查图片引用、Markdown格式等问题并自动修复
"""

import os
import re
import glob
from pathlib import Path

class EbookChecker:
    def __init__(self):
        self.issues = []
        self.fixes = []
        
    def log_issue(self, issue):
        """记录问题"""
        self.issues.append(issue)
        print(f"❌ {issue}")
        
    def log_fix(self, fix):
        """记录修复"""
        self.fixes.append(fix)
        print(f"✅ {fix}")
        
    def check_file_exists(self, file_path):
        """检查文件是否存在"""
        return Path(file_path).exists()
        
    def check_images(self):
        """检查图片文件和引用"""
        print("\n🖼️  检查图片文件...")
        
        # 检查图片目录
        image_dir = Path("docs/images")
        if not image_dir.exists():
            self.log_issue("图片目录 docs/images 不存在")
            return
            
        # 统计图片文件
        svg_files = list(image_dir.glob("*.svg"))
        png_files = list(image_dir.glob("*.png"))
        jpg_files = list(image_dir.glob("*.jpg"))
        
        print(f"📊 图片统计: {len(svg_files)} SVG, {len(png_files)} PNG, {len(jpg_files)} JPG")
        
        if len(svg_files) < 10:
            self.log_issue(f"SVG图片数量较少: {len(svg_files)}")
        else:
            self.log_fix(f"SVG图片数量正常: {len(svg_files)}")
            
    def check_image_references(self):
        """检查图片引用"""
        print("\n🔗 检查图片引用...")
        
        # 获取所有Markdown文件
        md_files = []
        md_files.extend(glob.glob("docs/chapters/*.md"))
        md_files.extend(glob.glob("docs/appendix/*.md"))
        md_files.extend(glob.glob("docs/about/*.md"))
        md_files.extend(["docs/index.md", "docs/preface.md", "docs/introduction.md"])
        
        broken_refs = []
        
        for md_file in md_files:
            if not os.path.exists(md_file):
                continue
                
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 查找图片引用
            img_refs = re.findall(r'src="([^"]*images/[^"]*)"', content)
            
            for ref in img_refs:
                # 计算实际路径
                if md_file.startswith("docs/chapters/") or md_file.startswith("docs/appendix/") or md_file.startswith("docs/about/"):
                    actual_path = ref.replace("../", "docs/")
                else:
                    actual_path = ref.replace("./", "docs/").replace("images/", "docs/images/")
                    
                if not os.path.exists(actual_path):
                    broken_refs.append((md_file, ref, actual_path))
                    
        if broken_refs:
            for md_file, ref, actual_path in broken_refs:
                self.log_issue(f"图片引用错误: {md_file} -> {ref} (实际路径: {actual_path})")
        else:
            self.log_fix("所有图片引用检查通过")
            
    def fix_image_containers(self):
        """修复图片容器格式"""
        print("\n🔧 修复图片容器...")
        
        md_files = glob.glob("docs/chapters/*.md") + glob.glob("docs/appendix/*.md")
        fixed_count = 0
        
        for md_file in md_files:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_content = content
            
            # 修复图片容器的开始标签
            content = re.sub(
                r'<div class="image-container"[^>]*>',
                '<div class="image-container">',
                content
            )
            
            # 修复img标签，移除内联样式
            content = re.sub(
                r'<img src="([^"]*)" alt="([^"]*)"[^>]*>',
                r'<img src="\1" alt="\2">',
                content
            )
            
            # 修复图片说明的p标签
            content = re.sub(
                r'<p style="[^"]*"><em>([^<]*)</em></p>',
                r'<p><em>\1</em></p>',
                content
            )
            
            if content != original_content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1
                
        if fixed_count > 0:
            self.log_fix(f"修复了 {fixed_count} 个文件的图片容器")
        else:
            self.log_fix("图片容器格式正常")
            
    def check_markdown_syntax(self):
        """检查Markdown语法"""
        print("\n📝 检查Markdown语法...")
        
        md_files = glob.glob("docs/**/*.md", recursive=True)
        issues_found = 0
        
        for md_file in md_files:
            with open(md_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines, 1):
                # 检查标题格式
                if line.startswith('#'):
                    if not line.startswith('# ') and len(line.strip()) > 1:
                        if not re.match(r'^#+\s', line):
                            self.log_issue(f"{md_file}:{i} 标题格式错误: {line.strip()}")
                            issues_found += 1
                            
        if issues_found == 0:
            self.log_fix("Markdown语法检查通过")
            
    def check_navigation(self):
        """检查导航配置"""
        print("\n🧭 检查导航配置...")
        
        if not os.path.exists("mkdocs.yml"):
            self.log_issue("mkdocs.yml 文件不存在")
            return
            
        with open("mkdocs.yml", 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查是否包含nav配置
        if "nav:" not in content:
            self.log_issue("mkdocs.yml 中缺少导航配置")
        else:
            self.log_fix("导航配置存在")
            
        # 检查导航中引用的文件是否存在
        nav_files = re.findall(r':\s*([^:\n]+\.md)', content)
        missing_files = []
        
        for nav_file in nav_files:
            nav_file = nav_file.strip()
            full_path = f"docs/{nav_file}"
            if not os.path.exists(full_path):
                missing_files.append(nav_file)
                
        if missing_files:
            for missing in missing_files:
                self.log_issue(f"导航中引用的文件不存在: {missing}")
        else:
            self.log_fix("导航引用的文件都存在")
            
    def generate_report(self):
        """生成检查报告"""
        print("\n" + "="*60)
        print("📋 检查报告")
        print("="*60)
        
        print(f"\n❌ 发现问题: {len(self.issues)} 个")
        for issue in self.issues:
            print(f"   • {issue}")
            
        print(f"\n✅ 修复完成: {len(self.fixes)} 项")
        for fix in self.fixes:
            print(f"   • {fix}")
            
        if len(self.issues) == 0:
            print("\n🎉 恭喜！所有检查都通过了！")
        else:
            print(f"\n⚠️  还有 {len(self.issues)} 个问题需要手动处理")
            
    def run_all_checks(self):
        """运行所有检查"""
        print("🔍 开始全面检查电子书...")
        
        self.check_images()
        self.check_image_references()
        self.fix_image_containers()
        self.check_markdown_syntax()
        self.check_navigation()
        
        self.generate_report()

def main():
    """主函数"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    checker = EbookChecker()
    checker.run_all_checks()

if __name__ == '__main__':
    main()
