#!/usr/bin/env python3
"""
Final cleanup for remaining issues in chapter 10
"""

import re

def final_cleanup():
    """Final cleanup of remaining formatting issues"""
    file_path = "docs/chapters/10_safety_risk_control.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    print("🧹 Final cleanup of Chapter 10...")
    
    # Fix 1: Remove any remaining malformed code blocks
    content = re.sub(r'```\s*\n([^`]*程度：[^`]*)\n```', lambda m: '\n'.join([f"**{line.strip()}**" if '：' in line and not line.startswith('**') else line for line in m.group(1).split('\n') if line.strip()]), content)
    
    # Fix 2: Fix mixed headers and content - separate them properly
    content = re.sub(r'(## [^#\n]+)\*\*([^*]+\*\*[^*]*)', r'\1\n\n**\2', content)
    
    # Fix 3: Format unformatted symptom descriptions
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Format symptom descriptions that aren't already formatted
        if ('程度：' in line or '情况：' in line or '范围：' in line or '时间：' in line) and not line.startswith('**'):
            if not line.strip().startswith('- ') and not line.strip().startswith('|') and '：' in line:
                # Split at colon and format
                parts = line.split('：', 1)
                if len(parts) == 2:
                    fixed_line = f"**{parts[0].strip()}：** {parts[1].strip()}"
                    fixed_lines.append(fixed_line)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    # Fix 4: Clean up spacing issues
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    # Fix 5: Ensure proper spacing around sections
    content = re.sub(r'(\*\*[^*]+：\*\*)\n([^-\n*])', r'\1\n\n\2', content)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if content != original_content:
        print("✅ Final cleanup completed!")
        return True
    else:
        print("ℹ️  No additional cleanup needed")
        return False

def main():
    """Main function"""
    print("🚀 Starting final cleanup...")
    print("=" * 40)
    
    if final_cleanup():
        print("\n🧪 Testing build...")
        import os
        result = os.system("python3 -m mkdocs build --quiet")
        if result == 0:
            print("✅ Build test passed!")
        else:
            print("❌ Build test failed!")
        
        # Run verification again
        print("\n🔍 Running final verification...")
        os.system("python3 verify_chapter10_final.py")
    
    print("\n🎉 Final cleanup completed!")

if __name__ == "__main__":
    main()
