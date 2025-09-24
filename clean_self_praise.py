#!/usr/bin/env python3
"""
清除正文中的自吹自擂标题，但保留内容
同时修复新发现的Markdown格式问题
"""

import os
import re
import glob

def clean_self_praise_titles(content):
    """清除自吹自擂的标题，但保留内容"""
    
    # 需要清除的自吹自擂标题模式
    self_praise_patterns = [
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
    ]
    
    # 逐个清除这些标题
    for pattern in self_praise_patterns:
        content = re.sub(pattern, '', content)
    
    return content

def fix_spaced_bold_issues(content):
    """修复新发现的空格粗体问题"""
    
    # 修复 **文字 ** 格式为 **文字**
    content = re.sub(r'\*\*([^*]+)\s+\*\*', r'**\1**', content)
    
    # 修复 ** 文字 ** 格式为 **文字**
    content = re.sub(r'\*\*\s+([^*]+)\s+\*\*', r'**\1**', content)
    
    # 修复 ** 文字** 格式为 **文字**
    content = re.sub(r'\*\*\s+([^*]+)\*\*', r'**\1**', content)
    
    return content

def clean_paragraph_symbols(content):
    """清除段落符号¶"""
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
        content = fix_spaced_bold_issues(content)
        content = clean_paragraph_symbols(content)
        
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
    print("🧹 清除自吹自擂标题并修复格式问题...")
    print("=" * 60)
    
    # 查找所有Markdown文件
    md_files = []
    for pattern in ['docs/**/*.md', 'docs/*.md', '*.md']:
        md_files.extend(glob.glob(pattern, recursive=True))
    
    # 去重并排序
    md_files = sorted(list(set(md_files)))
    
    # 排除一些不需要处理的文件
    exclude_files = [
        'README.md',
        'MKDOCS_SERVICE_INFO.md',
        'SPECIAL_BOLD_FIX_REPORT.md',
        'FINAL_MARKDOWN_NAKED_FIX_REPORT.md',
        'COMPREHENSIVE_MARKDOWN_FIX_REPORT.md',
        'MARKDOWN_FORMAT_FIX_REPORT.md',
        'MARKDOWN_NAKED_FIX_FINAL_REPORT.md',
    ]
    
    md_files = [f for f in md_files if not any(exclude in f for exclude in exclude_files)]
    
    fixed_count = 0
    cleaned_count = 0
    
    for file_path in md_files:
        if not os.path.exists(file_path):
            continue
            
        # 检查文件是否包含需要处理的内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        has_self_praise = any(phrase in content for phrase in [
            '脱口秀时间', '金句', '网络梗', '脱口秀'
        ])
        
        has_format_issues = any(issue in content for issue in [
            '** ', ' **', '¶'
        ])
        
        if has_self_praise or has_format_issues:
            print(f"📄 处理文件: {file_path}")
            
            if has_self_praise:
                print(f"  🧹 清除自吹自擂内容")
                cleaned_count += 1
                
            if has_format_issues:
                print(f"  🔧 修复格式问题")
            
            success, message = fix_file(file_path)
            
            if success:
                print(f"  ✅ {message}")
                fixed_count += 1
            else:
                print(f"  ⏭️ {message}")
    
    print()
    print("=" * 60)
    print(f"📊 处理统计:")
    print(f"  🧹 清除自吹自擂内容: {cleaned_count} 个文件")
    print(f"  🔧 修复格式问题: {fixed_count} 个文件")
    print(f"  📁 总处理文件: {len([f for f in md_files if os.path.exists(f)])}")
    
    if fixed_count > 0:
        print(f"\n🎉 处理完成！内容更加专业简洁！")
    else:
        print(f"\n✨ 所有文件都很完美，无需处理！")

if __name__ == "__main__":
    main()
