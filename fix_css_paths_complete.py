import os
from bs4 import BeautifulSoup

def fix_css_path(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # 确定页面深度和正确的CSS路径
    correct_css_path = ""
    if file_path == "index.html":
        correct_css_path = "assets/css/style.css"
    elif "/games/" in file_path.replace("\\", "/") or "\\games\\" in file_path:
        if file_path.endswith("index.html"):
            correct_css_path = "../assets/css/style.css"  # 类别索引页
        else:
            correct_css_path = "../../assets/css/style.css"  # 游戏详情页
    else:
        print(f"无法确定页面类型: {file_path}")
        return False
    
    # 修复CSS链接
    css_link = soup.select_one('link[rel="stylesheet"]')
    if css_link and css_link['href'] != correct_css_path:
        css_link['href'] = correct_css_path
        print(f"已修复CSS路径: {file_path} -> {correct_css_path}")
        
        # 保存修改后的文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))
        return True
    
    return False

def process_files(directory="."):
    fixed_count = 0
    
    # 处理主页
    if os.path.exists("index.html"):
        if fix_css_path("index.html"):
            fixed_count += 1
    
    # 处理所有HTML文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if fix_css_path(file_path):
                    fixed_count += 1
    
    return fixed_count

if __name__ == "__main__":
    games_directory = "games"
    total_fixed = process_files(games_directory)
    print(f"总共修复了 {total_fixed} 个页面的CSS路径") 