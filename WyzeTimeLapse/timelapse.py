import os
import subprocess
import cv2
import re
from tqdm import tqdm  # Progress bar library

def natural_sort_key(path):
    """ Sorts strings numerically when possible (e.g., '20250312/01/video.mp4' comes before '20250312/02/video.mp4'). """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', path)]

def find_videos(root_folder, extensions=(".mp4", ".avi", ".mov")):
    """ Recursively find all video files in subdirectories, sorted chronologically. """
    video_files = []
    for dirpath, _, filenames in os.walk(root_folder):
        for file in filenames:
            if file.lower().endswith(extensions):
                video_files.append(os.path.join(dirpath, file))
    
    # Sort files in chronological order
    video_files.sort(key=natural_sort_key)
    return video_files

def extract_frames_from_videos(video_files, output_folder, interval=30):
    """ Extract frames every `interval` seconds from all videos with progress bar. """
    os.makedirs(output_folder, exist_ok=True)
    frame_count = 0
    total_videos = len(video_files)

    for video_idx, video in enumerate(tqdm(video_files, desc="Processing Videos", unit="video")):
        cap = cv2.VideoCapture(video)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if not fps or fps <= 0:
            print(f"Skipping {video} (Invalid FPS)")
            continue
        
        frame_interval = int(fps * interval)  # Convert seconds to frame count
        frame_num = 0

        with tqdm(total=total_frames, desc=f"Extracting Frames ({video_idx+1}/{total_videos})", unit="frame", leave=False) as pbar:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                if frame_num % frame_interval == 0:
                    frame_path = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
                    cv2.imwrite(frame_path, frame)
                    frame_count += 1
                frame_num += 1
                pbar.update(1)

        cap.release()

def create_timelapse_from_frames(frame_folder, output_video, fps=30):
    """ Combine extracted frames into a timelapse video at `fps` FPS with progress bar. """
    ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"  # Update this path
    frame_count = len([f for f in os.listdir(frame_folder) if f.endswith(".jpg")])

    with tqdm(total=frame_count, desc="Creating Timelapse", unit="frame") as pbar:
        subprocess.run([
            ffmpeg_path, "-framerate", str(fps), 
            "-i", f"{frame_folder}/frame_%04d.jpg", 
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            output_video
        ], check=True)
        pbar.update(frame_count)

# Paths
wyze_root_folder = r"C:\Users\jakes\Desktop\Test"  # Update with your root directory
output_frames = "ExtractedFrames"
output_timelapse = "timelapse.mp4"

# Process
video_list = find_videos(wyze_root_folder)
extract_frames_from_videos(video_list, output_frames, interval=30)
create_timelapse_from_frames(output_frames, output_timelapse)

print("Timelapse video created successfully.")