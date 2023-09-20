from flask import current_app as app,request,jsonify,Response
from flask_restful import Resource
from app import api
import cv2
import os,argparse
import pytesseract
from PIL import Image
import re
import json

      
class VerifyDocumentAPI(Resource):
    def post(self):
        f=request.files['file']
        text = pytesseract.image_to_string(Image.open(f))

        word_list =[

            'BA LLB', 'BBA LLB','BCA LLB','B.Com LLB','B.Tech LLB',
            'B.Sc LLB', 'Bachelor of Arts and Bachelor of Legislative Law',
            'Bachelor of Legislative Law' , 'Bachelor of Business Administration and Bachelor of Legislative Law',
            'Doctor of Juridical Science' , 'Juris Doctor','Bachelor of Law in Intellectual Property Law',
            'LL.B','LLB', 'J.D.', 'LL.M.', 'Master of Laws', 'L.L.B.', 'LL.D.',
    'Legal Studies', 'Law Degree', 'Juridical Studies', 'Legal Education',

            'Bachelor of Law'
        ]        

        pattern = r'\b(?:' + '|'.join(re.escape(word) for word in word_list) + r')\b'

        final_res = {'verified':str(bool(re.search(pattern, text, flags=re.IGNORECASE)))}
        return Response(json.dumps(final_res),status=200)


api.add_resource(VerifyDocumentAPI,'/verify')
