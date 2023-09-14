import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from langchain.memory import MongoDBChatMessageHistory
from langchain.chains import RetrievalQA
from langchain import PromptTemplate
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM 
from transformers import pipeline
from langchain.llms import HuggingFacePipeline
import torch
from langchain.embeddings import SentenceTransformerEmbeddings


import os


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=400,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks, embedder):
    # embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embedder)
    vectorstore.merge_from(FAISS.load_local("./vectorstore", embedder))
    return vectorstore


def store_text(text_chunks):
    # embeddings = HuggingFaceInstructEmbeddings(
    #     model_name="hkunlp/instructor-large")
    embeddings = SentenceTransformerEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1")
    vectorstore  = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    if os.listdir('./vectorstore') != []:
       vectorstore.merge_from(FAISS.load_local("./vectorstore", embeddings))
    vectorstore.save_local("./vectorstore")


def get_conversation_chain(vectorstore):
    # llm = ChatOpenAI()
    checkpoint = "MBZUAI/LaMini-Flan-T5-783M"

    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    base_model = AutoModelForSeq2SeqLM.from_pretrained(
    checkpoint,
    device_map="auto",
    torch_dtype = torch.float32)

    pipe = pipeline(
    'text2text-generation',
    model = base_model,
    tokenizer = tokenizer,
    max_length = 512,
    do_sample = True,
    temperature = 0.3,
    top_p= 0.95
)
    llm = HuggingFacePipeline(pipeline=pipe)

    # llm = HuggingFaceHub(repo_id="google/flan-t5-large",
    #                      model_kwargs={"temperature": 0.5, "max_length": 512})

    # memory = ConversationBufferMemory(
    #     memory_key='chat_history', return_messages=True)
    # print(vectorstore.docstore._dict)

#     template = """
# Use the following context (delimited by <ctx></ctx>) and the chat history (delimited by <hs></hs>) to answer the question , if you dont know the answer say "I dont know" :
# ------
# <ctx>
# {context}
# </ctx>
# ------
# <hs>
# {chat_history}
# </hs>
# ------
# {question}
# Answer:
# """
#     prompt = PromptTemplate(
#         input_variables=["chat_history", "context", "question"],
#         template=template,
#     )

    custom_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question. At the end of standalone question add this 'Answer the question in German language.' If you do not know the answer reply with 'I am sorry'.
    Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:"""


    CUSTOM_QUESTION_PROMPT = PromptTemplate.from_template(custom_template)


    # conversation_chain = ConversationalRetrievalChain.from_llm(
    #     # chain_type='stuff',
    #     llm=llm,
    #     retriever=vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 6, 'lambda_mult': 0.25}),
    #     return_source_documents=True,
    # #     memory=ConversationBufferMemory(
    #         chat_memory=st.session_state.message_history,
        
    # memory_key='chat_history',
    # input_key='question',
    # output_key='answer',
    # return_messages=True
    #     ),

    #    condense_question_prompt=CUSTOM_QUESTION_PROMPT
    # )

    conversation_chain = RetrievalQA.from_chain_type(llm=llm,
        chain_type='stuff',
        retriever=vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":2}),
        return_source_documents=True,

#         chain_type_kwargs={
#         "verbose": True,
#         "memory": ConversationBufferMemory(
#     chat_memory=st.session_state.message_history,
#     memory_key='chat_history',
#     return_messages=True,
#     # output_key="answer"
# )
# }

        )
    return conversation_chain


def handle_userinput(user_question):
    # m_hist = st.session_state.message_history.messages
    # if m_hist is None:
    #     m_hist = []

    # response = st.session_state.conversation(
    #     {'query': user_question})
    # print(response)
    # # st.session_state.chat_history.append({'question':user_question,'answer':response['answer']})
    # st.session_state.message_history.add_user_message(response['question'])
    # st.session_state.message_history.add_ai_message(response['answer'])

    # for i, message in enumerate(st.session_state.message_history.messages):
    #     if i % 2 == 0:
    #         st.write(user_template.replace(
    #             "{{MSG}}", message.content), unsafe_allow_html=True)
    #     else:
    #         st.write(bot_template.replace(
    #             "{{MSG}}", message.content), unsafe_allow_html=True)

    # ---------------------------------------------
    
    response = st.session_state.conversation({'query': user_question})
    print(response)
    # st.session_state.chat_history = response['chat_history']
    st.session_state.message_history.add_user_message(response['query'])
    st.session_state.message_history.add_ai_message(response['result'])
    print("Source Docs:  " ,response["source_documents"])

    # print(response['answer'])


    for i, message in enumerate(st.session_state.message_history.messages):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)