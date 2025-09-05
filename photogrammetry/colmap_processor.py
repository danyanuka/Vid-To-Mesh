import subprocess
import os
import cv2
from pathlib import Path


class ColmapProcessor:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.database_path = self.project_path / "database.db"
        self.images_path = self.project_path / "images"
        self.sparse_path = self.project_path / "sparse"
        
        # Create directories if they don't exist
        self.images_path.mkdir(parents=True, exist_ok=True)
        self.sparse_path.mkdir(parents=True, exist_ok=True)
    
    def extract_frames_from_video(self, video_path, target_fps=10):
        print(f"Extracting frames from {video_path} at {target_fps} FPS...") 
        try:
            # Open video
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                print(f"Error: Could not open video file {video_path}")
                return False
            
            # Get video FPS
            video_fps = cap.get(cv2.CAP_PROP_FPS)
            frame_interval = int(video_fps / target_fps)
            
            print(f"Video FPS: {video_fps}, extracting every {frame_interval} frames")
            
            frame_count = 0
            extracted_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    frame_filename = f"frame_{extracted_count:06d}.jpg"
                    frame_path = self.images_path / frame_filename
                    cv2.imwrite(str(frame_path), frame)
                    extracted_count += 1
                
                frame_count += 1
            
            cap.release()
            print(f"Extracted {extracted_count} frames to {self.images_path}")
            return True
            
        except Exception as e:
            print(f"Frame extraction failed: {e}")
            return False
    
    def extract_features(self):
        """
        Run COLMAP feature extraction on images.
        Creates database.db with extracted features.
        """
        print("Extracting features...")
        
        cmd = [
            "colmap", "feature_extractor",
            "--database_path", str(self.database_path),
            "--image_path", str(self.images_path)
        ]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("Feature extraction completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Feature extraction failed: {e}")
            print(f"Error output: {e.stderr}")
            return False
    
    def match_features(self):
        """
        Run COLMAP feature matching between all images.
        Updates database.db with feature matches.
        """
        print("Matching features...")
        
        cmd = [
            "colmap", "exhaustive_matcher",
            "--database_path", str(self.database_path)
        ]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("Feature matching completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Feature matching failed: {e}")
            print(f"Error output: {e.stderr}")
            return False
    
    def create_sparse_reconstruction(self):
        """
        Run COLMAP mapper to create sparse 3D reconstruction.
        Creates sparse/ folder with cameras.bin, images.bin, points3D.bin
        """
        print("Creating sparse reconstruction...")
        
        cmd = [
            "colmap", "mapper",
            "--database_path", str(self.database_path),
            "--image_path", str(self.images_path),
            "--output_path", str(self.sparse_path)
        ]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("Sparse reconstruction completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Sparse reconstruction failed: {e}")
            print(f"Error output: {e.stderr}")
            return False
    
    def get_sparse_path(self):
        """
        Get the path to the sparse reconstruction folder.
        
        Returns:
            Path: Path to sparse/ folder containing reconstruction files
        """
        return self.sparse_path
    
    def check_colmap_available(self):
        """
        Check if COLMAP is available in the system PATH.
        
        Returns:
            bool: True if COLMAP is available, False otherwise
        """
        try:
            subprocess.run(["colmap", "--help"], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
