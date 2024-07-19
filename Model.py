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

    while True :
        query = input("\nEnter your query (type 'exit' to quit): ")
        if query.lower() == "exit":
            print("Exiting the program.")
            break
        
        print(send_query(query))

