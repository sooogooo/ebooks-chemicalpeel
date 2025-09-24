#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def count_chinese_chars(text):
    """统计中文字符数"""
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    return len(chinese_pattern.findall(text))

def analyze_chapters_for_expansion():
    """分析需要扩充的章节"""
    
    chapters_path = Path("docs/chapters")
    target_length = 6000
    
    chapters_to_expand = []
    
    for chapter_file in sorted(chapters_path.glob("[0-9][0-9]_*.md")):
        if '.backup' in chapter_file.name or 'display_backup' in chapter_file.name:
            continue
            
        with open(chapter_file, 'r', encoding='utf-8') as f:
            content = f.read()
            chinese_chars = count_chinese_chars(content)
            
            if chinese_chars < target_length:
                chapters_to_expand.append({
                    'file': chapter_file.name,
                    'current': chinese_chars,
                    'needed': target_length - chinese_chars,
                    'path': chapter_file
                })
                
    return chapters_to_expand

if __name__ == "__main__":
    chapters = analyze_chapters_for_expansion()
    
    print("需要扩充的章节:")
    for ch in chapters:
        print(f"  {ch['file']}: {ch['current']} → 6000 (需增加 {ch['needed']} 字)")
