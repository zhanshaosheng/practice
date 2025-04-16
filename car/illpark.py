import numpy as np

def calculate_iou(box1, box2):
    # box格式: x1, y1, x2, y2
    # 计算交集的坐标
    x_left = max(box1[0], box2[0])
    y_top = max(box1[1], box2[1])
    x_right = min(box1[2], box2[2])
    y_bottom = min(box1[3], box2[3])
    
    # 计算交集的宽度和高度
    inter_width = max(x_right - x_left, 0)
    inter_height = max(y_bottom - y_top, 0)
    
    # 计算交集面积
    inter_area = inter_width * inter_height
    
    # 计算两个矩形的面积
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    
    # 计算并集面积
    union_area = box1_area + box2_area - inter_area
    
    # 计算IoU
    iou = inter_area / union_area
    return iou

#找上一次的位置
def searchLast(carItem, lastCars):
    for item in lastCars:
        if calculate_iou(carItem, item) >= 0.9:
            return item
    return None
