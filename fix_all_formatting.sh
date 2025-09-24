#!/bin/bash

echo "开始修复所有章节的格式问题..."

# List of all chapter files
chapters=(
  "01_know_your_skin"
  "02_acid_science"
  "03_acid_encyclopedia"
  "04_preparation"
  "05_beginner_guide"
  "06_targeted_solutions"
  "07_product_selection"
  "08_care_during_process"
  "09_medical_grade_peels"
  "10_safety_risk_control"
  "11_evaluation_adjustment"
  "12_lifestyle_management"
  "13_makeup_balance"
  "14_community_sharing"
)

for chapter in "${chapters[@]}"; do
  file="docs/chapters/${chapter}.md"
  
  if [ -f "$file" ]; then
    echo "修复 $chapter..."
    
    # Create backup
    cp "$file" "${file}.backup"
    
    # Fix common formatting issues
    sed -i '
      # Fix broken headers with quotes and newlines
      s/^## \([^"]*\)"$/## \1"/g
      s/^## \([^"]*\)$/## \1/g
      
      # Remove standalone quote lines
      /^"$/d
      
      # Fix standalone hash symbols
      s/^#$/### /g
      s/^##$/#### /g
      
      # Fix image paths to use correct relative path
      s|](images/|](../../images/|g
      s|](../images/|](../../images/|g
      
      # Fix broken markdown formatting
      s/\*\*\([^*]*\)\*\*：\*\*$/\*\*\1：\*\*/g
      
      # Remove standalone punctuation lines
      /^？$/d
      /^）$/d
      /^分$/d
      /^比$/d
      /^间$/d
      /^估$/d
      /^仪$/d
      /^案$/d
      /^频$/d
      /^善$/d
      /^定$/d
      /^快$/d
      /^态$/d
      /^化$/d
      /^弱$/d
      /^级$/d
      /^性$/d
      /^量$/d
      /^度$/d
      /^果$/d
      /^问$/d
      /^源$/d
      /^单$/d
      /^则$/d
      /^验$/d
      /^记$/d
      /^升$/d
      /^子$/d
      /^理$/d
      /^和$/d
      /^奏$/d
      /^型$/d
      /^应$/d
      /^什$/d
      /^么$/d
      
      # Fix broken section headers
      s/^##$/#### /g
      s/^#$/### /g
    ' "$file"
    
    echo "✅ $chapter 修复完成"
  else
    echo "⚠️ 文件不存在: $file"
  fi
done

echo "所有章节格式修复完成！"
