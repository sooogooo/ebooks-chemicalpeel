#!/usr/bin/env python3
"""
Final verification of chapter 10 markdown cleanup
"""

import re

def final_verification():
    """Final verification of all fixes"""
    
    file_path = "docs/chapters/10_safety_risk_control.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔍 Final verification of Chapter 10 markdown cleanup...")
    print("=" * 60)
    
    issues = []
    
    # Check 1: Broken text splits
    broken_patterns = [
        r'[^。！？\n]+\n\n[一-龯]{1}\n\n',  # Single character on separate line
        r'\*\* \*\* ',  # Double bold markers
        r'：\*\*[^*\s]',  # Missing space after colon
        r'## [^#\n]*\*\*[^*]+\*\*',  # Mixed headers
    ]
    
    for pattern in broken_patterns:
        matches = re.findall(pattern, content)
        if matches:
            issues.extend([f"Pattern '{pattern}': {len(matches)} matches"])
    
    # Check 2: Incomplete words
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if len(line) == 1 and line in ['部', '品', '钟', '解', '受', '常', '敏', '口', '物', '华', '复', '区', '膏', '射', '肤', '用', '活', '酸', '洁', '水', '录', '质']:
            issues.append(f"Line {i}: Standalone character '{line}'")
    
    # Check 3: Unmatched bold markers
    bold_count = content.count('**')
    if bold_count % 2 != 0:
        issues.append(f"Unmatched bold markers: {bold_count} total")
    
    # Check 4: Specific fixed content
    test_cases = [
        ("用大量清水冲洗面部", "Face washing instruction"),
        ("适度运动，促进循环", "Exercise instruction"),
        ("情绪管理，减少压力", "Stress management"),
        ("**环境优化：**", "Environment optimization header"),
        ("酵素面膜（每周1次）", "Enzyme mask instruction"),
        ("充足睡眠，促进肌肤修复", "Sleep instruction"),
    ]
    
    for test_text, description in test_cases:
        if test_text not in content:
            issues.append(f"Missing expected text: {description}")
    
    # Summary
    if issues:
        print(f"❌ Found {len(issues)} remaining issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ All markdown cleanup issues resolved!")
        print("🎉 Chapter 10 is now clean and ready!")
    
    # Statistics
    print(f"\n📊 Chapter 10 Statistics:")
    print(f"  - Total characters: {len(content):,}")
    print(f"  - Total lines: {len(lines):,}")
    print(f"  - Bold markers: {bold_count}")
    print(f"  - Headers: {content.count('#')}")
    
    return len(issues) == 0

if __name__ == "__main__":
    success = final_verification()
    exit(0 if success else 1)
