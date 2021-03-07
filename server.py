from flask import Flask, jsonify, redirect, request, Response, render_template, url_for, send_from_directory
import base64
import os
import json
from flask_cors import CORS, cross_origin
import hashlib
import math
import requests
# import pyrebase
from werkzeug.utils import secure_filename
# from resume_parser2.resumeparse import resumeparse
# from sseclient import SSEClient

app = Flask(__name__)  # initializing flask app
CORS(app)  # to avoid CORS errors

UPLOAD_FOLDER = '../uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# cong = {

#     "apiKey": "AIzaSyANPQjD8WE5I6IqUsGdghkgtls_ZcUM2hg",
#     "authDomain": "myproject-99cc3.firebaseapp.com",
#     "databaseURL": "https://myproject-99cc3-default-rtdb.firebaseio.com",
#     "projectId": "myproject-99cc3",
#     "storageBucket": "myproject-99cc3.appspot.com",
#     "messagingSenderId": "686650502759",
#     "appId": "1:686650502759:web:336484c7ccd1882f866ec2"
# }

# firebase = pyrebase.initialize_app(cong)
# storage = firebase.storage()

# path_on_cloud = "resumes/file.pdf"


# def parse_file(filename):
#     resume = resumeparse.read_file(filename)
#     return resume


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def Welcome():
    return jsonify({'status': "success", 'message': "Welcome to Resume Parser API"})

@app.route('/UploadFile', methods=['POST'])
def UploadFile():
    print("inside upload file")
    if request.method == 'POST':
        print(request)
        print(request.files)
        # check if the post request has the file part
        if 'resume' not in request.files:
            print('No file part')
            return jsonify({'status': "failure", 'message': "No file part"})
        file = request.files['resume']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected file')
            return jsonify({'status': "failure", 'message': "No Selected File"})
        if file and allowed_file(file.filename):
            print(file.filename)
            # filename = secure_filename(file.filename)
            # path_on_cloud = "resumes/"+filename
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # storage.child(path_on_cloud).put(
            #     os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # resume = parse_file(os.path.join(
            #     app.config['UPLOAD_FOLDER'], filename))
            # print(resume)

    return jsonify({'status': "success", 'message': "File Uploaded Successfully"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(6060), debug=True, threaded=True)
    # URL : localhost:6060
    # API for Uploading Files : localhost:6060/UploadFile (POST) (try POSTMAN or INSOMNIA to test POST)
