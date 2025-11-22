import subprocess
from pathlib import Path

class OpenMVSProcessor:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.dense_path = self.project_path / "dense"
        self.mvs_file_path = self.dense_path / "scene.mvs"
        self.undistorted_imgs_folder = self.dense_path / "images"


    def interface_colmap(self):
        print("Running InterfaceCOLMAP...")

        cmd = [
            "InterfaceCOLMAP",
            "-w", str(self.dense_path),
            "-i", str(self.dense_path),
            "-o", str(self.mvs_file_path),
            "--image-folder", str(self.undistorted_imgs_folder)
        ]

        print(f"Command: {' '.join(cmd)}") 

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"InterfaceCOLMAP completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"InterfaceCOLMAP failed: {e}")
            print(f"Error output: {e.stderr}")
            return False

    def densify_pointcloud(self):
        print("Running DensifyPointCloud...")

        cmd = [
            "DensifyPointCloud",
            "-i", str(self.mvs_file_path),
            "-w", str(self.dense_path),
            "-v", str(3)
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"DensifyPointCloud completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"DensifyPointCloud failed: {e}")
            print(f"Error output: {e.stderr}")
            return False
   