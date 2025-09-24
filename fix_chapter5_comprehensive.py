#!/usr/bin/env python3
"""
Comprehensive formatting fix for chapter 5
"""

import re

def fix_chapter5_formatting():
    """Fix all formatting issues in chapter 5"""
    file_path = "docs/chapters/05_beginner_guide.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔧 Starting comprehensive formatting fixes for Chapter 5...")
    
    # Fix 1: Add space after colons in bold text
    # Pattern: **text：**content -> **text：** content
    pattern1 = r'\*\*([^*]+)：\*\*([^\n*])'
    replacement1 = r'**\1：** \2'
    content = re.sub(pattern1, replacement1, content)
    
    # Fix 2: Ensure proper spacing around list items
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Add empty line before list sections if missing
        if line.startswith('**推荐浓度：**') or line.startswith('**升级条件：**'):
            if i > 0 and lines[i-1].strip() != '':
                fixed_lines.append('')
        
        fixed_lines.append(line)
        
        # Add empty line after list sections if missing
        if line.startswith('**推荐浓度：**') or line.startswith('**升级条件：**'):
            # Check if next line is a list item
            if i + 1 < len(lines) and not lines[i+1].startswith('- '):
                fixed_lines.append('')
    
    content = '\n'.join(fixed_lines)
    
    # Fix 3: Ensure consistent spacing in time/frequency sections
    content = re.sub(r'\*\*频率：\*\*([^\n]+)', r'**频率：** \1', content)
    content = re.sub(r'\*\*间隔：\*\*([^\n]+)', r'**间隔：** \1', content)
    content = re.sub(r'\*\*观察期：\*\*([^\n]+)', r'**观察期：** \1', content)
    content = re.sub(r'\*\*调整原则：\*\*([^\n]+)', r'**调整原则：** \1', content)
    
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
        for issue in issues[:5]:  # Show first 5
            print(f"  {issue}")
        if len(issues) > 5:
            print(f"  ... and {len(issues) - 5} more")
    else:
        print("✅ All formatting issues fixed!")
    
    print("\n🎉 Chapter 5 comprehensive formatting completed!")

if __name__ == "__main__":
    fix_chapter5_formatting()
