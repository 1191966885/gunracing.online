import json
import os

try:
    # 检查文件是否存在
    if not os.path.exists('game_data.json'):
        print('错误：game_data.json 文件不存在')
        exit(1)
    
    # 检查文件大小
    file_size = os.path.getsize('game_data.json')
    print(f'文件大小: {file_size/1024:.2f} KB')
    
    # 尝试解析JSON
    with open('game_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not isinstance(data, list):
        print('错误：JSON格式不正确，应为数组格式')
        exit(1)
    
    print(f'游戏数据正常，包含{len(data)}个游戏记录')
    
    # 输出前三个游戏的标题和分类
    for i, game in enumerate(data[:3]):
        title = game.get('title', '无标题')
        category = game.get('category', '无分类')
        print(f'{i+1}. {title} - {category}')
        
except json.JSONDecodeError as e:
    print(f'JSON解析错误: {e}')
    print(f'错误位置: 行 {e.lineno}, 列 {e.colno}')
    print(f'错误内容: {e.msg}')
except Exception as e:
    print(f'发生错误: {e}') 