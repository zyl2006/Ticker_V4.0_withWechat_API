import cv2
import numpy as np
import os

input_dir = r"D:\Desktop\bluefont"  # 输入图片文件夹
output_root = r"D:\Desktop\bluefont\result"  # 输出文件夹

os.makedirs(output_root, exist_ok=True)

valid_ext = [".png", ".jpg", ".jpeg", ".bmp"]

for filename in os.listdir(input_dir):
    if not any(filename.lower().endswith(ext) for ext in valid_ext):
        continue

    input_path = os.path.join(input_dir, filename)
    print(f"🔍 正在处理: {input_path}")

    img = cv2.imread(input_path)

    # 1. 去除蓝色点
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([140, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    img[mask > 0] = [255, 255, 255]

    # 2. 灰度化 + 二值化
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 3. 去噪 + 平滑笔画
    kernel = np.ones((2, 2), np.uint8)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel, iterations=1)

    # 4. 轮廓检测（提取字符）
    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])

    name_no_ext = os.path.splitext(filename)[0]
    output_dir = os.path.join(output_root, name_no_ext)
    os.makedirs(output_dir, exist_ok=True)

    index = 0
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w > 5 and h > 10:  # 过滤噪点
            char_img = cleaned[y:y+h, x:x+w]

            # --- 清晰化处理 ---
            # 放大到128×128，保持比例
            #char_img = cv2.resize(char_img, (128, 128), interpolation=cv2.INTER_CUBIC)

            # 平滑边缘（抗锯齿）
            char_img = cv2.GaussianBlur(char_img, (3, 3), 0)
            _, char_img = cv2.threshold(char_img, 127, 255, cv2.THRESH_BINARY)

            # 反色：黑字白底
            char_img = 255 - char_img

            cv2.imwrite(os.path.join(output_dir, f"char_{index}.png"), char_img)
            index += 1

    print(f"✅ {filename} 处理完成，共保存 {index} 张字符到 {output_dir}")

print("🎉 所有图片已转为清晰字符数据集！")
