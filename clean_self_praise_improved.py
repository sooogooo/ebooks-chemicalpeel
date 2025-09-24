#!/usr/bin/env python3
"""
改进版：彻底清除正文中的自吹自擂标题，但保留内容
"""

import os
import re
import glob

def clean_self_praise_titles(content):
    """彻底清除自吹自擂的标题，但保留内容"""
    
    # 更全面的自吹自擂标题模式
    self_praise_patterns = [
        # 基本格式
        r'\*\*脱口秀时间：\*\*\s*',
        r'\*\*金句的力量：\*\*\s*',
        r'\*\*金句开场：\*\*\s*',
        r'\*\*金句：\*\*\s*',
        r'\*\*网络梗：\*\*\s*',
        r'\*\*脱口秀：\*\*\s*',
        r'\*\*终极金句：\*\*\s*',
        r'\*\*章末金句：\*\*\s*',
        r'\*\*每日金句：\*\*\s*',
        r'\*\*智慧金句：\*\*\s*',
        r'\*\*护肤金句：\*\*\s*',
        r'\*\*美肌金句：\*\*\s*',
        r'\*\*网络梗时间：\*\*\s*',
        
        # 带💡等emoji的格式
        r'\*\*💡\s*脱口秀时间：\*\*\s*',
        r'\*\*💡\s*金句：\*\*\s*',
        r'\*\*💡\s*网络梗：\*\*\s*',
        
        # 其他可能的格式
        r'脱口秀时间：\s*',
        r'金句开场：\s*',
        r'网络梗时间：\s*',
        r'金句：\s*',
        
        # 清除一些过于自夸的表述
        r'\*\*章末彩蛋：\*\*\s*',
        r'\*\*今日作业：\*\*\s*',
        r'\*\*下一章预告：\*\*\s*',
    ]
    
    # 逐个清除这些标题
    for pattern in self_praise_patterns:
        content = re.sub(pattern, '', content)
    
    # 清除一些特定的自吹自擂句式
    content = re.sub(r'这就是传说中的.*?啊！', '', content)
    content = re.sub(r'简直就是.*?的完美诠释！', '', content)
    
    return content

def fix_remaining_format_issues(content):
    """修复剩余的格式问题"""
    
    # 修复连续的粗体标记
    content = re.sub(r'\*\*([^*]+)\*\*\*\*([^*]+)\*\*', r'**\1** **\2**', content)
    
    # 清理多余的空行
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # 修复段落符号
    content = re.sub(r'¶\s*$', '', content, flags=re.MULTILINE)
    
    return content

def fix_file(file_path):
    """修复单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 应用所有修复
        content = clean_self_praise_titles(content)
        content = fix_remaining_format_issues(content)
        
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
    print("🧹 彻底清除自吹自擂内容...")
    print("=" * 50)
    
    # 只处理docs目录下的章节文件
    chapter_files = glob.glob('docs/chapters/*.md', recursive=True)
    other_docs = ['docs/preface.md', 'docs/introduction.md', 'docs/index.md', 'docs/epilogue.md']
    
    all_files = chapter_files + other_docs
    
    cleaned_count = 0
    
    for file_path in all_files:
        if not os.path.exists(file_path):
            continue
            
        # 检查文件是否包含需要清理的内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        has_self_praise = any(phrase in content for phrase in [
            '脱口秀时间', '金句', '网络梗', '章末彩蛋', '今日作业', '下一章预告'
        ])
        
        if has_self_praise:
            print(f"📄 清理文件: {file_path}")
            
            success, message = fix_file(file_path)
            
            if success:
                print(f"  ✅ {message}")
                cleaned_count += 1
            else:
                print(f"  ⏭️ {message}")
    
    print()
    print("=" * 50)
    print(f"🎉 清理完成！共处理了 {cleaned_count} 个文件")
    print("📖 内容现在更加专业和简洁！")

if __name__ == "__main__":
    main()
