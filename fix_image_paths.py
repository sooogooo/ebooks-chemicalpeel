#!/usr/bin/env python3
"""
Fix image path issues in markdown files
Change ../../images/ to ../images/
"""

import os
import re

def fix_image_paths(file_path):
    """Fix image paths in a single markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count occurrences before fixing
        wrong_paths = re.findall(r'\.\./\.\./images/', content)
        if not wrong_paths:
            return False
        
        # Fix the paths
        fixed_content = re.sub(r'\.\./\.\./images/', '../images/', content)
        
        # Write back the fixed content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"✅ Fixed {len(wrong_paths)} image paths in: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Main function to fix all markdown files"""
    docs_dir = "docs"
    fixed_files = 0
    total_fixes = 0
    
    print("🔧 Starting image path fixes...")
    print("=" * 50)
    
    # Walk through all markdown files
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                if fix_image_paths(file_path):
                    fixed_files += 1
    
    print("=" * 50)
    print(f"🎉 Fixed image paths in {fixed_files} files")
    
    # Test build after fixes
    print("\n🧪 Testing build after fixes...")
    os.system("python3 -m mkdocs build --quiet")
    print("✅ Build test completed")

if __name__ == "__main__":
    main()
