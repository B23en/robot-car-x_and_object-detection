class CheckBbox:
    def __init__(self):
        self.bbox_memory = {
            "go_straight": 0,
            "turn_left": 0,
            "turn_right": 0,
            "stop": 0
        }
        self.curr_bbox = {}
        self.second_bbox = {}

        self.size_offset = 40000
        self.detection_size = 9000

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
                if bbox_list[cls_name]['size'] > self.detection_size:
                    self.bbox_memory[cls_name] += 1
                if self.bbox_memory[cls_name] >= 3:
                    if (not self.curr_bbox) or (bbox_list[cls_name]['size'] > self.curr_bbox.get('size', -1)):
                        # demote current to second if exists
                        if self.curr_bbox and self.curr_bbox['cls_name'] != bbox_list[cls_name]['cls_name']:
                            self.second_bbox = self.curr_bbox
                        self.curr_bbox = bbox_list[cls_name]
                    elif (not self.second_bbox) or (bbox_list[cls_name]['size'] > self.second_bbox.get('size', -1)):
                        # Prevent second_bbox from having the same class as curr_bbox
                        if (not self.curr_bbox) or (bbox_list[cls_name]['cls_name'] != self.curr_bbox.get('cls_name')):
                            self.second_bbox = bbox_list[cls_name]
            else:
                self.bbox_memory[cls_name] = 0

        return self.get_curr_sign(), self.get_second_sign(), self.get_curr_size(), self.get_second_size()

    def get_curr_sign(self):
        if not self.curr_bbox or self.curr_bbox['size'] < self.detection_size:
            return "none"
        if self.second_bbox and (self.curr_bbox['cls_name'] == "stop" or self.second_bbox['cls_name'] == "stop") and (self.curr_bbox['size'] - self.second_bbox['size'] < self.size_offset):
            if self.curr_bbox['cls_name'] == "turn_right" or self.second_bbox['cls_name'] == "turn_right":
                return "stop_and_turn_right"
            elif self.curr_bbox['cls_name'] == "turn_left" or self.second_bbox['cls_name'] == "turn_left":
                return "stop_and_turn_left"
        return self.curr_bbox['cls_name']
    
    def get_second_sign(self):
        if not self.second_bbox:
            return "none"
        return self.second_bbox['cls_name']

    def get_curr_size(self):
        if not self.curr_bbox:
            return -1
        return self.curr_bbox['size']
    
    def get_second_size(self):
        if not self.second_bbox:
            return -1
        return self.second_bbox['size']
    
    def reset_curr_sign(self):
        self.curr_bbox = {}
        self.second_bbox = {}