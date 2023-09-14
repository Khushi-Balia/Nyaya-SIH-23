from flask import current_app as app,request,jsonify,Response
from flask_restful import  Resource, fields, marshal_with, reqparse
from app import api
import json
from utils import get_pdf_text,get_text_chunks,get_conversation_chain,get_vectorstore,handle_userinput,store_text
from langchain.memory import MongoDBChatMessageHistory
import os 
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS

message_context_args = {
    "session_id",
    "message" , 
    "context"
    
}

message_store_args = {

    "context"
}








class Message_ContextAPI(Resource):
    # def __init__(self) -> None:
    #     super().__init__()
    #     self.venue_args={'venue_id':1,'theatre_name':1,'average_ticket_price':1,'total_seats':1,'no_screens':1,'type':1,'theatre_chain':1,"city":1}

    
    def post(self):
        for arg in request.json :
            
            if arg not in message_context_args:
                return "Invalid JSON",400
        print(request.json)
        embeddings = SentenceTransformerEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1")

        memory = MongoDBChatMessageHistory(
        connection_string=os.environ["MONGODB_HOST"], session_id=request.json['session_id']
        )      

        text_chunks = get_text_chunks(request.json['context'])
        vector_store = FAISS.load_local("./vectorstore",embeddings)
        vector_store.merge_from(FAISS.from_texts(texts=text_chunks, embedding=embeddings))
        conversation = get_conversation_chain(
                    vector_store)
        response = conversation({'query': request.json['message']})
        memory.add_user_message(response['query'])
        memory.add_ai_message(response['result'])

        message_list = []
        message_list = list(map(lambda x : message_list.append(x.content),memory.messages))

        
        final_res = {'response':response['result'],'chat_history':message_list}
        print(final_res)
        return Response(json.dumps(final_res),status=200)
        # return Response(json.dumps({}),status=200)
        
        
class Message_StoreAPI(Resource):
    def post(self):
        for arg in request.json :
            
            if arg not in message_store_args:
                return "Invalid JSON",400
        



        store_text(get_text_chunks(request.json['context']))
        
     

      

api.add_resource(Message_ContextAPI,  '/message-context-api')
api.add_resource(Message_StoreAPI,  '/message-store-api')
