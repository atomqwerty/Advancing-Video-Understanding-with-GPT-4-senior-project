
# Advancing-Video-Understanding-with-GPT-4

an AI-powered chatbot that leverages Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs) to provide an intelligent question-answering system based on video lectures.


## Acknowledgements

 - This senior project could not have been completed without the support and guidance of several individuals. We would like to express our sincere gratitude to Asst. Prof. Dr. Tipajin Thaipisutikul, our advisor, for her close supervision, valuable suggestions, and strategic planning throughout the course of the project. Her support, including financial contributions, played a crucial role in the successful execution of this work.

 - We would also like to extend our heartfelt thanks to Asst. Prof. Dr. Thanapon Noraset, our co-advisor, for his guidance in establishing the project timeline, providing regular and constructive evaluations, and supporting the technical aspects of the development, particularly the provision of AI-related APIs and the server infrastructure used in building our chatbot.

 - Additionally, we would like to express our sincere appreciation to Prof. Ying Nong Chen for his generous support during our summer internship in Taiwan. His assistance with the accommodation rental process and his provision of a high-performance PC greatly facilitated our work and allowed us to continue developing the project seamlessly during our time abroad.



## Requirement
- Google Cloud Vision Api key
- Open AI Api key
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

