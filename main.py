import os
import key

import tools_SceneDetector as T_sceneDet
import tools_SpeechRecognitor as T_speechRec
import tools_OCRandTextCombineder as T_OCR
# Step 1: Scene Detection

# Step 2: Split Video into Multiple Clips

# Step 3: Speech Recognition using whisper

# Step 4: Generate Clip-Level Video Descriptions

# Example usage
if __name__ == "__main__":
    video_path = 'Video/Neural Networks for Machine Learning/Lecture 1.1.mp4'
    output_dir = 'clips/'
    json_path = 'Text_output\\json_transcript'
    prompt_path = 'Text_output'

    test=False
    # Step 1: Scene Detection
    scenes = T_sceneDet.scene_detection(video_path)
    print("Detected scenes:", scenes)

    # Step 2: Split Video into Multiple Clips
    clip_paths = T_sceneDet.split_video(video_path, scenes, output_dir)

    # Step 3: Speech Recognition using Whisper-Timestamped
    transcript = T_speechRec.speech_recognition(video_path, json_path)

#=======================adjustable======================
    # Step 4: Generate Clip Descriptions google
    clip_descriptions = T_OCR.clip_ocr_google(output_dir, transcript ,scenes,video_path.split('/'),prompt_path)
#=======================================================
    
