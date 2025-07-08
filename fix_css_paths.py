import os
import re
from bs4 import BeautifulSoup

def fix_css_paths(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # 查找CSS链接
    css_link = soup.select_one('link[rel="stylesheet"]')
    if css_link and css_link['href'] != "../../assets/css/style.css":
        # 修复CSS路径
        css_link['href'] = "../../assets/css/style.css"
        print(f"已修复CSS路径: {file_path}")
        
        # 保存修改后的文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))
        return True
    return False

def process_game_directory(directory):
    fixed_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html') and not file == "index.html":
                file_path = os.path.join(root, file)
                if fix_css_paths(file_path):
                    fixed_count += 1
    return fixed_count

if __name__ == "__main__":
    games_directory = "games"
    total_fixed = process_game_directory(games_directory)
    print(f"总共修复了 {total_fixed} 个游戏详情页的CSS路径") 