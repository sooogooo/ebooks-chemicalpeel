#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import glob
from pathlib import Path

def count_chinese_chars(text):
    """统计中文字符数"""
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    return len(chinese_pattern.findall(text))

def analyze_content():
    """分析内容完整性和统计信息"""
    
    docs_path = Path("docs")
    
    # 统计信息
    stats = {
        'total_files': 0,
        'total_chinese_chars': 0,
        'total_words': 0,
        'chapters': [],
        'missing_files': [],
        'broken_links': []
    }
    
    # 预期的章节文件
    expected_chapters = [
        '01_know_your_skin.md',
        '02_acid_science.md', 
        '03_acid_encyclopedia.md',
        '04_preparation.md',
        '05_beginner_guide.md',
        '06_targeted_solutions.md',
        '07_product_selection.md',
        '08_care_during_process.md',
        '09_medical_grade_peels.md',
        '10_safety_risk_control.md',
        '11_evaluation_adjustment.md',
        '12_lifestyle_management.md',
        '13_makeup_balance.md',
        '14_community_sharing.md'
    ]
    
    print("=== 《刷酸医美：刷出好气色》内容分析报告 ===\n")
    
    # 检查章节完整性
    print("📚 章节完整性检查:")
    chapters_path = docs_path / "chapters"
    
    for chapter in expected_chapters:
        chapter_file = chapters_path / chapter
        if chapter_file.exists():
            with open(chapter_file, 'r', encoding='utf-8') as f:
                content = f.read()
                chinese_chars = count_chinese_chars(content)
                word_count = len(content.split())
                
                stats['chapters'].append({
                    'file': chapter,
                    'chinese_chars': chinese_chars,
                    'word_count': word_count,
                    'size': len(content)
                })
                
                stats['total_chinese_chars'] += chinese_chars
                stats['total_words'] += word_count
                stats['total_files'] += 1
                
                print(f"  ✅ {chapter} - {chinese_chars:,} 中文字符")
        else:
            stats['missing_files'].append(chapter)
            print(f"  ❌ {chapter} - 文件缺失")
    
    # 检查其他重要文件
    print("\n📄 其他文件检查:")
    other_files = [
        'index.md',
        'preface.md', 
        'introduction.md',
        'epilogue.md'
    ]
    
    for file in other_files:
        file_path = docs_path / file
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                chinese_chars = count_chinese_chars(content)
                stats['total_chinese_chars'] += chinese_chars
                stats['total_files'] += 1
                print(f"  ✅ {file} - {chinese_chars:,} 中文字符")
        else:
            print(f"  ❌ {file} - 文件缺失")
    
    # 检查附录文件
    print("\n📋 附录文件检查:")
    appendix_path = docs_path / "appendix"
    if appendix_path.exists():
        for file in appendix_path.glob("*.md"):
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                chinese_chars = count_chinese_chars(content)
                stats['total_chinese_chars'] += chinese_chars
                stats['total_files'] += 1
                print(f"  ✅ {file.name} - {chinese_chars:,} 中文字符")
    
    # 检查图片文件
    print("\n🖼️  图片资源检查:")
    images_path = docs_path / "images"
    if images_path.exists():
        svg_files = list(images_path.glob("*.svg"))
        png_files = list(images_path.glob("*.png"))
        jpg_files = list(images_path.glob("*.jpg"))
        
        print(f"  📊 SVG图表: {len(svg_files)} 个")
        print(f"  🖼️  PNG图片: {len(png_files)} 个") 
        print(f"  📷 JPG图片: {len(jpg_files)} 个")
    
    # 统计总结
    print(f"\n📊 统计总结:")
    print(f"  📁 总文件数: {stats['total_files']}")
    print(f"  🔤 中文字符总数: {stats['total_chinese_chars']:,}")
    print(f"  📖 预估阅读时间: {stats['total_chinese_chars'] // 400:.0f} 分钟")
    print(f"  📄 预估页数: {stats['total_chinese_chars'] // 500:.0f} 页")
    
    # 章节字数分布
    print(f"\n📈 章节字数分布:")
    for chapter in stats['chapters']:
        print(f"  {chapter['file']}: {chapter['chinese_chars']:,} 字符")
    
    # 内容质量检查
    print(f"\n🔍 内容质量检查:")
    
    # 检查是否有空文件
    empty_files = [ch for ch in stats['chapters'] if ch['chinese_chars'] < 100]
    if empty_files:
        print(f"  ⚠️  疑似空文件: {len(empty_files)} 个")
        for f in empty_files:
            print(f"    - {f['file']}")
    else:
        print(f"  ✅ 无空文件")
    
    # 检查章节长度均衡性
    avg_length = stats['total_chinese_chars'] / len(stats['chapters']) if stats['chapters'] else 0
    short_chapters = [ch for ch in stats['chapters'] if ch['chinese_chars'] < avg_length * 0.5]
    long_chapters = [ch for ch in stats['chapters'] if ch['chinese_chars'] > avg_length * 2]
    
    if short_chapters:
        print(f"  📏 偏短章节 (<{avg_length*0.5:.0f}字): {len(short_chapters)} 个")
    if long_chapters:
        print(f"  📏 偏长章节 (>{avg_length*2:.0f}字): {len(long_chapters)} 个")
    
    if not short_chapters and not long_chapters:
        print(f"  ✅ 章节长度分布均衡")
    
    return stats

if __name__ == "__main__":
    analyze_content()
