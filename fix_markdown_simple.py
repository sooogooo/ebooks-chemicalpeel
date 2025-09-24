#!/usr/bin/env python3
"""
Simple Markdown formatting fixer for the Chemical Peel ebook.
"""

import os
import re
import glob

def fix_code_block_lists(content):
    """Fix lists that are incorrectly wrapped in code blocks"""
    # Pattern to match code blocks containing lists
    pattern = r'```\n((?:[^`]|`(?!``))*?(?:\d+\.\s+[^\n]+\n|[-*]\s+[^\n]+\n)(?:[^`]|`(?!``))*?)\n```'
    
    def replace_code_block(match):
        block_content = match.group(1).strip()
        # Convert to proper Markdown formatting
        lines = block_content.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('')
                continue
                
            # Check if it's a section header (ends with colon)
            if line.endswith('：') or line.endswith(':'):
                formatted_lines.append(f'**{line}**')
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    return re.sub(pattern, replace_code_block, content, flags=re.MULTILINE | re.DOTALL)

def check_and_fix_file(file_path):
    """Check and fix a single Markdown file"""
    print(f"Processing: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply fixes
        content = fix_code_block_lists(content)
        
        # Check if changes were made
        if content != original_content:
            # Backup original file
            backup_path = file_path + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ Fixed formatting issues")
            return True
        else:
            print(f"  ✅ No issues found")
            return False
            
    except Exception as e:
        print(f"  ❌ Error processing file: {e}")
        return False

def main():
    """Main function to process all Markdown files"""
    print("🔧 Simple Markdown Formatting Fixer")
    print("=" * 50)
    
    # Find all Markdown files
    docs_dir = "/home/sooogooo/AmazonQ/ebooks/ChemicalPell/docs"
    md_files = []
    
    # Find all .md files recursively
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    
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

if __name__ == "__main__":
    main()
