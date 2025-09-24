#!/usr/bin/env python3
"""
修复带空格的粗体格式问题
将 ** 文字：** 格式修复为 **文字：**
将 * 文字 * 格式修复为 *文字*
"""

import os
import re
import glob

def fix_spaced_bold_format(content):
    """修复带空格的粗体和斜体格式"""
    # 修复 ** 文字：** 格式为 **文字：**
    content = re.sub(r'\*\* ([^*]+)\*\*', r'**\1**', content)
    
    # 修复 * 文字 * 格式为 *文字*（但保留图片标题中的正确格式）
    # 只修复行尾有空格的情况
    content = re.sub(r'\* ([^*]+) \*$', r'*\1*', content, flags=re.MULTILINE)
    
    return content

def fix_file(file_path):
    """修复单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = fix_spaced_bold_format(content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "已修复"
        else:
            return False, "无需修复"
            
    except Exception as e:
        return False, f"错误: {str(e)}"

def main():
    """主函数"""
    print("🔧 修复带空格的粗体格式问题...")
    print("=" * 50)
    
    # 查找所有Markdown文件
    md_files = []
    for pattern in ['docs/**/*.md', 'docs/*.md', '*.md']:
        md_files.extend(glob.glob(pattern, recursive=True))
    
    # 去重并排序
    md_files = sorted(list(set(md_files)))
    
    fixed_count = 0
    
    for file_path in md_files:
        if not os.path.exists(file_path):
            continue
            
        # 检查文件是否包含问题格式
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if '** ' in content or ' *' in content:
            print(f"📄 修复文件: {file_path}")
            success, message = fix_file(file_path)
            
            if success:
                print(f"  ✅ {message}")
                fixed_count += 1
            else:
                print(f"  ⏭️ {message}")
    
    print()
    print("=" * 50)
    print(f"🎉 修复完成！共修复了 {fixed_count} 个文件")

if __name__ == "__main__":
    main()
