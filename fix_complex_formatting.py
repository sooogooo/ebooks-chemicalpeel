#!/usr/bin/env python3
"""
Advanced formatting fix for complex formatting issues
"""

import os
import re
import glob

def fix_complex_formatting(file_path):
    """Fix complex formatting issues in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 1: Handle complex patterns with multiple consecutive bold sections
        # Pattern: **text：** #### **text：** -> **text：**\n\n#### **text：**
        content = re.sub(r'\*\*([^*]+)：\*\* #### \*\*([^*]+)：\*\*', r'**\1：**\n\n#### **\2：**', content)
        
        # Fix 2: Handle patterns like **text：** - content
        content = re.sub(r'\*\*([^*]+)：\*\* - ', r'**\1：**\n\n- ', content)
        
        # Fix 3: Basic colon spacing fix
        content = re.sub(r'\*\*([^*]+)：\*\*([^\n*\s])', r'**\1：** \2', content)
        
        # Fix 4: Handle embedded formatting within lines
        # Split lines and process each one
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Handle lines with multiple formatting issues
            if '：**' in line and line.count('**') > 2:
                # Complex line with multiple bold sections
                # Try to separate them properly
                parts = re.split(r'(\*\*[^*]+：\*\*)', line)
                fixed_parts = []
                
                for part in parts:
                    if re.match(r'\*\*[^*]+：\*\*', part):
                        # This is a bold section with colon
                        fixed_parts.append(part)
                        # Add line break after bold sections if followed by content
                    else:
                        # Regular content
                        if part.strip():
                            fixed_parts.append(part)
                
                # Rejoin with proper spacing
                if len(fixed_parts) > 1:
                    fixed_line = fixed_parts[0]
                    for part in fixed_parts[1:]:
                        if part.strip():
                            if part.startswith(' '):
                                fixed_line += '\n\n' + part.strip()
                            else:
                                fixed_line += '\n\n' + part
                    fixed_lines.append(fixed_line)
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        content = '\n'.join(fixed_lines)
        
        # Fix 5: Clean up multiple consecutive empty lines
        content = re.sub(r'\n\n\n+', '\n\n', content)
        
        # Fix 6: Ensure proper spacing after headers
        content = re.sub(r'(#{1,6} [^\n]+)\n([^\n#])', r'\1\n\n\2', content)
        
        # Check if any changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Fix complex formatting in problematic files"""
    print("🔧 Starting advanced formatting fixes for complex issues...")
    print("=" * 60)
    
    # Target the problematic files specifically
    problematic_files = [
        "docs/chapters/13_makeup_balance.md",
        "docs/chapters/12_lifestyle_management.md", 
        "docs/chapters/10_safety_risk_control_clean.md",
        "docs/chapters/10_safety_risk_control.md",
        "docs/chapters/14_community_sharing.md"
    ]
    
    fixed_files = 0
    
    for file_path in problematic_files:
        if os.path.exists(file_path):
            chapter_name = os.path.basename(file_path)
            print(f"📝 Processing: {chapter_name}")
            
            if fix_complex_formatting(file_path):
                print(f"✅ Fixed complex formatting in: {chapter_name}")
                fixed_files += 1
            else:
                print(f"ℹ️  No changes needed: {chapter_name}")
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print("=" * 60)
    print(f"🎉 Completed! Fixed {fixed_files} files with complex formatting issues")
    
    # Test build after fixes
    print("\n🧪 Testing build after fixes...")
    result = os.system("python3 -m mkdocs build --quiet")
    if result == 0:
        print("✅ Build test passed!")
    else:
        print("❌ Build test failed!")
    
    # Final check for remaining issues
    print("\n🔍 Final check for remaining formatting issues...")
    remaining_issues = 0
    for file_path in problematic_files:
        if os.path.exists(file_path):
            result = os.system(f'grep -q "：\\*\\*[^[:space:]]" {file_path}')
            if result == 0:
                remaining_issues += 1
                print(f"⚠️  Still has issues: {os.path.basename(file_path)}")
    
    if remaining_issues == 0:
        print("✅ All formatting issues resolved!")
    else:
        print(f"⚠️  {remaining_issues} files still have formatting issues")

if __name__ == "__main__":
    main()
