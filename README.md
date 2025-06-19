# Advancing-Video-Understanding-with-GPT-4

an AI-powered chatbot that leverages Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs) to provide an intelligent question-answering system based on video lectures.


## Acknowledgements

 - This senior project could not have been completed without the support and guidance of several individuals. We would like to express our sincere gratitude to Asst. Prof. Dr. Tipajin Thaipisutikul, our advisor, for her close supervision, valuable suggestions, and strategic planning throughout the course of the project. Her support, including financial contributions, played a crucial role in the successful execution of this work.

 - We would also like to extend our heartfelt thanks to Asst. Prof. Dr. Thanapon Noraset, our co-advisor, for his guidance in establishing the project timeline, providing regular and constructive evaluations, and supporting the technical aspects of the development, particularly the provision of AI-related APIs and the server infrastructure used in building our chatbot.

 - Additionally, we would like to express our sincere appreciation to Prof. Ying Nong Chen for his generous support during our summer internship in Taiwan. His assistance with the accommodation rental process and his provision of a high-performance PC greatly facilitated our work and allowed us to continue developing the project seamlessly during our time abroad.



## Requirement
- Google Cloud Vision Api key
- Open AI Api key
- Flowise
## Installation
To get projects, follow these steps:
```bash
git clone https://github.com/atomqwerty/Advancing-Video-Understanding-with-GPT-4-senior-project.git
cd Advancing-Video-Understanding-with-GPT-4-senior-project
```
Install requirement with pip

```bash
pip install -r requirements.txt
```
    
## Run Locally

Clone the project

```bash
  git clone https://github.com/atomqwerty/Advancing-Video-Understanding-with-GPT-4-senior-project.git
```

Go to the project directory

```bash
  cd Advancing-Video-Understanding-with-GPT-4-senior-project
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Put the File Path in main.py 

-Video
```bash
  video_path = 'Video/Neural Networks for Machine Learning/Lecture 1.1.mp4'
```
-Output video clips
```bash
  output_dir = 'clips/'
```
-Output Json File
```bash
  json_path = 'Text_output\\json_transcript'
```
-Output Prompt File
```bash
  prompt_path = 'Text_output'
```
Run using python
```bash
Advancing-Video-Understanding-with-GPT-4-senior-project/main.py 
```
After this, put all the  prompt files in your local Learning Machine In this case, weare are using Flowise
![image](https://github.com/user-attachments/assets/6d60ba6b-a3c8-4af6-ba39-9841b0e5a3ac)
Then, after we upsert Promt file, we can start chatting with our chatbot
![image](https://github.com/user-attachments/assets/1c248a19-2c3f-4742-8287-f7a9e31e84c6)
## Running Evaluate

To run Evaluate, put your flowise api in eva.py
```bash
API_URL = "http://flowise.com/api/v1/prediction/xxxxxxx"
```
And prepare CSV Question and Anwser file in this format 
```bash
Number,Question,Answer,TimeStart,TimeEnd
```
- Example
```bash
1,Why do we need machine learning?,"We need machine learning because there are problems for which it is very difficult to write programs. For example, recognizing a three-dimensional object from a novel viewpoint in new lighting conditions in a cluttered scene is very challenging to program manually. Even if we could write such a program, it might be horrendously complicated. Machine learning allows us to create models that can handle these tasks by learning from examples.",0:00:10,0:00:38
```
Put the CSV Path in eva.py
```bash
csvpath='QA_20-2.csv'
```
Then run the following command

```bash
Advancing-Video-Understanding-with-GPT-4-senior-project/eva.py
```
The evaluation will came out in Evaluation.txt
- Example
  ```bash
  Question 1
  Ground truth time: 0:00:00-0:00:13
  Anwser time: 00:00:00.000-00:00:13.533
  Intersection Over Union: 1.0
  Precision: 1.0
  Start Difference: 0:00:00
  Question 2
  Ground truth time: 0:00:19-0:01:24
  Anwser time: 0:00:19-0:00:27
  Intersection Over Union: 0.12307692307692308
  Precision: 1.0
  Start Difference: 0:00:00
  Question 3
  Ground truth time: 0:00:13-0:01:27
  Anwser time: 0:00:32-0:00:37
  Intersection Over Union: 0.06756756756756757
  Precision: 1.0
  Start Difference: 0:00:19

