#!/usr/bin/env python3
"""
Comprehensive formatting fix for chapter 6
"""

import re

def fix_chapter6_formatting():
    """Fix all formatting issues in chapter 6"""
    file_path = "docs/chapters/06_targeted_solutions.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 Starting comprehensive formatting fixes for Chapter 6...")
    
    # Fix 1: Add space after colons in bold text
    # Pattern: **text：**content -> **text：** content
    pattern1 = r'\*\*([^*]+)：\*\*([^\n*])'
    replacement1 = r'**\1：** \2'
    content = re.sub(pattern1, replacement1, content)
    
    # Fix 2: Ensure proper spacing around list items
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Add empty line before important sections if missing
        if (line.startswith('**推荐浓度：**') or 
            line.startswith('**升级条件：**') or
            line.startswith('**使用频率：**') or
            line.startswith('**注意事项：**') or
            line.startswith('**效果预期：**')):
            if i > 0 and lines[i-1].strip() != '':
                fixed_lines.append('')
        
        fixed_lines.append(line)
        
        # Add empty line after list sections if missing
        if (line.startswith('**推荐浓度：**') or 
            line.startswith('**升级条件：**') or
            line.startswith('**使用频率：**') or
            line.startswith('**注意事项：**') or
            line.startswith('**效果预期：**')):
            # Check if next line is a list item
            if i + 1 < len(lines) and not lines[i+1].startswith('- '):
                fixed_lines.append('')
    
    content = '\n'.join(fixed_lines)
    
    # Fix 3: Ensure consistent spacing in various sections
    content = re.sub(r'\*\*机制：\*\*([^\n]+)', r'**机制：** \1', content)
    content = re.sub(r'\*\*危害程度：\*\*([^\n]+)', r'**危害程度：** \1', content)
    content = re.sub(r'\*\*敌情特点：\*\*([^\n]+)', r'**敌情特点：** \1', content)
    content = re.sub(r'\*\*作战策略：\*\*([^\n]+)', r'**作战策略：** \1', content)
    content = re.sub(r'\*\*感悟：\*\*([^\n]+)', r'**感悟：** \1', content)
    content = re.sub(r'\*\*的感悟：\*\*([^\n]+)', r'**的感悟：** \1', content)
    content = re.sub(r'\*\*特点：\*\*([^\n]+)', r'**特点：** \1', content)
    content = re.sub(r'\*\*方案：\*\*([^\n]+)', r'**方案：** \1', content)
    content = re.sub(r'\*\*建议：\*\*([^\n]+)', r'**建议：** \1', content)
    content = re.sub(r'\*\*重点：\*\*([^\n]+)', r'**重点：** \1', content)
    content = re.sub(r'\*\*目标：\*\*([^\n]+)', r'**目标：** \1', content)
    content = re.sub(r'\*\*时间：\*\*([^\n]+)', r'**时间：** \1', content)
    content = re.sub(r'\*\*产品：\*\*([^\n]+)', r'**产品：** \1', content)
    
    # Fix 4: Clean up multiple consecutive empty lines
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    # Write the fixed content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Comprehensive formatting fixes applied!")
    
    # Verify the fixes
    print("\n🔍 Verifying fixes...")
    with open(file_path, 'r', encoding='utf-8') as f:
        new_content = f.read()
    
    # Check for remaining issues
    issues = []
    lines = new_content.split('\n')
    
    for i, line in enumerate(lines, 1):
        if '**' in line and '：**' in line and not line.endswith('：**'):
            if '：**' in line and not ('：** ' in line or line.endswith('：**')):
                issues.append(f"Line {i}: {line.strip()}")
    
    if issues:
        print(f"❌ Still found {len(issues)} formatting issues:")
        for issue in issues[:10]:  # Show first 10
            print(f"  {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more")
    else:
        print("✅ All formatting issues fixed!")
    
    print(f"\n🎉 Chapter 6 comprehensive formatting completed!")

if __name__ == "__main__":
    fix_chapter6_formatting()
