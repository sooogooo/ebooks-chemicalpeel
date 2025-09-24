#!/usr/bin/env python3
"""
Fix all broken text splits in chapter 10
"""

import re

def fix_broken_text_splits():
    """Fix all instances where text has been incorrectly split across lines"""
    
    file_path = "docs/chapters/10_safety_risk_control.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    print("🔧 Fixing broken text splits...")
    
    # Define the fixes for broken text
    fixes = [
        # Fix "立即停止使用产品"
        (r'1\. 立即停止使用产\n\n品', '1. 立即停止使用产品'),
        
        # Fix "用大量清水冲洗面部" (already fixed above, but keeping for completeness)
        (r'1\. 用大量清水冲洗面\n\n部', '1. 用大量清水冲洗面部'),
        
        # Fix "冷毛巾敷脸，每次10分钟"
        (r'1\. 冷毛巾敷脸，每次10分\n\n钟', '1. 冷毛巾敷脸，每次10分钟'),
        
        # Fix "症状持续不缓解"
        (r'1\. 症状持续不缓\n\n解', '1. 症状持续不缓解'),
        
        # Fix "对酸类成分已知过敏"
        (r'- 对酸类成分已知过\n\n敏', '- 对酸类成分已知过敏'),
        
        # Fix "轻微刺痛，可以忍受"
        (r'- 轻微刺痛，可以忍\n\n受', '- 轻微刺痛，可以忍受'),
        
        # Fix "明显刺痛，影响日常"
        (r'- 明显刺痛，影响日\n\n常', '- 明显刺痛，影响日常'),
        
        # Fix "剧烈疼痛，无法忍受"
        (r'- 剧烈疼痛，无法忍\n\n受', '- 剧烈疼痛，无法忍受'),
        
        # Fix "立即停用所有产品"
        (r'1\. 立即停用所有产\n\n品', '1. 立即停用所有产品'),
        
        # Fix "剧烈疼痛，无法缓解"
        (r'1\. 剧烈疼痛，无法缓\n\n解', '1. 剧烈疼痛，无法缓解'),
        
        # Fix other common patterns
        (r'([^。！？\n]+)\n\n([一-龯]{1})\n\n([^。！？\n]+)', r'\1\2\3'),
    ]
    
    for old_pattern, new_text in fixes:
        content = re.sub(old_pattern, new_text, content)
    
    # Additional cleanup for standalone single characters that are clearly part of words
    lines = content.split('\n')
    fixed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if this is a standalone single character that should be joined with previous line
        if (len(line) == 1 and 
            line in ['部', '品', '钟', '解', '受', '常', '敏', '口', '物', '华', '复', '区', '膏', '射', '肤', '用', '活', '酸', '洁', '水', '录'] and
            i > 0 and i < len(lines) - 1):
            
            # Get the previous non-empty line
            prev_idx = i - 1
            while prev_idx >= 0 and not lines[prev_idx].strip():
                prev_idx -= 1
            
            if prev_idx >= 0:
                # Join with the previous line
                prev_line = lines[prev_idx].rstrip()
                if not prev_line.endswith(line):
                    lines[prev_idx] = prev_line + line
                # Skip the current single character line
                i += 1
                continue
        
        fixed_lines.append(lines[i])
        i += 1
    
    content = '\n'.join(fixed_lines)
    
    # Clean up excessive empty lines
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    # Write back the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    if content != original_content:
        print("✅ Fixed broken text splits!")
        return True
    else:
        print("ℹ️  No broken text splits found")
        return False

def main():
    """Main function"""
    
    print("🚀 Starting broken text splits fix...")
    print("=" * 50)
    
    if fix_broken_text_splits():
        print("\n🧪 Testing build...")
        import os
        result = os.system("python3 -m mkdocs build --quiet")
        if result == 0:
            print("✅ Build test passed!")
        else:
            print("❌ Build test failed!")
        
        # Check for remaining issues
        print("\n🔍 Checking for remaining broken text...")
        result = os.system("grep -n '^部$\\|^品$\\|^解$\\|^钟$\\|^受$\\|^常$\\|^敏$' docs/chapters/10_safety_risk_control.md")
        if result != 0:
            print("✅ No remaining broken text found!")
        else:
            print("⚠️  Some broken text may still remain")
    
    print("\n🎉 Broken text splits fix completed!")

if __name__ == "__main__":
    main()
