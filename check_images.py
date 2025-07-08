#!/usr/bin/env python3
import os
import glob
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
from collections import defaultdict
import concurrent.futures
import json
import random

class ImageChecker:
    def __init__(self, base_dir='.', category_dir=None, timeout=3):
        self.base_dir = os.path.abspath(base_dir)
        self.category_dir = category_dir  # 新增：特定分类目录
        self.timeout = timeout
        self.errors = defaultdict(list)
        self.total_images = 0
        self.failed_images = 0
        self.processed_files = 0
        
    def is_valid_local_file(self, src, html_path):
        """检查本地文件是否存在"""
        # 处理相对路径
        if src.startswith('/'):
            # 绝对路径（相对于网站根目录）
            full_path = os.path.join(self.base_dir, src.lstrip('/'))
        else:
            # 相对路径（相对于HTML文件所在目录）
            html_dir = os.path.dirname(html_path)
            full_path = os.path.normpath(os.path.join(html_dir, src))
            
        return os.path.exists(full_path), full_path
    
    def is_valid_remote_url(self, url):
        """检查远程URL是否可访问"""
        try:
            response = requests.head(url, timeout=self.timeout, allow_redirects=True)
            return response.status_code == 200, response.status_code
        except requests.exceptions.RequestException as e:
            return False, str(e)
    
    def get_category_from_path(self, path):
        """从文件路径中提取游戏分类"""
        parts = path.split(os.sep)
        if 'games' in parts:
            games_index = parts.index('games')
            if games_index + 1 < len(parts):
                return parts[games_index + 1]
        return "未知分类"
    
    def get_game_name(self, path):
        """从文件路径中提取游戏名称"""
        filename = os.path.basename(path)
        return os.path.splitext(filename)[0]
    
    def process_html_file(self, html_path):
        """处理单个HTML文件，提取和检查所有图片"""
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            img_tags = soup.find_all('img')
            
            category = self.get_category_from_path(html_path)
            game_name = self.get_game_name(html_path)
            
            for img in img_tags:
                src = img.get('src', '')
                if not src:
                    continue
                
                self.total_images += 1
                
                # 区分本地文件和远程URL
                if src.startswith(('http://', 'https://')):
                    is_valid, status = self.is_valid_remote_url(src)
                    if not is_valid:
                        self.failed_images += 1
                        self.errors[category].append({
                            'src': src,
                            'game': game_name,
                            'page': html_path,
                            'error': f"远程URL无效 (状态: {status})"
                        })
                else:
                    is_valid, full_path = self.is_valid_local_file(src, html_path)
                    if not is_valid:
                        self.failed_images += 1
                        self.errors[category].append({
                            'src': src,
                            'game': game_name,
                            'page': html_path,
                            'error': f"本地文件不存在 (路径: {full_path})"
                        })
            
            return len(img_tags)
        except Exception as e:
            print(f"处理文件 {html_path} 时出错: {e}")
            return 0
    
    def scan_directory(self):
        """递归扫描目录，查找所有HTML文件并处理"""
        # 修改：根据是否指定了分类目录来确定扫描路径
        if self.category_dir:
            scan_dir = self.category_dir
            if not os.path.exists(scan_dir):
                print(f"错误: 目录 '{scan_dir}' 不存在")
                return
        else:
            scan_dir = os.path.join(self.base_dir, 'games')
            if not os.path.exists(scan_dir):
                print(f"错误: 目录 '{scan_dir}' 不存在")
                return
        
        html_files = glob.glob(os.path.join(scan_dir, '**', '*.html'), recursive=True)
        print(f"找到 {len(html_files)} 个HTML文件")
        
        start_time = time.time()
        
        # 使用线程池加速处理
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(self.process_html_file, html_files))
        
        self.processed_files = len(html_files)
        
        end_time = time.time()
        print(f"扫描完成，耗时 {end_time - start_time:.2f} 秒")
    
    def generate_report(self):
        """生成错误报告"""
        print("\n===== 图片检查报告 =====")
        print(f"处理文件数: {self.processed_files}")
        print(f"检查图片总数: {self.total_images}")
        print(f"失败图片数: {self.failed_images}")
        
        if self.total_images > 0:
            print(f"失败率: {self.failed_images / self.total_images * 100:.2f}%\n")
        else:
            print("失败率: 0% (未检查到图片)\n")
        
        if not self.errors:
            print("未发现问题！所有图片都可以正确加载。")
            return
        
        print("按分类汇总的错误:")
        for category, errors in self.errors.items():
            print(f"\n== {category} ({len(errors)} 个错误) ==")
            
            # 按游戏名分组
            game_errors = defaultdict(list)
            for error in errors:
                game_errors[error['game']].append(error)
            
            for game, game_errs in game_errors.items():
                print(f"\n游戏: {game} ({len(game_errs)} 个错误)")
                for i, err in enumerate(game_errs, 1):
                    print(f"  {i}. 页面: {err['page']}")
                    print(f"     图片: {err['src']}")
                    print(f"     错误: {err['error']}")
        
        # 输出常见问题模式
        self.analyze_common_patterns()
    
    def analyze_common_patterns(self):
        """分析常见错误模式"""
        if not self.errors:
            return
        
        print("\n===== 常见问题模式分析 =====")
        
        # 收集所有错误的src
        all_srcs = []
        for errors in self.errors.values():
            for error in errors:
                all_srcs.append(error['src'])
        
        # 分析远程URL域名
        remote_domains = defaultdict(int)
        for src in all_srcs:
            if src.startswith(('http://', 'https://')):
                domain = urlparse(src).netloc
                remote_domains[domain] += 1
        
        if remote_domains:
            print("\n远程URL域名分布:")
            for domain, count in sorted(remote_domains.items(), key=lambda x: x[1], reverse=True):
                print(f"  {domain}: {count} 个错误")
        
        # 分析本地路径模式
        local_patterns = defaultdict(int)
        for src in all_srcs:
            if not src.startswith(('http://', 'https://')):
                # 提取路径模式（如 /assets/screenshots/）
                parts = src.split('/')
                if len(parts) >= 3:
                    pattern = '/'.join(parts[:3]) + '/'
                    local_patterns[pattern] += 1
        
        if local_patterns:
            print("\n本地路径模式分布:")
            for pattern, count in sorted(local_patterns.items(), key=lambda x: x[1], reverse=True):
                print(f"  {pattern}: {count} 个错误")
        
        # 提供可能的解决方案
        print("\n可能的解决方案:")
        print("1. 检查资源目录是否存在，特别是 '/assets/screenshots/' 目录")
        print("2. 验证远程URL是否有效，特别是高频出现的域名")
        print("3. 检查图片文件命名约定是否一致")
        print("4. 考虑使用占位图作为临时解决方案")

def main():
    print("===== 游戏站点图片检查工具 =====")
    
    # 直接指定目录路径
    specific_dir = input("请输入要检查的目录路径 (例如: G:\\game guowai\\games\\action): ").strip()
    if not specific_dir:
        specific_dir = None
        base_dir = input("请输入网站根目录路径 (默认为当前目录): ").strip() or '.'
    else:
        # 如果指定了特定目录，则尝试推断网站根目录
        parts = specific_dir.split(os.sep)
        if 'games' in parts:
            games_index = parts.index('games')
            base_dir = os.sep.join(parts[:games_index])
        else:
            base_dir = '.'
    
    checker = ImageChecker(base_dir=base_dir, category_dir=specific_dir)
    checker.scan_directory()
    checker.generate_report()
    
    # 导出错误报告到CSV文件
    export = input("\n是否导出错误报告到CSV文件? (y/n): ").strip().lower()
    if export == 'y':
        import csv
        
        filename = f"image_errors_{time.strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['分类', '游戏', '页面', '图片路径', '错误'])
            
            for category, errors in checker.errors.items():
                for error in errors:
                    writer.writerow([
                        category,
                        error['game'],
                        error['page'],
                        error['src'],
                        error['error']
                    ])
            
        print(f"错误报告已导出到 {filename}")

if __name__ == "__main__":
    main()

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