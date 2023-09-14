# # Use a pipeline as a high-level helper
# from transformers import pipeline

# pipe = pipeline("fill-mask", model="law-ai/InCaseLawBERT")

# print(pipe("Hello [MASK]"))
import requests
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
# from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from utils import get_pdf_text,get_text_chunks,get_conversation_chain,get_vectorstore,handle_userinput,store_text
import os 
from langchain.memory import MongoDBChatMessageHistory
from langchain.embeddings import SentenceTransformerEmbeddings

def main():
    load_dotenv()
    st.set_page_config(page_title="Nyaay-Chatbot",
                       page_icon=":robot_face:")
    st.write(css, unsafe_allow_html=True)
    
    st.header("Nyaay-Chatbot :robot_face:")
    user_question = st.text_input("Ask me your legal queries! :")

    if "message_history" not in st.session_state:
        st.session_state.message_history = MongoDBChatMessageHistory(
        connection_string=os.environ["MONGODB_HOST"], session_id="test15"
        )      
        for i, message in enumerate(st.session_state.message_history.messages):
            if i % 2 == 0:
                st.write(user_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
        

        
   

    # url = 'http://127.0.0.1:5000/message-context-api'
    # myobj = {'message': 'Hello'}

    # x = requests.post(url, json = myobj)
    # print(x.json())

    if "embeddings" not in st.session_state:
        # st.session_state.embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")
        st.session_state.embeddings = SentenceTransformerEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1")

        st.session_state.vector_store = FAISS.load_local("./vectorstore", st.session_state.embeddings)
    
    
        
        
    if "conversation" not in st.session_state:
        st.session_state.conversation = get_conversation_chain(st.session_state.vector_store)
   
    
    if user_question:
        handle_userinput(user_question)


    

    with st.sidebar:
        st.subheader("Your legal documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)
                

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)
                # store_text(text_chunks)
                # create vector store

                
                st.session_state.vector_store.merge_from(FAISS.from_texts(texts=text_chunks, embedding=st.session_state.embeddings))
                # vectorstore = get_vectorstore(text_chunks,st.session_state.embeddings)

                # create conversation chain

                # st.session_state.vector_store.save_local("./vectorstore")


                # mem = MongoDBChatMessageHistory(
                #     connection_string=os.environ["MONGODB_HOST"], session_id="test1"
                # )
                


                st.session_state.conversation = get_conversation_chain(
                    st.session_state.vector_store)


if __name__ == '__main__':
    main()