#!/usr/bin/env python3
"""
Comprehensive fix script for Chapters 13 and 14
Addresses HTML rendering issues discovered through browser simulation
"""

import re
import os

def fix_chapter_13():
    """Fix Chapter 13 formatting issues"""
    file_path = '/home/sooogooo/AmazonQ/ebooks/ChemicalPell/docs/chapters/13_makeup_balance.md'
    
    # Create backup
    backup_path = file_path + '.urgent_backup'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            backup_content = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(backup_content)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix broken headers and mixed formatting patterns
    content = re.sub(r'\*\*💄 刷酸期间的底妆"黄金法则"：\*\*', '**💄 刷酸期间的底妆"黄金法则"：**', content)
    content = re.sub(r'#### 法则一：产品选择要温和\*\*粉底液选择标准：\*\*', '#### 法则一：产品选择要温和\n\n**粉底液选择标准：**', content)
    content = re.sub(r'\*\*正确上妆步骤：\*\*1\. 妆前护肤（充分保湿）', '**正确上妆步骤：**\n\n1. 妆前护肤（充分保湿）', content)
    content = re.sub(r'\*\*刷酸期间常见问题及遮瑕：\*\*', '**刷酸期间常见问题及遮瑕：**', content)
    
    # Fix emoji headers and mixed content
    content = re.sub(r'\*\*👁️ 眼部化妆的特殊考虑：\*\*', '**👁️ 眼部化妆的特殊考虑：**', content)
    content = re.sub(r'#### 眼部肌肤保护：\*\*眼部特点：\*\*', '#### 眼部肌肤保护：\n\n**眼部特点：**', content)
    content = re.sub(r'\*\*眼影选择：\*\*', '**眼影选择：**', content)
    content = re.sub(r'\*\*口红选择：\*\*', '**口红选择：**', content)
    
    # Fix section headers with mixed formatting
    content = re.sub(r'\*\*🎨 个性化底妆搭配：\*\*', '**🎨 个性化底妆搭配：**', content)
    content = re.sub(r'#### 干燥脱皮期的底妆：\*\*肌肤状态：\*\*', '#### 干燥脱皮期的底妆：\n\n**肌肤状态：**', content)
    content = re.sub(r'\*\*肌肤状态：\*\*', '**肌肤状态：**', content)
    content = re.sub(r'\*\*底妆策略：\*\*', '**底妆策略：**', content)
    
    # Fix tool selection sections
    content = re.sub(r'\*\*🧽 工具选择的"卫生标准"：\*\*', '**🧽 工具选择的"卫生标准"：**', content)
    content = re.sub(r'#### 推荐化妆工具：\*\*美妆蛋：\*\*', '#### 推荐化妆工具：\n\n**美妆蛋：**', content)
    content = re.sub(r'\*\*为什么要重视清洁：\*\*', '**为什么要重视清洁：**', content)
    
    # Fix concealer sections
    content = re.sub(r'\*\*🎯 精准遮瑕的"技术流"：\*\*', '**🎯 精准遮瑕的"技术流"：**', content)
    content = re.sub(r'#### 痘痘遮瑕技巧：\*\*红肿痘痘：\*\*1\. 颜色校正：绿色遮瑕膏中和红色', '#### 痘痘遮瑕技巧：\n\n**红肿痘痘：**\n\n1. 颜色校正：绿色遮瑕膏中和红色', content)
    content = re.sub(r'\*\*红色痘印：\*\*', '**红色痘印：**', content)
    content = re.sub(r'\*\*浅色斑：\*\*', '**浅色斑：**', content)
    
    # Fix product recommendation sections
    content = re.sub(r'\*\*💝 不同需求的遮瑕"神器"：\*\*', '**💝 不同需求的遮瑕"神器"：**', content)
    content = re.sub(r'#### 按质地分类：\*\*液体遮瑕：\*\*', '#### 按质地分类：\n\n**液体遮瑕：**', content)
    content = re.sub(r'\*\*色彩校正：\*\*', '**色彩校正：**', content)
    
    # Fix makeup removal sections
    content = re.sub(r'\*\*🧼 为什么卸妆更重要了？\*\*', '**🧼 为什么卸妆更重要了？**', content)
    content = re.sub(r'#### 刷酸期间的特殊考虑：\*\*肌肤敏感性增加：\*\*', '#### 刷酸期间的特殊考虑：\n\n**肌肤敏感性增加：**', content)
    content = re.sub(r'\*\*💧 温和卸妆的"黄金流程"：\*\*', '**💧 温和卸妆的"黄金流程"：**', content)
    content = re.sub(r'#### 步骤一：眼唇卸妆\*\*为什么要分开卸妆：\*\*', '#### 步骤一：眼唇卸妆\n\n**为什么要分开卸妆：**', content)
    content = re.sub(r'\*\*卸妆产品选择：\*\*', '**卸妆产品选择：**', content)
    content = re.sub(r'\*\*为什么需要二次清洁：\*\*', '**为什么需要二次清洁：**', content)
    
    # Fix product recommendation sections
    content = re.sub(r'\*\*🌟 刷酸期间的卸妆"好帮手"：\*\*', '**🌟 刷酸期间的卸妆"好帮手"：**', content)
    content = re.sub(r'#### 温和卸妆油：\*\*推荐产品：\*\*', '#### 温和卸妆油：\n\n**推荐产品：**', content)
    content = re.sub(r'\*\*推荐产品：\*\*', '**推荐产品：**', content)
    
    # Clean up multiple empty lines
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Chapter 13 formatting fixes applied!")

def fix_chapter_14():
    """Fix Chapter 14 formatting issues"""
    file_path = '/home/sooogooo/AmazonQ/ebooks/ChemicalPell/docs/chapters/14_community_sharing.md'
    
    # Create backup
    backup_path = file_path + '.urgent_backup'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            backup_content = f.read()
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(backup_content)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix broken text patterns and mixed formatting
    content = re.sub(r'征\*\*🌟 什么样的社群值得加入？\*\*##', '征\n\n### 🌟 什么样的社群值得加入？', content)
    content = re.sub(r'\*\*##$', '**', content, flags=re.MULTILINE)
    content = re.sub(r'##$', '', content, flags=re.MULTILINE)
    
    # Fix section headers with mixed formatting
    content = re.sub(r'## 优质刷酸社群的特征\*\*🌟 什么样的社群值得加入？\*\*##', '### 优质刷酸社群的特征\n\n**🌟 什么样的社群值得加入？**', content)
    content = re.sub(r'## 特征一：理性科学的氛围\*\*理性社群的表现：\*\*', '#### 特征一：理性科学的氛围\n\n**理性社群的表现：**', content)
    content = re.sub(r'## 特征二：友善互助的环境\*\*友善社群的特点：\*\*', '#### 特征二：友善互助的环境\n\n**友善社群的特点：**', content)
    content = re.sub(r'## 特征三：专业可靠的信息\*\*专业社群的标准：\*\*', '#### 特征三：专业可靠的信息\n\n**专业社群的标准：**', content)
    
    # Fix broken text continuations
    content = re.sub(r'- 讨论基于科学事实，不传播谣言', '- 讨论基于科学事实，不传播谣言', content)
    content = re.sub(r'- 成员之间相互尊重，不恶意攻击', '- 成员之间相互尊重，不恶意攻击', content)
    content = re.sub(r'- 有专业人士参与指导', '- 有专业人士参与指导', content)
    
    # Fix search and sharing sections
    content = re.sub(r'\*\*🔍 寻找优质社群的攻略：\*\*', '**🔍 寻找优质社群的攻略：**', content)
    content = re.sub(r'## 渠道一：专业平台\*\*推荐平台：\*\*', '#### 渠道一：专业平台\n\n**推荐平台：**', content)
    content = re.sub(r'## 渠道二：线下活动\*\*活动类型：\*\*', '#### 渠道二：线下活动\n\n**活动类型：**', content)
    content = re.sub(r'## 渠道三：朋友推荐\*\*推荐来源：\*\*', '#### 渠道三：朋友推荐\n\n**推荐来源：**', content)
    
    # Fix sharing experience sections
    content = re.sub(r'\*\*💎 什么样的分享最有价值？\*\*', '**💎 什么样的分享最有价值？**', content)
    content = re.sub(r'## 要素一：详细的背景信息\*\*必须包含的信息：\*\*', '#### 要素一：详细的背景信息\n\n**必须包含的信息：**', content)
    content = re.sub(r'## 要素二：客观的效果描述\*\*客观描述的标准：\*\*', '#### 要素二：客观的效果描述\n\n**客观描述的标准：**', content)
    content = re.sub(r'## 要素三：实用的使用技巧\*\*技巧分享内容：\*\*', '#### 要素三：实用的使用技巧\n\n**技巧分享内容：**', content)
    content = re.sub(r'## 要素四：诚实的风险提醒\*\*风险提醒包括：\*\*', '#### 要素四：诚实的风险提醒\n\n**风险提醒包括：**', content)
    
    # Fix warning and judgment sections
    content = re.sub(r'\*\*⚠️ 分享经验的红线：\*\*', '**⚠️ 分享经验的红线：**', content)
    content = re.sub(r'## 不要做的事情：', '#### 不要做的事情：', content)
    content = re.sub(r'## 应该做的事情：', '#### 应该做的事情：', content)
    
    # Fix information verification sections
    content = re.sub(r'\*\*🕵️ 如何识别假消息？\*\*', '**🕵️ 如何识别假消息？**', content)
    content = re.sub(r'## 警惕信号一：过度夸大的效果\*\*不靠谱的表述：\*\*', '#### 警惕信号一：过度夸大的效果\n\n**不靠谱的表述：**', content)
    content = re.sub(r'## 警惕信号二：缺乏具体信息\*\*信息不足的表现：\*\*', '#### 警惕信号二：缺乏具体信息\n\n**信息不足的表现：**', content)
    content = re.sub(r'## 警惕信号三：商业推广痕迹\*\*商业推广的特征：\*\*', '#### 警惕信号三：商业推广痕迹\n\n**商业推广的特征：**', content)
    
    # Fix rational judgment sections
    content = re.sub(r'\*\*🧠 如何做出理性判断？\*\*', '**🧠 如何做出理性判断？**', content)
    content = re.sub(r'## 方法一：多方验证\*\*验证渠道：\*\*', '#### 方法一：多方验证\n\n**验证渠道：**', content)
    content = re.sub(r'## 方法二：成分分析\*\*分析要点：\*\*', '#### 方法二：成分分析\n\n**分析要点：**', content)
    content = re.sub(r'## 方法三：渐进尝试\*\*尝试原则：\*\*', '#### 方法三：渐进尝试\n\n**尝试原则：**', content)
    
    # Fix mindset and philosophy sections
    content = re.sub(r'\*\*🧘♀️ 什么是健康的刷酸心态？\*\*', '**🧘♀️ 什么是健康的刷酸心态？**', content)
    content = re.sub(r'## 心态一：科学理性\*\*科学理性的表现：\*\*', '#### 心态一：科学理性\n\n**科学理性的表现：**', content)
    content = re.sub(r'## 心态二：耐心坚持\*\*耐心坚持的重要性：\*\*', '#### 心态二：耐心坚持\n\n**耐心坚持的重要性：**', content)
    content = re.sub(r'## 心态三：适度平衡\*\*适度平衡的含义：\*\*', '#### 心态三：适度平衡\n\n**适度平衡的含义：**', content)
    
    # Fix anxiety and philosophy sections
    content = re.sub(r'\*\*😌 如何保持护肤的快乐？\*\*', '**😌 如何保持护肤的快乐？**', content)
    content = re.sub(r'## 焦虑的来源：\*\*常见焦虑源：\*\*', '#### 焦虑的来源：\n\n**常见焦虑源：**', content)
    content = re.sub(r'## 缓解焦虑的方法：\*\*心理调节：\*\*', '#### 缓解焦虑的方法：\n\n**心理调节：**', content)
    
    # Fix philosophy sections
    content = re.sub(r'\*\*🌱 可持续的美丽观念：\*\*', '**🌱 可持续的美丽观念：**', content)
    content = re.sub(r'## 哲学一：健康第一\*\*健康优先的原则：\*\*', '#### 哲学一：健康第一\n\n**健康优先的原则：**', content)
    content = re.sub(r'## 哲学二：自然美丽\*\*自然美丽的理念：\*\*', '#### 哲学二：自然美丽\n\n**自然美丽的理念：**', content)
    content = re.sub(r'## 哲学三：可持续发展\*\*可持续美丽的要素：\*\*', '#### 哲学三：可持续发展\n\n**可持续美丽的要素：**', content)
    
    # Fix summary sections
    content = re.sub(r'## 🎯 核心社群参与原则', '### 🎯 核心社群参与原则', content)
    content = re.sub(r'## ✅ 理性刷酸达人检查清单', '### ✅ 理性刷酸达人检查清单', content)
    content = re.sub(r'## 💡 刷酸达人的人生感悟', '### 💡 刷酸达人的人生感悟', content)
    content = re.sub(r'## 全书总结：你的美丽人生刚刚开始', '### 全书总结：你的美丽人生刚刚开始', content)
    
    # Remove standalone punctuation lines
    content = re.sub(r'^：$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^"$', '', content, flags=re.MULTILINE)
    
    # Clean up multiple empty lines
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Chapter 14 formatting fixes applied!")

def main():
    """Main function to fix both chapters"""
    print("🚨 Emergency fix for Chapters 13 and 14 HTML rendering issues")
    print("Based on browser simulation analysis")
    print()
    
    fix_chapter_13()
    fix_chapter_14()
    
    print()
    print("🎯 Emergency fixes completed for both chapters!")
    print("📊 Fixed HTML rendering issues discovered through browser simulation")

if __name__ == "__main__":
    main()
