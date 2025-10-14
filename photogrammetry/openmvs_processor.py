import subprocess
from pathlib import Path

class OpenMVSProcessor:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.dense_path = self.project_path / "dense"
    
   