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

if __name__=='__main__':
    load_dotenv()
    st.set_page_config(page_title="Nyaay-Ingest",
                        page_icon=":robot_face:")
    st.subheader("Your legal documents")
    pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
    if st.button("Process"):
            with st.spinner("Processing"):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                embeddings = SentenceTransformerEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1")
                vector_store = FAISS.load_local("./vectorstore",embeddings)
                vector_store.merge_from(FAISS.from_texts(texts=text_chunks, embedding=embeddings))
                vector_store.save_local("./vectorstore")
