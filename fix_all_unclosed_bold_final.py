#!/usr/bin/env python3
"""
Final automated fix for all unclosed bold markers
"""

import re

def fix_all_unclosed_bold():
    """Fix all unclosed bold markers systematically"""
    
    file_path = "docs/chapters/10_safety_risk_control.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    print("🔧 Fixing all unclosed bold markers systematically...")
    
    # Step 1: Fix all section headers that are missing closing **
    content = re.sub(r'\*\*([^*\n]+)：\n', r'**\1：**\n\n', content)
    
    # Step 2: Fix all bold items that are missing closing **
    content = re.sub(r'\*\*([^*\n]+)：([^*\n]+)\n', r'**\1：** \2\n\n', content)
    
    # Step 3: Fix specific patterns
    lines = content.split('\n')
    fixed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this line starts with ** but doesn't end with **
        if line.startswith('**') and '：' in line and not line.endswith('**'):
            # This is likely a section header that needs fixing
            if '：' in line:
                parts = line.split('：', 1)
                if len(parts) == 2:
                    if parts[1].strip():  # Has content after colon
                        fixed_line = f"**{parts[0][2:]}：** {parts[1]}"
                    else:  # No content after colon
                        fixed_line = f"**{parts[0][2:]}：**"
                    fixed_lines.append(fixed_line)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
        
        i += 1
    
    content = '\n'.join(fixed_lines)
    
    # Step 4: Clean up excessive empty lines
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    # Step 5: Ensure proper spacing after section headers
    content = re.sub(r'(\*\*[^*]+：\*\*)\n([^-\n*])', r'\1\n\n\2', content)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if content != original_content:
        print("✅ All unclosed bold markers fixed!")
        return True
    else:
        print("ℹ️  No unclosed bold markers found")
        return False

def verify_bold_markers():
    """Verify that all bold markers are properly closed"""
    
    file_path = "docs/chapters/10_safety_risk_control.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    issues = []
    
    for i, line in enumerate(lines, 1):
        # Count ** markers in each line
        bold_count = line.count('**')
        if bold_count % 2 != 0:
            issues.append(f"Line {i}: Unmatched bold markers ({bold_count}) - {line}")
    
    return issues

def main():
    """Main function"""
    
    print("🚀 Starting final automated bold marker fix...")
    print("=" * 60)
    
    if fix_all_unclosed_bold():
        # Verify the fixes
        issues = verify_bold_markers()
        
        if issues:
            print(f"\n⚠️  Still found {len(issues)} issues:")
            for issue in issues[:5]:
                print(f"  {issue}")
            if len(issues) > 5:
                print(f"  ... and {len(issues) - 5} more")
        else:
            print("\n✅ All bold markers are now properly closed!")
        
        # Test build
        print("\n🧪 Testing build...")
        import os
        result = os.system("python3 -m mkdocs build --quiet")
        if result == 0:
            print("✅ Build test passed!")
        else:
            print("❌ Build test failed!")
    
    print("\n🎉 Final automated fix completed!")

if __name__ == "__main__":
    main()
