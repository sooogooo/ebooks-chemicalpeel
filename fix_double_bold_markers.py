#!/usr/bin/env python3
"""
Fix all double bold markers in chapter 10
"""

import re

def fix_double_bold_markers():
    """Fix all instances of double bold markers like ** **"""
    
    file_path = "docs/chapters/10_safety_risk_control.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    print("🔧 Fixing double bold markers...")
    
    # Fix the pattern: **text：** ** content
    content = re.sub(r'\*\*([^*]+：)\*\* \*\* ([^\n]+)', r'**\1** \2', content)
    
    # Fix other double bold patterns
    content = re.sub(r'\*\* \*\* ', '** ', content)
    
    # Write back the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if content != original_content:
        print("✅ Fixed double bold markers!")
        return True
    else:
        print("ℹ️  No double bold markers found")
        return False

def main():
    """Main function"""
    
    print("🚀 Starting double bold markers fix...")
    print("=" * 50)
    
    if fix_double_bold_markers():
        print("\n🧪 Testing build...")
        import os
        result = os.system("python3 -m mkdocs build --quiet")
        if result == 0:
            print("✅ Build test passed!")
        else:
            print("❌ Build test failed!")
        
        # Check for remaining double bold markers
        print("\n🔍 Checking for remaining double bold markers...")
        result = os.system("grep -c '\\*\\* \\*\\* ' docs/chapters/10_safety_risk_control.md")
        if result != 0:
            print("✅ No remaining double bold markers found!")
        else:
            print("⚠️  Some double bold markers may still remain")
    
    print("\n🎉 Double bold markers fix completed!")

if __name__ == "__main__":
    main()
