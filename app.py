
from utils import get_pdf_text,get_text_chunks,get_conversation_chain,get_vectorstore,handle_userinput
import os
from flask import Flask
from flask_restful import  Api

# logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


app = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    
    if os.getenv('ENV', "development") == "production":
      app.logger.info("Currently no production config is setup.")
      raise Exception("Currently no production config is setup.")
    else:
      app.logger.info("Starting Local Development.")
      print("Starting Local Development")
    #   app.config.from_object(LocalDevelopmentConfig)
    app.app_context().push()
    # user_datastore=SQLAlchemySessionUserDatastore(db.session,User,Role)
    # security=Security(app,user_datastore)
    app.logger.info("App setup complete")
    api = Api(app)
    return app,api

app ,api= create_app()

# Import all the controllers so they are loaded

from application.api import * #Import all APIs
from application.controllers import *



if __name__ == '__main__':
  # Run the Flask app
  app.run(debug=True)

