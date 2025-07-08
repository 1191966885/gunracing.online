import os
from bs4 import BeautifulSoup

def fix_game_detail_css_path(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    css_link = soup.select_one('link[rel="stylesheet"]')
    
    if css_link and css_link['href'] != "../../assets/css/style.css":
        css_link['href'] = "../../assets/css/style.css"
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))
        
        print(f"已修复游戏详情页CSS路径: {file_path}")
        return True
    
    return False

def process_game_files(category):
    category_path = os.path.join("games", category)
    fixed_count = 0
    
    for file_name in os.listdir(category_path):
        if file_name.endswith('.html') and file_name != "index.html":
            file_path = os.path.join(category_path, file_name)
            if fix_game_detail_css_path(file_path):
                fixed_count += 1
    
    return fixed_count

# 处理所有类别下的游戏详情页
categories = ["puzzle", "action", "shooting", "racing", "casual", "sports"]
total_fixed = 0

for category in categories:
    fixed = process_game_files(category)
    total_fixed += fixed

print(f"总共修复了 {total_fixed} 个游戏详情页的CSS路径") 