import os
import key
from langchain_community.chat_models import ChatOpenAI

import tools_SceneDetector as T_sceneDet
import tools_SpeechRecognitor as T_speechRec
import tools_OCRandTextCombineder as T_OCR
import tools_PromptGenerator as T_promptGen
import Model 

os.environ["OPENAI_API_KEY"] = key.API_KEY
llm=ChatOpenAI()

# Step 1: Scene Detection

# Step 2: Split Video into Multiple Clips

# Step 3: Speech Recognition using whisper

# Step 4: Generate Clip-Level Video Descriptions

# Step 6: Generate a Persona using GPT-4

# Example usage
if __name__ == "__main__":
    video_path = 'Video\\Lecture 16.4 — The fog of progress — [ Deep Learning _ Geoffrey Hinton _ UofT ].mp4'
    output_dir = 'clips/'
    json_path = 'Text_output\\json_transcript'
    prompt_path = 'Text_output\\promt'

    test=True
    # Step 1: Scene Detection
    scenes = T_sceneDet.scene_detection(video_path)
    # print("Detected scenes:", scenes)

    # Step 2: Split Video into Multiple Clips
    clip_paths = T_sceneDet.split_video(video_path, scenes, output_dir)

    # Step 3: Speech Recognition using Whisper-Timestamped
    # transcript = T_speechRec.speech_recognition(video_path, json_path)

    # Skip step 3
    transcript = T_speechRec.skip_speech_recognition(json_path)

    # Step 4: Generate Clip Descriptions
    clip_descriptions = T_OCR.clip_ocr(output_dir, transcript ,scenes)

    print("Clip Descriptions:", clip_descriptions)
    # write_txt(clip_descriptions,"clip_descriptions")
    
    # Step 6: Create Persona
    T_promptGen.generate_Persona_txt(clip_descriptions,prompt_path)
    # Step 7: Chat
    Model.main("Text_output")
    # clear clips
    T_sceneDet.clear_dir(output_dir)
