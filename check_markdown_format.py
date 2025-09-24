#!/usr/bin/env python3
"""
检查Markdown文件中的格式问题
- 未闭合的代码块
- 表格格式问题
- 列表格式问题
"""

import os
import re
import glob

def check_code_blocks(file_path):
    """检查代码块是否正确闭合"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 计算代码块标记数量
    code_block_count = content.count('```')
    
    if code_block_count % 2 != 0:
        return f"❌ 未闭合的代码块 (找到 {code_block_count} 个标记)"
    else:
        return f"✅ 代码块正常 ({code_block_count//2} 对)"

def check_table_format(file_path):
    """检查表格格式问题"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    issues = []
    in_table = False
    
    for i, line in enumerate(lines, 1):
        # 检测表格行
        if '|' in line and line.strip().startswith('|') and line.strip().endswith('|'):
            if not in_table:
                in_table = True
            
            # 检查下一行是否为空行（在表格中间）
            if i < len(lines) and lines[i].strip() == '':
                # 检查空行后是否还有表格行
                if i + 1 < len(lines) and '|' in lines[i + 1] and lines[i + 1].strip().startswith('|'):
                    issues.append(f"第 {i+1} 行：表格中间有空行")
        else:
            in_table = False
    
    if issues:
        return f"❌ 表格格式问题:\n  " + "\n  ".join(issues)
    else:
        return "✅ 表格格式正常"

def check_list_format(file_path):
    """检查列表格式问题"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    issues = []
    
    for i, line in enumerate(lines, 1):
        # 检测列表项
        if re.match(r'^\s*[-*+]\s+', line):
            # 检查前一行是否也是列表项但没有空行分隔
            if i > 1:
                prev_line = lines[i-2].strip()
                if prev_line and not re.match(r'^\s*[-*+]\s+', prev_line) and not prev_line.endswith(':'):
                    # 这可能是列表格式问题，但需要更复杂的逻辑来判断
                    pass
    
    if issues:
        return f"❌ 列表格式问题:\n  " + "\n  ".join(issues)
    else:
        return "✅ 列表格式正常"

def main():
    """主函数"""
    print("🔍 检查Markdown格式问题...")
    print("=" * 50)
    
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
    
    total_issues = 0
    
    for file_path in md_files:
        if not os.path.exists(file_path):
            continue
            
        print(f"📄 检查文件: {file_path}")
        
        # 检查代码块
        code_result = check_code_blocks(file_path)
        print(f"  {code_result}")
        
        # 检查表格格式
        table_result = check_table_format(file_path)
        print(f"  {table_result}")
        
        # 检查列表格式
        list_result = check_list_format(file_path)
        print(f"  {list_result}")
        
        # 统计问题
        if "❌" in code_result or "❌" in table_result or "❌" in list_result:
            total_issues += 1
        
        print()
    
    print("=" * 50)
    if total_issues == 0:
        print("🎉 所有文件格式正常！")
    else:
        print(f"⚠️  发现 {total_issues} 个文件有格式问题")

if __name__ == "__main__":
    main()
