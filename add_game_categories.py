import json
import random

# 游戏分类
categories = ["Action", "Racing", "Shooting", "Puzzle", "Sports", "Casual"]

# 各种可能的标签
tags_by_category = {
    "Action": ["Platformer", "Fighting", "Adventure", "Ninja", "Survival", "Runner"],
    "Racing": ["Cars", "Speed", "Multiplayer", "Drift", "Offroad", "Simulation"],
    "Shooting": ["FPS", "Zombie", "Sniper", "War", "Survival", "Battle"],
    "Puzzle": ["Match-3", "Logic", "Brain", "Strategy", "Physics", "Casual"],
    "Sports": ["Football", "Basketball", "Tennis", "Soccer", "Golf", "Multiplayer"],
    "Casual": ["Idle", "Clicker", "Simulation", "Time Management", "Building", "Relaxing"]
}

# 读取游戏数据
with open('game_data.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

# 添加分类和标签
for game in games:
    if "category" not in game:
        # 根据游戏标题和描述选择合适的分类
        title_lower = game["title"].lower()
        desc_lower = game["description"].lower()
        
        # 尝试根据关键词匹配分类
        if any(word in title_lower or word in desc_lower for word in ["shoot", "gun", "sniper", "fps", "battle"]):
            category = "Shooting"
        elif any(word in title_lower or word in desc_lower for word in ["race", "car", "drift", "speed", "driving"]):
            category = "Racing"
        elif any(word in title_lower or word in desc_lower for word in ["puzzle", "brain", "match", "logic", "solve"]):
            category = "Puzzle"
        elif any(word in title_lower or word in desc_lower for word in ["sport", "soccer", "football", "basketball", "tennis"]):
            category = "Sports"
        elif any(word in title_lower or word in desc_lower for word in ["idle", "clicker", "farm", "city", "tycoon"]):
            category = "Casual"
        else:
            category = "Action"  # 默认分类
            
        game["category"] = category
        
        # 添加标签
        if "tags" not in game:
            # 为每个游戏随机选择2-3个标签
            num_tags = random.randint(2, 3)
            game["tags"] = random.sample(tags_by_category[category], num_tags)

# 保存修改后的游戏数据
with open('game_data.json', 'w', encoding='utf-8') as f:
    json.dump(games, f, indent=2, ensure_ascii=False)

print(f"已成功为{len(games)}个游戏添加分类和标签") 