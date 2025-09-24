#!/usr/bin/env python3
"""
Fix unclosed bold markers in chapter 10
"""

import re

def fix_unclosed_bold():
    """Fix unclosed bold markers"""
    
    file_path = "docs/chapters/10_safety_risk_control.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    print("🔧 Fixing unclosed bold markers...")
    
    # Fix specific patterns
    fixes = [
        # Fix symptom description headers
        (r'\*\*症状表现：\n\*\*([^*]+)：\*\* ([^\n]+)\n\n\*\*持续时间：\n([^\n]+)\n\*\*([^*]+)：\*\* ([^\n]+)',
         r'**症状表现：**\n\n**\1：** \2\n\n**持续时间：** \3\n\n**\4：** \5'),
        
        # Fix成因分析 headers
        (r'\*\*成因分析：\n- ', r'**成因分析：**\n\n- '),
        
        # Fix处理方法 headers  
        (r'\*\*处理方法：\n\n([0-9])', r'**处理方法：**\n\n\1'),
        
        # Fix other section headers
        (r'\*\*([^*]+)：\n([^*\n-])', r'**\1：**\n\n\2'),
        
        # Fix broken bold sections
        (r'\*\*([^*]+)：\n\*\*([^*]+)：\*\* ', r'**\1：**\n\n**\2：** '),
    ]
    
    for old, new in fixes:
        content = re.sub(old, new, content, flags=re.MULTILINE)
    
    # Manual fixes for specific broken sections
    manual_fixes = [
        ('**症状表现：\n**刺激程度：** 轻微刺痛，类似蚊虫叮咬\n\n**持续时间：\n5-30分钟\n**影响范围：** 局部区域',
         '**症状表现：**\n\n**刺激程度：** 轻微刺痛，类似蚊虫叮咬\n\n**持续时间：** 5-30分钟\n\n**影响范围：** 局部区域'),
        
        ('**成因分析：\n- 角质层较薄的区域更敏感',
         '**成因分析：**\n\n- 角质层较薄的区域更敏感'),
        
        ('**处理方法：\n\n1. 停止按摩，让产品自然吸收',
         '**处理方法：**\n\n1. 停止按摩，让产品自然吸收'),
    ]
    
    for old, new in manual_fixes:
        content = content.replace(old, new)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if content != original_content:
        print("✅ Fixed unclosed bold markers!")
        return True
    else:
        print("ℹ️  No unclosed bold markers found")
        return False

def main():
    """Main function"""
    
    print("🚀 Starting unclosed bold marker fix...")
    print("=" * 50)
    
    if fix_unclosed_bold():
        print("\n🧪 Testing build...")
        import os
        result = os.system("python3 -m mkdocs build --quiet")
        if result == 0:
            print("✅ Build test passed!")
        else:
            print("❌ Build test failed!")
    
    print("\n🎉 Unclosed bold marker fix completed!")

if __name__ == "__main__":
    main()
