import datetime
import os
import cv2
import pytesseract
import json
import time

#/ setting
#/ snapped time between scene                                 
snapping = 5                                     
def write_txt(str,name):
    with open(name+'.txt', 'w',encoding="utf-8") as f:
        f.write(str) 

def frame_extracter(video):

    frames = video.get(cv2.CAP_PROP_FRAME_COUNT) 
    fps = video.get(cv2.CAP_PROP_FPS) 
    seconds = int(frames / fps) - snapping              #/ for ending, -5 snapping scene 
    
    frame_id = int(fps*(seconds))

    video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
    ret, frame = video.read()

    return frame

# =============google part=================

from google.cloud import vision
import os 

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"rag-for-video-lectures-5da7f3f48b27.json"

def detect_text_from_memory(image):
    """Detects text in an image loaded into memory using Google Vision API."""
    # Initialize the Vision API client
    client = vision.ImageAnnotatorClient()

    # Convert the numpy array (image) to bytes
    _, encoded_image = cv2.imencode('.jpg', image)
    content = encoded_image.tobytes()

    # Create an Image object
    image = vision.Image(content=content)

    # Perform text detection
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # Collect detected text (first element contains all text)
    detected_text = texts[0].description if texts else ''
    
    # Handle errors
    if response.error.message:
        raise Exception(f"API Error: {response.error.message}")

    return detected_text

# ====================adjustable===================

def cap_last_sec_tes(frame):
    # Convert image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply threshold to convert to binary image
    threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # Pass the image through pytesseract or google
    # ===========tesseract============
    text = pytesseract.image_to_string(threshold_img)
    # ===========google============
    # text = detect_text(threshold_img)
    # Print the extracted text
    return text

def cap_last_sec_google(frame):
    # Convert image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply threshold to convert to binary image
    threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # Pass the image through pytesseract or google
    # ===========tesseract============
    # text = pytesseract.image_to_string(threshold_img)
    # ===========google============
    text = detect_text_from_memory(threshold_img)
    # Print the extracted text
    return text

# ====================final===================

def clip_ocr_tes(dir,result,scene_time_stamp,video_path,prompt_path):
    seconds = time.time()
    output = ''
    i=0
    # print(dir)

    sentence = result["segments"]
    files = os.listdir(dir)
    files_sorted = sorted(files, key=lambda x: int(x.split("_")[1].split(".")[0]))
    for name in (files_sorted):
    # Open file
        n=0
        transcript=''
        with open(os.path.join(dir, name)) as f:
            video_crr = cv2.VideoCapture(dir+name)
            frame = frame_extracter(video_crr)
            content = cap_last_sec_tes(frame)

            str_crr = f"Scene: {i+1} " +f"timestamp: {scene_time_stamp[i][0]} - {scene_time_stamp[i][1]} "+'\n' + content + '\n'
            for j in sentence :
                n+=1
                timestamp_start =j["start"]
                timestamp_end =j["end"]
                audio_log = j["text"]
                if timestamp_start>= scene_time_stamp[i][0].get_seconds():
                    transcript+=f"<utterance number= {n} start="+str(datetime.timedelta(seconds=timestamp_start))+' end= '+str(datetime.timedelta(seconds=timestamp_end))+"\n"+audio_log+"\n"
                if timestamp_end>= scene_time_stamp[i][1].get_seconds():
                    break
            str_crr+=f'<utterances>\n {transcript}\n</utterance>\n</scene>\n</lecture>\n</course>'
            write_txt(str_crr,f'{prompt_path}/{video_path[2]}-sc{i+1}')
            output = output + str_crr
        i+=1
    # write_txt(output,"test_script")
    return output

def clip_ocr_google(dir,result,scene_time_stamp,video_path,prompt_path):
    seconds = time.time()
    output = ''
    i=0

    sentence = result["segments"]
    
    files = os.listdir(dir)
    files_sorted = sorted(files, key=lambda x: int(x.split("_")[1].split(".")[0]))
    for name in files_sorted:
        print(name)
    # Open file
        n=0
        transcript=''
        with open(os.path.join(dir, name)) as f:
            video_crr = cv2.VideoCapture(dir+name)
            frame = frame_extracter(video_crr)
            content = cap_last_sec_google(frame)

            str_crr = f"<scene: {i+1} " +f"timestamp: {scene_time_stamp[i][0]} - {scene_time_stamp[i][1]}> "+'\n' + content + '\n'
            for j in sentence :
                n+=1
                timestamp_start =j["start"]
                timestamp_end =j["end"]
                audio_log = j["text"]
                if timestamp_start>= scene_time_stamp[i][0].get_seconds():
                    transcript+=f"<utterance number= {n} start="+str(datetime.timedelta(seconds=timestamp_start))+' end= '+str(datetime.timedelta(seconds=timestamp_end))+"\n"+audio_log+"\n"
                if timestamp_end>= scene_time_stamp[i][1].get_seconds():
                    break
            str_crr+=f'<utterances>\n {transcript}\n</utterance>\n</scene>\n</lecture>\n</course>'
            write_txt(str_crr,f'{prompt_path}/{video_path[2]}-sc{i+1}')
            output = output + str_crr
        i+=1
    # write_txt(output,"test_script")
    return output
