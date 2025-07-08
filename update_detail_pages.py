import os
import re
from bs4 import BeautifulSoup

def update_detail_page(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # 检查是否为详情页而非类别索引页
    if soup.select('div.game-detail') and not file_path.endswith('index.html'):
        # 已经是新结构，跳过
        print(f"跳过已经是新结构的页面: {file_path}")
        return False
    
    # 如果是类别索引页，不做处理
    if file_path.endswith('index.html'):
        print(f"跳过类别索引页: {file_path}")
        return False
    
    # 找到内容区域
    content_section = soup.select_one('section.content')
    if not content_section:
        print(f"未找到内容区域: {file_path}")
        return False
    
    # 查找主要游戏信息
    title = soup.select_one('.main-header h1').text.strip() if soup.select_one('.main-header h1') else ""
    
    # 查找游戏分类和描述
    game_category = "Unknown"
    for link in soup.select('.category-item'):
        if 'active' in link.get('class', []):
            game_category = link.text.strip()
            break
    
    # 查找iframe
    iframe = soup.select_one('iframe')
    iframe_src = iframe['src'] if iframe else ""
    
    # 提取游戏描述
    description_tags = soup.find_all('p')
    game_description = ""
    if len(description_tags) > 1:
        game_description = description_tags[1].text.strip()
    
    # 提取游戏说明
    instructions = ""
    for p in description_tags[2:]:
        if p.text and "Website:" not in p.text:
            instructions += p.text.strip() + "\n"
    
    # 提取游戏ID并构建图片URL
    game_id = ""
    if iframe_src and "gamedistribution.com" in iframe_src:
        game_id = iframe_src.split("/")[-1]
        if not game_id:
            game_id = iframe_src.split("/")[-2]
    
    image_url = f"https://img.gamedistribution.com/{game_id}-512x384.jpg" if game_id else ""
    
    # 构建新的HTML结构
    new_content = f"""
    <div class="game-detail">
        <div class="game-preview">
            <img src="{image_url}" alt="{title}" class="game-detail-image">
        </div>
        <div class="game-info-detail">
            <h2>{title}</h2>
            
            <div class="game-tags detail-tags">
                <span>{game_category}</span>
            </div>
            
            <div class="game-description">
                <h3>Game Description</h3>
                <p>{game_description}</p>
            </div>
            
            <div class="game-instructions">
                <h3>Instructions</h3>
                <p>{instructions}</p>
            </div>
            
            <a href="#game-iframe" class="play-btn detail-play">Play Game</a>
        </div>
    </div>
    
    <div class="game-iframe" id="game-iframe">
        <h3>Play Online</h3>
        <div class="iframe-container">
            <iframe src="{iframe_src}" width="800" height="600" scrolling="none" frameborder="0" allowfullscreen></iframe>
        </div>
    </div>
    """
    
    # 更新内容区域
    content_section.clear()
    content_section.append(BeautifulSoup(new_content, 'html.parser'))
    
    # 保存修改后的文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))
    
    print(f"已更新详情页: {file_path}")
    return True

def process_game_directory(directory):
    updated = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                if update_detail_page(file_path):
                    updated += 1
    return updated

if __name__ == "__main__":
    games_directory = "games"
    total_updated = process_game_directory(games_directory)
    print(f"总共更新了 {total_updated} 个游戏详情页") 