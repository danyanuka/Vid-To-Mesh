from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')

# Load video
video_path = 'assets/indoor-flight.mp4'
cap = cv2.VideoCapture(video_path)

# Read Frames
ret = True
while ret:
    ret, frame = cap.read()
    if ret:
  # detect And track objects
        results = model.track(frame,persist = True)
  # Plot Results
        frame_ = results[0].plot()
  # VIZUALIZE
        cv2.imshow('frame', frame_)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

