#!/usr/bin/env python3
"""
Targeted fix for specific formatting issues in chapter 10
"""

import re

def fix_specific_issues():
    """Fix specific formatting issues identified"""
    file_path = "docs/chapters/10_safety_risk_control.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    print("🔧 Fixing specific formatting issues in Chapter 10...")
    
    # Fix 1: Fix broken symptom descriptions in code blocks
    # Replace malformed code blocks with proper formatting
    content = re.sub(r'```\n干燥程度：比平时明显干燥\n\n燥\n\n脱皮情况：细小皮屑，不明显\n\n影响区域：T区、鼻翼等角质较厚部位\n```', 
                     '**干燥程度：** 比平时明显干燥\n\n**脱皮情况：** 细小皮屑，不明显\n\n**影响区域：** T区、鼻翼等角质较厚部位', content)
    
    # Fix 2: Fix other broken symptom blocks
    content = re.sub(r'```\n干燥程度：严重干燥，紧绷不适\n\n脱皮情况：大片脱皮，影响外观\n\n影响区域：全脸或大面积区域\n\n伴随症状：可能有轻微刺痛\n```',
                     '**干燥程度：** 严重干燥，紧绷不适\n\n**脱皮情况：** 大片脱皮，影响外观\n\n**影响区域：** 全脸或大面积区域\n\n**伴随症状：** 可能有轻微刺痛', content)
    
    # Fix 3: Fix broken burn symptom block
    content = re.sub(r'```\n灼伤程度：皮肤破损、糜烂\n\n疼痛程度：剧烈疼痛\n\n影响范围：局部或大面积\n\n伴随症状：可能有渗液、结痂\n```',
                     '**灼伤程度：** 皮肤破损、糜烂\n\n**疼痛程度：** 剧烈疼痛\n\n**影响范围：** 局部或大面积\n\n**伴随症状：** 可能有渗液、结痂', content)
    
    # Fix 4: Fix mixed header and content issues
    content = re.sub(r'## 过敏反应的分级识别\*\*🔍 过敏反应识别表：\*\* \| 等级 \| 症状表现 \| 持续时间 \| 处理方式 \| 就医需求',
                     '## 过敏反应的分级识别\n\n**🔍 过敏反应识别表：**\n\n| 等级 | 症状表现 | 持续时间 | 处理方式 | 就医需求', content)
    
    # Fix 5: Fix other mixed content
    content = re.sub(r'## 第四步：观察记录（30分钟-24小时）\*\*观察要点：\*\* 1\. 记录症状变',
                     '## 第四步：观察记录（30分钟-24小时）\n\n**观察要点：**\n\n1. 记录症状变', content)
    
    content = re.sub(r'## 第五步：寻求帮助（必要时）\*\*就医指征：\*\* 1\. 症状持续不缓',
                     '## 第五步：寻求帮助（必要时）\n\n**就医指征：**\n\n1. 症状持续不缓', content)
    
    # Fix 6: Fix medical project conflicts section
    content = re.sub(r'## 医美项目冲突：不能重叠的"施工期"\*\*🏥 与医美项目的时间冲突：\*\* #',
                     '## 医美项目冲突：不能重叠的"施工期"\n\n**🏥 与医美项目的时间冲突：**\n\n#', content)
    
    # Fix 7: Fix emergency level sections
    content = re.sub(r'## 一级紧急（轻微不适）\*\*症状特征：\*\*',
                     '## 一级紧急（轻微不适）\n\n**症状特征：**', content)
    
    content = re.sub(r'## 二级紧急（中度不适）\*\*症状特征：\*\*',
                     '## 二级紧急（中度不适）\n\n**症状特征：**', content)
    
    # Fix 8: Clean up any remaining formatting issues
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    # Write back the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if content != original_content:
        print("✅ Specific formatting issues fixed!")
        return True
    else:
        print("ℹ️  No specific issues found")
        return False

def main():
    """Main function"""
    print("🚀 Starting targeted fix for Chapter 10...")
    print("=" * 50)
    
    if fix_specific_issues():
        print("\n🧪 Testing build...")
        import os
        result = os.system("python3 -m mkdocs build --quiet")
        if result == 0:
            print("✅ Build test passed!")
        else:
            print("❌ Build test failed!")
    
    print("\n🎉 Targeted fix completed!")

if __name__ == "__main__":
    main()
