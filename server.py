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
from resumeparse import resumeparse
# from sseclient import SSEClient
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
from models import Model
import skillSuggestion

app = Flask(__name__)  # initializing flask app
CORS(app)  # to avoid CORS errors

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#firestore sdk code
cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred)

# documento = db.collection(u'BD_canciones').document(u'cancion4')

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


def parse_file(filename):
    resume = resumeparse.read_file(filename)
    return resume


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def Welcome():
    return jsonify({'status': "success", 'message': "Welcome to Resume Parser API"})


@app.route('/GetBehaviours/<userid>', methods=['GET'])
def GetBehaviours(userid):
    print(userid)
    db = firestore.client()
    # docs = db.collection(u'cities').where(u'capital', u'==', True).stream()

    try:
        userChoices = db.collection(u'Behaviour_DB').where(u'userId', u'==', int(userid)).stream()
        # docs = userChoices.get()
        userChoicesList = []
        for doc in userChoices:
            userChoicesList.append(doc.to_dict())
            # print(u'Doc Data:{}'.format(doc.to_dict()))

        return jsonify({'status': "success", 'message': "Records Found", 'data': userChoicesList})
    except google.cloud.exceptions.NotFound:
        print(u'Missing data')
        return jsonify({'status': "Failed", 'message': "No Records Found"})


@app.route('/SetBehaviours/<userid>', methods=['POST'])
def SetBehaviours(userid):
    db = firestore.client()

    try:
        data = request.form['data']
        data = list(eval(data))
        for item in data:
            # print(item)
            docId = userid+"-"+item['cardId']
            db.collection(u'Behaviour_DB').document(docId).set(item)
            # print(res)
        # for doc in userChoices:
            # print(u'Doc Data:{}'.format(doc.to_dict()))
        # doc_ref.add({u'name': u'test', u'added': u'just now'})
        # db.collection(u'Behaviour_DB').doc('').update({ "friends": { "friend-uid-3": true } })
        # doc_ref.set(, { merge: true });

        return jsonify({'status': "success", 'message': "Data Updated Successfully"})
    except Exception as e: 
        print(e)
        return jsonify({'status': "Failed", 'message': "Something Went Wrong"})


@app.route('/UploadFile', methods=['POST'])
def UploadFile():
    print("inside upload file")
    if request.method == 'POST':
        # print(request)
        # print(request.files)
        if 'resume' not in request.files:
            print('No file part')
            return jsonify({'status': "FAIL", 'message': "No file part"})
        file = request.files['resume']
        if file.filename == '':
            print('No selected file')
            return jsonify({'status': "FAIL", 'message': "No Selected File"})
        if file and allowed_file(file.filename):
            print("FileName is: "+str(file.filename))
            filename = secure_filename(file.filename)
            # path_on_cloud = "resumes/"+filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # storage.child(path_on_cloud).put(
            #     os.path.join(app.config['UPLOAD_FOLDER'], filename))
            resume = parse_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # print(resume)
            if len(resume['grade_input']) > 0:
                model = Model()
                classifier = model.svm_classifier()
                prediction = classifier.predict([resume['grade_input']])
                # print(prediction)
            else:
                print("resume.grade_input is empty")

            if len(resume['skills']) > 0:
                suggestedSkills = skillSuggestion.suggestSkills(resume['skills'])
            else:
                print("resume.skills are empty")

        else:
            return jsonify({'status': "FAIL", 'message': "Extension Not Allowed"})

    return jsonify({'status': "success", 'message': "File Uploaded Successfully", "data": resume, "grade": prediction[0], "suggSkills": suggestedSkills})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(6060), debug=True, threaded=True)
    # URL : localhost:6060
    # API for Uploading Files : localhost:6060/UploadFile (POST) (try POSTMAN or INSOMNIA to test POST)
