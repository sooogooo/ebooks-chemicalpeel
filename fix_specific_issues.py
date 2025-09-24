#!/usr/bin/env python3
"""修复具体的格式问题"""

import re
from pathlib import Path

def fix_specific_file(file_path):
    """修复单个文件的具体问题"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 修复 "**文字：** " -> "**文字：**"
    content = re.sub(r'\*\*([^*]+)：\*\* ', r'**\1：**', content)
    
    # 修复 "## 标题：** 内容：**" -> "## 标题\n\n**内容：**"
    content = re.sub(r'## ([^*]+)：\*\* ([^*]+)：\*\*', r'## \1\n\n**\2：**', content)
    
    # 修复未闭合的粗体 "**文字：*" -> "**文字：**"
    content = re.sub(r'\*\*([^*]+)：\*(?!\*)', r'**\1：**', content)
    
    # 修复嵌套粗体问题
    content = re.sub(r'\*\*([^*]+)\*\*([^*]*)\*\*([^*]+)\*\*', r'**\1** \2 **\3**', content)
    
    # 修复特殊的标题格式问题
    content = re.sub(r'### ([^*]+)\*\*([^*]+)', r'### \1\n\n**\2**', content)
    
    # 修复行尾的格式问题
    content = re.sub(r'([^*])\*\*([^*]+)\*\*$', r'\1**\2**', content, flags=re.MULTILINE)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    """主函数"""
    problem_files = [
        'docs/chapters/08_care_during_process.md',
        'docs/chapters/09_medical_grade_peels.md', 
        'docs/chapters/10_safety_risk_control.md',
        'docs/chapters/12_lifestyle_management.md',
        'docs/chapters/13_makeup_balance.md',
        'docs/chapters/14_community_sharing.md'
    ]
    
    fixed_count = 0
    
    for file_path in problem_files:
        path = Path(file_path)
        if path.exists():
            if fix_specific_file(path):
                print(f"✅ 修复: {file_path}")
                fixed_count += 1
            else:
                print(f"⚪ 无需修复: {file_path}")
    
    print(f"\n📊 总计修复 {fixed_count} 个文件")

if __name__ == "__main__":
    main()
