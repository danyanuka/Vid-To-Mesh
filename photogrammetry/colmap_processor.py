import subprocess
from pathlib import Path


class ColmapProcessor:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.database_path = self.project_path / "database.db"
        self.images_path = self.project_path / "images"
        self.sparse_path = self.project_path / "sparse"
        
        # Only create sparse here; extractor is the owner of images/
        self.sparse_path.mkdir(parents=True, exist_ok=True)


    def extract_features(self):
        """
        Creates database.db with extracted features.
        """
        print("Extracting features...")
        
        cmd = [
            "colmap", "feature_extractor",
            "--database_path", str(self.database_path),
            "--image_path", str(self.images_path),
            "--ImageReader.camera_model", "SIMPLE_RADIAL",
            "--ImageReader.single_camera", "1" #Treat as single camera
            
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("Feature extraction completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Feature extraction failed: {e}")
            print(f"Error output: {e.stderr}")
            return False

    
    def match_features(self):
        """
        Run COLMAP sequential_matcher.
        creates database.db
        """
        print("Matching features...")
        
        cmd = [
            "colmap", "sequential_matcher",
            "--database_path", str(self.database_path)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
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
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("Sparse reconstruction completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Sparse reconstruction failed: {e}")
            print(f"Error output: {e.stderr}")
            return False

