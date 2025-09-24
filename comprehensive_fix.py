#!/usr/bin/env python3
"""全面修复Markdown格式问题"""

import re
from pathlib import Path

def comprehensive_fix(content):
    """全面修复Markdown格式"""
    
    # 1. 修复 "**文字：**" 后面有空格的问题
    content = re.sub(r'\*\*([^*]+)：\*\* ', r'**\1：**', content)
    
    # 2. 修复 "**文字** ：" -> "**文字**："
    content = re.sub(r'\*\*([^*]+)\*\* ：', r'**\1**：', content)
    
    # 3. 修复 "-**文字**" -> "- **文字**"
    content = re.sub(r'^(\s*)-\*\*([^*]+)\*\*', r'\1- **\2**', content, flags=re.MULTILINE)
    
    # 4. 修复多个连续的 "****" -> "**"
    content = re.sub(r'\*{4,}', '**', content)
    
    # 5. 修复 "## 标题 **内容：**" -> "## 标题\n\n**内容：**"
    content = re.sub(r'^(## [^*]+) \*\*([^*]+)：\*\*', r'\1\n\n**\2：**', content, flags=re.MULTILINE)
    
    # 6. 修复行内的格式问题 "文字**标题**：文字" -> "文字\n\n**标题**：文字"
    content = re.sub(r'([^*\n])\*\*([^*]+)：\*\*([^*])', r'\1\n\n**\2：**\3', content)
    
    # 7. 修复对话格式
    content = re.sub(r'\*\*([^*]+)\*\*：\"([^"]+)\"', r'**\1**："\2"', content)
    
    # 8. 修复特殊的标题格式
    content = re.sub(r'([^#])\*\*🧪 ([^*]+)：\*\*\*\*', r'\1\n\n**🧪 \2：**', content)
    content = re.sub(r'([^#])\*\*🌟 ([^*]+)？\*\*\*\*', r'\1\n\n**🌟 \2？**', content)
    
    return content

def fix_file(file_path):
    """修复单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        fixed_content = comprehensive_fix(original_content)
        
        if fixed_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            return True
        
        return False
    
    except Exception as e:
        print(f"错误处理 {file_path}: {e}")
        return False

def main():
    """主函数"""
    chapter_files = [
        'docs/chapters/08_care_during_process.md',
        'docs/chapters/09_medical_grade_peels.md', 
        'docs/chapters/10_safety_risk_control.md',
        'docs/chapters/11_evaluation_adjustment.md',
        'docs/chapters/12_lifestyle_management.md',
        'docs/chapters/13_makeup_balance.md',
        'docs/chapters/14_community_sharing.md'
    ]
    
    fixed_count = 0
    
    print("🔧 开始全面修复格式问题...")
    
    for file_path in chapter_files:
        path = Path(file_path)
        if path.exists():
            if fix_file(path):
                print(f"✅ 修复: {file_path}")
                fixed_count += 1
            else:
                print(f"⚪ 无需修复: {file_path}")
    
    print(f"\n📊 总计修复 {fixed_count} 个文件")

if __name__ == "__main__":
    main()
