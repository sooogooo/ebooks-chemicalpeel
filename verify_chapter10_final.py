#!/usr/bin/env python3
"""
Final verification of chapter 10 formatting fixes
"""

import re

def verify_chapter10():
    """Verify all formatting issues are resolved"""
    file_path = "docs/chapters/10_safety_risk_control.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔍 Final verification of Chapter 10 formatting...")
    print("=" * 60)
    
    issues = []
    
    # Check 1: Long dialogue lines
    if '**厂长（你）**："各位，我们的目标是什么？"**安全主管**' in content:
        issues.append("Long dialogue line still exists")
    else:
        print("✅ Dialogue formatting: Fixed")
    
    # Check 2: Code blocks with symptom descriptions
    code_blocks = re.findall(r'```[^`]*```', content, re.DOTALL)
    symptom_in_code = 0
    for block in code_blocks:
        if '程度：' in block or '情况：' in block or '范围：' in block:
            symptom_in_code += 1
    
    if symptom_in_code > 0:
        issues.append(f"Found {symptom_in_code} symptom descriptions still in code blocks")
    else:
        print("✅ Symptom descriptions: Properly formatted")
    
    # Check 3: Missing spaces after colons
    colon_issues = re.findall(r'\*\*[^*]+：\*\*[^\s\n]', content)
    if colon_issues:
        issues.append(f"Found {len(colon_issues)} missing spaces after colons")
    else:
        print("✅ Colon spacing: Correct")
    
    # Check 4: Mixed header and content
    mixed_content = re.findall(r'##[^#\n]*\*\*[^*]+\*\*', content)
    if mixed_content:
        issues.append(f"Found {len(mixed_content)} mixed header/content issues")
    else:
        print("✅ Header formatting: Clean")
    
    # Check 5: Malformed symptom descriptions
    lines = content.split('\n')
    unformatted_symptoms = 0
    for line in lines:
        if ('程度：' in line or '情况：' in line or '范围：' in line) and not line.startswith('**'):
            if not line.strip().startswith('- ') and not line.strip().startswith('|'):
                unformatted_symptoms += 1
    
    if unformatted_symptoms > 0:
        issues.append(f"Found {unformatted_symptoms} unformatted symptom descriptions")
    else:
        print("✅ Symptom formatting: Consistent")
    
    # Summary
    print("\n" + "=" * 60)
    if issues:
        print(f"❌ Found {len(issues)} remaining issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("🎉 All formatting issues resolved!")
        print("✅ Chapter 10 is ready for publication!")
    
    # Statistics
    print(f"\n📊 Chapter 10 Statistics:")
    print(f"  - Total lines: {len(lines)}")
    print(f"  - Symptom sections: {content.count('**症状表现：**')}")
    print(f"  - Processing sections: {content.count('**处理方法：**')}")
    print(f"  - Emergency sections: {content.count('**应急处理**')}")

if __name__ == "__main__":
    verify_chapter10()
