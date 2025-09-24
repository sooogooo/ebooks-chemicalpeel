#!/usr/bin/env python3
"""
Final comprehensive cleanup of all markdown artifacts in chapter 10
"""

import re

def final_comprehensive_cleanup():
    """Final comprehensive cleanup"""
    
    file_path = "docs/chapters/10_safety_risk_control.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    print("🧹 Final comprehensive cleanup...")
    
    # Step 1: Fix all broken symptom descriptions
    content = re.sub(r'\*\*痘痘类型：以白头、黑头为主\*\* \*\*痘痘数量：比平时增加20-50%\*\* \*\*出现位置：原本就有问题的区域\*\* \*\*持续时间：\*\* 2-4周',
                     '**痘痘类型：** 以白头、黑头为主\n\n**痘痘数量：** 比平时增加20-50%\n\n**出现位置：** 原本就有问题的区域\n\n**持续时间：** 2-4周', content)
    
    # Step 2: Fix broken section headers and content
    broken_sections = [
        # Fix reaction characteristics
        (r'\*\*时间规律：\*\* - 使用后立即出现 - 15-30分钟内缓解 - 不会持续恶化 - 下次使用反应减轻\*\*❌ 过敏反应的特征：\*\* \*\*反应特点：\*\*',
         '**时间规律：**\n\n- 使用后立即出现\n- 15-30分钟内缓解\n- 不会持续恶化\n- 下次使用反应减轻\n\n**❌ 过敏反应的特征：**\n\n**反应特点：**'),
        
        (r'\*\*时间规律：\*\* - 可能延迟出现 - 持续时间长 - 症状逐渐加重 - 再次接触反应更严重',
         '**时间规律：**\n\n- 可能延迟出现\n- 持续时间长\n- 症状逐渐加重\n- 再次接触反应更严重'),
        
        # Fix emergency handling sections
        (r'过敏应急处理流程\*\*🚨 过敏反应应急处理SOP：\*\* \*\* #',
         '过敏应急处理流程\n\n**🚨 过敏反应应急处理SOP：**'),
        
        (r'\*\*清洁方法：\*\* 1\. 用大量清水冲洗面',
         '**清洁方法：**\n\n1. 用大量清水冲洗面'),
        
        # Fix contraindication sections
        (r'绝对禁忌症：\*\* 不能碰的"雷区"\*\*🚫 绝对不能刷酸的情况：\*\* #',
         '绝对禁忌症：不能碰的"雷区"\n\n**🚫 绝对不能刷酸的情况：**'),
        
        (r'禁忌一：\*\* 肌肤破损期\*\*具体情况：\*\*',
         '禁忌一：肌肤破损期\n\n**具体情况：**'),
        
        (r'\*\*风险说明：\*\* - 可能导致感染加重 - 延缓伤口愈合 - 增加疤痕形成风险 - 可能引起色素沉着',
         '**风险说明：**\n\n- 可能导致感染加重\n- 延缓伤口愈合\n- 增加疤痕形成风险\n- 可能引起色素沉着'),
        
        (r'禁忌二：\*\* 过敏体质期\*\*具体情况：\*\*',
         '禁忌二：过敏体质期\n\n**具体情况：**'),
        
        (r'禁忌三：\*\* 特殊生理期\*\*具体情况：\*\*',
         '禁忌三：特殊生理期\n\n**具体情况：**'),
    ]
    
    for old, new in broken_sections:
        content = re.sub(old, new, content)
    
    # Step 3: Fix all remaining formatting issues
    # Fix standalone ** markers
    content = re.sub(r'\*\*\s*\n', '\n', content)
    content = re.sub(r'\n\*\*\s*\n', '\n\n', content)
    
    # Fix broken bold sections
    content = re.sub(r'\*\*([^*]+)：\*\* ([^*\n]+) \*\*([^*]+)：\*\* ([^*\n]+) \*\*([^*]+)：\*\* ([^*\n]+)',
                     r'**\1：** \2\n\n**\3：** \4\n\n**\5：** \6', content)
    
    # Fix section headers that got mixed with content
    content = re.sub(r'(## [^#\n]+)\*\*([^*]+)\*\*([^#\n]*)', r'\1\n\n**\2**\3', content)
    
    # Step 4: Clean up spacing
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    # Step 5: Ensure proper formatting for all bold sections
    content = re.sub(r'\*\*([^*]+)：\*\*\n([^-\n*])', r'**\1：**\n\n\2', content)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if content != original_content:
        print("✅ Final cleanup completed!")
        return True
    else:
        print("ℹ️  No issues found to clean up")
        return False

def main():
    """Main function"""
    
    print("🚀 Starting final comprehensive cleanup...")
    print("=" * 60)
    
    if final_comprehensive_cleanup():
        print("\n🧪 Testing build...")
        import os
        result = os.system("python3 -m mkdocs build --quiet")
        if result == 0:
            print("✅ Build test passed!")
        else:
            print("❌ Build test failed!")
        
        # Check for remaining artifacts
        print("\n🔍 Checking for remaining artifacts...")
        result = os.system("python3 find_markdown_artifacts.py")
    
    print("\n🎉 Final cleanup completed!")

if __name__ == "__main__":
    main()
