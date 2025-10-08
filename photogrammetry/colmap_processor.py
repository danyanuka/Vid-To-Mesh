import subprocess
import os
import cv2
from pathlib import Path
import sharp_frames
import shutil


class ColmapProcessor:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.database_path = self.project_path / "database.db"
        self.images_path = self.project_path / "images"
        self.sparse_path = self.project_path / "sparse"
        
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
                    frame_filename = f"frame_{extracted_count:03d}.jpg"
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


    # SHARP-FRAMES Otliner remover (Works on Photos set extracted by cv2)
    def extract_frames_outliner_remover(self, video_path, target_fps=10):
        print(f"Extracting frames from {video_path} at {target_fps} FPS...") 
        try:
            # Open video
            cap = cv2.VideoCapture(video_path)
            temp_path = self.project_path / "_temp_frames"
            temp_path.mkdir(parents=True, exist_ok=True)

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
                    frame_filename = f"frame_{extracted_count:03d}.jpg"
                    frame_path = temp_path / frame_filename
                    cv2.imwrite(str(frame_path), frame)
                    extracted_count += 1

                frame_count += 1

            cap.release()
            print(f"Extracted total of {extracted_count} frames")

            # --- Remove blurry frames using SharpFrames CLI ---
            cmd = [
                "sharp-frames",                   # CLI name
                str(temp_path),            # input folder
                str(self.images_path),                # output folder
                "--selection-method", "outlier-removal",
                "--outlier-sensitivity", "85"
            ]
    
            try:
                subprocess.run(cmd, check=True, text=True)
                shutil.rmtree(temp_path)
                final_count = len(list(self.images_path.glob("*.jpg")))
                print(f"Blur removal complete! {final_count} frames remain in {self.images_path}")
                return final_count
            except subprocess.CalledProcessError as e:
                print(f"SharpFrames outlier-removal failed: {e}")
                return extracted_count  # fallback to unfiltered frames
            except FileNotFoundError:
                print("SharpFrames CLI not found. Install it and ensure it's in PATH.")
                return extracted_count

        except Exception as e:
            print(f"Frame extraction failed: {e}")
            return False

    
    # SHARP-FRAMES Default Best-N (Works on a video)
    def extract_sharp_frames(self, video_path, target_fps=10):
        print(f"Extracting frames from {video_path} at {target_fps} FPS...")
        cmd = [
            "sharp-frames",
            str(video_path), 
            str(self.images_path),
            "--fps", str(target_fps),
            "--num-frames" , "500"
        ]

        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            extracted_count = len(list(self.images_path.glob("*.jpg")))
            print(f"Extraction complete! Total frames saved: {extracted_count}")
            return extracted_count  

        except Exception as e:
            print(f"Sharp-Frame extraction failed: {e}")
            return False

    
        
    
    def extract_features(self):
        """
        Creates database.db with extracted features.
        """
        print("Extracting features...")
        
        cmd = [
            "colmap", "feature_extractor",
            "--database_path", str(self.database_path),
            "--image_path", str(self.images_path),
            "--ImageReader.camera_model", "OPENCV",
            "--ImageReader.single_camera", "1" #Treat as single camera
            
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
            "colmap", "sequential_matcher",
            "--database_path", str(self.database_path)
        ]
        
        try:
            result = subprocess.run(cmd, check=True, text=True)
            print("Feature matching completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Feature matching failed: {e}")
            print(f"Error output: {e.stderr}")
            return False
    
    def sparse_reconstruct(self):
        """
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
        return self.sparse_path
    
    def check_colmap_available(self):
        """
        Check if COLMAP is available in the system PATH.
        """
        try:
            subprocess.run(["colmap", "--help"], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
