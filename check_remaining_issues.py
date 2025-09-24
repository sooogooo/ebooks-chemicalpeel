#!/usr/bin/env python3
"""检查剩余的Markdown格式问题"""

import re
from pathlib import Path

def check_file_issues(file_path):
    """检查单个文件的格式问题"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, 1):
            # 检查各种格式问题
            if '** ' in line or ' **' in line:
                issues.append(f"第{i}行: 粗体格式问题 - {line.strip()}")
            
            # 检查未闭合的粗体
            bold_count = line.count('**')
            if bold_count % 2 != 0 and '```' not in line:
                issues.append(f"第{i}行: 未闭合粗体 - {line.strip()}")
            
            # 检查其他问题
            if re.search(r'\*\*[^*]*\*\*[^*]*\*\*', line):
                issues.append(f"第{i}行: 可能的嵌套粗体 - {line.strip()}")
    
    except Exception as e:
        issues.append(f"读取错误: {e}")
    
    return issues

def main():
    """主函数"""
    base_dir = Path('docs')
    problem_files = []
    
    # 重点检查后半部章节
    chapter_files = [
        'chapters/08_care_during_process.md',
        'chapters/09_medical_grade_peels.md', 
        'chapters/10_safety_risk_control.md',
        'chapters/11_evaluation_adjustment.md',
        'chapters/12_lifestyle_management.md',
        'chapters/13_makeup_balance.md',
        'chapters/14_community_sharing.md'
    ]
    
    print("🔍 检查后半部章节的格式问题...")
    
    for chapter in chapter_files:
        file_path = base_dir / chapter
        if file_path.exists():
            issues = check_file_issues(file_path)
            if issues:
                problem_files.append((str(file_path), issues))
                print(f"\n❌ {file_path}:")
                for issue in issues[:5]:  # 只显示前5个问题
                    print(f"   {issue}")
                if len(issues) > 5:
                    print(f"   ... 还有 {len(issues)-5} 个问题")
    
    if not problem_files:
        print("✅ 后半部章节格式检查完成，未发现问题")
    else:
        print(f"\n📊 发现 {len(problem_files)} 个文件有格式问题")
    
    return problem_files

if __name__ == "__main__":
    main()
