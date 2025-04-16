import math


class Tracker:
    def __init__(self):
        # 存储目标的中心位置
        self.center_points = {}
        # ID计数
        # 每当检测到一个新的目标id时, 计数将增加1
        self.id_count = 0

    def update(self, objects_rect):
        # 目标的方框和ID
        objects_bbs_ids = []

        # 获取新目标的中心点
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # 看看这个目标是否已经被检测到过
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 35:
                    self.center_points[id] = (cx, cy)
                    # print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # 检测到新目标，分配ID给新目标
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # 按中心点清理字典, 删除不再使用的ID
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # 更新字典, 删除未使用的ID
        self.center_points = new_center_points.copy()
        return objects_bbs_ids