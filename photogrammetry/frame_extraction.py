import subprocess
from pathlib import Path
import shutil
import cv2


class FrameExtractor:
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.output_dir = self.project_root / "images"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # # Temporary folder for pre-filter frames
        # self.temp_dir = self.project_root / "frames_pre_filter"
        # self.temp_dir.mkdir(parents=True, exist_ok=True)

    # Only cv2
    def extract_frames_from_video(self, video_path: str, target_fps: int = 7):
        print(f"Extracting frames from {video_path} at {target_fps} FPS...")
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print(f"Error: Could not open video file {video_path}")
                return False

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
                    frame_path = self.output_dir / frame_filename
                    cv2.imwrite(str(frame_path), frame)
                    extracted_count += 1
                frame_count += 1

            cap.release()
            print(f"Extracted {extracted_count} frames to {self.output_dir}")
            return extracted_count
        except Exception as e:
            print(f"Frame extraction failed: {e}")
            return False


    def extract_frames_outlier_removal(self, video_path: str, target_fps: int = 10):
        print(f"Extracting frames (with outlier removal) from {video_path} at {target_fps} FPS...")
        try:
            cap = cv2.VideoCapture(video_path)
            temp_path = self.output_dir.parent / "_temp_frames"
            temp_path.mkdir(parents=True, exist_ok=True)

            if not cap.isOpened():
                print(f"Error: Could not open video file {video_path}")
                return False

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
            print(f"Extracted total of {extracted_count} frames before outlier removal")

            cmd = [
                "sharp-frames",
                str(temp_path),
                str(self.output_dir),
                "--selection-method", "outlier-removal",
                "--outlier-sensitivity", "85",
            ]

            try:
                subprocess.run(cmd, check=True, text=True)
                shutil.rmtree(temp_path)
                final_count = len(list(self.output_dir.glob("*.jpg")))
                print(f"Blur removal complete! {final_count} frames remain in {self.output_dir}")
                return final_count
            except subprocess.CalledProcessError as e:
                print(f"SharpFrames outlier-removal failed: {e}")
                return extracted_count
            except FileNotFoundError:
                print("SharpFrames CLI not found. Install it and ensure it's in PATH.")
                return extracted_count
        except Exception as e:
            print(f"Outlier-removal pipeline failed: {e}")
            return False


    def sharp_frames_best_n(self, video_path: str, target_fps: int = 10, num_frames: int = 500):
        print(f"Sharp-frames best-n from {video_path} at {target_fps} FPS (num_frames={num_frames})...")
        cmd = [
            "sharp-frames",
            str(video_path),
            str(self.output_dir),
            "--fps", str(target_fps),
            "--num-frames", str(num_frames),
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            extracted_count = len(list(self.output_dir.glob("*.jpg")))
            print(f"Extraction complete! Total frames saved: {extracted_count}")
            return extracted_count
        except Exception as e:
            print(f"Sharp-frames best-n failed: {e}")
            return False
            

    def sharp_frames_batched(self, video_path: str, batch_size: int = 4, batch_buffer: int = 0, fps: int = 30):
        print(f"Sharp-frames batched (batch_size={batch_size}, batch_buffer={batch_buffer}, fps={fps})...")
        cmd = [
            "sharp-frames",
            str(video_path),
            str(self.output_dir),
            "--selection-method", "batched",
            "--batch-size", str(batch_size),
            "--batch-buffer", str(batch_buffer),
            "--fps", str(fps)
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            extracted_count = len(list(self.output_dir.glob("*.jpg")))
            print(f"Extraction complete! Total frames saved: {extracted_count}")
            return extracted_count
        except Exception as e:
            print(f"Sharp-frames batched failed: {e}")
            return False

    # accepts temp folder since it works on images not video
    def outlier_remover_only(self):
        cmd = [
            "sharp-frames",
            str(self.temp_dir),        # input frames
            str(self.output_dir),      # output filtered frames
            "--selection-method", "outlier-removal",
            "--outlier-sensitivity", "70",
        ]
        try:
            subprocess.run(cmd, check=True, text=True)
            # Remove the temporary pre-filter folder
            shutil.rmtree(self.temp_dir)
            final_count = len(list(self.output_dir.glob("*.jpg")))
            print(f"Blur removal complete! {final_count} frames remain in {self.output_dir}")
            return final_count
        except subprocess.CalledProcessError as e:
            print(f"SharpFrames outlier-removal failed: {e}")
            return 0
        except FileNotFoundError:
            print("SharpFrames CLI not found. Install it and ensure it's in PATH.")
            return 0
        except Exception as e:
            print(f"Outlier-removal pipeline failed: {e}")
            return 0




