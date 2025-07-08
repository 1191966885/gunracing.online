import os
import re
from bs4 import BeautifulSoup

def fix_navigation_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # 确定页面深度
    depth = file_path.count(os.sep)
    if file_path == "index.html":
        depth = 0
    elif "/games/" in file_path.replace("\\", "/"):
        if file_path.endswith("index.html"):
            depth = 2  # 类别首页
        else:
            depth = 3  # 游戏详情页
    
    # 获取导航链接
    nav_links = soup.select('.category-list .category-item')
    
    if not nav_links:
        print(f"未找到导航链接: {file_path}")
        return False
    
    fixed = False
    
    # 根据页面深度修复链接
    for link in nav_links:
        href = link.get('href', '')
        text = link.text.strip().lower()
        
        if depth == 0:  # 主页
            if text == 'home':
                if href != "index.html":
                    link['href'] = "index.html"
                    fixed = True
            else:
                correct_href = f"games/{text}/index.html"
                if href != correct_href:
                    link['href'] = correct_href
                    fixed = True
        
        elif depth == 2:  # 类别首页
            if text == 'home':
                if href != "../../index.html":
                    link['href'] = "../../index.html"
                    fixed = True
            else:
                correct_href = f"../{text}/index.html"
                if href != correct_href:
                    link['href'] = correct_href
                    fixed = True
        
        elif depth == 3:  # 游戏详情页
            if text == 'home':
                if href != "../../index.html":
                    link['href'] = "../../index.html"
                    fixed = True
            else:
                correct_href = f"../{text}/index.html"
                if href != correct_href:
                    link['href'] = correct_href
                    fixed = True
    
    if fixed:
        # 保存修改后的文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))
        print(f"已修复导航链接: {file_path}")
        return True
    
    return False

def fix_sidebar_logo_link(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # 确定页面深度
    depth = file_path.count(os.sep)
    if file_path == "index.html":
        depth = 0
    elif "/games/" in file_path.replace("\\", "/"):
        if file_path.endswith("index.html"):
            depth = 2  # 类别首页
        else:
            depth = 3  # 游戏详情页
    
    # 获取LOGO链接
    logo_link = soup.select_one('.sidebar-header .logo')
    
    if not logo_link:
        print(f"未找到LOGO链接: {file_path}")
        return False
    
    fixed = False
    
    # 根据页面深度修复LOGO链接
    href = logo_link.get('href', '')
    if depth == 0:  # 主页
        if href != "index.html":
            logo_link['href'] = "index.html"
            fixed = True
    elif depth == 2 or depth == 3:  # 类别首页或游戏详情页
        if href != "../../index.html":
            logo_link['href'] = "../../index.html"
            fixed = True
    
    if fixed:
        # 保存修改后的文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))
        print(f"已修复LOGO链接: {file_path}")
        return True
    
    return False

def process_files(directory="."):
    fixed_nav_count = 0
    fixed_logo_count = 0
    
    # 处理主页
    if os.path.exists("index.html"):
        if fix_navigation_links("index.html"):
            fixed_nav_count += 1
        if fix_sidebar_logo_link("index.html"):
            fixed_logo_count += 1
    
    # 处理所有HTML文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if fix_navigation_links(file_path):
                    fixed_nav_count += 1
                if fix_sidebar_logo_link(file_path):
                    fixed_logo_count += 1
    
    return fixed_nav_count, fixed_logo_count

if __name__ == "__main__":
    games_directory = "games"
    nav_count, logo_count = process_files(games_directory)
    print(f"总共修复了 {nav_count} 个导航链接和 {logo_count} 个LOGO链接") 