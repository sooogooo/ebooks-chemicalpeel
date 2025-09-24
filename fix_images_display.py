#!/usr/bin/env python3
"""
Image display checker and fixer for the Chemical Peel ebook.
"""

import os
import re

def check_image_files():
    """Check if all referenced SVG files exist"""
    images_dir = "/home/sooogooo/AmazonQ/ebooks/ChemicalPell/docs/images"
    
    # Get list of existing SVG files
    existing_svgs = []
    if os.path.exists(images_dir):
        for file in os.listdir(images_dir):
            if file.endswith('.svg'):
                existing_svgs.append(file)
    
    print(f"📁 Found {len(existing_svgs)} SVG files in images directory:")
    for svg in sorted(existing_svgs):
        print(f"  ✅ {svg}")
    
    return existing_svgs

def check_image_references():
    """Check all image references in Markdown files"""
    docs_dir = "/home/sooogooo/AmazonQ/ebooks/ChemicalPell/docs"
    image_refs = []
    
    # Find all .md files recursively
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Find all image references
                    pattern = r'!\[([^\]]*)\]\(([^)]+\.svg)\)'
                    matches = re.findall(pattern, content)
                    
                    for alt_text, image_path in matches:
                        # Extract just the filename
                        filename = os.path.basename(image_path)
                        image_refs.append({
                            'file': file_path,
                            'alt_text': alt_text,
                            'path': image_path,
                            'filename': filename
                        })
                        
                except Exception as e:
                    print(f"❌ Error reading {file_path}: {e}")
    
    return image_refs

def validate_images():
    """Validate that all image references point to existing files"""
    print("🔍 Checking Image References")
    print("=" * 50)
    
    existing_svgs = check_image_files()
    image_refs = check_image_references()
    
    print(f"\n📊 Found {len(image_refs)} image references in Markdown files:")
    
    missing_images = []
    valid_images = []
    
    for ref in image_refs:
        if ref['filename'] in existing_svgs:
            valid_images.append(ref)
            print(f"  ✅ {ref['filename']} - {ref['alt_text']}")
        else:
            missing_images.append(ref)
            print(f"  ❌ {ref['filename']} - MISSING!")
    
    print(f"\n📈 Summary:")
    print(f"  ✅ Valid references: {len(valid_images)}")
    print(f"  ❌ Missing images: {len(missing_images)}")
    
    if missing_images:
        print(f"\n🚨 Missing Images:")
        for ref in missing_images:
            print(f"  - {ref['filename']} (referenced in {os.path.basename(ref['file'])})")
    
    return len(missing_images) == 0

def test_mkdocs_build():
    """Test if MkDocs can build successfully"""
    print("\n🏗️  Testing MkDocs Build")
    print("=" * 30)
    
    os.chdir("/home/sooogooo/AmazonQ/ebooks/ChemicalPell")
    
    # Try to build
    result = os.system("mkdocs build --quiet 2>/dev/null")
    
    if result == 0:
        print("✅ MkDocs build successful!")
        return True
    else:
        print("❌ MkDocs build failed!")
        print("💡 Try running: mkdocs build --verbose")
        return False

def main():
    """Main function"""
    print("🖼️  Image Display Checker")
    print("=" * 50)
    
    # Validate images
    images_valid = validate_images()
    
    # Test MkDocs build
    build_success = test_mkdocs_build()
    
    print("\n" + "=" * 50)
    print("🎉 Check Complete!")
    
    if images_valid and build_success:
        print("✅ All images are valid and MkDocs builds successfully!")
        print("\n💡 Next steps:")
        print("1. Run: mkdocs serve")
        print("2. Open: http://127.0.0.1:8000")
        print("3. Check that all images display correctly")
    else:
        print("❌ Issues found that need to be resolved:")
        if not images_valid:
            print("  - Missing image files")
        if not build_success:
            print("  - MkDocs build errors")

if __name__ == "__main__":
    main()
