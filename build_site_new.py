import os
import json
import shutil
import re
from datetime import datetime

# Define category mapping (English)
CATEGORY_MAP = {
    "Action": "Action",
    "Racing": "Racing",
    "Shooting": "Shooting",
    "Puzzle": "Puzzle",
    "Sports": "Sports",
    "Casual": "Casual",
    ".io": ".IO Games",
    "Clicker": "Clicker",
    "Adventure": "Adventure",
    "Driving": "Driving",
    "Beauty": "Beauty",
    "Other": "Other"
}

# Create directory if it doesn't exist
def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

# 读取模板文件
def read_template(template_name):
    with open(f"templates/{template_name}.html", "r", encoding="utf-8") as f:
        return f.read()

# Write HTML file
def write_html(filepath, content):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated file: {filepath}")

# 清理文件名(移除非法字符)
def clean_filename(name):
    # 使用正则表达式替换非法字符
    # 这样避免了在f-string中使用反斜杠
    filename = re.sub(r'[<>:"/\\|?*]', '', name)
    filename = filename.replace(" ", "_").lower()
    return filename

# 构建游戏卡片HTML
def build_game_card(game, with_description=False, is_category_page=False):
    title = game.get("title", "")
    slug = clean_filename(title)
    category = game.get("category", "").lower()
    description = game.get("description", "")
    tags = game.get("tags", [])
    
    # 准备标签HTML
    tags_html = " ".join(['<span>{}</span>'.format(tag) for tag in tags])
    
    # 准备描述
    desc_html = ""
    if with_description and description:
        # 截断描述，保留大约100个字符
        short_desc = description[:100] + "..." if len(description) > 100 else description
        desc_html = f'<p class="game-desc">{short_desc}</p>'
    
    # 构建游戏卡片HTML
    card_html = """
    <div class="game-card">
        <a href="{url}" class="game-cover-link">
            <div class="game-cover-container">
                <img class="game-cover" src="{thumb}" alt="{title}">
            </div>
        </a>
        <div class="game-info">
            <h3><a href="{url}">{title}</a></h3>
            <div class="game-tags">{tags}</div>
            <div class="game-category">
                <span>{category}</span>
            </div>
            {desc}
            <a href="{url}" class="play-btn">Play Now</a>
        </div>
    </div>
    """
    
    # 修改为相对路径
    if category.startswith('.'):
        category_path = category  # 保持.io这样的特殊类别名称
    else:
        category_path = category
        
    # 根据页面类型选择正确的相对路径
    if is_category_page:
        # 在分类页面中，游戏详情页在同一目录下
        url = "{}.html".format(slug)
    else:
        # 在首页使用相对路径
        url = "games/{}/{}.html".format(category_path, slug)
    
    return card_html.format(
        url=url,
        thumb=game.get("thumb", "/assets/images/placeholder.svg"),
        title=title,
        tags=tags_html,
        category=CATEGORY_MAP.get(game.get("category", ""), game.get("category", "")),
        desc=desc_html
    )

# 构建游戏详情页
def fix_game_detail_paths(game_detail_html, game_category, game_slug):
    """Fix paths in game detail pages to use relative paths instead of absolute paths"""
    # 删除搜索脚本引用
    if '</head>' in game_detail_html:
        game_detail_html = game_detail_html.replace('<script src="../../assets/js/search.js"></script>\n</head>', '</head>')
    
    # Fix CSS path
    game_detail_html = game_detail_html.replace('<link rel="stylesheet" href="/assets/css/style.css">', 
                                              '<link rel="stylesheet" href="../../assets/css/style.css">')
    game_detail_html = game_detail_html.replace('<link rel="stylesheet" href="assets/css/style.css">', 
                                              '<link rel="stylesheet" href="../../assets/css/style.css">')
    
    # Fix homepage links
    game_detail_html = game_detail_html.replace('<a href="../../index.html" class="logo">', 
                                              '<a href="../../index.html" class="logo">')
    game_detail_html = game_detail_html.replace('<a href="../../index.html" class="category-item', 
                                              '<a href="../../index.html" class="category-item')
    game_detail_html = game_detail_html.replace('<a href="../../index.html" class="logo">', 
                                              '<a href="../../index.html" class="logo">')
    game_detail_html = game_detail_html.replace('<a href="../../index.html" class="category-item', 
                                              '<a href="../../index.html" class="category-item')
    
    # Fix category page links
    game_detail_html = game_detail_html.replace('href="games/shooting/index.html"', 'href="../shooting/index.html"')
    game_detail_html = game_detail_html.replace('href="games/racing/index.html"', 'href="../racing/index.html"')
    game_detail_html = game_detail_html.replace('href="games/action/index.html"', 'href="../action/index.html"')
    game_detail_html = game_detail_html.replace('href="games/puzzle/index.html"', 'href="../puzzle/index.html"')
    game_detail_html = game_detail_html.replace('href="games/sports/index.html"', 'href="../sports/index.html"')
    game_detail_html = game_detail_html.replace('href="games/casual/index.html"', 'href="../casual/index.html"')
    game_detail_html = game_detail_html.replace('href="games/.io/index.html"', 'href="../.io/index.html"')
    game_detail_html = game_detail_html.replace('href="games/clicker/index.html"', 'href="../clicker/index.html"')
    game_detail_html = game_detail_html.replace('href="games/adventure/index.html"', 'href="../adventure/index.html"')
    game_detail_html = game_detail_html.replace('href="games/driving/index.html"', 'href="../driving/index.html"')
    game_detail_html = game_detail_html.replace('href="games/beauty/index.html"', 'href="../beauty/index.html"')
    game_detail_html = game_detail_html.replace('href="games/other/index.html"', 'href="../other/index.html"')
    
    # Fix existing game detail links
    game_detail_html = game_detail_html.replace('href="../../games/action/"', 'href="../action/index.html"')
    game_detail_html = game_detail_html.replace('href="../../games/adventure/"', 'href="../adventure/index.html"')
    game_detail_html = game_detail_html.replace('href="../../games/racing/"', 'href="../racing/index.html"')
    game_detail_html = game_detail_html.replace('href="../../games/driving/"', 'href="../driving/index.html"')
    game_detail_html = game_detail_html.replace('href="../../games/shooting/"', 'href="../shooting/index.html"')
    game_detail_html = game_detail_html.replace('href="../../games/puzzle/"', 'href="../puzzle/index.html"')
    game_detail_html = game_detail_html.replace('href="../../games/sports/"', 'href="../sports/index.html"')
    game_detail_html = game_detail_html.replace('href="../../games/casual/"', 'href="../casual/index.html"')
    game_detail_html = game_detail_html.replace('href="../../games/clicker/"', 'href="../clicker/index.html"')
    game_detail_html = game_detail_html.replace('href="../../games/.io/"', 'href="../.io/index.html"')
    game_detail_html = game_detail_html.replace('href="../../games/beauty/"', 'href="../beauty/index.html"')
    game_detail_html = game_detail_html.replace('href="../../games/other/"', 'href="../other/index.html"')
    
    # Fix absolute category page links
    game_detail_html = game_detail_html.replace('<a href="/games/shooting/" class="category-item', 
                                              '<a href="../shooting/index.html" class="category-item')
    game_detail_html = game_detail_html.replace('<a href="/games/racing/" class="category-item', 
                                              '<a href="../racing/index.html" class="category-item')
    game_detail_html = game_detail_html.replace('<a href="/games/action/" class="category-item', 
                                              '<a href="../action/index.html" class="category-item')
    game_detail_html = game_detail_html.replace('<a href="/games/puzzle/" class="category-item', 
                                              '<a href="../puzzle/index.html" class="category-item')
    game_detail_html = game_detail_html.replace('<a href="/games/sports/" class="category-item', 
                                              '<a href="../sports/index.html" class="category-item')
    game_detail_html = game_detail_html.replace('<a href="/games/casual/" class="category-item', 
                                              '<a href="../casual/index.html" class="category-item')
    game_detail_html = game_detail_html.replace('<a href="/games/.io/" class="category-item', 
                                              '<a href="../.io/index.html" class="category-item')
    game_detail_html = game_detail_html.replace('<a href="/games/clicker/" class="category-item', 
                                              '<a href="../clicker/index.html" class="category-item')
    game_detail_html = game_detail_html.replace('<a href="/games/adventure/" class="category-item', 
                                              '<a href="../adventure/index.html" class="category-item')
    game_detail_html = game_detail_html.replace('<a href="/games/driving/" class="category-item', 
                                              '<a href="../driving/index.html" class="category-item')
    game_detail_html = game_detail_html.replace('<a href="/games/beauty/" class="category-item', 
                                              '<a href="../beauty/index.html" class="category-item')
    game_detail_html = game_detail_html.replace('<a href="/games/other/" class="category-item', 
                                              '<a href="../other/index.html" class="category-item')
    
    # 修复目录形式的链接
    game_detail_html = game_detail_html.replace('href="../action/"', 'href="../action/index.html"')
    game_detail_html = game_detail_html.replace('href="../racing/"', 'href="../racing/index.html"')
    game_detail_html = game_detail_html.replace('href="../shooting/"', 'href="../shooting/index.html"')
    game_detail_html = game_detail_html.replace('href="../puzzle/"', 'href="../puzzle/index.html"')
    game_detail_html = game_detail_html.replace('href="../sports/"', 'href="../sports/index.html"')
    game_detail_html = game_detail_html.replace('href="../casual/"', 'href="../casual/index.html"')
    game_detail_html = game_detail_html.replace('href="../.io/"', 'href="../.io/index.html"')
    game_detail_html = game_detail_html.replace('href="../clicker/"', 'href="../clicker/index.html"')
    game_detail_html = game_detail_html.replace('href="../adventure/"', 'href="../adventure/index.html"')
    game_detail_html = game_detail_html.replace('href="../driving/"', 'href="../driving/index.html"')
    game_detail_html = game_detail_html.replace('href="../beauty/"', 'href="../beauty/index.html"')
    game_detail_html = game_detail_html.replace('href="../other/"', 'href="../other/index.html"')
    
    # 修改游戏详情页链接 
    game_detail_html = game_detail_html.replace(f'<a href="/games/{game_category}/{game_slug}.html"', 
                                               f'<a href="{game_slug}.html"')
    
    # Update sidebar navigation to match the format used in category pages
    if '<nav class="category-list">' in game_detail_html and '</nav>' in game_detail_html:
        nav_start = game_detail_html.find('<nav class="category-list">')
        nav_end = game_detail_html.find('</nav>', nav_start) + 6
        
        # Update navigation with all categories
        current_category = game_category.lower()
        
        new_nav = '''            <nav class="category-list">
                <a href="../../index.html" class="category-item">Home</a>
                <a href="../action/index.html" class="category-item{0}">Action</a>
                <a href="../adventure/index.html" class="category-item{1}">Adventure</a>
                <a href="../racing/index.html" class="category-item{2}">Racing</a>
                <a href="../driving/index.html" class="category-item{3}">Driving</a>
                <a href="../shooting/index.html" class="category-item{4}">Shooting</a>
                <a href="../puzzle/index.html" class="category-item{5}">Puzzle</a>
                <a href="../sports/index.html" class="category-item{6}">Sports</a>
                <a href="../casual/index.html" class="category-item{7}">Casual</a>
                <a href="../clicker/index.html" class="category-item{8}">Clicker</a>
                <a href="../.io/index.html" class="category-item{9}">.IO Games</a>
                <a href="../beauty/index.html" class="category-item{10}">Beauty</a>
                <a href="../other/index.html" class="category-item{11}">Other</a>
            </nav>'''.format(
            ' active' if current_category == 'action' else '',
            ' active' if current_category == 'adventure' else '',
            ' active' if current_category == 'racing' else '',
            ' active' if current_category == 'driving' else '',
            ' active' if current_category == 'shooting' else '',
            ' active' if current_category == 'puzzle' else '',
            ' active' if current_category == 'sports' else '',
            ' active' if current_category == 'casual' else '',
            ' active' if current_category == 'clicker' else '',
            ' active' if current_category == '.io' else '',
            ' active' if current_category == 'beauty' else '',
            ' active' if current_category == 'other' else ''
        )
        
        game_detail_html = game_detail_html[:nav_start] + new_nav + game_detail_html[nav_end:]
    
    return game_detail_html

def build_game_detail(game, header_template, footer_template):
    title = game.get("title", "")
    category = game.get("category", "")
    description = game.get("description", "")
    instructions = game.get("instructions", "")
    tags = game.get("tags", [])
    
    # 准备标签HTML
    tags_html = " ".join(['<span>{}</span>'.format(tag) for tag in tags])
    
    # 设置标题和描述
    header = header_template.replace("{{title}}", title + " - Gun Racing Games")
    header = header.replace("{{description}}", description)
    header = header.replace("{{header}}", title)
    header = header.replace("{{subheader}}", category + " - Play Online For Free")
    
    # 设置活动类别
    active_class = {
        "Action": "action_active",
        "Racing": "racing_active", 
        "Shooting": "shooting_active",
        "Puzzle": "puzzle_active",
        "Sports": "sports_active",
        "Casual": "casual_active",
        ".io": "io_active",
        "Clicker": "clicker_active",
        "Adventure": "adventure_active",
        "Driving": "driving_active",
        "Beauty": "beauty_active",
        "Other": "other_active"
    }
    for cat in active_class:
        if cat == category:
            header = header.replace("{{" + active_class[cat] + "}}", "active")
        else:
            header = header.replace("{{" + active_class[cat] + "}}", "")
    header = header.replace("{{home_active}}", "")
    
    # 构建游戏详情HTML
    game_html = """
    <div class="game-detail">
        <div class="game-preview">
            <img src="{thumb}" alt="{title}" class="game-detail-image">
        </div>
        <div class="game-info-detail">
            <h2>{title}</h2>
            
            <div class="game-tags detail-tags">
                {tags}
            </div>
            
            <div class="game-description">
                <h3>Game Description</h3>
                <p>{description}</p>
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
            <iframe src="{iframe_url}" width="800" height="600" scrolling="none" frameborder="0" allowfullscreen></iframe>
        </div>
    </div>
    """.format(
        title=title,
        thumb=game.get("thumb", "../../assets/images/placeholder.svg"),
        tags=tags_html,
        description=description,
        instructions=instructions,
        iframe_url=game.get("url", "").replace("https://www.crazygames.com/game/", "https://www.crazygames.com/embed/")
    )
    
    # 拼接完整HTML
    html_content = header + game_html + footer_template
    
    # 修复路径问题
    html_content = fix_game_detail_paths(html_content, category.lower(), clean_filename(title))
    
    # 保存游戏详情页
    game_dir = os.path.join("games", category.lower())
    ensure_directory(game_dir)
    filepath = os.path.join(game_dir, clean_filename(title) + ".html")
    write_html(filepath, html_content)

# 构建分类页面
def fix_category_page_paths(category_html, category):
    """Fix paths in category pages to use relative paths instead of absolute paths"""
    # 删除搜索脚本引用
    if '</head>' in category_html:
        category_html = category_html.replace('<script src="../../assets/js/search.js"></script>\n</head>', '</head>')
    
    # Fix CSS path
    category_html = category_html.replace('<link rel="stylesheet" href="/assets/css/style.css">', 
                                         '<link rel="stylesheet" href="../../assets/css/style.css">')
    category_html = category_html.replace('<link rel="stylesheet" href="assets/css/style.css">', 
                                         '<link rel="stylesheet" href="../../assets/css/style.css">')
    
    # Fix homepage link
    category_html = category_html.replace('<a href="../../index.html" class="logo">', 
                                         '<a href="../../index.html" class="logo">')
    category_html = category_html.replace('<a href="../../index.html" class="category-item', 
                                         '<a href="../../index.html" class="category-item')
    category_html = category_html.replace('<a href="index.html" class="category-item', 
                                         '<a href="../../index.html" class="category-item')
    
    # Fix category page links for all categories
    category_html = category_html.replace('<a href="/games/shooting/" class="category-item', 
                                         '<a href="../shooting/index.html" class="category-item')
    category_html = category_html.replace('<a href="/games/racing/" class="category-item', 
                                         '<a href="../racing/index.html" class="category-item')
    category_html = category_html.replace('<a href="/games/action/" class="category-item', 
                                         '<a href="../action/index.html" class="category-item')
    category_html = category_html.replace('<a href="/games/puzzle/" class="category-item', 
                                         '<a href="../puzzle/index.html" class="category-item')
    category_html = category_html.replace('<a href="/games/sports/" class="category-item', 
                                         '<a href="../sports/index.html" class="category-item')
    category_html = category_html.replace('<a href="/games/casual/" class="category-item', 
                                         '<a href="../casual/index.html" class="category-item')
    category_html = category_html.replace('<a href="/games/.io/" class="category-item', 
                                         '<a href="../.io/index.html" class="category-item')
    category_html = category_html.replace('<a href="/games/clicker/" class="category-item', 
                                         '<a href="../clicker/index.html" class="category-item')
    category_html = category_html.replace('<a href="/games/adventure/" class="category-item', 
                                         '<a href="../adventure/index.html" class="category-item')
    category_html = category_html.replace('<a href="/games/driving/" class="category-item', 
                                         '<a href="../driving/index.html" class="category-item')
    category_html = category_html.replace('<a href="/games/beauty/" class="category-item', 
                                         '<a href="../beauty/index.html" class="category-item')
    category_html = category_html.replace('<a href="/games/other/" class="category-item', 
                                         '<a href="../other/index.html" class="category-item')
    
    # 修复从模板生成的导航链接
    category_html = category_html.replace('<a href="games/action/index.html" class="category-item', 
                                         '<a href="../action/index.html" class="category-item')
    category_html = category_html.replace('<a href="games/adventure/index.html" class="category-item', 
                                         '<a href="../adventure/index.html" class="category-item')
    category_html = category_html.replace('<a href="games/racing/index.html" class="category-item', 
                                         '<a href="../racing/index.html" class="category-item')
    category_html = category_html.replace('<a href="games/driving/index.html" class="category-item', 
                                         '<a href="../driving/index.html" class="category-item')
    category_html = category_html.replace('<a href="games/shooting/index.html" class="category-item', 
                                         '<a href="../shooting/index.html" class="category-item')
    category_html = category_html.replace('<a href="games/puzzle/index.html" class="category-item', 
                                         '<a href="../puzzle/index.html" class="category-item')
    category_html = category_html.replace('<a href="games/sports/index.html" class="category-item', 
                                         '<a href="../sports/index.html" class="category-item')
    category_html = category_html.replace('<a href="games/casual/index.html" class="category-item', 
                                         '<a href="../casual/index.html" class="category-item')
    category_html = category_html.replace('<a href="games/clicker/index.html" class="category-item', 
                                         '<a href="../clicker/index.html" class="category-item')
    category_html = category_html.replace('<a href="games/.io/index.html" class="category-item', 
                                         '<a href="../.io/index.html" class="category-item')
    category_html = category_html.replace('<a href="games/beauty/index.html" class="category-item', 
                                         '<a href="../beauty/index.html" class="category-item')
    category_html = category_html.replace('<a href="games/other/index.html" class="category-item', 
                                         '<a href="../other/index.html" class="category-item')
    
    # 修改游戏详情页链接
    category_html = re.sub(r'<a href="/games/' + category + '/(.+?\.html)"', 
                          r'<a href="\1"', 
                          category_html)
    
    return category_html

def build_category_page(category, games, header_template, footer_template):
    category_name = CATEGORY_MAP.get(category, category)
    
    # Set active category
    active_class = {
        "Action": "action_active",
        "Racing": "racing_active", 
        "Shooting": "shooting_active",
        "Puzzle": "puzzle_active",
        "Sports": "sports_active",
        "Casual": "casual_active",
        ".io": "io_active",
        "Clicker": "clicker_active",
        "Adventure": "adventure_active",
        "Driving": "driving_active",
        "Beauty": "beauty_active",
        "Other": "other_active"
    }
    
    header = header_template.replace("{{title}}", category_name + " Games - Gun Racing Games")
    header = header.replace("{{description}}", "Play the best free online " + category_name + " games at Gun Racing Games! Action-packed " + category_name.lower() + " games with no download required.")
    header = header.replace("{{header}}", category_name + " Games")
    header = header.replace("{{subheader}}", str(len(games)) + " free " + category_name.lower() + " games to play online without download!")
    
    # 设置活动类别
    for cat in active_class:
        if cat == category:
            header = header.replace("{{" + active_class[cat] + "}}", "active")
        else:
            header = header.replace("{{" + active_class[cat] + "}}", "")
    header = header.replace("{{home_active}}", "")
    
    # 构建游戏卡片网格，传递is_category_page=True
    game_cards = "".join([build_game_card(game, is_category_page=True) for game in games])
    games_grid = '<div class="game-grid">' + game_cards + '</div>'
    
    # 拼接完整HTML
    html_content = header + games_grid + footer_template
    
    # 修复路径问题
    html_content = fix_category_page_paths(html_content, category)
    
    # 保存分类页面
    category_dir = os.path.join("games", category.lower())
    ensure_directory(category_dir)
    filepath = os.path.join(category_dir, "index.html")
    write_html(filepath, html_content)

# 修改fix_homepage_paths函数，删除搜索脚本引用
def fix_homepage_paths(homepage_html):
    """Fix paths in the homepage to use relative paths"""
    # 删除搜索脚本引用
    if '</head>' in homepage_html:
        homepage_html = homepage_html.replace('<script src="assets/js/search.js"></script>\n</head>', '</head>')
    
    # Fix CSS path
    homepage_html = homepage_html.replace('<link rel="stylesheet" href="/assets/css/style.css">', 
                                       '<link rel="stylesheet" href="assets/css/style.css">')
    
    # Fix homepage links
    homepage_html = homepage_html.replace('<a href="/" class="logo">', 
                                       '<a href="index.html" class="logo">')
    homepage_html = homepage_html.replace('<a href="/" class="category-item', 
                                       '<a href="index.html" class="category-item')
    
    # Fix category page links
    homepage_html = homepage_html.replace('href="/games/action/', 
                                        'href="games/action/')
    homepage_html = homepage_html.replace('href="/games/racing/', 
                                        'href="games/racing/')
    homepage_html = homepage_html.replace('href="/games/shooting/', 
                                        'href="games/shooting/')
    homepage_html = homepage_html.replace('href="/games/puzzle/', 
                                        'href="games/puzzle/')
    homepage_html = homepage_html.replace('href="/games/sports/', 
                                        'href="games/sports/')
    homepage_html = homepage_html.replace('href="/games/casual/', 
                                        'href="games/casual/')
    homepage_html = homepage_html.replace('href="/games/.io/', 
                                        'href="games/.io/')
    homepage_html = homepage_html.replace('href="/games/clicker/', 
                                        'href="games/clicker/')
    homepage_html = homepage_html.replace('href="/games/adventure/', 
                                        'href="games/adventure/')
    homepage_html = homepage_html.replace('href="/games/driving/', 
                                        'href="games/driving/')
    homepage_html = homepage_html.replace('href="/games/beauty/', 
                                        'href="games/beauty/')
    homepage_html = homepage_html.replace('href="/games/other/', 
                                        'href="games/other/')
    
    return homepage_html

def build_homepage(games, header_template, footer_template):
    """Build the homepage with pagination"""
    print("Building homepage...")
    
    # 每页显示的游戏数量
    games_per_page = 28
    
    # 计算总页数
    total_pages = (len(games) + games_per_page - 1) // games_per_page
    print(f"总共 {len(games)} 个游戏，每页 {games_per_page} 个，共 {total_pages} 页")
    
    # 为每一页创建HTML
    for page_num in range(1, total_pages + 1):
        # 计算当前页的游戏范围
        start_idx = (page_num - 1) * games_per_page
        end_idx = min(start_idx + games_per_page, len(games))
        current_page_games = games[start_idx:end_idx]
        
        # 创建分页导航
        pagination_html = create_pagination(page_num, total_pages)
        
        # 创建游戏卡片HTML
        game_cards_html = ""
        for game in current_page_games:
            game_cards_html += build_game_card(game, with_description=True)
        
        # 组合页面内容
        content = f"""
        <div class="pagination">{pagination_html}</div>
        <div class="game-grid featured-grid">
            {game_cards_html}
        </div>
        <div class="pagination">{pagination_html}</div>
        """
        
        # 使用模板创建完整页面
        page_title = "Free Online Games - Gun Racing Games"
        page_description = "Play the best free online games at Gun Racing Games! Over 1000 free games including action, shooting, racing, puzzle and more. No download required, play instantly!"
        
        # 替换模板变量
        page_html = header_template.replace("{{title}}", page_title)
        page_html = page_html.replace("{{description}}", page_description)
        page_html = page_html.replace("{{header}}", "All Games")
        page_html = page_html.replace("{{subheader}}", "Play the best free online games instantly with no download required!")
        page_html = page_html.replace("{{home_active}}", "active")
        
        # 清除其他活动状态标记
        for category in CATEGORY_MAP.keys():
            cat_lower = category.lower()
            page_html = page_html.replace(f"{{{{{cat_lower}_active}}}}", "")
        
        # 添加内容和页脚
        page_html += content + footer_template
        
        # 保存页面
        if page_num == 1:
            filename = "index.html"
        else:
            filename = f"page{page_num}.html"
        
        write_html(filename, page_html)
        
        # 如果是分页页面（非首页），修正导航链接路径
        if page_num > 1:
            # 读取刚刚写入的文件
            with open(filename, 'r', encoding='utf-8') as f:
                page_content = f.read()
            
            # 修正导航链接路径，确保它们指向正确的路径
            # 这里我们需要确保分页页面上的导航链接是正确的
            # 例如，从page2.html点击"Action"应该正确导航到games/action/index.html
            
            # 写回文件
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(page_content)

# 构建分页导航HTML
def create_pagination(current_page, total_pages):
    pagination_html = ''
    
    # 上一页按钮
    if current_page > 1:
        prev_page = "index.html" if current_page == 2 else f"page{current_page - 1}.html"
        pagination_html += f'<a href="{prev_page}" class="page-nav prev" aria-label="Previous page"><i class="page-icon">←</i></a>'
    else:
        pagination_html += '<span class="page-nav prev disabled" aria-label="Previous page"><i class="page-icon">←</i></span>'
    
    # 页码
    for i in range(1, total_pages + 1):
        if i == current_page:
            pagination_html += f'<span class="page-number current">{i}</span>'
        else:
            page_link = "index.html" if i == 1 else f"page{i}.html"
            pagination_html += f'<a href="{page_link}" class="page-number">{i}</a>'
    
    # 下一页按钮
    if current_page < total_pages:
        next_page = f"page{current_page + 1}.html"
        pagination_html += f'<a href="{next_page}" class="page-nav next" aria-label="Next page"><i class="page-icon">→</i></a>'
    else:
        pagination_html += '<span class="page-nav next disabled" aria-label="Next page"><i class="page-icon">→</i></span>'
    
    return pagination_html

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

# 创建默认CSS样式
def create_default_css():
    css_path = "assets/css/style.css"
    if not os.path.exists(css_path):
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

# 创建模板文件
def create_templates():
    # 创建header模板(如果不存在)
    header_template_path = "templates/header.html"
    if not os.path.exists(header_template_path) or os.path.getsize(header_template_path) == 0:
        header_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}} - Gun Racing Games</title>
    <link rel="stylesheet" href="assets/css/style.css">
    <meta name="description" content="{{description}}">
</head>
<body>
    <div class="layout">
        <!-- Sidebar Navigation -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <a href="index.html" class="logo"> 
                    <span class="logo-icon">🔫</span> 
                    <span class="logo-text">Gun Racing Games</span> 
                </a>
            </div>
            <nav class="category-list">
                <a href="index.html" class="category-item {{home_active}}">Home</a>
                <a href="games/action/index.html" class="category-item {{action_active}}">Action</a>
                <a href="games/adventure/index.html" class="category-item {{adventure_active}}">Adventure</a>
                <a href="games/racing/index.html" class="category-item {{racing_active}}">Racing</a>
                <a href="games/driving/index.html" class="category-item {{driving_active}}">Driving</a>
                <a href="games/shooting/index.html" class="category-item {{shooting_active}}">Shooting</a>
                <a href="games/puzzle/index.html" class="category-item {{puzzle_active}}">Puzzle</a>
                <a href="games/sports/index.html" class="category-item {{sports_active}}">Sports</a>
                <a href="games/casual/index.html" class="category-item {{casual_active}}">Casual</a>
                <a href="games/clicker/index.html" class="category-item {{clicker_active}}">Clicker</a>
                <a href="games/.io/index.html" class="category-item {{io_active}}">.IO Games</a>
                <a href="games/beauty/index.html" class="category-item {{beauty_active}}">Beauty</a>
                <a href="games/other/index.html" class="category-item {{other_active}}">Other</a>
            </nav>
            <div class="sidebar-footer">
                <p>© 2024 <a href="https://gunracing.online/" target="_blank">gunracing games</a></p>
            </div>
        </aside>

        <!-- Main Content -->
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
                <p>Website: <a href="https://gunracing.online/" target="_blank">https://gunracing.online/</a> | For educational purposes only</p>
            </footer>
        </main>
    </div>
</body>
</html>
"""
        write_html(footer_template_path, footer_template)

# 为子目录游戏详情页添加CSS和JS路径修正
def adjust_paths_for_detail(html_content):
    # 修正CSS路径
    adjusted = html_content.replace('href="assets/css/style.css"', 'href="../../assets/css/style.css"')
    # 删除搜索JS脚本引用
    adjusted = adjusted.replace('<script src="../../assets/js/search.js"></script>\n</head>', '</head>')
    return adjusted

# 为子目录分类页面添加CSS和JS路径修正
def adjust_paths_for_category(html_content):
    # 修正CSS路径
    adjusted = html_content.replace('href="assets/css/style.css"', 'href="../../assets/css/style.css"')
    # 删除搜索JS脚本引用
    adjusted = adjusted.replace('<script src="../../assets/js/search.js"></script>\n</head>', '</head>')
    return adjusted

# 为主页添加CSS和JS路径修正
def adjust_paths_for_home(html_content):
    # 删除搜索JS脚本引用
    adjusted = html_content.replace('<script src="assets/js/search.js"></script>\n</head>', '</head>')
    return adjusted

# 主函数
def main():
    print("Building static game website...")
    start_time = datetime.now()
    
        # 检查是否存在游戏数据文件
    try:
        if os.path.exists("games.json"):
            with open("games.json", "r", encoding="utf-8") as f:
                games = json.load(f)
            print(f"Loaded {len(games)} games from games.json")
        elif os.path.exists("crazy_games.json"):
            with open("crazy_games.json", "r", encoding="utf-8") as f:
                games = json.load(f)
                print(f"Loaded {len(games)} games from crazy_games.json")
        else:
            print("Error: No games data file found (tried games.json and crazy_games.json)")
            return
    except Exception as e:
        print(f"Failed to load game data: {e}")
        return
    
    # 确保必要的目录存在
    ensure_directory("games")
    for category in CATEGORY_MAP.keys():
        ensure_directory(f"games/{category}")
    
    # 复制静态资源
    copy_static_assets()
    
    # 创建默认CSS
    create_default_css()

    # 读取模板
    header_template = read_template("header")
    footer_template = read_template("footer")
    
    # 按分类分组游戏
    categories = {}
    for game in games: # 使用加载的游戏数据
        cat = game.get("category", "Other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(game)
    
    # 构建分类页面
    for category, cat_games in categories.items():
        if category in CATEGORY_MAP:
            print(f"Building category page: {category} ({len(cat_games)} games)")
            build_category_page(category, cat_games, header_template, footer_template)
    
    # Build game detail pages
    print("Building game detail pages...")
    for game in games: # 使用加载的游戏数据
        if "title" in game and "category" in game:
            build_game_detail(game, header_template, footer_template)
    
    # Build homepage
    print("Building homepage...")
    build_homepage(games, header_template, footer_template) # 使用加载的游戏数据
    
    # Update all category pages
    # update_all_category_pages() # This function is not defined in the original file
    
    # Update all game detail pages
    # update_all_game_detail_pages() # This function is not defined in the original file
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    print(f"Website build complete! Took {duration:.2f} seconds")
    print("Generated pages:")
    print("- index.html (Home)")
    for category in CATEGORY_MAP:
        if category in categories:
            print(f"- games/{category.lower()}/index.html ({CATEGORY_MAP[category]} category page)")
    print(f"- Total: {sum(len(cat_games) for cat_games in categories.values() if cat_games[0].get('category', '') in CATEGORY_MAP)} game detail pages")
    print("\nYou can open index.html in your browser to access the website.")
    # check_category_links() # This function is not defined in the original file

if __name__ == "__main__":
    main()
