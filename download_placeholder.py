import requests
import os

# 确保images目录存在
if not os.path.exists('images'):
    os.makedirs('images')

# 下载占位图片
placeholder_url = "https://via.placeholder.com/512x384.png?text=Game+Image"
placeholder_path = "images/placeholder.png"

try:
    print(f"开始下载占位图片: {placeholder_url}")
    response = requests.get(placeholder_url)
    response.raise_for_status()  # 确保请求成功
    
    with open(placeholder_path, 'wb') as f:
        f.write(response.content)
    
    print(f"成功下载占位图片到: {placeholder_path}")
except Exception as e:
    print(f"下载占位图片失败: {e}")

# 创建一个简单的本地占位图片（备用方案）
backup_content = '''
<svg xmlns="http://www.w3.org/2000/svg" width="512" height="384" viewBox="0 0 512 384">
  <rect width="512" height="384" fill="#e0e0e0"/>
  <text x="50%" y="50%" font-family="Arial" font-size="24" text-anchor="middle" fill="#888888">游戏图片</text>
</svg>
'''

with open("images/local_placeholder.svg", 'w', encoding='utf-8') as f:
    f.write(backup_content)

print("创建了本地SVG占位图片")

# 修改index.html中的占位图片路径
index_path = "index.html"
if os.path.exists(index_path):
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换占位图路径
    content = content.replace("'images/placeholder.png'", "'images/placeholder.png', 'images/local_placeholder.svg'")
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("已更新index.html中的占位图路径")
else:
    print(f"未找到文件: {index_path}") 