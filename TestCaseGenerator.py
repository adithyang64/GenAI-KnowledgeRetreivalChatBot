from langchain.chat_models.openai import ChatOpenAI
import openai
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.document_loaders import DirectoryLoader

def document_parse_loader():
    directory = 'temp_documents/'

    documents = load_docs(directory)
    len(documents)

    #print(documents)
    #print(documents[0].page_content)
    txt_content = documents[0].page_content
    print(txt_content)
    return txt_content

def load_docs(directory):
        loader = DirectoryLoader(directory)
        documents = loader.load()
        return documents


def testcase_generator(txt_content,user_question):
    # Define prompt
    # prompt_template = """{ques}:
    # "{text}"
    # Test Cases:"""
    # prompt = PromptTemplate.from_template(prompt_template)
    ques = user_question
    # Define prompt
    prompt_template = ques+"""{text}"Test Cases:"""
    print(prompt_template)
    prompt = PromptTemplate.from_template(prompt_template)
    
    # Define LLM chain
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key="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")
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Get the text to be summarized
    text = txt_content
    

    # Generate summary
    summary = llm_chain.run(text)

    # Print the summary
    print(summary)
    return summary
