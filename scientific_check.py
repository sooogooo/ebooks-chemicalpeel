#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def check_scientific_accuracy():
    """检查科学性和准确性"""
    
    print("🔬 科学性和准确性检查:\n")
    
    # 关键科学术语检查
    scientific_terms = {
        '酸类': ['水杨酸', '果酸', '乳酸', '杏仁酸', '壬二酸', '维A酸'],
        '皮肤结构': ['角质层', '表皮', '真皮', '皮脂腺', '毛囊'],
        '生理过程': ['角质代谢', '细胞更新', '胶原蛋白', '弹性纤维'],
        '安全指标': ['pH值', '浓度', '刺激性', '过敏反应', '光敏性']
    }
    
    docs_path = Path("docs")
    chapters_path = docs_path / "chapters"
    
    term_coverage = {}
    
    # 检查术语覆盖度
    for category, terms in scientific_terms.items():
        found_terms = []
        
        for chapter_file in chapters_path.glob("*.md"):
            if chapter_file.name.endswith('.backup') or 'display_backup' in chapter_file.name:
                continue
                
            try:
                with open(chapter_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    for term in terms:
                        if term in content:
                            found_terms.append(term)
            except:
                continue
        
        coverage = len(set(found_terms)) / len(terms) * 100
        term_coverage[category] = {
            'coverage': coverage,
            'found': list(set(found_terms)),
            'missing': [t for t in terms if t not in found_terms]
        }
        
        print(f"  📋 {category}: {coverage:.1f}% 覆盖")
        if coverage < 80:
            print(f"    ⚠️  缺失术语: {', '.join(term_coverage[category]['missing'])}")
    
    # 检查引用和参考文献
    print(f"\n📚 引用和参考文献检查:")
    
    reference_patterns = [
        r'参考文献',
        r'引用',
        r'\[.*?\]',  # 引用标记
        r'研究表明',
        r'临床试验',
        r'皮肤科医生'
    ]
    
    total_references = 0
    
    for chapter_file in chapters_path.glob("*.md"):
        if chapter_file.name.endswith('.backup') or 'display_backup' in chapter_file.name:
            continue
            
        try:
            with open(chapter_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                chapter_refs = 0
                for pattern in reference_patterns:
                    matches = re.findall(pattern, content)
                    chapter_refs += len(matches)
                
                if chapter_refs > 0:
                    total_references += chapter_refs
                    print(f"  ✅ {chapter_file.name}: {chapter_refs} 个引用")
        except:
            continue
    
    print(f"  📊 总引用数: {total_references}")
    
    # 检查安全警告
    print(f"\n⚠️  安全警告检查:")
    
    safety_keywords = [
        '注意', '警告', '禁忌', '副作用', '过敏', 
        '刺激', '敏感', '测试', '咨询医生', '专业指导'
    ]
    
    safety_mentions = 0
    
    for chapter_file in chapters_path.glob("*.md"):
        if chapter_file.name.endswith('.backup') or 'display_backup' in chapter_file.name:
            continue
            
        try:
            with open(chapter_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                for keyword in safety_keywords:
                    if keyword in content:
                        safety_mentions += content.count(keyword)
        except:
            continue
    
    print(f"  🛡️  安全提醒总数: {safety_mentions}")
    
    if safety_mentions < 20:
        print(f"  ⚠️  建议增加更多安全提醒")
    else:
        print(f"  ✅ 安全提醒充足")
    
    return term_coverage

def check_content_continuity():
    """检查内容连续性"""
    
    print(f"\n🔗 内容连续性检查:")
    
    docs_path = Path("docs")
    chapters_path = docs_path / "chapters"
    
    # 预期的章节顺序
    expected_order = [
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
    
    # 检查章节标题和编号
    for i, chapter in enumerate(expected_order, 1):
        chapter_file = chapters_path / chapter
        
        if chapter_file.exists():
            try:
                with open(chapter_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # 检查是否有标题
                    title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
                    if title_match:
                        title = title_match.group(1)
                        print(f"  ✅ 第{i:02d}章: {title}")
                    else:
                        print(f"  ⚠️  第{i:02d}章: 缺少标题")
            except:
                print(f"  ❌ 第{i:02d}章: 读取失败")
        else:
            print(f"  ❌ 第{i:02d}章: 文件缺失")
    
    # 检查内部链接
    print(f"\n🔗 内部链接检查:")
    
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    broken_links = []
    
    for chapter_file in chapters_path.glob("*.md"):
        if chapter_file.name.endswith('.backup') or 'display_backup' in chapter_file.name:
            continue
            
        try:
            with open(chapter_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                links = re.findall(link_pattern, content)
                
                for link_text, link_url in links:
                    if link_url.startswith('http'):
                        continue  # 外部链接
                    
                    # 检查内部链接是否存在
                    if link_url.startswith('../'):
                        target_path = docs_path / link_url[3:]
                    else:
                        target_path = chapter_file.parent / link_url
                    
                    if not target_path.exists():
                        broken_links.append(f"{chapter_file.name}: {link_url}")
        except:
            continue
    
    if broken_links:
        print(f"  ❌ 发现 {len(broken_links)} 个失效链接:")
        for link in broken_links[:5]:  # 只显示前5个
            print(f"    - {link}")
    else:
        print(f"  ✅ 内部链接检查通过")

if __name__ == "__main__":
    check_scientific_accuracy()
    check_content_continuity()
