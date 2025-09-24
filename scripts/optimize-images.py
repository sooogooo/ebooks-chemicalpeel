#!/usr/bin/env python3
"""SVG图片压缩优化脚本"""

import os
import re
from pathlib import Path

def optimize_svg(file_path):
    """优化单个SVG文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 移除注释
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # 移除多余空白
    content = re.sub(r'\s+', ' ', content)
    content = re.sub(r'>\s+<', '><', content)
    
    # 移除不必要的属性
    content = re.sub(r'\s+id="[^"]*"', '', content)
    content = re.sub(r'\s+class=""', '', content)
    
    # 优化数值精度
    content = re.sub(r'(\d+\.\d{3,})', lambda m: f"{float(m.group(1)):.2f}", content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    
    return len(content)

def main():
    images_dir = Path('docs/images')
    if not images_dir.exists():
        print("图片目录不存在")
        return
    
    total_saved = 0
    for svg_file in images_dir.glob('*.svg'):
        original_size = svg_file.stat().st_size
        new_size = optimize_svg(svg_file)
        saved = original_size - new_size
        total_saved += saved
        print(f"优化 {svg_file.name}: 节省 {saved} 字节")
    
    print(f"总计节省: {total_saved} 字节")

if __name__ == "__main__":
    main()
