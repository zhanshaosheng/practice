import cv2
import numpy as np
from tracker import *
import pandas as pd
from ultralytics import YOLO

# 加载模型
model = YOLO('yolov8s.pt')

#绘制违停区域
def draw_area(event, x, y, flags, param):
    global area 

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(area ) == 4:
            return
        print(event, x, y)
        area.append([x, y])


#创建窗口并注册鼠标事件
cv2.namedWindow('detecting')
cv2.setMouseCallback('detecting', draw_area)

# 选择需要检测的视频
cap = cv2.VideoCapture('v.mp4')     

# 读取类别名称
my_file = open("coco.txt", "r")
data = my_file.read()
#类别名称的字符串转化成列表
class_list = data.split("\n")

count = 0

area = []
# 跟踪算法
tracker = Tracker()

#获取FPS
fps = cap.get(cv2.CAP_PROP_FPS)

while True:
    ret, frame = cap.read()
    #循环读取视频
    if not ret:
        cap = cv2.VideoCapture('v.mp4') 
        continue
        # break

    count += 1
    #每三帧只检测一帧率
    if count % 3 != 0:
        continue
    frame = cv2.resize(frame, (1020, 500))

    results = model.predict(frame)
    # print(results)
    a = results[0].boxes.boxes
    px = pd.DataFrame(a).astype("float")
    # print(px)
    list = []

    # 使用YOLOv8的检测结果, 进行算法设计
    for index, row in px.iterrows():
        # print(row)

        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        c = class_list[d]
        if 'car' in c:
            list.append([x1, y1, x2, y2])
            
    bbox_id = tracker.update(list)
    

    # 画出区域
    for item in bbox_id:  
        x1, y1, x2, y2, id = item
        if len(area) == 4:
            if cv2.pointPolygonTest(np.array(area, np.int32), (int((x1+x2)/2), int((y1+y2)/2)), False) >= 0:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                print("bbox.len:",bbox_id.__len__())
                print(bbox_id)
    #绘制违停区域
    if len(area) == 4:
        cv2.polylines(frame,[np.array(area, np.int32)], True, (255,0,0),5)
    else:
        cv2.polylines(frame,[np.array(area, np.int32)], False, (255,0,0),5)
    cv2.imshow("detecting", frame)


    if cv2.waitKey(int(1000//fps) - 5) & 0xFF == 27:
        break
    
# 刷新，释放资源
cap.release()
cv2.destroyAllWindows()
