#!/usr/bin/env python3
"""
Comprehensive fix for all markdown artifacts in chapter 10
"""

import re

def fix_all_artifacts():
    """Fix all markdown artifacts in chapter 10"""
    
    file_path = "docs/chapters/10_safety_risk_control.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    print("🔧 Fixing all markdown artifacts in Chapter 10...")
    
    # Fix 1: Mixed headers and content - separate them properly
    content = re.sub(r'(## [^#\n]+)\*\*([^*]+\*\*[^*]*)', r'\1\n\n**\2', content)
    
    # Fix 2: Broken bold sections at end of lines
    content = re.sub(r'([^*])\*\*([^*]+：\*\*) ([0-9])', r'\1\n\n**\2\n\n\3', content)
    
    # Fix 3: Fix unmatched bold markers
    content = re.sub(r'\*\*\s*\n', '\n', content)  # Remove standalone **
    content = re.sub(r'\*\*\s*#', '\n\n#', content)  # Fix ** before headers
    
    # Fix 4: Fix broken list continuations
    content = re.sub(r'品\n\n([0-9])', r'品\n\n\1', content)
    content = re.sub(r'解\n\n([0-9])', r'解\n\n\1', content)
    content = re.sub(r'钟\n\n([0-9])', r'钟\n\n\1', content)
    content = re.sub(r'部\n\n([0-9])', r'部\n\n\1', content)
    
    # Fix 5: Fix specific broken sections
    fixes = [
        # Fix broken emergency handling sections
        (r'4\. 立即就医，寻求专业帮助\*\*就医准备：\*\* 1\. 记录使用的产品信息',
         '4. 立即就医，寻求专业帮助\n\n**就医准备：**\n\n1. 记录使用的产品信息'),
        
        (r'4\. 立即就医，不要延误\*\*注意事项：\*\* 1\. 不要涂抹任何药膏',
         '4. 立即就医，不要延误\n\n**注意事项：**\n\n1. 不要涂抹任何药膏'),
        
        # Fix broken section headers
        (r'## 过敏 VS 正常反应的区别\*\*✅ 正常刺激反应的特征：\*',
         '## 过敏 VS 正常反应的区别\n\n**✅ 正常刺激反应的特征：**'),
        
        (r'## 过敏应急处理流程\*\*🚨 过敏反应应急处理SOP：',
         '## 过敏应急处理流程\n\n**🚨 过敏反应应急处理SOP：**'),
        
        # Fix broken step headers
        (r'## 第一步：立即停止（0-5分钟）\*\*紧急行动：\*\* 1\. 立即停止使用产',
         '## 第一步：立即停止（0-5分钟）\n\n**紧急行动：**\n\n1. 立即停止使用产'),
        
        (r'## 第二步：清洁处理（5-15分钟）\*\*清洁方法：',
         '## 第二步：清洁处理（5-15分钟）\n\n**清洁方法：**'),
        
        (r'## 第三步：降温舒缓（15-30分钟）\*\*舒缓措施：\*\* 1\. 冷毛巾敷脸，每次10分',
         '## 第三步：降温舒缓（15-30分钟）\n\n**舒缓措施：**\n\n1. 冷毛巾敷脸，每次10分'),
        
        # Fix other broken sections
        (r'禁忌期间的替代方案\*\*🔄 不能刷酸时的护肤策略：',
         '禁忌期间的替代方案\n\n**🔄 不能刷酸时的护肤策略：**'),
        
        (r'替代方案一：温和去角质\*\*替代方法：\*\*',
         '替代方案一：温和去角质\n\n**替代方法：**'),
        
        (r'替代方案二：保湿修复\*\*重点护理：',
         '替代方案二：保湿修复\n\n**重点护理：**'),
        
        (r'替代方案三：生活调理\*\*内调外养：',
         '替代方案三：生活调理\n\n**内调外养：**'),
        
        # Fix drug conflict sections
        (r'药物治疗冲突：不能同行的"单行道"\*\*💊 与口服药物的相互作用：',
         '药物治疗冲突：不能同行的"单行道"\n\n**💊 与口服药物的相互作用：**'),
        
        (r'冲突药物二：光敏性药物\*\*常见药物：',
         '冲突药物二：光敏性药物\n\n**常见药物：**'),
        
        (r'冲突药物三：激素类药物\*\*药物类型：',
         '冲突药物三：激素类药物\n\n**药物类型：**'),
        
        # Fix medical project conflicts
        (r'医美项目冲突：不能重叠的"施工期"\*\*🏥 与医美项目的时间冲突：\*\* #',
         '医美项目冲突：不能重叠的"施工期"\n\n**🏥 与医美项目的时间冲突：**'),
        
        # Fix emergency level sections
        (r'一级紧急（轻微不适）\*\*症状特征：\*\*',
         '一级紧急（轻微不适）\n\n**症状特征：**'),
        
        (r'二级紧急（中度不适）\*\*症状特征：\*\*',
         '二级紧急（中度不适）\n\n**症状特征：**'),
        
        (r'三级紧急（严重反应）\*\*症状特征：\*\*',
         '三级紧急（严重反应）\n\n**症状特征：**'),
    ]
    
    for old, new in fixes:
        content = re.sub(old, new, content)
    
    # Fix 6: Clean up formatting issues
    content = re.sub(r'\n\n\n+', '\n\n', content)  # Remove excessive empty lines
    content = re.sub(r'\*\*\s*\*\*', '', content)  # Remove empty bold sections
    
    # Fix 7: Ensure proper spacing around sections
    content = re.sub(r'(\*\*[^*]+：\*\*)\n([^-\n*])', r'\1\n\n\2', content)
    
    # Write back the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if content != original_content:
        print("✅ All markdown artifacts fixed!")
        return True
    else:
        print("ℹ️  No artifacts found to fix")
        return False

def verify_fixes():
    """Verify that the fixes worked"""
    
    print("\n🔍 Verifying fixes...")
    
    file_path = "docs/chapters/10_safety_risk_control.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines, 1):
        # Check for mixed headers
        if line.startswith('#') and '**' in line:
            issues.append(f"Line {i}: Mixed header - {line}")
        
        # Check for unmatched bold markers
        if line.count('**') % 2 != 0:
            issues.append(f"Line {i}: Unmatched bold - {line}")
        
        # Check for broken formatting
        if '**' in line and '：**' in line and not line.startswith('**'):
            if not line.strip().startswith('- ') and not line.strip().startswith('|'):
                issues.append(f"Line {i}: Potential issue - {line}")
    
    if issues:
        print(f"⚠️  Still found {len(issues)} issues:")
        for issue in issues[:5]:  # Show first 5
            print(f"  {issue}")
        if len(issues) > 5:
            print(f"  ... and {len(issues) - 5} more")
    else:
        print("✅ All issues appear to be fixed!")
    
    return len(issues)

def main():
    """Main function"""
    
    print("🚀 Starting comprehensive markdown artifact fix...")
    print("=" * 60)
    
    if fix_all_artifacts():
        remaining_issues = verify_fixes()
        
        # Test build
        print("\n🧪 Testing build...")
        import os
        result = os.system("python3 -m mkdocs build --quiet")
        if result == 0:
            print("✅ Build test passed!")
        else:
            print("❌ Build test failed!")
        
        print(f"\n📊 Summary:")
        print(f"  Remaining issues: {remaining_issues}")
        print(f"  Status: {'✅ Success' if remaining_issues == 0 else '⚠️ Needs more work'}")
    
    print("\n🎉 Markdown artifact fix completed!")

if __name__ == "__main__":
    main()
