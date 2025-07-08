import os
import glob

def fix_css_paths():
    # 修复分类页面的CSS路径
    category_pages = glob.glob('games/*/index.html')
    for page in category_pages:
        with open(page, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 修复CSS路径
        content = content.replace('href="assets/css/style.css"', 'href="../../assets/css/style.css"')
        
        # 修复导航链接路径
        content = content.replace('href="games/shooting/index.html"', 'href="../shooting/index.html"')
        content = content.replace('href="games/racing/index.html"', 'href="../racing/index.html"')
        content = content.replace('href="games/action/index.html"', 'href="../action/index.html"')
        content = content.replace('href="games/puzzle/index.html"', 'href="../puzzle/index.html"')
        content = content.replace('href="games/sports/index.html"', 'href="../sports/index.html"')
        content = content.replace('href="games/casual/index.html"', 'href="../casual/index.html"')
        content = content.replace('href="index.html"', 'href="../../index.html"')
        
        with open(page, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"已修复分类页面: {page}")

    # 修复游戏详情页的CSS路径
    game_pages = []
    for category in ['shooting', 'racing', 'action', 'puzzle', 'sports', 'casual']:
        game_pages.extend(glob.glob(f'games/{category}/*.html'))
    
    # 排除索引页
    game_pages = [page for page in game_pages if not page.endswith('index.html')]
    
    for page in game_pages:
        with open(page, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 修复CSS路径
        content = content.replace('href="assets/css/style.css"', 'href="../../assets/css/style.css"')
        
        # 修复导航链接路径
        content = content.replace('href="games/shooting/index.html"', 'href="../shooting/index.html"')
        content = content.replace('href="games/racing/index.html"', 'href="../racing/index.html"')
        content = content.replace('href="games/action/index.html"', 'href="../action/index.html"')
        content = content.replace('href="games/puzzle/index.html"', 'href="../puzzle/index.html"')
        content = content.replace('href="games/sports/index.html"', 'href="../sports/index.html"')
        content = content.replace('href="games/casual/index.html"', 'href="../casual/index.html"')
        content = content.replace('href="index.html"', 'href="../index.html"')
        
        with open(page, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"已修复游戏页面: {page}")

if __name__ == "__main__":
    fix_css_paths()
    print("所有路径修复完成！") 