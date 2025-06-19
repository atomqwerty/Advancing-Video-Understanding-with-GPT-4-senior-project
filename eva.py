import json
import requests
import csv
import re
import os
import pandas as pd
from datetime import datetime, timedelta, time
from bert_score import score
from deepeval.metrics import FaithfulnessMetric
from deepeval.test_case import LLMTestCase
API_URL = "http://flowise.northanapon.com/api/v1/prediction/xxxxxxxx-xxxx-xxxx-xxxxxxxxxxxx"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Load API key securely

csvpath='QA_20-2.csv'

def deep_eval(question, response,rag):
    test_case=LLMTestCase(
    input=question, 
    actual_output=response,
    retrieval_context=rag
    )
    metric = FaithfulnessMetric(threshold=0.5)

    metric.measure(test_case)
    print(metric.score)
    print(metric.reason)
    print(metric.is_successful())
    return metric.score

def convert_to_datetime(timestamp):
    formats = ['%H:%M:%S.%f', '%H:%M:%S', '%H:%M']
    for fmt in formats:
        try:
            return datetime.strptime(timestamp, fmt).time()
        except ValueError:
            continue
    raise ValueError(f"Timestamp format not recognized: {timestamp}")

def calculate_time_gap(start_time, end_time):
    datetime_start = datetime.combine(datetime.min, start_time)
    datetime_end = datetime.combine(datetime.min, end_time)
    return abs(datetime_start - datetime_end)

def time_to_seconds(t):
    return t.hour * 3600 + t.minute * 60 + t.second

def query(payload):
    response = requests.post(API_URL, json=payload)
    if response.status_code == 200:
        response_data = response.json()
        # Extract the generated text
        generated_text = response_data.get("text", "")
        # Extract the retrieved context, assuming it is part of the response
        retrieved_context = response_data.get("sourceDocuments", [])
        retrieved_context = [item["pageContent"] for item in retrieved_context]
        return generated_text, retrieved_context
    else:
        print("Error:", response.status_code, response.text)
        return ""

# Read the CSV file
with open(csvpath, 'r') as file:
    next(file)  # Skip header
    csv_reader = csv.reader(file)
    eva = "Number,ground truth time,Answer,Answer time,IOU,Precision,Start Difference,BERT Precision,BERT Recall,BERT F1,DeepEval Faithfulness Score\n"
    
    refs = []
    hyps = []
    i = 0

    for row in csv_reader:
        question = row[1]
        ground_truth_start = row[3]
        ground_truth_end = row[4]

        # Get the response from the API
        output,retrieved_context = query({"question": question})
        with open("output.json", "w") as f:  # Open file in write mode
            json.dump(retrieved_context, f)  # Convert dict to JSON and write
        # Clean the response text
        refs.append(row[2])
        cleaned_text = re.sub(r"\*\*Timestamp:\*\* \d{2}:\d{2}:\d{2} - \d{2}:\d{2}:\d{2}\n?", "", output)
        cleaned_text = re.sub(r"\*\*Scene:\*\* \d+\n?", "", cleaned_text)
        hyps.append(cleaned_text)

        # Extract timestamps
        timestamp_pattern = r"(\d{1,2}:\d{2}:\d{2}(?:\.\d{3})?)\s*(?:-|to)\s*(\d{1,2}:\d{2}:\d{2}(?:\.\d{3})?)"
        timestamps = re.findall(timestamp_pattern, output)
        escaped_output = output.replace('"', '""')
        eva += f'{i + 1},{ground_truth_start}-{ground_truth_end},"{escaped_output}",'

        if timestamps:
            try:
                ans_start_time = convert_to_datetime(timestamps[0][0])
                ans_end_time = convert_to_datetime(timestamps[0][1])
                gt_start_time = convert_to_datetime(ground_truth_start)
                gt_end_time = convert_to_datetime(ground_truth_end)

                start_max = max(ans_start_time, gt_start_time)
                end_min = min(ans_end_time, gt_end_time)
                start_min = min(ans_start_time, gt_start_time)
                end_max = max(ans_end_time, gt_end_time)

                intersec_time = max(time_to_seconds(end_min) - time_to_seconds(start_max), 0)
                union_time = abs(time_to_seconds(end_max) - time_to_seconds(start_min))
                iou = intersec_time / union_time if union_time else 0

                answer_duration = abs(time_to_seconds(ans_start_time) - time_to_seconds(ans_end_time))
                precision = intersec_time / answer_duration if answer_duration else 0

                start_difference = calculate_time_gap(gt_start_time, ans_start_time)

                print(f"Question {i + 1}: {question}\n")
                # print(f"Answer:{output}\n")
                # print(f"Rag:{retrieved_context}\n")
                # print(f"Intersection Over Union: {iou}")
                # print(f"Precision: {precision}")
                # print(f"Start Difference: {start_difference}\n")

                eva += f"{ans_start_time}-{ans_end_time},{iou},{precision},{start_difference}"
            except Exception as e:
                print(f"Error processing question {i + 1}: {e}")
                eva += "0,0,0"
        else:
            print("No timestamp provided in the answer")
            eva += "0,0,0"

        # Compute BERTScore
        P, R, F1 = score(hyps, refs, lang="en", verbose=True)
        eva += f",{P.mean().item()},{R.mean().item()},{F1.mean().item()}"

        # Compute DeepEval Score
        deep_eval_score = deep_eval(row[1], cleaned_text,retrieved_context)
        eva += f",{deep_eval_score}\n"  # Fixed incorrect formatting

        i += 1

# Save evaluation results
with open("evaluation_results.csv", "w") as eval_file:
    eval_file.write(eva)
