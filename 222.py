import cv2
import os

# 输入和输出路径
input_image = r"D:\Desktop\ticket1.jpg"
output_dir = r"D:\Desktop\chars"
os.makedirs(output_dir, exist_ok=True)

# 读图
img = cv2.imread(input_image)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 二值化
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 形态学操作，去噪点
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# 找连通域
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(morph, connectivity=8)

char_id = 0
for i, stat in enumerate(stats):
    x, y, w, h, area = stat
    # 过滤掉太小或太大的区域（避免噪点或整块背景）
    if 10 < w < 200 and 10 < h < 200:
        char = img[y:y+h, x:x+w]
        cv2.imwrite(f"{output_dir}/char_{char_id}.png", char)
        char_id += 1

print(f"✅ 已经提取 {char_id} 个字符，保存在 {output_dir}/ 文件夹里")
