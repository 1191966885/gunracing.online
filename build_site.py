import os
import json
import shutil
from datetime import datetime

# 定义分类映射(英文到中文)
CATEGORY_MAP = {
    "Action": "动作游戏",
    "Racing": "赛车游戏",
    "Shooting": "射击游戏",
    "Puzzle": "益智游戏",
    "Sports": "体育游戏",
    "Casual": "休闲游戏"
}

# 创建目录(如果不存在)
def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"创建目录: {directory}")

# 读取模板文件
def read_template(template_name):
    with open(f"templates/{template_name}.html", "r", encoding="utf-8") as f:
        return f.read()

# 写入HTML文件
def write_html(filepath, content):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"生成文件: {filepath}")

# 构建游戏卡片HTML
def build_game_card(game, with_description=False):
    thumb = game.get("thumb", "/assets/images/placeholder.svg")
    title = game.get("title", "未命名游戏")
    game_url = f"/games/{game['category'].lower()}/{clean_filename(title)}.html"
    
    tags_html = ""
    if "tags" in game and isinstance(game["tags"], list) and len(game["tags"]) > 0:
        tags = "".join([f'<span>{tag}</span>' for tag in game["tags"]])
        tags_html = f'<div class="game-tags">{tags}</div>'
    
    description_html = ""
    if with_description and "description" in game:
        short_desc = game["description"][:120] + "..." if len(game["description"]) > 120 else game["description"]
        description_html = f'<p class="game-desc">{short_desc}</p>'
    
    return f"""
    <div class="game-card">
        <a href="{game_url}" class="game-cover-link">
            <div class="game-cover-container">
                <img class="game-cover" src="{thumb}" alt="{title}">
            </div>
        </a>
        <div class="game-info">
            <h3><a href="{game_url}">{title}</a></h3>
            {tags_html}
            <div class="game-category">
                <span>{CATEGORY_MAP.get(game.get('category', ''), '其他游戏')}</span>
            </div>
            {description_html}
            <a href="{game['url']}" target="_blank" class="play-btn">立即游戏</a>
        </div>
    </div>
    """

# 清理文件名(移除非法字符)
def clean_filename(name):
    # 在Python 3.6+中，反斜杠在f-string表达式中需要特殊处理
    invalid_chars = '<>:"/' + r'\|?*'  # 使用原始字符串来避免转义问题
    filename = "".join(c for c in name if c not in invalid_chars)
    filename = filename.replace(" ", "_").lower()
    return filename

# 构建游戏详情页
def build_game_detail(game, header_template, footer_template):
    title = game.get("title", "未命名游戏")
    description = game.get("description", "")
    category = game.get("category", "")
    
    # 设置活跃类别
    active_class = {
        "Action": "action_active",
        "Racing": "racing_active", 
        "Shooting": "shooting_active",
        "Puzzle": "puzzle_active",
        "Sports": "sports_active",
        "Casual": "casual_active"
    }
    
    header = header_template.replace("{{title}}", title)
    header = header.replace("{{description}}", description)
    header = header.replace("{{header}}", title)
    header = header.replace("{{subheader}}", f"{CATEGORY_MAP.get(category, '游戏')} - 在线免费玩")
    
    # 设置活动类别
    for cat in active_class:
        if cat == category:
            header = header.replace(f"{{{{{active_class[cat]}}}}}", "active")
        else:
            header = header.replace(f"{{{{{active_class[cat]}}}}}", "")
    header = header.replace("{{home_active}}", "")
    
    # 构建游戏详情HTML
    game_html = f"""
    <div class="game-detail">
        <div class="game-preview">
            <img src="{game.get('thumb', '/assets/images/placeholder.svg')}" alt="{title}" class="game-detail-image">
        </div>
        <div class="game-info-detail">
            <h2>{title}</h2>
            
            <div class="game-tags detail-tags">
                {' '.join([f'<span>{tag}</span>' for tag in game.get('tags', [])])}
            </div>
            
            <div class="game-description">
                <h3>游戏介绍</h3>
                <p>{description}</p>
            </div>
            
            <div class="game-instructions">
                <h3>游戏指南</h3>
                <p>{game.get('instructions', '暂无游戏指南').replace('\n', '<br>')}</p>
            </div>
            
            <a href="{game.get('url', '#')}" target="_blank" class="play-btn detail-play">立即开始游戏</a>
        </div>
    </div>
    
    <div class="game-iframe">
        <h3>在线游戏</h3>
        <div class="iframe-container">
            <iframe src="{game.get('iframe_url', '')}" width="{game.get('width', 800)}" height="{game.get('height', 600)}" scrolling="none" frameborder="0" allowfullscreen></iframe>
        </div>
    </div>
    """
    
    # 拼接完整HTML
    html_content = header + game_html + footer_template
    
    # 保存游戏详情页
    game_dir = f"games/{category.lower()}"
    ensure_directory(game_dir)
    filepath = f"{game_dir}/{clean_filename(title)}.html"
    write_html(filepath, html_content)

# 构建分类页面
def build_category_page(category, games, header_template, footer_template):
    category_name = CATEGORY_MAP.get(category, category)
    
    # 设置活跃类别
    active_class = {
        "Action": "action_active",
        "Racing": "racing_active", 
        "Shooting": "shooting_active",
        "Puzzle": "puzzle_active",
        "Sports": "sports_active",
        "Casual": "casual_active"
    }
    
    header = header_template.replace("{{title}}", category_name)
    header = header.replace("{{description}}", f"在枪车游戏网免费玩最好玩的{category_name}！最新最全的在线{category_name}，无需下载，立即开始游戏。")
    header = header.replace("{{header}}", category_name)
    header = header.replace("{{subheader}}", f"共有 {len(games)} 款免费{category_name}，无需下载，即点即玩！")
    
    # 设置活动类别
    for cat in active_class:
        if cat == category:
            header = header.replace(f"{{{{{active_class[cat]}}}}}", "active")
        else:
            header = header.replace(f"{{{{{active_class[cat]}}}}}", "")
    header = header.replace("{{home_active}}", "")
    
    # 构建游戏卡片网格
    game_cards = "".join([build_game_card(game) for game in games])
    games_grid = f'<div class="game-grid">{game_cards}</div>'
    
    # 拼接完整HTML
    html_content = header + games_grid + footer_template
    
    # 保存分类页面
    category_dir = f"games/{category.lower()}"
    ensure_directory(category_dir)
    write_html(f"{category_dir}/index.html", html_content)

# 构建主页
def build_homepage(all_games, header_template, footer_template):
    # 准备特色游戏(从每个分类中选择一些)
    featured_games = []
    categories = {}
    
    # 按分类分组游戏
    for game in all_games:
        cat = game.get("category", "Other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(game)
    
    # 从每个分类中选择一些游戏作为特色
    for cat, games in categories.items():
        featured_games.extend(games[:3])  # 每个分类选3个
    
    # 如果特色游戏不足12个，添加更多游戏
    if len(featured_games) < 12 and all_games:
        remaining = 12 - len(featured_games)
        for game in all_games:
            if game not in featured_games:
                featured_games.append(game)
                remaining -= 1
                if remaining <= 0:
                    break
    
    # 设置首页为活动状态
    header = header_template.replace("{{title}}", "免费在线游戏")
    header = header.replace("{{description}}", "在枪车游戏网免费玩最好玩的在线游戏！超过1000款免费游戏，包括动作、射击、赛车、益智等多种类型，无需下载，立即开始游戏。")
    header = header.replace("{{header}}", "热门游戏推荐")
    header = header.replace("{{subheader}}", "畅玩最好玩的免费在线游戏，无需下载，即点即玩！")
    
    # 清除所有分类的活动状态，设置首页为活动
    header = header.replace("{{home_active}}", "active")
    header = header.replace("{{action_active}}", "")
    header = header.replace("{{racing_active}}", "")
    header = header.replace("{{shooting_active}}", "")
    header = header.replace("{{puzzle_active}}", "")
    header = header.replace("{{sports_active}}", "")
    header = header.replace("{{casual_active}}", "")
    
    # 构建特色游戏区域
    featured_html = "".join([build_game_card(game, True) for game in featured_games[:12]])
    featured_section = f"""
    <div class="game-grid featured-grid">
        {featured_html}
    </div>
    """
    
    # 构建分类区域
    categories_html = ""
    for category, cat_name in CATEGORY_MAP.items():
        if category in categories and categories[category]:
            cat_games = categories[category][:4]  # 每个分类显示4个游戏
            cat_url = f"/games/{category.lower()}/"
            
            game_cards = "".join([build_game_card(game) for game in cat_games])
            
            categories_html += f"""
            <div class="category-section">
                <div class="category-header">
                    <h2>{cat_name}</h2>
                    <a href="{cat_url}" class="view-all">查看全部</a>
                </div>
                <div class="game-grid category-grid">
                    {game_cards}
                </div>
            </div>
            """
    
    # 拼接完整HTML
    html_content = header + featured_section + categories_html + footer_template
    
    # 保存首页
    write_html("index.html", html_content)

# 复制静态资源文件
def copy_static_assets():
    # 复制CSS文件
    ensure_directory("assets/css")
    
    # 从旧站点复制样式表(如果存在)
    if os.path.exists("style.css"):
        shutil.copy("style.css", "assets/css/style.css")
        print("复制样式表: style.css -> assets/css/style.css")
    
    # 复制图片占位符
    ensure_directory("assets/images")
    if os.path.exists("images/local_placeholder.svg"):
        shutil.copy("images/local_placeholder.svg", "assets/images/placeholder.svg")
        print("复制占位图: images/local_placeholder.svg -> assets/images/placeholder.svg")

# 主函数
def main():
    print("开始构建静态游戏网站...")
    start_time = datetime.now()
    
    # 确保必要的目录存在
    for category in CATEGORY_MAP:
        ensure_directory(f"games/{category.lower()}")
    
    ensure_directory("assets/css")
    ensure_directory("assets/js")
    ensure_directory("assets/images")
    ensure_directory("templates")
    
    # 创建header模板(如果不存在)
    header_template_path = "templates/header.html"
    if not os.path.exists(header_template_path) or os.path.getsize(header_template_path) == 0:
        header_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}} - 枪车游戏网 | gunracing games</title>
    <link rel="stylesheet" href="/assets/css/style.css">
    <meta name="description" content="{{description}}">
</head>
<body>
    <div class="layout">
        <!-- 侧边栏导航 -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <a href="/" class="logo"> 
                    <span class="logo-icon">🔫</span> 
                    <span class="logo-text">枪车游戏网</span> 
                </a>
            </div>
            <nav class="category-list">
                <a href="/" class="category-item {{home_active}}">首页</a>
                <a href="/games/shooting/" class="category-item {{shooting_active}}">射击游戏</a>
                <a href="/games/racing/" class="category-item {{racing_active}}">赛车游戏</a>
                <a href="/games/action/" class="category-item {{action_active}}">动作游戏</a>
                <a href="/games/puzzle/" class="category-item {{puzzle_active}}">益智游戏</a>
                <a href="/games/sports/" class="category-item {{sports_active}}">体育游戏</a>
                <a href="/games/casual/" class="category-item {{casual_active}}">休闲游戏</a>
            </nav>
            <div class="sidebar-footer">
                <p>© 2024 <a href="https://gunracing.online/" target="_blank">gunracing games</a></p>
            </div>
        </aside>

        <!-- 主要内容 -->
        <main class="main-content">
            <header class="main-header">
                <h1>{{header}}</h1>
                <p class="main-desc">{{subheader}}</p>
            </header>
            <section class="content">
"""
        write_html(header_template_path, header_template)
    
    # 创建footer模板(如果不存在)
    footer_template_path = "templates/footer.html"
    if not os.path.exists(footer_template_path) or os.path.getsize(footer_template_path) == 0:
        footer_template = """
            </section>
            <footer class="main-footer">
                <p>网站域名: <a href="https://gunracing.online/" target="_blank">https://gunracing.online/</a> | 仅供学习交流使用</p>
            </footer>
        </main>
    </div>
</body>
</html>
"""
        write_html(footer_template_path, footer_template)
    
    # 读取模板
    header_template = read_template("header")
    footer_template = read_template("footer")
    
    # 读取游戏数据
    try:
        with open("game_data.json", "r", encoding="utf-8") as f:
            games = json.load(f)
            print(f"成功加载游戏数据，共 {len(games)} 款游戏")
    except Exception as e:
        print(f"读取游戏数据失败: {e}")
        return
    
    # 复制静态资源
    copy_static_assets()
    
    # 按分类分组游戏
    categories = {}
    for game in games:
        cat = game.get("category", "Other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(game)
    
    # 构建分类页面
    for category, cat_games in categories.items():
        if category in CATEGORY_MAP:
            print(f"构建分类页面: {category} ({len(cat_games)} 款游戏)")
            build_category_page(category, cat_games, header_template, footer_template)
    
    # 构建游戏详情页
    print("构建游戏详情页...")
    for game in games:
        if "title" in game and "category" in game:
            build_game_detail(game, header_template, footer_template)
    
    # 构建首页
    print("构建首页...")
    build_homepage(games, header_template, footer_template)
    
    # 添加CSS样式表(如果不存在)
    css_path = "assets/css/style.css"
    if not os.path.exists(css_path):
        # 这里添加默认的CSS样式
        default_css = """
:root {
    --bg-color: #191c24;
    --sidebar-bg: #15171e;
    --text-color: #e0e0e0;
    --accent-color: #ffb300;
    --card-bg: #22252f;
    --border-color: #2d303a;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Microsoft YaHei', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    line-height: 1.6;
}

a {
    text-decoration: none;
    color: inherit;
}

/* 布局 */
.layout {
    display: grid;
    grid-template-columns: 230px 1fr;
    min-height: 100vh;
}

/* 侧边栏 */
.sidebar {
    background-color: var(--sidebar-bg);
    padding: 20px;
    position: sticky;
    top: 0;
    height: 100vh;
    display: flex;
    flex-direction: column;
}

.sidebar-header {
    margin-bottom: 30px;
}

.logo {
    display: flex;
    align-items: center;
    gap: 10px;
}

.logo-icon {
    font-size: 24px;
}

.logo-text {
    font-size: 20px;
    font-weight: bold;
    color: var(--accent-color);
}

.category-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    flex-grow: 1;
}

.category-item {
    text-decoration: none;
    color: var(--text-color);
    padding: 10px 15px;
    border-radius: 8px;
    transition: all 0.2s ease;
}

.category-item:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

.category-item.active {
    background-color: var(--accent-color);
    color: #000;
    font-weight: 500;
}

.sidebar-footer {
    margin-top: 20px;
    font-size: 12px;
    color: #888;
}

.sidebar-footer a {
    color: var(--accent-color);
    text-decoration: none;
}

/* 主要内容 */
.main-content {
    padding: 30px;
}

.main-header {
    margin-bottom: 30px;
}

.main-header h1 {
    font-size: 28px;
    margin-bottom: 10px;
    color: var(--accent-color);
}

.main-desc {
    color: #aaa;
    max-width: 800px;
}

/* 游戏网格 */
.game-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 40px;
}

/* 游戏卡片 */
.game-card {
    background-color: var(--card-bg);
    border-radius: 10px;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid var(--border-color);
    height: 100%;
    display: flex;
    flex-direction: column;
}

.game-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
}

.game-cover-container {
    position: relative;
    width: 100%;
    height: 0;
    padding-bottom: 75%;
    overflow: hidden;
}

.game-cover {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.game-card:hover .game-cover {
    transform: scale(1.05);
}

.game-info {
    padding: 15px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
}

.game-info h3 {
    margin-bottom: 10px;
    font-size: 16px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    line-height: 1.3;
    height: 2.6em;
}

.game-info h3 a:hover {
    color: var(--accent-color);
}

.game-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-bottom: 10px;
}

.game-tags span {
    background-color: rgba(255, 255, 255, 0.1);
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 12px;
}

.game-category {
    margin-bottom: 10px;
}

.game-category span {
    background-color: var(--accent-color);
    color: #000;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
}

.game-desc {
    margin-bottom: 15px;
    font-size: 14px;
    color: #aaa;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    flex-grow: 1;
}

.play-btn {
    display: block;
    width: 100%;
    padding: 10px;
    text-align: center;
    background-color: var(--accent-color);
    color: #000;
    text-decoration: none;
    border-radius: 5px;
    font-weight: 500;
    transition: background-color 0.2s ease;
    margin-top: auto;
}

.play-btn:hover {
    background-color: #ffc233;
}

/* 分类区域 */
.category-section {
    margin-bottom: 50px;
}

.category-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 10px;
}

.category-header h2 {
    color: var(--accent-color);
    font-size: 22px;
}

.view-all {
    color: var(--accent-color);
    font-size: 14px;
    padding: 5px 10px;
    border: 1px solid var(--accent-color);
    border-radius: 4px;
    transition: all 0.2s ease;
}

.view-all:hover {
    background-color: var(--accent-color);
    color: #000;
}

/* 游戏详情页 */
.game-detail {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 30px;
    margin-bottom: 40px;
}

.game-preview {
    border-radius: 10px;
    overflow: hidden;
    background-color: var(--card-bg);
    border: 1px solid var(--border-color);
}

.game-detail-image {
    width: 100%;
    height: auto;
    display: block;
}

.game-info-detail h2 {
    font-size: 28px;
    margin-bottom: 15px;
    color: var(--accent-color);
}

.detail-tags {
    margin-bottom: 20px;
}

.game-description, .game-instructions {
    margin-bottom: 20px;
}

.game-description h3, .game-instructions h3 {
    font-size: 18px;
    margin-bottom: 10px;
    color: #ccc;
}

.detail-play {
    max-width: 300px;
    padding: 12px 20px;
    font-size: 18px;
}

.game-iframe {
    margin-bottom: 40px;
}

.game-iframe h3 {
    font-size: 22px;
    margin-bottom: 15px;
    color: var(--accent-color);
}

.iframe-container {
    position: relative;
    padding-bottom: 56.25%;
    height: 0;
    overflow: hidden;
    border-radius: 10px;
    background-color: #000;
}

.iframe-container iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: none;
}

/* 页脚 */
.main-footer {
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid var(--border-color);
    color: #888;
    font-size: 12px;
}

.main-footer a {
    color: var(--accent-color);
    text-decoration: none;
}

/* 响应式适配 */
@media (max-width: 992px) {
    .game-detail {
        grid-template-columns: 1fr;
    }
    
    .game-preview {
        max-width: 500px;
        margin: 0 auto;
    }
}

@media (max-width: 768px) {
    .layout {
        grid-template-columns: 1fr;
    }
    
    .sidebar {
        position: static;
        height: auto;
        padding-bottom: 10px;
    }
    
    .category-list {
        flex-direction: row;
        overflow-x: auto;
        padding-bottom: 10px;
        flex-wrap: nowrap;
    }
    
    .category-item {
        white-space: nowrap;
        flex-shrink: 0;
    }
    
    .main-content {
        padding: 20px;
    }
    
    .game-grid {
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    }
}
"""
        write_html(css_path, default_css)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"网站构建完成！用时 {duration:.2f} 秒")
    print("已生成的页面:")
    print("- index.html (首页)")
    for category in CATEGORY_MAP:
        if category in categories:
            print(f"- games/{category.lower()}/index.html ({CATEGORY_MAP[category]}分类页)")
    print(f"- 共 {sum(len(cat_games) for cat_games in categories.values())} 个游戏详情页")
    print("\n您可以通过浏览器打开 index.html 来访问网站。")

if __name__ == "__main__":
    main()
