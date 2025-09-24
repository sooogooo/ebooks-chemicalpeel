#!/usr/bin/env python3
"""
Check for potential numbered list formatting issues across all chapters
"""

import os
import re
import glob

def check_numbered_lists(file_path):
    """Check for numbered lists that might need to be bullet points"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        issues = []
        
        for i, line in enumerate(lines, 1):
            # Look for numbered lists with bold items that might be categories/options
            if re.match(r'^\d+\. \*\*[^*]+\*\*', line):
                # Check context to see if this looks like options/categories
                context_before = lines[max(0, i-3):i-1] if i > 1 else []
                context_after = lines[i:min(len(lines), i+3)]
                
                # Look for indicators that this should be bullet points
                indicators = [
                    '正确做法', '错误做法', '注意事项', '要点', '特点',
                    '优点', '缺点', '建议', '方法', '策略'
                ]
                
                context_text = ' '.join(context_before + context_after)
                if any(indicator in context_text for indicator in indicators):
                    issues.append({
                        'line': i,
                        'content': line.strip(),
                        'context': context_text[:100] + '...' if len(context_text) > 100 else context_text
                    })
        
        return issues
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return []

def main():
    """Check all chapters for potential list formatting issues"""
    print("🔍 Checking for potential numbered list formatting issues...")
    print("=" * 70)
    
    chapter_files = glob.glob("docs/chapters/*.md")
    chapter_files.sort()
    
    total_issues = 0
    
    for file_path in chapter_files:
        chapter_name = os.path.basename(file_path)
        issues = check_numbered_lists(file_path)
        
        if issues:
            print(f"\n📝 {chapter_name}:")
            for issue in issues:
                print(f"  Line {issue['line']}: {issue['content']}")
                print(f"    Context: {issue['context']}")
            total_issues += len(issues)
        else:
            print(f"✅ {chapter_name}: No issues found")
    
    print("=" * 70)
    if total_issues > 0:
        print(f"⚠️  Found {total_issues} potential formatting issues")
        print("These numbered lists might need to be converted to bullet points")
    else:
        print("✅ No potential formatting issues found!")

if __name__ == "__main__":
    main()
