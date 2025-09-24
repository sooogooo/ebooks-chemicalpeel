#!/usr/bin/env python3
"""
最终修复图片路径脚本
解决MkDocs中图片无法显示的问题
"""

import os
import re
import glob

def fix_image_paths():
    """修复所有Markdown文件中的图片路径"""
    
    # 定义需要处理的目录
    directories = [
        'docs/chapters',
        'docs/appendix', 
        'docs/about'
    ]
    
    # 图片路径模式
    image_pattern = r'!\[([^\]]*)\]\(images/([^)]+)\)'
    
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
                
                # 修复图片路径：images/xxx.svg -> ../images/xxx.svg
                if directory == 'docs/chapters':
                    # 章节文件需要 ../images/
                    content = re.sub(image_pattern, r'![\1](../images/\2)', content)
                elif directory == 'docs/appendix':
                    # 附录文件需要 ../images/
                    content = re.sub(image_pattern, r'![\1](../images/\2)', content)
                elif directory == 'docs/about':
                    # 关于文件需要 ../images/
                    content = re.sub(image_pattern, r'![\1](../images/\2)', content)
                
                # 如果内容有变化，写回文件
                if content != original_content:
                    # 创建备份
                    backup_path = file_path + '.backup'
                    if not os.path.exists(backup_path):
                        with open(backup_path, 'w', encoding='utf-8') as f:
                            f.write(original_content)
                    
                    # 写入修复后的内容
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    fixed_files.append(file_path)
                    print(f"  ✅ 已修复图片路径")
                else:
                    print(f"  ℹ️  无需修复")
                    
            except Exception as e:
                print(f"  ❌ 处理失败: {e}")
    
    # 处理根目录的文档文件
    root_files = ['docs/index.md', 'docs/preface.md', 'docs/introduction.md', 'docs/epilogue.md']
    
    for file_path in root_files:
        if not os.path.exists(file_path):
            continue
            
        print(f"处理根目录文件: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 根目录文件直接使用 images/
            content = re.sub(r'!\[([^\]]*)\]\(\.\./images/([^)]+)\)', r'![\1](images/\2)', content)
            
            if content != original_content:
                # 创建备份
                backup_path = file_path + '.backup'
                if not os.path.exists(backup_path):
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        f.write(original_content)
                
                # 写入修复后的内容
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                fixed_files.append(file_path)
                print(f"  ✅ 已修复图片路径")
            else:
                print(f"  ℹ️  无需修复")
                
        except Exception as e:
            print(f"  ❌ 处理失败: {e}")
    
    print(f"\n修复完成！共处理了 {len(fixed_files)} 个文件:")
    for file_path in fixed_files:
        print(f"  - {file_path}")

def verify_images():
    """验证图片文件是否存在"""
    print("\n验证图片文件...")
    
    image_dir = 'docs/images'
    if not os.path.exists(image_dir):
        print(f"❌ 图片目录不存在: {image_dir}")
        return
    
    svg_files = glob.glob(f"{image_dir}/*.svg")
    print(f"找到 {len(svg_files)} 个SVG文件:")
    
    for svg_file in sorted(svg_files):
        file_size = os.path.getsize(svg_file)
        print(f"  ✅ {os.path.basename(svg_file)} ({file_size} bytes)")

if __name__ == "__main__":
    print("🔧 开始修复图片路径...")
    fix_image_paths()
    verify_images()
    print("\n🎉 修复完成！请重启MkDocs服务查看效果。")
