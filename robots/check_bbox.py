class CheckBbox:
    def __init__(self):
        self.bbox_memory = {
            "go_straight": 0,
            "turn_left": 0,
            "turn_right": 0,
            "stop": 0
        }
        self.curr_bbox = {}

    def check(self, pred_results):
        bbox_list = {}
        for box in pred_results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            bbox = {
                "conf": float(box.conf[0]),
                "cls_id": int(box.cls[0]),
                "cls_name": pred_results[0].names[int(box.cls[0])],
                "size": (x2 - x1) * (y2 - y1)
            }
            cls_name = bbox['cls_name']
            if cls_name in bbox_list:
                if bbox['size'] > bbox_list[cls_name]['size']:
                    bbox_list[cls_name] = bbox      
            else:
                bbox_list[cls_name] = bbox

        for cls_name in ['go_straight', 'turn_left', 'turn_right', 'stop']:
            if cls_name in bbox_list:
                self.bbox_memory[cls_name] += 1
                if self.bbox_memory[cls_name] >= 3:
                    if (not self.curr_bbox) or (bbox_list[cls_name]['size'] > self.curr_bbox.get('size', -1)):
                        self.curr_bbox = bbox_list[cls_name]
            else:
                self.bbox_memory[cls_name] = 0

        return self.get_curr_sign()

    def get_curr_sign(self):
        if not self.curr_bbox:
            return "none"
        return self.curr_bbox['cls_name']
    
    def reset_curr_sign(self):
        self.curr_bbox = {}