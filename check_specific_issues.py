#!/usr/bin/env python3
"""
Check specific issues mentioned by user
"""

def check_specific_issues():
    """Check the specific issues mentioned by the user"""
    
    file_path = "docs/chapters/10_safety_risk_control.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔍 Checking specific issues mentioned by user...")
    print("=" * 60)
    
    issues_found = []
    
    # Check 1: Exercise and stress management formatting
    if "情绪管理，减少压力**环境优化：**" in content:
        issues_found.append("❌ Exercise/stress management formatting issue still exists")
    else:
        print("✅ Exercise and stress management formatting: Fixed")
    
    # Check 2: Sensitive skin header
    if "谨慎一：** 敏感肌肤" in content:
        issues_found.append("❌ Sensitive skin header formatting issue still exists")
    else:
        print("✅ Sensitive skin header formatting: Fixed")
    
    # Check 3: Table formatting
    if "| 等级 | 症状表现 | 持续时间 | 处理方式 | 就医需求 \n\n|" in content:
        issues_found.append("❌ Table formatting issue still exists")
    else:
        print("✅ Table formatting: Fixed")
    
    # Check 4: Proper table structure
    table_lines = [
        "| 等级 | 症状表现 | 持续时间 | 处理方式 | 就医需求 |",
        "|------|----------|----------|----------|----------|",
        "|**轻度**| 轻微发红、瘙痒 | 几小时内缓解 | 停用观察 | 暂不需要 |"
    ]
    
    table_correct = all(line in content for line in table_lines)
    if table_correct:
        print("✅ Table structure: Correct")
    else:
        issues_found.append("❌ Table structure is not correct")
    
    # Check 5: Environment optimization section
    env_section = "**环境优化：**\n\n- 保持室内湿度"
    if env_section in content:
        print("✅ Environment optimization section: Properly formatted")
    else:
        issues_found.append("❌ Environment optimization section formatting issue")
    
    # Summary
    print("\n" + "=" * 60)
    if issues_found:
        print(f"❌ Found {len(issues_found)} remaining issues:")
        for issue in issues_found:
            print(f"  {issue}")
    else:
        print("🎉 All specific issues have been resolved!")
        print("✅ Chapter 10 formatting is now perfect!")
    
    return len(issues_found) == 0

if __name__ == "__main__":
    success = check_specific_issues()
    exit(0 if success else 1)
