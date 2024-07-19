from scenedetect import VideoManager, SceneManager #
from scenedetect.detectors import ContentDetector

import os
import glob

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

#create all items in the dir
def create_dir_ifnotexist(name):
    os.makedirs(name, exist_ok=True)

#clear all items in the dir
def clear_dir(name):
    for f in glob.glob(name+'/*'):
        os.remove(f)

def scene_detection(video_path,threshold=7.0):
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))
    video_manager.set_downscale_factor()
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)
    scene_list = scene_manager.get_scene_list()
    video_manager.release()
    return scene_list

# T_sceneDet : scene_detection

def split_video(video_path, scene_list, output_dir):

    clip_paths = []

    create_dir_ifnotexist(output_dir)
    clear_dir(output_dir)

    # saving the output
    for i, scene in enumerate(scene_list):
        start, end = scene[0].get_seconds(), scene[1].get_seconds()
        clip_path = os.path.join(output_dir, f"clip_{i+1}.mp4")
        ffmpeg_extract_subclip(video_path, start, end, targetname=clip_path)
        clip_paths.append(clip_path)

    return clip_paths
