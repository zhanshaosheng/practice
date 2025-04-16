import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
# 设置画布大小
height, width = 600, 600
canvas = np.zeros((height, width, 3), dtype="uint8") + 255

# 设置冰淇淋的颜色
ice_cream_color = (255, 192, 203)  # 粉色
cone_color = (139, 69, 19)  # 棕色

# 创建一个空白画布
canvas = np.zeros((height, width, 3), dtype="uint8") + 255

# 画冰淇淋桶锥形
cv2.line(canvas, (300, 500), (200, 220), cone_color, 5)  # 画锥形冰淇淋筒
cv2.line(canvas, (300, 500), (400, 220), cone_color, 5)  # 画锥形冰淇淋筒
cv2.line(canvas, (200, 220), (400, 220), cone_color, 5)  # 画锥形冰淇淋筒
#画甜筒弧度
cv2.ellipse(canvas, (300, 220), (100, 130), 0, 180, 360, ice_cream_color, -1)  # 画一个椭圆


#合适的位置写上姓名学号、张三_20212147
pil_img = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR))
draw = ImageDraw.Draw(pil_img)
fontStyle = ImageFont.truetype('STSONG.TTF', 15, encoding = 'utf-8')
draw.text((50, 50), '张三_20212147', 0, font=fontStyle)
canvas = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
cv2.imshow("window1", canvas)
cv2.waitKey(0)  # 等待按键事件，按下任意键继续执行
cv2.destroyAllWindows()  # 关闭所有窗口