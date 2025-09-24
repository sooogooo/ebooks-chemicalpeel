#!/usr/bin/env python3
"""
Check for markdown rendering issues in chapter 7
"""

import re

def check_markdown_issues():
    """Check for potential markdown rendering issues"""
    file_path = "docs/chapters/07_product_selection.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    issues = []
    
    print("🔍 Checking Chapter 7 for markdown rendering issues...")
    print("=" * 60)
    
    for i, line in enumerate(lines, 1):
        # Check for malformed list items
        if line.startswith('-') and not line.startswith('- ') and not line.startswith('---'):
            issues.append(f"Line {i}: Malformed list item - {line}")
        
        # Check for missing spaces after bold markers
        if '**' in line and '：**' in line:
            if re.search(r'\*\*[^*]+：\*\*[^\s]', line):
                issues.append(f"Line {i}: Missing space after colon - {line}")
        
        # Check for potential unrendered markdown
        if line.strip().startswith('**') and line.strip().endswith('**') and '：' in line:
            # This might be a header that should have proper spacing
            if i < len(lines) and lines[i].strip() and not lines[i].startswith('-'):
                issues.append(f"Line {i}: Potential formatting issue - {line}")
    
    if issues:
        print(f"❌ Found {len(issues)} potential issues:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("✅ No obvious markdown rendering issues found!")
    
    # Check for specific patterns that might cause rendering problems
    print("\n🔍 Checking for specific patterns...")
    
    # Look for brand sections
    brand_sections = re.findall(r'\*\*代表品牌：\*\*\n((?:- \*\*[^*]+\*\*[^\n]*\n?)+)', content)
    print(f"Found {len(brand_sections)} brand sections")
    
    # Look for analysis sections
    analysis_sections = re.findall(r'\*\*特点分析：\*\*\n((?:- [^\n]*\n?)+)', content)
    print(f"Found {len(analysis_sections)} analysis sections")
    
    # Check if any sections are malformed
    malformed_sections = 0
    for section in brand_sections + analysis_sections:
        if not section.strip():
            malformed_sections += 1
    
    if malformed_sections > 0:
        print(f"⚠️  Found {malformed_sections} potentially malformed sections")
    else:
        print("✅ All sections appear to be properly formatted")
    
    print("\n🎉 Chapter 7 markdown check completed!")

if __name__ == "__main__":
    check_markdown_issues()
