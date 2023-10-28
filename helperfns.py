import io
import streamlit as st
from streamlit_chat import message
import docx
import os
import sys
import base64
import atexit
import pinecone
import urllib

from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

from video2txt import video_to_text

from constants import openai_key,pinecone_environment,pinecone_api_key,pinecone_index
print(openai_key)

def prompt_form(self):
    """
    Displays the prompt form
    """
    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_area(
            "Query:",
            placeholder="Ask me anything about the document...",
            key="input",
            label_visibility="collapsed",
        )
        submit_button = st.form_submit_button(label="Send")
        
        is_ready = submit_button and user_input
    return is_ready, user_input

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

def initialize():
    if "assistant" not in st.session_state:
        st.session_state["assistant"] = "Hey, How can I Help You !! 👋"
    if "user" not in st.session_state:
        st.session_state["user"] = "Hello Mr.Bot !!"

def generate_messages(container):
    if st.session_state["chat_history"]:
        with container:
            for i in range(len(st.session_state["chat_history"])):
                message(
                    st.session_state["chat_history"][i],
                    is_user=True if i % 2 == 0 else False,
                    key=f"history_{i}_user",
                    #avatar_style="big-smile" if i % 2 == 0 else "thumbs",
                    avatar_style="initials" if i % 2 == 0 else "initials",
                    seed="H" if i % 2 == 0 else "AI",
                )

def load_docs(directory):
  loader = DirectoryLoader(directory)
  documents = loader.load()
  return documents

def split_docs(documents,chunk_size=250,chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs
 
def get_similiar_docs(query,index, k=2, score=False):
  print(index)
  if score:
    similar_docs = index.similarity_search_with_score(query, k=k)
  else:
    similar_docs = index.similarity_search(query, k=k)
  return similar_docs
 
def init_pinecone(docs, embeddings):
	pinecone.init(
		api_key=pinecone_api_key,
		environment=pinecone_environment
	)
	index_name = pinecone_index
	index = Pinecone.from_documents(docs, embeddings, index_name=index_name)
	return index

def save_embeddings():
	directory = 'temp_documents/'
	documents = load_docs(directory)
	#len(documents)
	#print(documents)
	#print(documents[0].page_content)
	txt_content = documents[0].page_content
	#print(txt_content)
	docs = split_docs(documents)
	print(len(docs))
	#print(docs[0].page_content)
    
    #embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
	embeddings = OpenAIEmbeddings(model_name="text-embedding-ada-002",openai_api_key=openai_key)
	print("I'm here after creating Embeddings")
    
    
	query_result = embeddings.embed_query("Hello world")
	len(query_result)
	return init_pinecone(docs, embeddings)

def get_answer(query,index,chain):
  similar_docs = get_similiar_docs(query,index)
  answer = chain.run(input_documents=similar_docs, question=query)
  return answer

def qa_chatbot(index):
    # Create a text box and a submit button
    st.subheader("Let's Chat....")
    # user_input = st.text_area("Please Ask Your Question")

    response_container, prompt_container = st.container(), st.container()

    # Initialize the chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

        # Add the initial greeting messages to the chat history
        st.session_state["chat_history"].append("Hello Mr.Bot !!")
        st.session_state["chat_history"].append("Hey, How can I Help You !! 👋")

    with prompt_container:
        # Display the prompt form
        with st.form(key="my_form", clear_on_submit=True):
            user_input = st.text_area(
                "Query:",
                placeholder="Ask me anything about the document...",
                key="input",
                label_visibility="collapsed",
            )
            submit_button = st.form_submit_button(label="Send")

            is_ready = submit_button and user_input

        # Generate the AI response
        if is_ready:
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()

            model_name = "gpt-3.5-turbo"
            llm = OpenAI(model_name=model_name,openai_api_key=openai_key)
            print("I'm inside qa_chatbot, Before initializing Chain")
            chain = load_qa_chain(llm, chain_type="stuff")
            print("I'm inside qa_chatbot, Before asking Question")
            #query = "Who is Virat Kohli?"
            query=user_input
            answer = get_answer(query,index,chain)
            print(answer)
            #output = "Output from AI"
            output = answer

            sys.stdout = old_stdout

            # Add the user input and AI output to the chat history
            st.session_state["chat_history"].append(user_input)
            st.session_state["chat_history"].append(output)

        # Display the chat history
    generate_messages(response_container)   

    #if st.button("Submit"):
    #document_content = document_parse_loader()
    #answer_fr_user = testcase_generator(document_content,user_input)
    #st.write(answer_fr_user)

def upload_docs_display(temp_folder_path):

    # Upload multiple documents
    uploaded_files = st.file_uploader("Upload documents (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"], accept_multiple_files=True)

    # Create a temp folder if it doesn't exist
    temp_folder = temp_folder_path #"temp_documents" "temp_videos"
    os.makedirs(temp_folder, exist_ok=True)

    # Create a list to keep track of temporary files
    temp_files = []

    # Count the number of successfully uploaded files
    num_uploaded_files = 0

    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Determine the file type and process accordingly
            file_extension = uploaded_file.name.split(".")[-1].lower()

            if file_extension == "pdf":
                num_uploaded_files += 1

            elif file_extension == "docx":
                num_uploaded_files += 1

            elif file_extension == "txt":
                num_uploaded_files += 1

            # Save the uploaded file to the temp folder
            temp_file_path = os.path.join(temp_folder, uploaded_file.name)
            temp_files.append(temp_file_path)

            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(uploaded_file.read())

    # Display the number of successfully uploaded files in the console
    if num_uploaded_files > 0:
        st.write(f"Successfully uploaded {num_uploaded_files} files")
        flag=1
    else:
        st.write("Waiting for Files to be Uploaded...")
        flag=0
    
    return flag,temp_files

def upload_video_display(temp_folder_path):
    # Upload multiple videos
    uploaded_videos = st.file_uploader("Upload video files (MP4, AVI, etc.)", type=["mp4", "avi", "mov"], accept_multiple_files=True)

    # Create a temp folder for videos if it doesn't exist
    temp_video_folder = "temp_videos"
    os.makedirs(temp_video_folder, exist_ok=True)

    # Create a list to keep track of temporary video files
    temp_video_files = []

    # Count the number of successfully uploaded videos
    num_uploaded_videos = 0

    if uploaded_videos:
        for uploaded_video in uploaded_videos:
            # Save the uploaded video file to the temp folder for videos
            temp_video_path = os.path.join(temp_video_folder, uploaded_video.name)
            temp_video_files.append(temp_video_path)

            with open(temp_video_path, "wb") as temp_file:
                temp_file.write(uploaded_video.read())

            num_uploaded_videos += 1

    # Display the number of successfully uploaded videos in the console
    if num_uploaded_videos > 0:
        st.write(f"Successfully uploaded {num_uploaded_videos} videos")
        video_to_text()
        
        # Create a text box and a submit button
        st.subheader("Let's Chat....")
        # user_input = st.text_area("Please Ask Your Question")
        # if st.button("Submit"):
        #     st.write("You submitted:", user_input)
        flag=2

    else:
        st.write("Waiting for Videos to be Uploaded...")
        flag=0
    
    return flag,temp_video_files

# Cleanup files when the Streamlit server is killed
def cleanup_temp_files(temp_files):
    for temp_file in temp_files:
        try:
            if os.path.isfile(temp_file):
                os.unlink(temp_file)
        except Exception as e:
            st.write(f"Error deleting file: {temp_file}")
            st.write(e)

def cleanup_temp_video_files(temp_video_files):
    for temp_video_file in temp_video_files:
        try:
            if os.path.isfile(temp_video_file):
                os.unlink(temp_video_file)
        except Exception as e:
            # st.write(f"Error deleting video file: {temp_video_file}")
            # st.write(e)
            print("Unable to Delete Unknown File present in the path")