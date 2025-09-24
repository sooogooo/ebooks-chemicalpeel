#!/usr/bin/env python3
"""
最终清理脚本：清除所有剩余的自吹自擂内容和格式问题
"""

import os
import re
import glob

def final_cleanup(content):
    """最终清理所有问题"""
    
    # 清除各种自吹自擂的表述
    self_praise_patterns = [
        r'\*\*金句来了：\*\*\s*',
        r'金句来了：\s*',
        r'\*\*脱口秀时间：\*\*\s*',
        r'脱口秀时间：\s*',
        r'\*\*网络梗时间：\*\*\s*',
        r'网络梗时间：\s*',
        r'\*\*💡\s*脱口秀时间：\*\*\s*',
        r'\*\*💡\s*金句：\*\*\s*',
        r'\*\*章末彩蛋：\*\*\s*',
        r'\*\*今日作业：\*\*\s*',
        r'\*\*下一章预告：\*\*\s*',
        r'\*\*终极金句：\*\*\s*',
        r'\*\*智慧金句：\*\*\s*',
        r'\*\*护肤金句：\*\*\s*',
        r'\*\*美肌金句：\*\*\s*',
    ]
    
    # 逐个清除这些标题
    for pattern in self_praise_patterns:
        content = re.sub(pattern, '', content)
    
    # 修复格式问题
    # 1. 确保标题前后有空行
    content = re.sub(r'([^\n])(##\s+)', r'\1\n\n\2', content)
    content = re.sub(r'(##[^\n]+)([^\n])', r'\1\n\n\2', content)
    
    # 2. 修复列表格式
    content = re.sub(r'^-\*\*', r'- **', content, flags=re.MULTILINE)
    content = re.sub(r'^-([^*\s])', r'- \1', content, flags=re.MULTILINE)
    
    # 3. 清理多余的空行
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # 4. 修复段落符号
    content = re.sub(r'¶\s*$', '', content, flags=re.MULTILINE)
    
    # 5. 修复粗体格式的剩余问题
    content = re.sub(r'\*\*([^*]+)\s+\*\*', r'**\1**', content)
    content = re.sub(r'\*\*\s+([^*]+)\*\*', r'**\1**', content)
    
    return content

def fix_file(file_path):
    """修复单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = final_cleanup(content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "已清理"
        else:
            return False, "无需处理"
            
    except Exception as e:
        return False, f"错误: {str(e)}"

def main():
    """主函数"""
    print("🧹 最终清理：清除所有剩余问题...")
    print("=" * 50)
    
    # 处理所有docs目录下的文件
    md_files = glob.glob('docs/**/*.md', recursive=True)
    
    cleaned_count = 0
    
    for file_path in md_files:
        if not os.path.exists(file_path):
            continue
            
        # 检查文件是否包含需要清理的内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        has_issues = any(phrase in content for phrase in [
            '金句来了', '脱口秀时间', '网络梗时间', '章末彩蛋', 
            '今日作业', '下一章预告', '¶', '-**'
        ])
        
        if has_issues:
            print(f"📄 清理文件: {file_path}")
            
            success, message = fix_file(file_path)
            
            if success:
                print(f"  ✅ {message}")
                cleaned_count += 1
            else:
                print(f"  ⏭️ {message}")
    
    print()
    print("=" * 50)
    print(f"🎉 最终清理完成！共处理了 {cleaned_count} 个文件")
    print("📖 内容现在完全专业化！")

if __name__ == "__main__":
    main()
