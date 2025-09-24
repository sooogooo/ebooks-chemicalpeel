#!/usr/bin/env python3
"""
Comprehensive Markdown formatting checker and fixer for the Chemical Peel ebook.
Fixes common Markdown rendering issues.
"""

import os
import re
import glob
from pathlib import Path

def fix_code_block_lists(content):
    """Fix lists that are incorrectly wrapped in code blocks"""
    # Pattern to match code blocks containing lists
    pattern = r'```\n((?:[^`]|`(?!``))*?(?:\d+\.\s+[^\n]+\n|[-*]\s+[^\n]+\n)(?:[^`]|`(?!``))*?)\n```'
    
    def replace_code_block(match):
        block_content = match.group(1).strip()
        # Convert to proper Markdown formatting
        lines = block_content.split('\n')
        formatted_lines = []
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('')
                continue
                
            # Check if it's a section header (ends with colon)
            if line.endswith('：') or line.endswith(':'):
                if current_section:
                    formatted_lines.append('')
                formatted_lines.append(f'**{line}**')
                current_section = line
            # Check if it's a numbered list item
            elif re.match(r'^\d+\.\s+', line):
                formatted_lines.append(line)
            # Check if it's a bullet point
            elif re.match(r'^[-*]\s+', line):
                formatted_lines.append(line)
            else:
                # Regular text
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    return re.sub(pattern, replace_code_block, content, flags=re.MULTILINE | re.DOTALL)

def fix_image_references(content):
    """Ensure image references are properly formatted"""
    # Fix image paths that might be incorrect
    content = re.sub(r'!\[([^\]]+)\]\(\.\.\/images\/', r'![\1](images/', content)
    
    # Ensure images in div containers have proper structure
    pattern = r'<div class="image-container">\s*!\[([^\]]+)\]\(([^)]+)\)\s*<p><em>([^<]+)</em></p>\s*</div>'
    
    def fix_image_container(match):
        alt_text = match.group(1)
        image_path = match.group(2)
        caption = match.group(3)
        
        return f'''<div class="image-container">
  ![{alt_text}]({image_path})
  <p><em>{caption}</em></p>
</div>'''
    
    content = re.sub(pattern, fix_image_container, content, flags=re.MULTILINE | re.DOTALL)
    
    return content

def fix_heading_spacing(content):
    """Fix spacing around headings"""
    # Ensure proper spacing before headings
    content = re.sub(r'\n(#{1,6}\s+[^\n]+)', r'\n\n\1', content)
    # Remove excessive spacing
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content

def fix_list_formatting(content):
    """Fix list formatting issues"""
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Fix numbered lists that might be missing proper spacing
        if re.match(r'^\d+\.\s+', line.strip()):
            if i > 0 and lines[i-1].strip() and not re.match(r'^\d+\.\s+', lines[i-1].strip()):
                if not lines[i-1].strip().endswith(':') and not lines[i-1].strip().endswith('：'):
                    fixed_lines.append('')
        
        # Fix bullet points
        if re.match(r'^[-*]\s+', line.strip()):
            if i > 0 and lines[i-1].strip() and not re.match(r'^[-*]\s+', lines[i-1].strip()):
                if not lines[i-1].strip().endswith(':') and not lines[i-1].strip().endswith('：'):
                    fixed_lines.append('')
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def check_and_fix_file(file_path):
    """Check and fix a single Markdown file"""
    print(f"Processing: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply fixes
        content = fix_code_block_lists(content)
        content = fix_image_references(content)
        content = fix_heading_spacing(content)
        content = fix_list_formatting(content)
        
        # Check if changes were made
        if content != original_content:
            # Backup original file
            backup_path = file_path + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ Fixed formatting issues (backup saved as {backup_path})")
            return True
        else:
            print(f"  ✅ No issues found")
            return False
            
    except Exception as e:
        print(f"  ❌ Error processing file: {e}")
        return False

def main():
    """Main function to process all Markdown files"""
    print("🔧 Markdown Formatting Fixer")
    print("=" * 50)
    
    # Find all Markdown files
    docs_dir = Path("/home/sooogooo/AmazonQ/ebooks/ChemicalPell/docs")
    md_files = []
    
    # Add all .md files in docs directory and subdirectories
    for pattern in ["*.md", "**/*.md"]:
        md_files.extend(docs_dir.glob(pattern))
    
    if not md_files:
        print("❌ No Markdown files found!")
        return
    
    print(f"📁 Found {len(md_files)} Markdown files")
    print()
    
    fixed_count = 0
    for md_file in sorted(md_files):
        if check_and_fix_file(md_file):
            fixed_count += 1
    
    print()
    print("=" * 50)
    print(f"🎉 Processing complete!")
    print(f"📊 Files processed: {len(md_files)}")
    print(f"🔧 Files fixed: {fixed_count}")
    
    if fixed_count > 0:
        print()
        print("💡 Recommendations:")
        print("1. Test the site with: mkdocs serve")
        print("2. Check image display in browser")
        print("3. Verify all formatting looks correct")
        print("4. If satisfied, remove .backup files")

if __name__ == "__main__":
    main()
