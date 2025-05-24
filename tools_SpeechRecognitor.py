import whisper_timestamped as whisper
import json

def dump_json(name, content):
    with open(name+".json", "w" ) as outfile:
        # outfile.write( json.dumps(result, indent = 2, ensure_ascii = False))
        json.dump(content, outfile)

    
def speech_recognition(video_path,file_name):
    try:
        model = whisper.load_model("tiny", device="cpu")
        result = model.transcribe(video_path,language="en")
        
        # save json file
        dump_json(file_name, result)

        return result
    
    except Exception as e:
        print(f"Error during ASR: {e}")
        return "No transcription."
def skip_speech_recognition(jsonName):
    file = open(jsonName+'.json')
    result = json.load(file)
    return result