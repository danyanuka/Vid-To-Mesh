from yolo_detection import yolo_main
from photogrammetry.colmap_processor import ColmapProcessor
from photogrammetry.openmvs_processor import OpenMVSProcessor
from photogrammetry.frame_extraction import FrameExtractor
import uuid

video_path = 'assets/nordo_indoor (2).mp4'
# yolo_main.run(video_path)

temp_folder = f"temp_processing/{uuid.uuid4()}/"

extractor = FrameExtractor(temp_folder)
colmap_processor = ColmapProcessor(temp_folder)
openmvs_processor = OpenMVSProcessor(temp_folder)



# Extract sharp images using sharp-frames
extractor.sharp_frames_batched(video_path)
# Colmap - 
# Result - sparse reconstruction (cameras,frames,points3d)
colmap_processor.extract_features()
colmap_processor.match_features()
colmap_processor.sparse_reconstruct()
# Convert colmap results to OpenMVS desired format (Undistorted images / MVS File)
colmap_processor.image_undistorter()
# OpenMVS-
openmvs_processor.interface_colmap()
openmvs_processor.densify_pointcloud()
