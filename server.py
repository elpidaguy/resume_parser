from flask import Flask, jsonify, redirect, request,Response, render_template, url_for, send_from_directory
import base64
import os
import json
from flask_cors import CORS, cross_origin
import hashlib
import math
import requests

app = Flask(__name__)  #initializing flask app
CORS(app) #to avoid CORS errors

@app.route('/UploadFile',methods=['POST'])
def UploadFile():

    #Reference : https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

    #NOTE: Try to open this project with VSCODE and install 1.python module 2. TODO Tree 3. Rainbow Brackets
    #Follow these steps to complete your API

    '''TODO: 

    Step 0 : Run pip install -r requirements.txt

    Step 1: Upload File via REQUESTS to local directory named upload (You can ask sir if its sufficient if we upload all files on server rather than firebase ? upload in upload folder only : go to step 4 )

    STEP 2: Call functions from resumeparser.py to parse file and return the result generated to this function 
    
    STEP 3: Set the result in local variable and then call FIREBASE db API from Python to save the result in DB
    
    STEP 4: On success of above API, call FIREBASE Function for uploading file to Server'''

    
    return jsonify({'status': "success", 'message': "File Uploaded Successfully"})

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=int(6060),debug=True, threaded=True) 
    #URL : localhost:6060
    # API for Uploading Files : localhost:6060/UploadFile (POST) (try POSTMAN or INSOMNIA to test POST)