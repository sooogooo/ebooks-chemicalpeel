#!/usr/bin/env python3
"""检查和修复Markdown中的格式问题"""

import os
import re
from pathlib import Path

def fix_markdown_formatting(content):
    """修复Markdown格式问题"""
    
    # 修复 "** 文字 **" -> "**文字**"
    content = re.sub(r'\*\* ([^*]+) \*\*', r'**\1**', content)
    
    # 修复 "**文字 **" -> "**文字**"
    content = re.sub(r'\*\*([^*]+) \*\*', r'**\1**', content)
    
    # 修复 "** 文字**" -> "**文字**"
    content = re.sub(r'\*\* ([^*]+)\*\*', r'**\1**', content)
    
    # 修复单独的 "**" 标记
    content = re.sub(r'(?<!\*)\*\*(?!\*)', '**', content)
    
    # 修复列表项中的格式
    content = re.sub(r'^(\s*[-*+]\s+)\*\* ([^*]+) \*\*', r'\1**\2**', content, flags=re.MULTILINE)
    
    return content

def scan_and_fix_files():
    """扫描并修复所有Markdown文件"""
    
    base_dir = Path('.')
    markdown_files = []
    
    # 查找所有Markdown文件
    for pattern in ['docs/**/*.md', '*.md']:
        markdown_files.extend(base_dir.glob(pattern))
    
    fixed_files = []
    
    for file_path in markdown_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # 检查是否有问题的格式
            if '** ' in original_content or ' **' in original_content:
                fixed_content = fix_markdown_formatting(original_content)
                
                if fixed_content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    
                    fixed_files.append(str(file_path))
                    print(f"✅ 修复: {file_path}")
                    
                    # 显示修复的内容示例
                    lines = original_content.split('\n')
                    for i, line in enumerate(lines):
                        if '** ' in line or ' **' in line:
                            print(f"   第{i+1}行: {line.strip()}")
                            break
        
        except Exception as e:
            print(f"❌ 错误处理 {file_path}: {e}")
    
    if not fixed_files:
        print("✅ 未发现需要修复的格式问题")
    else:
        print(f"\n📊 总计修复 {len(fixed_files)} 个文件")
    
    return fixed_files

if __name__ == "__main__":
    print("🔍 扫描Markdown格式问题...")
    scan_and_fix_files()
