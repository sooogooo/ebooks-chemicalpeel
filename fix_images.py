#!/usr/bin/env python3
"""
批量修复图片容器的脚本
移除内联样式，使用CSS类
"""

import os
import re
import glob

def fix_image_containers(file_path):
    """修复单个文件中的图片容器"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
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
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已修复: {file_path}")

def main():
    """主函数"""
    # 修复所有章节文件
    chapter_files = glob.glob('docs/chapters/*.md')
    for file_path in chapter_files:
        fix_image_containers(file_path)
    
    # 修复附录文件
    appendix_files = glob.glob('docs/appendix/*.md')
    for file_path in appendix_files:
        fix_image_containers(file_path)
    
    print("所有图片容器已修复完成！")

if __name__ == '__main__':
    main()
