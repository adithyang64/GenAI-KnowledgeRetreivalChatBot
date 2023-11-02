# Knowledge Retreival ChatBot

## Project Overview
This project encompasses a web-based chatbot application developed with Streamlit, aimed at providing answers to user queries. Below, we outline the key components and functionalities of this project:

## Solution

### File Upload and Parsing
Users can upload documents or videos containing their questions, which are subsequently parsed.
For videos, Moviepy.editor is used to extract the audio, which is saved in .wav format with the codec set to pcm_s161e.
The transcribed text is generated using the open-source speech_recognition library developed by CMUSphinx.

### Text Processing
The transcribed text is loaded using a Directory Loader and split into chunks using the RecursiveCharacterTextSplitter.
The chunk size and overlap values can be adjusted to improve accuracy.

### Text Embeddings
Text embeddings are created using OpenAI's text-embedding-ada-002 model.
These embeddings are stored in a Vector DB, PineCone, which is initialized and maintained within the specified index.

## Approaches to Answering Questions

### Approach 1 - Simple and Direct
This approach is designed for answering straightforward questions.
When a user poses a question, our chatbot uses GPT-3.5 Turbo LLM to search the PineCone index for similar words with a similarity score.
If a match is found, the chatbot leverages the LangChain Library's qa chain to provide an answer. If the question is out of context, the bot indicates that it cannot answer.

### Approach 2 - Prompt-Based
In this approach, the chatbot obtains the user's question and sends it to the LLM based on a predefined prompt template.
Utilizing the LangChain Library - LLM chain, the chatbot answers the question based on the response from the LLM.

## Tech Stack

Streamlit
OpenAI's API ->  text-embedding-ada-002 & gpt-turbo-3.5
Vector Database -> PineCone
Py Libraries -> Moviepy.editor, speech_recognition (By CMUSphinx)


Getting Started
Update the Constant Values such as Pinecone Key, Env, Index & OpenAI Key in "constants.py"

Install the required dependencies in the virtual environment :
```
pip install -r requirements.txt
```

Launch the Service :
```
streamlit run app.py
```

Once all the setup is complete, you can begin interacting with our chatbot and asking questions.
