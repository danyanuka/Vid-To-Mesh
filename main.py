from yolo_detection import yolo_main
from photogrammetry.colmap_processor import ColmapProcessor
from photogrammetry.frame_extraction import FrameExtractor
import uuid

video_path = 'assets/Mansion-1.25min-30fps.mp4'
# yolo_main.run(video_path)

temp_folder = f"temp_processing/{uuid.uuid4()}/"

extractor = FrameExtractor(temp_folder)
processor = ColmapProcessor(temp_folder)


# current best is batch size 4 giving 450 frames with 33k points3d
# NEXT TRY CV2 ONLY WITH THE NORDO (2) 450 frames compare to the current best batch method size 4
# Experiment with SIMPLE-RADIAL and OPENCV FISHEYE

extractor.sharp_frames_batched(video_path)

# Colmap - 
# Result - sparse reconstruction (cameras,framess,points3d)
processor.extract_features()
processor.match_features()
processor.sparse_reconstruct()

# OpenMVS-
