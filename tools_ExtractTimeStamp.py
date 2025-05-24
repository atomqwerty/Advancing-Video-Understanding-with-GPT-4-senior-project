from datetime import datetime
import json
import re

def read_queries_from_file(file_path,str):
    f = open(file_path)
    data = json.load(f)
    return (data[str].values())

def extract_timestamps(file_path):
    # Define the regular expression pattern for timestamps
    timestamp_pattern = r'\d{1,2}:\d{2}:\d{2}(?:\.\d{3})?\s*(?:-|to)\s*\d{1,2}:\d{2}:\d{2}(?:\.\d{3})?|\d{1,2}:\d{2}:\d{2}(?:\.\d{3})?|\d{1,2}:\d{2}\s*(?:-|to)\s*\d{1,2}:\d{2}'
    
    with open(file_path, 'r') as file:
        text = file.read()
    
    # Use regular expression to find all timestamps
    timestamps = re.findall(timestamp_pattern, text)
    
    return timestamps

def convert_to_datetime(timestamp):
    # Define possible datetime formats
    formats = ['%H:%M:%S.%f', '%H:%M:%S', '%H:%M']
    
    # Try each format to convert the timestamp
    for fmt in formats:
        try:
            return datetime.strptime(timestamp, fmt).time()
        except ValueError:
            continue
    
    raise ValueError(f"Timestamp format not recognized: {timestamp}")


file_path = 'Ans.txt'  # Replace with the path to your text file
timestamps = extract_timestamps(file_path)

# Print the extracted timestamps
start_time=list(read_queries_from_file('QA_2min_csv.json','TimeStart'))
end_time=list(read_queries_from_file('QA_2min_csv.json','TimeEnd'))
print(start_time)

for i in range (len(timestamps)):
    print(i)
    time_range=timestamps[i].split(' ')
    ansstart_time = convert_to_datetime(time_range[0])
    # gtstart_time = convert_to_datetime(start_time[i])
    
    ansend_time = convert_to_datetime(time_range[2])
    print(ansstart_time,' ')
    
