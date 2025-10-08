from yolo_detection import yolo_main
from photogrammetry.colmap_processor import ColmapProcessor
import uuid

video_path = 'assets/nordo_indoor (2).mp4'
# yolo_main.run(video_path)

temp_folder = f"temp_processing/{uuid.uuid4()}/"
processor = ColmapProcessor(temp_folder)

# Process video
processor.extract_frames_outliner_remover(video_path, 10)
processor.extract_features()
processor.match_features()
processor.sparse_reconstruct()