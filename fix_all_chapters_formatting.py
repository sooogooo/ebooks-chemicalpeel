#!/usr/bin/env python3
"""
Universal formatting fix for all chapters
"""

import os
import re
import glob

def fix_chapter_formatting(file_path):
    """Fix formatting issues in a single chapter"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 1: Add space after colons in bold text
        # Pattern: **text：**content -> **text：** content
        pattern1 = r'\*\*([^*]+)：\*\*([^\n*])'
        replacement1 = r'**\1：** \2'
        content = re.sub(pattern1, replacement1, content)
        
        # Fix 2: Ensure proper spacing around list items
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            # Add empty line before important sections if missing
            if (line.startswith('**推荐浓度：**') or 
                line.startswith('**升级条件：**') or
                line.startswith('**使用频率：**') or
                line.startswith('**注意事项：**') or
                line.startswith('**效果预期：**') or
                line.startswith('**特点：**') or
                line.startswith('**建议：**') or
                line.startswith('**重点：**')):
                if i > 0 and lines[i-1].strip() != '':
                    fixed_lines.append('')
            
            fixed_lines.append(line)
        
        content = '\n'.join(fixed_lines)
        
        # Fix 3: Ensure consistent spacing in various common patterns
        patterns_to_fix = [
            r'\*\*机制：\*\*([^\n]+)', r'\*\*危害程度：\*\*([^\n]+)',
            r'\*\*敌情特点：\*\*([^\n]+)', r'\*\*作战策略：\*\*([^\n]+)',
            r'\*\*感悟：\*\*([^\n]+)', r'\*\*的感悟：\*\*([^\n]+)',
            r'\*\*特点：\*\*([^\n]+)', r'\*\*方案：\*\*([^\n]+)',
            r'\*\*建议：\*\*([^\n]+)', r'\*\*重点：\*\*([^\n]+)',
            r'\*\*目标：\*\*([^\n]+)', r'\*\*时间：\*\*([^\n]+)',
            r'\*\*产品：\*\*([^\n]+)', r'\*\*频率：\*\*([^\n]+)',
            r'\*\*间隔：\*\*([^\n]+)', r'\*\*观察期：\*\*([^\n]+)',
            r'\*\*调整原则：\*\*([^\n]+)', r'\*\*浓度：\*\*([^\n]+)',
            r'\*\*成分：\*\*([^\n]+)', r'\*\*效果：\*\*([^\n]+)',
            r'\*\*适用：\*\*([^\n]+)', r'\*\*禁忌：\*\*([^\n]+)',
            r'\*\*价格：\*\*([^\n]+)', r'\*\*品牌：\*\*([^\n]+)',
            r'\*\*类型：\*\*([^\n]+)', r'\*\*优点：\*\*([^\n]+)',
            r'\*\*缺点：\*\*([^\n]+)', r'\*\*评分：\*\*([^\n]+)'
        ]
        
        for pattern in patterns_to_fix:
            content = re.sub(pattern, lambda m: f'**{m.group(0)[2:-2].split("：")[0]}：** {m.group(1)}', content)
        
        # Fix 4: Clean up multiple consecutive empty lines
        content = re.sub(r'\n\n\n+', '\n\n', content)
        
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
    """Fix formatting in all chapters"""
    print("🔧 Starting universal formatting fixes for all chapters...")
    print("=" * 60)
    
    # Find all chapter files
    chapter_files = glob.glob("docs/chapters/*.md")
    chapter_files.sort()
    
    fixed_files = 0
    total_files = len(chapter_files)
    
    for file_path in chapter_files:
        chapter_name = os.path.basename(file_path)
        print(f"📝 Processing: {chapter_name}")
        
        if fix_chapter_formatting(file_path):
            print(f"✅ Fixed formatting in: {chapter_name}")
            fixed_files += 1
        else:
            print(f"ℹ️  No changes needed: {chapter_name}")
    
    print("=" * 60)
    print(f"🎉 Completed! Fixed {fixed_files} out of {total_files} chapter files")
    
    # Test build after fixes
    print("\n🧪 Testing build after fixes...")
    result = os.system("python3 -m mkdocs build --quiet")
    if result == 0:
        print("✅ Build test passed!")
    else:
        print("❌ Build test failed!")

if __name__ == "__main__":
    main()
