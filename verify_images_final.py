#!/usr/bin/env python3
"""
最终验证图片显示的脚本
检查所有图片是否能正确显示
"""

import requests
import re
import glob
import os

def verify_all_images():
    """验证所有图片是否能正确显示"""
    
    base_url = "http://localhost:8001"
    
    # 检查的页面列表
    pages_to_check = [
        "/chapters/01_know_your_skin/",
        "/chapters/02_acid_science/", 
        "/chapters/03_acid_encyclopedia/",
        "/chapters/05_beginner_guide/",
        "/chapters/06_targeted_solutions/",
        "/chapters/07_product_selection/",
        "/chapters/08_care_during_process/",
        "/chapters/09_medical_grade_peels/",
        "/chapters/10_safety_risk_control/",
        "/chapters/11_evaluation_adjustment/",
        "/chapters/12_lifestyle_management/",
        "/about/charts/"
    ]
    
    total_images = 0
    working_images = 0
    broken_images = []
    
    print("🔍 开始验证图片显示...")
    
    for page in pages_to_check:
        try:
            print(f"\n📄 检查页面: {page}")
            
            # 获取页面内容
            response = requests.get(f"{base_url}{page}", timeout=10)
            if response.status_code != 200:
                print(f"  ❌ 页面无法访问: {response.status_code}")
                continue
            
            # 查找所有SVG图片
            img_tags = re.findall(r'<img[^>]*src=(["\'])([^"\']*\.svg)\1[^>]*>', response.text)
            
            if not img_tags:
                print(f"  ℹ️  未找到SVG图片")
                continue
            
            for quote, img_src in img_tags:
                total_images += 1
                
                # 构建完整的图片URL
                if img_src.startswith('../../'):
                    img_url = f"{base_url}/{img_src[6:]}"
                elif img_src.startswith('../'):
                    img_url = f"{base_url}/{img_src[3:]}"
                else:
                    img_url = f"{base_url}/{img_src}"
                
                # 测试图片是否可访问
                try:
                    img_response = requests.head(img_url, timeout=5)
                    if img_response.status_code == 200:
                        working_images += 1
                        print(f"  ✅ {os.path.basename(img_src)}")
                    else:
                        broken_images.append((page, img_src, img_response.status_code))
                        print(f"  ❌ {os.path.basename(img_src)} - HTTP {img_response.status_code}")
                except Exception as e:
                    broken_images.append((page, img_src, str(e)))
                    print(f"  ❌ {os.path.basename(img_src)} - {e}")
                    
        except Exception as e:
            print(f"  ❌ 页面检查失败: {e}")
    
    # 输出总结
    print(f"\n📊 验证结果总结:")
    print(f"  📈 总图片数: {total_images}")
    print(f"  ✅ 正常显示: {working_images}")
    print(f"  ❌ 显示异常: {len(broken_images)}")
    print(f"  📊 成功率: {working_images/total_images*100:.1f}%" if total_images > 0 else "  📊 成功率: 0%")
    
    if broken_images:
        print(f"\n❌ 异常图片详情:")
        for page, img_src, error in broken_images:
            print(f"  - {page}: {img_src} ({error})")
    else:
        print(f"\n🎉 所有图片都能正常显示！")
    
    return len(broken_images) == 0

def check_image_files():
    """检查图片文件是否存在"""
    print(f"\n📁 检查图片文件...")
    
    image_dir = "docs/images"
    if not os.path.exists(image_dir):
        print(f"❌ 图片目录不存在: {image_dir}")
        return False
    
    svg_files = glob.glob(f"{image_dir}/*.svg")
    print(f"找到 {len(svg_files)} 个SVG文件:")
    
    for svg_file in sorted(svg_files):
        file_size = os.path.getsize(svg_file)
        print(f"  📄 {os.path.basename(svg_file)} ({file_size:,} bytes)")
    
    return len(svg_files) > 0

if __name__ == "__main__":
    print("🚀 开始最终验证...")
    
    # 检查图片文件
    files_ok = check_image_files()
    
    if files_ok:
        # 验证图片显示
        display_ok = verify_all_images()
        
        if display_ok:
            print(f"\n🎉 恭喜！图片显示问题已完全解决！")
            print(f"💡 你可以访问 http://localhost:8001 查看完整效果")
        else:
            print(f"\n⚠️  还有一些图片显示问题需要解决")
    else:
        print(f"\n❌ 图片文件检查失败，请先确保图片文件存在")
