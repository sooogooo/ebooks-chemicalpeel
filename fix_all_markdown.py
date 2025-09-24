#!/usr/bin/env python3
"""
全面修复所有Markdown文件的格式问题
按最严格的标准确保Markdown被正确解析
"""

import os
import re
import glob
from pathlib import Path

def fix_bold_with_emoji(content):
    """修复粗体+emoji的格式问题"""
    # 修复 **emoji文字**紧跟文字 的情况
    content = re.sub(r'\*\*([^*]+)\*\*([^\s])', r'**\1** \2', content)
    return content

def fix_headers(content):
    """确保标题前后有正确的空行"""
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # 检测标题行
        if re.match(r'^#{1,6}\s+', line):
            # 标题前需要空行（除非是文件开头）
            if i > 0 and fixed_lines and fixed_lines[-1].strip() != '':
                fixed_lines.append('')
            fixed_lines.append(line)
            # 标题后需要空行（除非下一行已经是空行）
            if i < len(lines) - 1 and lines[i + 1].strip() != '':
                fixed_lines.append('')
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def fix_lists(content):
    """修复列表格式"""
    lines = content.split('\n')
    fixed_lines = []
    in_list = False
    
    for i, line in enumerate(lines):
        # 检测列表项
        if re.match(r'^\s*[-*+]\s+', line) or re.match(r'^\s*\d+\.\s+', line):
            # 如果不在列表中，且前一行不是空行，添加空行
            if not in_list and fixed_lines and fixed_lines[-1].strip() != '':
                fixed_lines.append('')
            fixed_lines.append(line)
            in_list = True
        else:
            # 如果刚退出列表，且当前行不是空行，添加空行
            if in_list and line.strip() != '' and not re.match(r'^\s*[-*+]\s+', line):
                if fixed_lines and fixed_lines[-1].strip() != '':
                    fixed_lines.append('')
            fixed_lines.append(line)
            if line.strip() != '':
                in_list = False
    
    return '\n'.join(fixed_lines)

def fix_code_blocks(content):
    """修复代码块格式"""
    lines = content.split('\n')
    fixed_lines = []
    in_code_block = False
    
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            if not in_code_block:
                # 代码块开始前需要空行
                if fixed_lines and fixed_lines[-1].strip() != '':
                    fixed_lines.append('')
                in_code_block = True
            else:
                # 代码块结束
                in_code_block = False
            fixed_lines.append(line)
            # 代码块后需要空行
            if not in_code_block and i < len(lines) - 1 and lines[i + 1].strip() != '':
                fixed_lines.append('')
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def fix_tables(content):
    """修复表格格式"""
    lines = content.split('\n')
    fixed_lines = []
    in_table = False
    
    for i, line in enumerate(lines):
        # 检测表格行
        if '|' in line and line.strip().startswith('|') and line.strip().endswith('|'):
            if not in_table:
                # 表格开始前需要空行
                if fixed_lines and fixed_lines[-1].strip() != '':
                    fixed_lines.append('')
                in_table = True
            fixed_lines.append(line)
        else:
            if in_table and line.strip() == '':
                # 跳过表格中的空行
                continue
            elif in_table and line.strip() != '':
                # 表格结束，添加空行
                if fixed_lines and fixed_lines[-1].strip() != '':
                    fixed_lines.append('')
                in_table = False
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def fix_paragraphs(content):
    """修复段落间距"""
    # 确保段落之间有空行
    content = re.sub(r'\n([^\n\s#*`|>-])', r'\n\n\1', content)
    # 移除多余的空行（超过2个连续空行）
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content

def fix_emphasis(content):
    """修复强调格式（粗体、斜体）"""
    # 确保粗体标记周围有适当的空格
    content = re.sub(r'(\S)\*\*([^*]+)\*\*(\S)', r'\1 **\2** \3', content)
    # 确保斜体标记周围有适当的空格
    content = re.sub(r'(\S)\*([^*]+)\*(\S)', r'\1 *\2* \3', content)
    return content

def fix_links_and_images(content):
    """修复链接和图片格式"""
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # 图片前后需要空行
        if re.match(r'^\s*!\[.*\]\(.*\)\s*$', line):
            if fixed_lines and fixed_lines[-1].strip() != '':
                fixed_lines.append('')
            fixed_lines.append(line)
            fixed_lines.append('')
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def fix_blockquotes(content):
    """修复引用块格式"""
    lines = content.split('\n')
    fixed_lines = []
    in_blockquote = False
    
    for line in lines:
        if line.strip().startswith('>'):
            if not in_blockquote:
                # 引用块前需要空行
                if fixed_lines and fixed_lines[-1].strip() != '':
                    fixed_lines.append('')
                in_blockquote = True
            fixed_lines.append(line)
        else:
            if in_blockquote and line.strip() != '':
                # 引用块后需要空行
                if fixed_lines and fixed_lines[-1].strip() != '':
                    fixed_lines.append('')
                in_blockquote = False
            fixed_lines.append(line)
            if line.strip() != '':
                in_blockquote = False
    
    return '\n'.join(fixed_lines)

def fix_horizontal_rules(content):
    """修复分隔线格式"""
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # 检测分隔线
        if re.match(r'^\s*[-*_]{3,}\s*$', line):
            # 分隔线前后需要空行
            if fixed_lines and fixed_lines[-1].strip() != '':
                fixed_lines.append('')
            fixed_lines.append(line)
            fixed_lines.append('')
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def clean_up_spacing(content):
    """清理多余的空格和空行"""
    # 移除行尾空格
    content = re.sub(r' +\n', '\n', content)
    # 移除文件开头的空行
    content = content.lstrip('\n')
    # 确保文件以单个换行符结尾
    content = content.rstrip('\n') + '\n'
    # 限制连续空行不超过2个
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content

def fix_markdown_file(file_path):
    """修复单个Markdown文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 按顺序应用所有修复
        content = fix_bold_with_emoji(content)
        content = fix_headers(content)
        content = fix_lists(content)
        content = fix_code_blocks(content)
        content = fix_tables(content)
        content = fix_emphasis(content)
        content = fix_links_and_images(content)
        content = fix_blockquotes(content)
        content = fix_horizontal_rules(content)
        content = fix_paragraphs(content)
        content = clean_up_spacing(content)
        
        # 只有内容发生变化时才写入文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "已修复"
        else:
            return False, "无需修复"
            
    except Exception as e:
        return False, f"错误: {str(e)}"

def main():
    """主函数"""
    print("🔧 开始全面修复所有Markdown文件...")
    print("=" * 60)
    
    # 查找所有Markdown文件
    md_files = []
    for pattern in ['docs/**/*.md', 'docs/*.md', '*.md']:
        md_files.extend(glob.glob(pattern, recursive=True))
    
    # 去重并排序
    md_files = sorted(list(set(md_files)))
    
    if not md_files:
        print("❌ 未找到Markdown文件")
        return
    
    print(f"📁 找到 {len(md_files)} 个Markdown文件")
    print()
    
    fixed_count = 0
    error_count = 0
    
    for file_path in md_files:
        if not os.path.exists(file_path):
            continue
            
        print(f"📄 处理文件: {file_path}")
        
        success, message = fix_markdown_file(file_path)
        
        if success:
            print(f"  ✅ {message}")
            fixed_count += 1
        elif "错误" in message:
            print(f"  ❌ {message}")
            error_count += 1
        else:
            print(f"  ⏭️  {message}")
    
    print()
    print("=" * 60)
    print(f"📊 修复统计:")
    print(f"  ✅ 已修复文件: {fixed_count}")
    print(f"  ⏭️  无需修复: {len(md_files) - fixed_count - error_count}")
    print(f"  ❌ 错误文件: {error_count}")
    print(f"  📁 总文件数: {len(md_files)}")
    
    if fixed_count > 0:
        print(f"\n🎉 成功修复了 {fixed_count} 个文件的Markdown格式问题！")
    else:
        print(f"\n✨ 所有文件格式都正确，无需修复！")

if __name__ == "__main__":
    main()
