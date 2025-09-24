#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门修复列表格式问题的脚本
"""

import os
import re

def fix_specific_list_issues(content):
    """修复特定的列表格式问题"""
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 检查是否是 **标题：** 格式
        if re.match(r'^\*\*[^*]+：\*\*\s*$', line.strip()):
            fixed_lines.append(line)
            
            # 确保下一行是空行或列表项
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                
                # 如果下一行不是空行且不是列表项，添加空行
                if next_line.strip() != '' and not next_line.strip().startswith('-') and not re.match(r'^\d+\.', next_line.strip()):
                    fixed_lines.append('')
                
                # 如果下一行是列表项但前面没有空行，添加空行
                elif next_line.strip().startswith('-') or re.match(r'^\d+\.', next_line.strip()):
                    if i > 0 and lines[i-1].strip() != '':
                        # 检查前面是否已经有空行
                        if not (len(fixed_lines) > 0 and fixed_lines[-1] == ''):
                            pass  # 不需要额外空行
                    
        # 检查列表项格式
        elif line.strip().startswith('- '):
            # 确保列表项格式正确
            content_part = line.strip()[2:].strip()
            if content_part:
                # 保持原有的缩进
                indent = len(line) - len(line.lstrip())
                fixed_lines.append(' ' * indent + '- ' + content_part)
            else:
                fixed_lines.append(line)
        
        # 检查有序列表项格式
        elif re.match(r'^\s*\d+\.\s+', line):
            # 保持有序列表格式
            fixed_lines.append(line)
        
        else:
            fixed_lines.append(line)
        
        i += 1
    
    return '\n'.join(fixed_lines)

def fix_specific_formatting_issues(file_path):
    """修复特定文件的格式问题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 修复列表格式问题
        content = fix_specific_list_issues(content)
        
        # 修复特定的格式问题
        # 1. 确保 **标题：** 后面有适当的空行
        content = re.sub(r'(\*\*[^*]+：\*\*)\n([^-\n\s])', r'\1\n\n\2', content)
        
        # 2. 修复列表项之间的空行问题
        content = re.sub(r'(- [^\n]+)\n\n(- [^\n]+)', r'\1\n\2', content)
        
        # 3. 确保列表组之间有空行
        content = re.sub(r'(- [^\n]+)\n(\*\*[^*]+：\*\*)', r'\1\n\n\2', content)
        
        # 4. 移除多余的空行
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    docs_dir = "/home/sooogooo/AmazonQ/ebooks/ChemicalPell/docs"
    
    # 重点修复的文件
    target_files = [
        "chapters/04_preparation.md",
        "chapters/01_know_your_skin.md", 
        "chapters/02_acid_science.md",
        "chapters/03_acid_encyclopedia.md",
        "chapters/05_beginner_guide.md",
        "chapters/06_targeted_solutions.md",
        "chapters/07_product_selection.md",
        "chapters/08_care_during_process.md",
        "chapters/09_medical_grade_peels.md",
        "chapters/10_safety_risk_control.md",
        "chapters/11_evaluation_adjustment.md",
        "chapters/12_lifestyle_management.md",
        "chapters/13_makeup_balance.md",
        "chapters/14_community_sharing.md"
    ]
    
    fixed_count = 0
    
    for file_rel_path in target_files:
        file_path = os.path.join(docs_dir, file_rel_path)
        if os.path.exists(file_path):
            print(f"检查文件: {file_rel_path}")
            if fix_specific_formatting_issues(file_path):
                print(f"  ✅ 已修复格式问题")
                fixed_count += 1
            else:
                print(f"  ℹ️  格式正常")
        else:
            print(f"  ❌ 文件不存在: {file_path}")
    
    print(f"\n✅ 完成！修复了 {fixed_count} 个文件的格式问题")

if __name__ == "__main__":
    main()
