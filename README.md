"""
# Frames Extractor
Handles extracting frames from video files and filtering them for sharpness.
Methods:

**1. extract_frames_from_video**
    - Extracts frames from a video at a specified target FPS using OpenCV.
    - Parameters:
        - video_path: path to the input video file.
        - target_fps: desired frames per second to extract (default: 7).
    - Outputs:
        - Saves extracted frames as JPEG images in the 'images/' folder.
        - Returns count of extracted frames or False if failed.

**2. extract_frames_outlier_removal**
    - Extracts frames from a video at target FPS, temporarily saves them, then filters out blurry frames using the 'sharp-frames' CLI tool with outlier removal method.
    - Parameters:
        - video_path: video file path.
        - target_fps: target FPS for extraction (default: 10).
    - Outputs:
        - Saves filtered sharp frames in 'images/' folder.
        - Cleans up temporary folder.
        - Returns count of final frames or False if process fails.

**3. sharp_frames_best_n**
    - Uses 'sharp-frames' CLI tool to extract the best N sharp frames from a video at specified FPS.
    - Parameters:
        - video_path: input video file.
        - target_fps: FPS setting (default: 10).
        - num_frames: desired number of sharp frames to extract.
    - Outputs:
        - Saves selected frames to 'images/' folder.
        - Returns count of saved frames or False on failure.

**4. sharp_frames_batched**
    	- Extracts sharp frames in batches from the video using the 'sharp-frames' batched selection method.
    	- Parameters:
    	    - video_path: input video path.
    	    - batch_size: number of frames per batch (default: 4).
    	    - batch_buffer: extra frames buffer per batch (default: 0).
    	    - fps: original video FPS (default: 30).
    	- Outputs:
    	    - Saves selected frames to 'images/' folder.
    	    - Returns final saved frame count or False on failure.

**5. outlier_remover_only**
    - Runs sharp-frames outlier removal on an existing temporary folder of frames, filtering blurry frames.
    - Inputs:
        - Uses the `temp_dir` folder as source frames.
    - Outputs:
        - Saves filtered frames to 'images/' folder.
        - Removes temporary folder.
        - Returns count of sharp frames or 0 if failed.


**Notes:**  
- All frame extraction methods save output into the 'images/' subfolder under the given project root.
- The class depends on the external 'sharp-frames' CLI tool for sharpness-based frame filtering.
- Handles errors gracefully, returning counts or False/0 on failure.
- The class mainly uses OpenCV for initial frame extraction, with subsequent CLI-based filtering steps.





# Colmap Pipeline Commands
Automates key COLMAP steps to create a sparse 3D reconstruction from images.
Steps:

**1. Feature Extraction**
    - Extracts visual features (keypoints and descriptors) from input images.
    - Parameters:
        - database_path: path to COLMAP database file (stores extracted features)
        - image_path: directory containing images to process
        - camera_model (default: "OPENCV"): intrinsic camera model to assume
        - single_camera (default: True): treats all images as from the same camera
    - Output: updates the database with extracted features

**2. Feature Matching**
    - Matches features between sequential image pairs based on descriptors.
    - Parameters:
        - database_path: path to COLMAP database file containing extracted features
    - Output: database updated with matched feature pairs

**3. Sparse Reconstruction**
    - Triangulates matched features to recover camera poses and sparse 3D points.
    - Parameters:
       - database_path: COLMAP database with matches and features
       - image_path: input images directory
       - output_path: directory to save sparse reconstruction files
    - Output: creates sparse reconstruction files including cameras.bin, images.bin, points3D.bin in output_path

**Notes:**  
- Sparse reconstruction folder is auto-created if not present.
- Each step runs COLMAP as a subprocess and handles errors gracefully.
- This class covers the core sparse pipeline; dense reconstruction and meshing is next using OpenMVS.


# For OpenMvs to accepts colmap , Ensure the images are undistorted (PINHOLE)

# OpenMVS Pipeline Commands README

1. **InterfaceCOLMAP**  
   - Converts COLMAP sparse reconstruction data (cameras, images, points3D) into an OpenMVS `.mvs` project file.  
   - Parameters:  
      - `--input-file`: Path to COLMAP sparse folder (containing cameras.bin, images.bin, points3D.bin)  
      - `--output-file`: Path to save the generated `.mvs` file  
   - Output: `.mvs` file with sparse reconstruction ready for dense processing.

2. **DensifyPointCloud**  
   - Computes dense 3D point cloud by estimating depth maps from images using multi-view stereo.  
   - Parameters:  
      - `--input-file`: `.mvs` project file from InterfaceCOLMAP  
      - `--output-file`: Path to save updated `.mvs` file with dense point cloud  
   - Output: `.mvs` file containing dense, colorized point cloud.

3. **ReconstructMesh**  
   - Generates a polygonal mesh by triangulating the dense point cloud points.  
   - Parameters:  
      - `--input-file`: `.mvs` file with dense point cloud  
      - `--output-file`: Path to save mesh `.mvs` file  
   - Output: `.mvs` file containing reconstructed 3D mesh geometry.

4. **RefineMesh**  
   - Smooths and improves the mesh by reducing noise and artifacts for better surface quality.  
   - Parameters:  
      - `--input-file`: Mesh `.mvs` file from ReconstructMesh  
      - `--output-file`: Path to save refined `.mvs` mesh  
   - Output: Refined `.mvs` mesh file with improved quality.

5. **TextureMesh**  
   - Projects image textures onto the refined mesh, creating a photorealistic textured 3D model.  
   - Parameters:  
      - `--input-file`: Refined mesh `.mvs` file  
      - `--output-file`: Save path for textured `.mvs` model  
   - Output: Textured `.mvs` file ready for visualization or export.


**Notes:**  
- Each step processes the output of the previous command, building progressively from sparse points to a textured 3D mesh.  
- All outputs are stored as `.mvs` project files for easy pipeline compatibility.  
- This pipeline forms the core OpenMVS reconstruction workflow from COLMAP data for high-quality 3D model generation.

"""
