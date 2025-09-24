#!/usr/bin/env python3
"""
Find and fix markdown artifacts in chapter 10 by analyzing HTML output
"""

import re
import subprocess

def find_markdown_artifacts():
    """Find markdown artifacts by analyzing the HTML content"""
    
    print("🔍 Scanning Chapter 10 for markdown artifacts...")
    print("=" * 60)
    
    # Read the HTML file
    try:
        with open('/tmp/chapter10.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print("❌ HTML file not found. Fetching from server...")
        # Try to fetch again
        result = subprocess.run(['curl', '-s', 'http://127.0.0.1:8000/chapters/10_safety_risk_control/'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            html_content = result.stdout
            with open('/tmp/chapter10.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
        else:
            print("❌ Failed to fetch HTML content")
            return []
    
    artifacts = []
    
    # Look for markdown artifacts in the HTML
    # 1. Unrendered bold text with colons
    bold_artifacts = re.findall(r'\*\*[^*]+：\*\*[^*\s]', html_content)
    for artifact in bold_artifacts:
        artifacts.append(f"Unrendered bold text: {artifact}")
    
    # 2. Mixed headers and content
    mixed_headers = re.findall(r'<h[1-6][^>]*>[^<]*\*\*[^*]+\*\*[^<]*</h[1-6]>', html_content)
    for artifact in mixed_headers:
        artifacts.append(f"Mixed header content: {artifact}")
    
    # 3. Unrendered markdown in navigation
    nav_artifacts = re.findall(r'<span class=md-ellipsis>[^<]*\*\*[^*]+\*\*[^<]*</span>', html_content)
    for artifact in nav_artifacts:
        artifacts.append(f"Navigation markdown artifact: {artifact}")
    
    # 4. Broken list items
    list_artifacts = re.findall(r'<li[^>]*>[^<]*\*\*[^*]+\*\*[^<]*</li>', html_content)
    for artifact in list_artifacts:
        artifacts.append(f"List item markdown artifact: {artifact}")
    
    # 5. Paragraph artifacts
    para_artifacts = re.findall(r'<p[^>]*>[^<]*\*\*[^*]+\*\*[^<]*</p>', html_content)
    for artifact in para_artifacts:
        artifacts.append(f"Paragraph markdown artifact: {artifact}")
    
    return artifacts

def analyze_source_file():
    """Analyze the source markdown file for issues"""
    
    print("\n🔍 Analyzing source markdown file...")
    
    file_path = "docs/chapters/10_safety_risk_control.md"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines, 1):
        # Look for mixed content in headers
        if line.startswith('#') and '**' in line:
            issues.append(f"Line {i}: Mixed header content - {line}")
        
        # Look for unformatted bold sections
        if '**' in line and '：**' in line and not line.startswith('**'):
            if not line.strip().startswith('- ') and not line.strip().startswith('|'):
                issues.append(f"Line {i}: Potential formatting issue - {line}")
        
        # Look for broken markdown structures
        if line.count('**') % 2 != 0:
            issues.append(f"Line {i}: Unmatched bold markers - {line}")
    
    return issues

def main():
    """Main function"""
    
    # Find artifacts in HTML
    html_artifacts = find_markdown_artifacts()
    
    if html_artifacts:
        print(f"❌ Found {len(html_artifacts)} HTML artifacts:")
        for i, artifact in enumerate(html_artifacts[:10], 1):  # Show first 10
            print(f"  {i}. {artifact}")
        if len(html_artifacts) > 10:
            print(f"  ... and {len(html_artifacts) - 10} more")
    else:
        print("✅ No HTML artifacts found!")
    
    # Analyze source file
    source_issues = analyze_source_file()
    
    if source_issues:
        print(f"\n❌ Found {len(source_issues)} source file issues:")
        for i, issue in enumerate(source_issues[:10], 1):  # Show first 10
            print(f"  {i}. {issue}")
        if len(source_issues) > 10:
            print(f"  ... and {len(source_issues) - 10} more")
    else:
        print("\n✅ No source file issues found!")
    
    print(f"\n📊 Summary:")
    print(f"  HTML artifacts: {len(html_artifacts)}")
    print(f"  Source issues: {len(source_issues)}")
    print(f"  Total problems: {len(html_artifacts) + len(source_issues)}")

if __name__ == "__main__":
    main()
