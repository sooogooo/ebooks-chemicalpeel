#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
格式修复脚本 - 修复markdown文件中的列表格式问题
"""

import os
import re
import glob

def fix_list_formatting(content):
    """修复列表格式问题"""
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # 修复：**标题：** 后面应该有空行
        if re.match(r'^\*\*.*：\*\*$', line.strip()):
            fixed_lines.append(line)
            # 检查下一行是否为空行，如果不是则添加空行
            if i + 1 < len(lines) and lines[i + 1].strip() != '':
                if not lines[i + 1].startswith('- ') and not lines[i + 1].startswith('1. '):
                    fixed_lines.append('')
        
        # 修复：确保列表项格式一致
        elif re.match(r'^- ', line):
            # 无序列表项，保持原样
            fixed_lines.append(line)
        
        elif re.match(r'^\d+\. ', line):
            # 有序列表项，保持原样
            fixed_lines.append(line)
        
        # 修复：确保列表项的子项缩进正确
        elif re.match(r'^   - ', line):
            # 子列表项，保持原样
            fixed_lines.append(line)
        
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def fix_header_formatting(content):
    """修复标题格式问题"""
    # 确保标题前后有适当的空行
    content = re.sub(r'\n(#{1,6} [^\n]+)\n(?!\n)', r'\n\1\n\n', content)
    
    # 修复：确保 🔸 标题格式正确
    content = re.sub(r'^#### 🔸 ([^\n]+)$', r'#### 🔸 \1', content, flags=re.MULTILINE)
    
    return content

def fix_bold_text_formatting(content):
    """修复加粗文本格式"""
    # 确保 **文本：** 格式正确
    content = re.sub(r'\*\*([^*]+)：\*\*', r'**\1：**', content)
    
    return content

def process_file(file_path):
    """处理单个文件"""
    print(f"处理文件: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 应用各种修复
        content = fix_list_formatting(content)
        content = fix_header_formatting(content)
        content = fix_bold_text_formatting(content)
        
        # 移除多余的空行（超过2个连续空行的情况）
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # 如果内容有变化，则写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ 已修复格式问题")
        else:
            print(f"  ℹ️  无需修复")
            
    except Exception as e:
        print(f"  ❌ 处理失败: {e}")

def main():
    """主函数"""
    docs_dir = "/home/sooogooo/AmazonQ/ebooks/ChemicalPell/docs"
    
    # 查找所有markdown文件
    md_files = []
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    
    print(f"找到 {len(md_files)} 个markdown文件")
    print("开始修复格式问题...\n")
    
    for file_path in md_files:
        process_file(file_path)
    
    print(f"\n✅ 格式修复完成！处理了 {len(md_files)} 个文件")

if __name__ == "__main__":
    main()
