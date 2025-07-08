import json
import os
import random

def update_homepage():
    # 读取游戏数据
    with open('game_data.json', 'r', encoding='utf-8') as f:
        games = json.load(f)
    
    # 随机打乱游戏顺序
    random.shuffle(games)
    
    # 读取当前主页内容
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 查找内容部分的开始和结束位置
    content_start = html_content.find('<section class="content">')
    content_end = html_content.find('</section>', content_start)
    
    # 提取页面头部和尾部
    header = html_content[:content_start + len('<section class="content">')]
    footer = html_content[content_end:]
    
    # 创建新的游戏卡片HTML
    game_cards_html = '\n<div class="game-grid">\n'
    
    for game in games:
        title = game['title']
        thumb = game['thumb']
        category = game['category'].lower()
        tags = game['tags']
        description = game['description']
        
        # 如果描述太长，截断它
        if len(description) > 100:
            description = description[:97] + '...'
        
        # 生成游戏卡片HTML
        game_card = f'''
    <div class="game-card">
        <a href="games/{category}/{title.lower().replace(" ", "_").replace(":", "_").replace("'", "").replace("&", "and").replace("-", "_")}.html" class="game-cover-link">
            <div class="game-cover-container">
                <img class="game-cover" src="{thumb}" alt="{title}">
            </div>
        </a>
        <div class="game-info">
            <h3><a href="games/{category}/{title.lower().replace(" ", "_").replace(":", "_").replace("'", "").replace("&", "and").replace("-", "_")}.html">{title}</a></h3>
            <div class="game-tags">{" ".join(f'<span>{tag}</span>' for tag in tags)}</div>
            <div class="game-category">
                <span>{category}</span>
            </div>
            <p class="game-desc">{description}</p>
            <a href="games/{category}/{title.lower().replace(" ", "_").replace(":", "_").replace("'", "").replace("&", "and").replace("-", "_")}.html" class="play-btn">Play Now</a>
        </div>
    </div>
    '''
        game_cards_html += game_card
    
    game_cards_html += '</div>\n'
    
    # 更新主页标题
    header = header.replace('<h1>Popular Games</h1>', '<h1>All Games</h1>')
    header = header.replace('<p class="main-desc">Play the best free online games instantly with no download required!</p>', 
                          '<p class="main-desc">Browse our complete collection of free online games - no categories, just fun!</p>')
    
    # 组合新的HTML内容
    new_html_content = header + game_cards_html + footer
    
    # 保存更新后的主页
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html_content)
    
    print("主页已更新，现在显示全部游戏!")

if __name__ == "__main__":
    update_homepage() 