import os
import shutil
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.messages import HumanMessage, SystemMessage
import streamlit as st
import key
from tools_PromptGenerator import write_txt
import json
from datetime import datetime,timedelta,time
import re

os.environ["OPENAI_API_KEY"] = key.API_KEY

# DATA_PATH = "Text_output"
CHROMA_PATH = "chroma"

# Load all documents(.txt) from folder(DATA_PATH)
def load_documents(DATA_PATH) :
    loader = DirectoryLoader(DATA_PATH, glob = "*.txt", loader_cls=TextLoader)
    documents = loader.load()
    return documents

# Split all of documents to small chunks of text
def split_text(DATA_PATH) :
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False,
        add_start_index = True
       )
    chunks = text_splitter.split_documents(load_documents(DATA_PATH))
    return chunks

# Clear out the database
def clear_database() :
    try :
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
            print("cleared databased")
    except:
        print("Can not remove databased")


# Save all chunks to vector database
def save_to_database(DATA_PATH) :

    clear_database()
    
    # get chunks of documents
    chunks = split_text(DATA_PATH)
    # print(chunks)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )

    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

template = """"
context :

{context}

---

Answer the question based on the above context and give the timestamp and scence number: {question}
"""

def send_query(query) :
    # Prepare the DB.
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=OpenAIEmbeddings())

    # Find similar k chunks for create context 
    results = db.similarity_search_with_relevance_scores(query, k=5)

    # Format context
    context = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    # print(context)
    # print()

    # Create promt
    prompt_template = PromptTemplate.from_template(template)
    prompt = prompt_template.format(context=context, question=query)
    # prompt = query
    # print(prompt)

    #Send prompt to llm
    model = ChatOpenAI(
        # model="gpt-4-turbo",
    )

    #Prepare persona

    persona = "You are a helpful assistant! Your name is Bob."

    messages = [
    SystemMessage(
        content= persona
    ),
    HumanMessage(
        content= prompt
    )
    ]

    response_text = model.invoke(messages)
    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"{response_text.content}\nSources: {sources}"

    return formatted_response

def app():

    # Setup app title
    st.title("Chat")

    # Build a prompt input template to display the prompts
    query = st.chat_input("Pass Your Prompt here")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # If the user hits enter then
    if query :
        #Display the prompt
        st.chat_message("user").markdown(query)

        #Store the user prompt in state 
        st.session_state.messages.append({"role":"user","content":query})

        #Send the prompt to the model
        response = send_query(query)
    
        #Display the response
        st.chat_message("assistant").markdown(response)

        #Store the model response in state
        st.session_state.messages.append({"role":"assistant","content":response})

def main(DATA_PATH) :
    #create database
    save_to_database(DATA_PATH)

    # while True :
    #     query = input("\nEnter your query (type 'exit' to quit): ")
    #     if query.lower() == "exit":
    #         print("Exiting the program.")
    #         break
        
    #     print(send_query(query))
    file_path = "QA_2min_csv.json"  # Replace with your file path
    queries = read_queries_from_file(file_path,'Question')
    log=''
    eva=''

    start_time=list(read_queries_from_file('QA_2min_csv.json','TimeStart'))
    end_time=list(read_queries_from_file('QA_2min_csv.json','TimeEnd'))
    i=0
    for query in queries:
        ans=send_query(query)
        log+=query+'\n'+ans+'\n'
        print("Question",(i+1))
        print(query)
        print(ans)
        try:
            timestamp_pattern = r'\d{1,2}:\d{2}:\d{2}(?:\.\d{3})?\s*(?:-|to)\s*\d{1,2}:\d{2}:\d{2}(?:\.\d{3})?|\d{1,2}:\d{2}:\d{2}(?:\.\d{3})?|\d{1,2}:\d{2}\s*(?:-|to)\s*\d{1,2}:\d{2}'
            timestamps = re.findall(timestamp_pattern, ans)
            time_range=timestamps[0].split(' ')
            ans_start_time = convert_to_datetime(time_range[0])
            ans_end_time = convert_to_datetime(time_range[2])
            gt_start_time = convert_to_datetime(start_time[i])
            gt_end_time = convert_to_datetime(end_time[i])
            
            start_max = max(ans_start_time, gt_start_time)
            end_min = min(ans_end_time, gt_end_time)
            start_min = min(ans_start_time, gt_start_time)
            end_max = max(ans_end_time, gt_end_time)

            intersec_time=abs(time_to_seconds(start_max)-time_to_seconds(end_min))
            union_time=abs(time_to_seconds(start_min)-time_to_seconds(end_max))
            print("Intersection Over Union: ",intersec_time/union_time)

            print("Precision",intersec_time/abs(time_to_seconds(ans_start_time)-time_to_seconds(ans_end_time)))

            print("Startdif: ",calculate_time_gap(gt_start_time,ans_start_time))
            eva += (
            "Question " + str(i + 1) +'\n' + 
            'Ground truth time: '+start_time[i]+'-'+end_time[i]+'\n'+
            'Anwser time: '+time_range[0]+'-'+time_range[2]+'\n'+
            "Intersection Over Union: " + str(intersec_time / union_time) + '\n' +
            "Precision: " + str(intersec_time / abs(time_to_seconds(ans_start_time) - time_to_seconds(ans_end_time))) + '\n' +
            "Start Difference: " + str(calculate_time_gap(gt_start_time, ans_start_time)) + '\n'+'\n'
            )
        except IndexError:
            print("No time stamp provide in the Anwser")
        i+=1
    write_txt(log,'Ans')
    write_txt(eva,'Evaluation') 
def calculate_time_gap(start_time, end_time):
    # Convert time objects to datetime objects on the same arbitrary date
    datetime_start = datetime.combine(datetime.min, start_time)
    datetime_end = datetime.combine(datetime.min, end_time)
    
    # Calculate the difference
    if datetime_end < datetime_start:
         return datetime_start - datetime_end
    else:
        return datetime_end - datetime_start

def read_queries_from_file(file_path,str):
    f = open(file_path)
    data = json.load(f)
    return (data[str].values())

def time_to_seconds(t):
    # Calculate total seconds since midnight
    return t.hour * 3600 + t.minute * 60 + t.second

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



