#!/usr/bin/env python3
"""
Fix all instances where bold headers should be on new lines
"""

import re

def fix_bold_headers_newline():
    """Fix bold headers that should be on new lines"""
    
    file_path = "docs/chapters/10_safety_risk_control.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    print("🔧 Fixing bold headers that should be on new lines...")
    
    # Pattern to match text followed immediately by **header:**
    # This will match cases like "text**Header：**" and convert to "text\n\n**Header：**"
    pattern = r'([^*\n]+)\*\*([^*]+：)\*\*'
    
    def replacement(match):
        text = match.group(1).rstrip()
        header = match.group(2)
        return f"{text}\n\n**{header}**"
    
    content = re.sub(pattern, replacement, content)
    
    # Clean up any excessive empty lines that might have been created
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    # Write back the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if content != original_content:
        print("✅ Fixed bold headers positioning!")
        return True
    else:
        print("ℹ️  No issues found to fix")
        return False

def verify_fixes():
    """Verify the fixes"""
    
    file_path = "docs/chapters/10_safety_risk_control.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for remaining issues
    remaining_issues = re.findall(r'[^*\n]+\*\*[^*]+：\*\*', content)
    
    if remaining_issues:
        print(f"⚠️  Found {len(remaining_issues)} remaining issues:")
        for issue in remaining_issues[:5]:  # Show first 5
            print(f"  {issue}")
        if len(remaining_issues) > 5:
            print(f"  ... and {len(remaining_issues) - 5} more")
    else:
        print("✅ All bold header positioning issues fixed!")

def main():
    """Main function"""
    
    print("🚀 Starting bold header positioning fix...")
    print("=" * 50)
    
    if fix_bold_headers_newline():
        verify_fixes()
        
        print("\n🧪 Testing build...")
        import os
        result = os.system("python3 -m mkdocs build --quiet")
        if result == 0:
            print("✅ Build test passed!")
        else:
            print("❌ Build test failed!")
    
    print("\n🎉 Bold header positioning fix completed!")

if __name__ == "__main__":
    main()
