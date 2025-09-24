#!/usr/bin/env python3
"""
Comprehensive formatting fix for chapter 10
"""

import re

def fix_chapter10_formatting():
    """Fix all formatting issues in chapter 10"""
    file_path = "docs/chapters/10_safety_risk_control.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    print("🔧 Starting comprehensive formatting fixes for Chapter 10...")
    
    # Fix 1: Fix the dialogue section - split long dialogue line
    dialogue_pattern = r'\*\*厂长（你）\*\*："各位，我们的目标是什么？"\*\*安全主管\*\*："安全生产，零事故！"\*\*技术员\*\*："但是产量和效果怎么办？"\*\*安全主管\*\*："没有安全，就没有产量！安全是一切的前提！"\*\*质检员\*\*："我们要建立完善的风险识别和应急处理机制！"\*\*厂长\*\*："说得对！宁可慢一点，也不能出事故！"'
    
    dialogue_replacement = '''**厂长（你）**："各位，我们的目标是什么？"

**安全主管**："安全生产，零事故！"

**技术员**："但是产量和效果怎么办？"

**安全主管**："没有安全，就没有产量！安全是一切的前提！"

**质检员**："我们要建立完善的风险识别和应急处理机制！"

**厂长**："说得对！宁可慢一点，也不能出事故！"'''
    
    content = re.sub(dialogue_pattern, dialogue_replacement, content)
    
    # Fix 2: Add space after colons in bold text
    content = re.sub(r'\*\*([^*]+)：\*\*([^\n*\s])', r'**\1：** \2', content)
    
    # Fix 3: Fix symptom display sections - ensure proper formatting
    # Look for sections like "伴随症状：明显发红，轻微肿胀" that should be bold
    content = re.sub(r'^([^*\n]+症状)：([^\n]+)$', r'**\1：** \2', content, flags=re.MULTILINE)
    content = re.sub(r'^(持续时间)：([^\n]+)$', r'**\1：** \2', content, flags=re.MULTILINE)
    content = re.sub(r'^(影响范围)：([^\n]+)$', r'**\1：** \2', content, flags=re.MULTILINE)
    content = re.sub(r'^(刺激程度)：([^\n]+)$', r'**\1：** \2', content, flags=re.MULTILINE)
    
    # Fix 4: Ensure proper spacing around sections
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Add empty line before important sections if missing
        if (line.startswith('**症状表现：**') or 
            line.startswith('**成因分析：**') or
            line.startswith('**处理方法：**') or
            line.startswith('**后续护理：**') or
            line.startswith('**风险评估**') or
            line.startswith('**应急处理**')):
            if i > 0 and lines[i-1].strip() != '':
                fixed_lines.append('')
        
        fixed_lines.append(line)
        
        # Add empty line after certain sections if missing
        if (line.startswith('**症状表现：**') or 
            line.startswith('**成因分析：**') or
            line.startswith('**处理方法：**')):
            if i + 1 < len(lines) and lines[i+1].strip() and not lines[i+1].startswith('- '):
                fixed_lines.append('')
    
    content = '\n'.join(fixed_lines)
    
    # Fix 5: Ensure proper code block formatting for symptom displays
    # Replace simple symptom lists with proper formatting
    symptom_pattern = r'```\n(刺激程度：[^\n]+\n\n持续时间：[^\n]+\n\n影响范围：[^\n]+\n\n伴随症状：[^\n]+)\n```'
    def format_symptoms(match):
        symptoms = match.group(1)
        formatted = re.sub(r'^([^：]+)：(.+)$', r'**\1：** \2', symptoms, flags=re.MULTILINE)
        return formatted
    
    content = re.sub(symptom_pattern, format_symptoms, content)
    
    # Fix 6: Clean up multiple consecutive empty lines
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    # Write the fixed content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if content != original_content:
        print("✅ Comprehensive formatting fixes applied!")
        return True
    else:
        print("ℹ️  No changes needed")
        return False

def verify_fixes():
    """Verify the formatting fixes"""
    file_path = "docs/chapters/10_safety_risk_control.md"
    
    print("\n🔍 Verifying fixes...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for remaining issues
    issues = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines, 1):
        # Check for long dialogue lines
        if '**厂长（你）**' in line and '**安全主管**' in line:
            issues.append(f"Line {i}: Long dialogue line still exists")
        
        # Check for missing spaces after colons
        if '**' in line and '：**' in line and not ('：** ' in line or line.endswith('：**')):
            issues.append(f"Line {i}: Missing space after colon - {line.strip()}")
        
        # Check for unformatted symptom descriptions
        if line.strip() and '：' in line and not line.startswith('**') and not line.startswith('-'):
            if any(keyword in line for keyword in ['症状', '程度', '时间', '范围']):
                issues.append(f"Line {i}: Potentially unformatted symptom - {line.strip()}")
    
    if issues:
        print(f"⚠️  Found {len(issues)} remaining issues:")
        for issue in issues[:10]:  # Show first 10
            print(f"  {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more")
    else:
        print("✅ All formatting issues appear to be fixed!")

def main():
    """Main function"""
    print("🚀 Starting Chapter 10 comprehensive formatting fix...")
    print("=" * 60)
    
    if fix_chapter10_formatting():
        verify_fixes()
        
        # Test build
        print("\n🧪 Testing build...")
        import os
        result = os.system("python3 -m mkdocs build --quiet")
        if result == 0:
            print("✅ Build test passed!")
        else:
            print("❌ Build test failed!")
    
    print("\n🎉 Chapter 10 formatting fix completed!")

if __name__ == "__main__":
    main()
