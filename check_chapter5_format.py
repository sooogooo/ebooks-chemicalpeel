#!/usr/bin/env python3
"""
Check the formatting fixes in chapter 5
"""

def check_formatting():
    """Check if the formatting issues are fixed"""
    file_path = "docs/chapters/05_beginner_guide.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔍 Checking Chapter 5 formatting...")
    print("=" * 50)
    
    # Check for proper spacing after colons
    issues = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines, 1):
        if '**' in line and '：**' in line and not line.endswith('：**'):
            # Check if there's proper spacing after the colon
            if '：**' in line and not ('：** ' in line or line.endswith('：**')):
                issues.append(f"Line {i}: Missing space after colon - {line.strip()}")
    
    if issues:
        print("❌ Found formatting issues:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("✅ No formatting issues found!")
    
    # Check for proper list formatting
    print("\n📋 Checking list formatting...")
    list_sections = []
    in_list = False
    current_section = []
    
    for line in lines:
        if line.startswith('**推荐浓度：**') or line.startswith('**升级条件：**'):
            if current_section:
                list_sections.append(current_section)
            current_section = [line]
            in_list = True
        elif in_list and line.startswith('- **'):
            current_section.append(line)
        elif in_list and line.strip() == '':
            continue
        elif in_list and line.startswith('**'):
            list_sections.append(current_section)
            current_section = []
            in_list = False
    
    if current_section:
        list_sections.append(current_section)
    
    print(f"Found {len(list_sections)} list sections")
    for i, section in enumerate(list_sections, 1):
        print(f"  Section {i}: {len(section)} items")
        if len(section) > 1:
            print(f"    Header: {section[0]}")
            print(f"    Items: {len(section)-1}")
    
    print("\n🎉 Chapter 5 formatting check completed!")

if __name__ == "__main__":
    check_formatting()
