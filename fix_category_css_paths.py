import os
from bs4 import BeautifulSoup

categories = ["puzzle", "action", "shooting", "racing", "casual", "sports"]

for category in categories:
    index_path = os.path.join("games", category, "index.html")
    
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        css_link = soup.select_one('link[rel="stylesheet"]')
        
        if css_link:
            css_link['href'] = "../assets/css/style.css"
            print(f"已修复类别页面CSS路径: {index_path}")
            
            with open(index_path, 'w', encoding='utf-8') as file:
                file.write(str(soup)) 