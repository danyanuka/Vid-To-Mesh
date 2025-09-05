from yolo_detection import yolo_main
from photogrammetry.colmap_processor import ColmapProcessor
import uuid

video_path = 'assets/indoor-flight.mp4'
# yolo_main.run(video_path)

temp_folder = f"temp_processing/{uuid.uuid4()}/"
processor = ColmapProcessor(temp_folder)

# Process video
processor.extract_frames_from_video(video_path)
processor.extract_features()
processor.match_features()
processor.create_sparse_reconstruction()