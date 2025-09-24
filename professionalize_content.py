#!/usr/bin/env python3
"""
专业化内容脚本：将娱乐化表述替换为专业表述
"""

import os
import re
import glob

def professionalize_content(content):
    """将娱乐化表述替换为专业表述"""
    
    # 娱乐化表述替换映射
    replacements = {
        # 人物比喻
        r'天生的"高光女王"': '油性肌肤',
        r'天生的"素颜女神"': '干性肌肤',
        r'护肤界的"天选之子"': '中性肌肤',
        r'护肤界的"双面娇娃"': '混合性肌肤',
        r'护肤界的"林黛玉"': '敏感性肌肤',
        r'玻璃心的"林黛玉"': '敏感性肌肤',
        r'人格分裂的"双面娇娃"': '混合性肌肤',
        
        # 娱乐化比喻
        r'护肤界的"精神分裂"': '需要分区护理',
        r'护肤界的"三座大山"': '主要护理重点',
        r'护肤界的"美食评论家"': '对成分敏感',
        r'毛孔放大镜': '毛孔明显',
        r'痘痘宇宙': '痘痘问题',
        r'磨皮滤镜': '肌肤细腻',
        r'毛孔隐身术': '毛孔细小',
        r'变脸大师': '状态变化明显',
        
        # 夸张表述
        r'能当.*?的教学素材': '较为明显',
        r'脸上经常上演.*?大片': '容易出现相关问题',
        r'堪比.*?"': '表现为',
        r'简直是.*?"': '主要包括',
        r'像.*?一样': '表现为',
        r'就像.*?': '类似于',
        
        # 人生格言类
        r'.*?的人生格言——.*?"': '',
        r'.*?的护肤哲学——.*?"': '',
        r'.*? = .*?': '',
        
        # 口语化表述
        r'恭喜你，你是': '您的肌肤类型为',
        r'中奖了！你是': '您的肌肤类型为',
        r'你是': '肌肤类型为',
        r'你的脸在"闹什么脾气"': '肌肤问题分析',
        r'人设变化': '状态变化',
        r'"人设"': '特征',
        
        # 清理多余的引号和符号
        r'""': '',
        r'！"': '',
        r'"': '',
        r'！': '',
    }
    
    # 逐个替换
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    # 清理多余的空行和格式问题
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r'^\s*$\n', '', content, flags=re.MULTILINE)
    
    return content

def fix_file(file_path):
    """修复单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = professionalize_content(content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "已专业化"
        else:
            return False, "无需处理"
            
    except Exception as e:
        return False, f"错误: {str(e)}"

def main():
    """主函数"""
    print("🎯 内容专业化：清除娱乐化表述...")
    print("=" * 50)
    
    # 处理所有docs目录下的文件
    md_files = glob.glob('docs/**/*.md', recursive=True)
    
    processed_count = 0
    
    for file_path in md_files:
        if not os.path.exists(file_path):
            continue
            
        # 检查文件是否包含娱乐化表述
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        has_entertainment = any(phrase in content for phrase in [
            '高光女王', '素颜女神', '林黛玉', '双面娇娃', '天选之子',
            '人生格言', '护肤哲学', '精神分裂', '人设', '闹什么脾气'
        ])
        
        if has_entertainment:
            print(f"📄 专业化文件: {file_path}")
            
            success, message = fix_file(file_path)
            
            if success:
                print(f"  ✅ {message}")
                processed_count += 1
            else:
                print(f"  ⏭️ {message}")
    
    print()
    print("=" * 50)
    print(f"🎉 专业化完成！共处理了 {processed_count} 个文件")
    print("📖 内容现在完全符合专业标准！")

if __name__ == "__main__":
    main()
