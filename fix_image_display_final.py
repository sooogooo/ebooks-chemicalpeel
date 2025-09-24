#!/usr/bin/env python3
"""
修复图片显示问题的最终脚本
将HTML div容器内的Markdown图片语法转换为纯Markdown格式
"""

import os
import re
import glob

def fix_image_display():
    """修复所有Markdown文件中的图片显示问题"""
    
    # 定义需要处理的目录
    directories = [
        'docs/chapters',
        'docs/appendix', 
        'docs/about'
    ]
    
    # 图片容器模式：匹配 <div class="image-container"> ... </div>
    container_pattern = r'<div class="image-container">\s*!\[([^\]]*)\]\(([^)]+)\)\s*<p><em>([^<]*)</em></p>\s*</div>'
    
    fixed_files = []
    
    for directory in directories:
        if not os.path.exists(directory):
            print(f"目录不存在: {directory}")
            continue
            
        # 查找所有Markdown文件
        md_files = glob.glob(f"{directory}/*.md")
        
        for file_path in md_files:
            if file_path.endswith('.backup'):
                continue
                
            print(f"处理文件: {file_path}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # 替换图片容器为纯Markdown格式
                def replace_container(match):
                    alt_text = match.group(1)
                    image_path = match.group(2)
                    caption = match.group(3)
                    
                    return f"""![{alt_text}]({image_path})

*{caption}*"""
                
                content = re.sub(container_pattern, replace_container, content, flags=re.MULTILINE | re.DOTALL)
                
                # 如果内容有变化，写回文件
                if content != original_content:
                    # 创建备份
                    backup_path = file_path + '.display_backup'
                    if not os.path.exists(backup_path):
                        with open(backup_path, 'w', encoding='utf-8') as f:
                            f.write(original_content)
                    
                    # 写入修复后的内容
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    fixed_files.append(file_path)
                    print(f"  ✅ 已修复图片显示")
                else:
                    print(f"  ℹ️  无需修复")
                    
            except Exception as e:
                print(f"  ❌ 处理失败: {e}")
    
    print(f"\n修复完成！共处理了 {len(fixed_files)} 个文件:")
    for file_path in fixed_files:
        print(f"  - {file_path}")

def verify_image_syntax():
    """验证图片语法是否正确"""
    print("\n验证图片语法...")
    
    directories = ['docs/chapters', 'docs/appendix', 'docs/about']
    
    for directory in directories:
        if not os.path.exists(directory):
            continue
            
        md_files = glob.glob(f"{directory}/*.md")
        
        for file_path in md_files:
            if file_path.endswith('.backup'):
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 查找图片引用
                image_refs = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
                
                if image_refs:
                    print(f"\n📁 {file_path}:")
                    for alt_text, image_path in image_refs:
                        print(f"  🖼️  {alt_text}: {image_path}")
                        
            except Exception as e:
                print(f"  ❌ 读取失败: {e}")

if __name__ == "__main__":
    print("🔧 开始修复图片显示问题...")
    fix_image_display()
    verify_image_syntax()
    print("\n🎉 修复完成！请重启MkDocs服务查看效果。")
