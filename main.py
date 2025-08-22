from ultralytics import YOLO
import cv2

model = YOLO('yolov8n-seg.pt')

# Load video
video_path = 'assets/indoor-flight.mp4'
cap = cv2.VideoCapture(video_path)


detected_objects = []

class DetectedObject:
    def __init__(self, obj_id, label, masked_image):
        self.obj_id = obj_id
        self.label = label
        self.masked_image = masked_image

# Read Frames
ret = True
while ret:
    ret, frame = cap.read()
    if ret:
  # detect And track objects
        results = model.track(frame, persist=True, retina_masks=True, verbose=False)
  # Plot Results
        frame_ = results[0].plot()
  # VIZUALIZE
        cv2.namedWindow("window", cv2.WINDOW_NORMAL)
        cv2.imshow('frame', frame_)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

