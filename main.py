from ultralytics import YOLO
import cv2
import numpy as np
import printUtils

model = YOLO('yolov8n-seg.pt')

# Load video
video_path = 'assets/indoor-flight.mp4'
cap = cv2.VideoCapture(video_path)


detected_objects = {}

class DetectedObject:
    def __init__(self, obj_id, label, masked_image, score):
        self.obj_id = obj_id
        self.label = label
        self.masked_image = masked_image
        self.score = score

    @staticmethod
    def compute_score(box, mask):
        # Confidence
        confidence = float(box.conf.item())
        # Mask area
        mask_area = mask.sum().item()
        # Box area
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
        box_area = max((x2 - x1), 0) * max((y2 - y1), 0)
        # Final score
        area_ratio = mask_area / box_area if box_area > 0 else 0
        return confidence * area_ratio

# Read Frames
ret = True
while ret:
    ret, frame = cap.read()
    if ret:
        results = model.track(frame, persist=True, retina_masks=True, verbose=False)
        result = results[0]
        # printUtils.show_frames_in_loop(result)

        for i, box in enumerate(result.boxes):
            if box.id is None:
                continue
            obj_id = int(box.id.item())

            cls_id = int(box.cls)
            label = result.names[cls_id]

            mask = result.masks.data[i]
            mask_image = cv2.bitwise_and(frame, frame, mask=(mask.cpu().numpy()).astype(np.uint8))

            score = DetectedObject.compute_score(box, mask)

            if obj_id not in detected_objects or score > detected_objects[obj_id].score:
                detected_objects[obj_id] = DetectedObject(obj_id, label, mask_image, score)
            
printUtils.print_and_view_detections(detected_objects)
