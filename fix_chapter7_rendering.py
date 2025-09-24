#!/usr/bin/env python3
"""
Fix potential rendering issues in chapter 7
"""

import re

def fix_chapter7_rendering():
    """Fix rendering issues in chapter 7"""
    file_path = "docs/chapters/07_product_selection.md"
    
    try:
        # Read with explicit UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        print("🔧 Checking and fixing Chapter 7 rendering issues...")
        
        # Fix 1: Ensure proper spacing after headers
        content = re.sub(r'\*\*([^*]+)：\*\*\n([^-\n])', r'**\1：**\n\n\2', content)
        
        # Fix 2: Ensure proper spacing before list sections
        content = re.sub(r'([^\n])\n\*\*代表品牌：\*\*', r'\1\n\n**代表品牌：**', content)
        content = re.sub(r'([^\n])\n\*\*特点分析：\*\*', r'\1\n\n**特点分析：**', content)
        
        # Fix 3: Ensure proper list formatting
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            # Check for malformed list items
            if line.startswith('-') and not line.startswith('- ') and not line.startswith('---'):
                # Fix malformed list item
                fixed_line = '- ' + line[1:]
                fixed_lines.append(fixed_line)
                print(f"Fixed malformed list item: {line} -> {fixed_line}")
            else:
                fixed_lines.append(line)
        
        content = '\n'.join(fixed_lines)
        
        # Fix 4: Clean up multiple consecutive empty lines
        content = re.sub(r'\n\n\n+', '\n\n', content)
        
        # Fix 5: Ensure proper spacing around brand sections
        content = re.sub(r'\*\*代表品牌：\*\*\n\n(- \*\*)', r'**代表品牌：**\n\1', content)
        content = re.sub(r'\*\*特点分析：\*\*\n\n(- )', r'**特点分析：**\n\1', content)
        
        # Check if any changes were made
        if content != original_content:
            # Write back the fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ Fixed rendering issues in Chapter 7")
            return True
        else:
            print("ℹ️  No rendering issues found in Chapter 7")
            return False
            
    except Exception as e:
        print(f"❌ Error processing Chapter 7: {e}")
        return False

def verify_fix():
    """Verify the fix by checking specific sections"""
    file_path = "docs/chapters/07_product_selection.md"
    
    print("\n🔍 Verifying fixes...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for brand sections
    brand_sections = re.findall(r'\*\*代表品牌：\*\*\n((?:- \*\*[^*]+\*\*[^\n]*\n?)+)', content)
    analysis_sections = re.findall(r'\*\*特点分析：\*\*\n((?:- [^\n]*\n?)+)', content)
    
    print(f"✅ Found {len(brand_sections)} properly formatted brand sections")
    print(f"✅ Found {len(analysis_sections)} properly formatted analysis sections")
    
    # Check for malformed list items
    malformed_items = re.findall(r'^-[^ ]', content, re.MULTILINE)
    if malformed_items:
        print(f"⚠️  Still found {len(malformed_items)} malformed list items")
    else:
        print("✅ No malformed list items found")

def main():
    """Main function"""
    print("🚀 Starting Chapter 7 rendering fix...")
    print("=" * 50)
    
    if fix_chapter7_rendering():
        verify_fix()
        
        # Test build
        print("\n🧪 Testing build...")
        import os
        result = os.system("python3 -m mkdocs build --quiet")
        if result == 0:
            print("✅ Build test passed!")
        else:
            print("❌ Build test failed!")
    
    print("\n🎉 Chapter 7 rendering fix completed!")

if __name__ == "__main__":
    main()
