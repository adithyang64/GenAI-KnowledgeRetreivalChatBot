import streamlit as st
import docx
import os
import io
import sys
import atexit
from TestCaseGenerator import document_parse_loader, testcase_generator
from helperfns import generate_messages, initialize, qa_chatbot
from streamlit_chat import message
import base64
from video2txt import video_to_text


st.set_page_config(layout="wide", page_icon="💬", page_title="Chat-Bot 🤖")
#st.set_page_bg(image="bg-img.jpg")

# def get_base64(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()


# def set_background(png_file):
#     bin_str = get_base64(png_file)
#     page_bg_img = '''
#     <style>
#     .stApp {
#     background-image: url("data:image/png;base64,%s");
#     background-size: cover;
#     }
#     </style>
#     ''' % bin_str
#     st.markdown(page_bg_img, unsafe_allow_html=True)

# set_background('bg-img.jpg')


# Streamlit app title
st.title("Knowledge Retrieval Chatbot")

with st.sidebar:

    # Create tabs for uploading documents and videos
    selected_tab = st.radio("Select File Type:", ["Upload Documents (PDF, DOCX, TXT)", "Upload Videos"])

    if selected_tab == "Upload Documents (PDF, DOCX, TXT)":
        # Upload multiple documents
        uploaded_files = st.file_uploader("Upload documents (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"], accept_multiple_files=True)

        # Create a temp folder if it doesn't exist
        temp_folder = "temp_documents"
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

    else:
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
if flag==1:
    tab1, tab2 = st.tabs(["Ask Questions to Chatbot", "Make your Life Easy"])
    with tab1:
        qa_chatbot()
    with tab2:
        st.subheader("Get Assistance")
        user_input = st.text_area("Please Ask Your Question")
        if st.button("Submit"):
            document_content = document_parse_loader()
            answer_fr_user = testcase_generator(document_content,user_input)
            st.write(answer_fr_user)

# Cleanup files when the Streamlit server is killed
def cleanup_temp_files():
    for temp_file in temp_files:
        try:
            if os.path.isfile(temp_file):
                os.unlink(temp_file)
        except Exception as e:
            st.write(f"Error deleting file: {temp_file}")
            st.write(e)

def cleanup_temp_video_files():
    for temp_video_file in temp_video_files:
        try:
            if os.path.isfile(temp_video_file):
                os.unlink(temp_video_file)
        except Exception as e:
            # st.write(f"Error deleting video file: {temp_video_file}")
            # st.write(e)
            print("Unable to Delete Unknown File present in the path")

# Cleanup functions to run when we exit
try:
    atexit.register(cleanup_temp_files)
    atexit.register(cleanup_temp_video_files)
except Exception as e:
    print(Exception)