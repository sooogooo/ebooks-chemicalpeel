#!/usr/bin/env python3
"""
修复Markdown渲染问题的脚本
解决"markdown裸奔"问题，确保所有Markdown语法正确渲染
"""

import os
import re
import glob

def fix_markdown_rendering():
    """修复所有Markdown文件的渲染问题"""
    
    # 定义需要处理的目录
    directories = [
        'docs/chapters',
        'docs/appendix', 
        'docs/about',
        'docs'
    ]
    
    fixed_files = []
    
    for directory in directories:
        if not os.path.exists(directory):
            print(f"目录不存在: {directory}")
            continue
            
        # 查找所有Markdown文件
        md_files = glob.glob(f"{directory}/*.md")
        
        for file_path in md_files:
            if file_path.endswith('.backup'):
                continue
                
            print(f"处理文件: {file_path}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # 修复常见的Markdown渲染问题
                content = fix_common_issues(content)
                
                # 如果内容有变化，写回文件
                if content != original_content:
                    # 创建备份
                    backup_path = file_path + '.render_backup'
                    if not os.path.exists(backup_path):
                        with open(backup_path, 'w', encoding='utf-8') as f:
                            f.write(original_content)
                    
                    # 写入修复后的内容
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    fixed_files.append(file_path)
                    print(f"  ✅ 已修复渲染问题")
                else:
                    print(f"  ℹ️  无需修复")
                    
            except Exception as e:
                print(f"  ❌ 处理失败: {e}")
    
    print(f"\n修复完成！共处理了 {len(fixed_files)} 个文件:")
    for file_path in fixed_files:
        print(f"  - {file_path}")

def fix_common_issues(content):
    """修复常见的Markdown渲染问题"""
    
    # 1. 确保列表项前有空行
    content = re.sub(r'(\*\*[^*]+\*\*[^:\n]*：)\n(-)', r'\1\n\n\2', content)
    
    # 2. 确保代码块前后有空行
    content = re.sub(r'([^\n])\n```', r'\1\n\n```', content)
    content = re.sub(r'```\n([^\n])', r'```\n\n\1', content)
    
    # 3. 确保标题前后有空行
    content = re.sub(r'([^\n])\n(#{1,6}\s)', r'\1\n\n\2', content)
    content = re.sub(r'(#{1,6}[^\n]*)\n([^\n#])', r'\1\n\n\2', content)
    
    # 4. 修复表格格式
    content = re.sub(r'([^\n])\n(\|[^|\n]*\|)', r'\1\n\n\2', content)
    
    # 5. 确保引用块前后有空行
    content = re.sub(r'([^\n])\n(>)', r'\1\n\n\2', content)
    
    # 6. 修复列表项格式 - 确保列表项之间的间距正确
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        fixed_lines.append(line)
        
        # 如果当前行是粗体文本后跟冒号，下一行是列表项，确保有空行
        if (re.match(r'\*\*[^*]+\*\*[^:\n]*：\s*$', line) and 
            i + 1 < len(lines) and 
            lines[i + 1].strip().startswith('-')):
            fixed_lines.append('')
    
    content = '\n'.join(fixed_lines)
    
    # 7. 清理多余的空行（超过2个连续空行的情况）
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    # 8. 确保文件末尾有且仅有一个换行符
    content = content.rstrip() + '\n'
    
    return content

def validate_markdown_syntax():
    """验证Markdown语法是否正确"""
    print("\n验证Markdown语法...")
    
    directories = ['docs/chapters', 'docs/appendix', 'docs/about']
    issues = []
    
    for directory in directories:
        if not os.path.exists(directory):
            continue
            
        md_files = glob.glob(f"{directory}/*.md")
        
        for file_path in md_files:
            if file_path.endswith('.backup'):
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查常见问题
                file_issues = []
                
                # 检查未闭合的粗体标记
                bold_count = content.count('**')
                if bold_count % 2 != 0:
                    file_issues.append("未闭合的粗体标记")
                
                # 检查未闭合的斜体标记
                italic_count = content.count('*') - bold_count * 2
                if italic_count % 2 != 0:
                    file_issues.append("未闭合的斜体标记")
                
                # 检查代码块
                code_block_count = content.count('```')
                if code_block_count % 2 != 0:
                    file_issues.append("未闭合的代码块")
                
                if file_issues:
                    issues.append((file_path, file_issues))
                else:
                    print(f"  ✅ {os.path.basename(file_path)}")
                    
            except Exception as e:
                issues.append((file_path, [f"读取错误: {e}"]))
    
    if issues:
        print(f"\n⚠️  发现 {len(issues)} 个文件有语法问题:")
        for file_path, file_issues in issues:
            print(f"  - {file_path}:")
            for issue in file_issues:
                print(f"    • {issue}")
    else:
        print(f"\n🎉 所有Markdown文件语法正确！")

if __name__ == "__main__":
    print("🔧 开始修复Markdown渲染问题...")
    fix_markdown_rendering()
    validate_markdown_syntax()
    print("\n🎉 修复完成！请重启MkDocs服务查看效果。")
