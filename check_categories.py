import json

# 读取游戏数据
with open('game_data.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

# 打印前5个游戏的分类和标签
print('示例游戏分类:')
for i, game in enumerate(games[:5]):
    title = game['title']
    category = game['category']
    tags = ', '.join(game['tags'])
    print(f"{i+1}. {title}: {category}, 标签: {tags}")

# 统计每个分类的游戏数量
category_counts = {}
for game in games:
    cat = game['category']
    if cat in category_counts:
        category_counts[cat] += 1
    else:
        category_counts[cat] = 1

# 打印分类统计
print("\n游戏分类统计:")
for cat, count in category_counts.items():
    print(f"{cat}: {count}个游戏") 