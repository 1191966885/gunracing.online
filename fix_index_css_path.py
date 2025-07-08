import os
from bs4 import BeautifulSoup

def fix_index_css_path(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # 查找CSS链接
    css_link = soup.select_one('link[rel="stylesheet"]')
    if css_link:
        # 对于首页，正确的路径是assets/css/style.css
        if file_path == "index.html":
            css_link['href'] = "assets/css/style.css"
        # 对于类别索引页，正确的路径是../assets/css/style.css
        else:
            css_link['href'] = "../assets/css/style.css"
        
        print(f"已修复CSS路径: {file_path}")
        
        # 保存修改后的文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))
        return True
    return False

# 修复主首页
fix_index_css_path("index.html")

# 修复类别索引页
categories = ["puzzle", "action", "shooting", "racing", "casual", "sports"]
for category in categories:
    category_index_path = os.path.join("games", category, "index.html")
    if os.path.exists(category_index_path):
        fix_index_css_path(category_index_path) 