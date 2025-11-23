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
            "-i", ".",  # Current directory (dense folder), InterfaceCOLMAP finds sparse/ inside
            "-o", "scene.mvs",  # Relative to dense folder
            "--image-folder", str(self.undistorted_imgs_folder.resolve())  # Absolute path so .mvs file stores absolute paths
        ]

        print(f"Command: {' '.join(cmd)}")

        try:
            # Run from dense folder, matching manual execution
            subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=str(self.dense_path))
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
            "-i", "scene.mvs",  # Relative to dense folder
            "-w", ".",  # Current directory (dense folder)
            "-v", str(3)
        ]

        try:
            # Run from dense folder, matching manual execution
            subprocess.run(cmd, check=True, text=True, cwd=str(self.dense_path))
            print(f"DensifyPointCloud completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"DensifyPointCloud failed: {e}")
            print(f"Error output: {e.stderr}")
            return False
   