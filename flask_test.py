from flask import Flask, request, jsonify, render_template, send_file, redirect, flash
import uuid
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField, StringField
from flask_wtf import FlaskForm
import requests
import os
from werkzeug.datastructures import FileStorage
import json
import shutil
XI_API_KEY = "067b3f82874d1f95f8ba0945f192d5bd"
def models_imp(XI_API_KEY):
    url = "https://api.elevenlabs.io/v1/models"
    headers = {
  "Accept": "application/json",
  "xi-api-key": XI_API_KEY
  }
    response = requests.get(url, headers=headers)
    return response
def send_text_to_speech_api(XI_API_KEY, text, filenames,selectedgender,selectedaccent):   
    url = f"https://api.elevenlabs.io/v1/voices/add"
        
    headers = {
      "Accept": "application/json",
      "xi-api-key": XI_API_KEY
    }
    labels = {
        "accent": selectedaccent,
        "gender": selectedgender
    }

    data = {
            'name': 'Test1',
    'labels': json.dumps(labels),
    'description': 'An old man'
        }
    
     
    files = []
    for filename in filenames:
        file_path = os.path.join(app.config['records'], filename)
        files.append(('files', (filename, open(file_path, 'rb'), 'audio/mpeg')))

    response = requests.post(url, headers=headers, data=data, files=files)
    print(response.text)
    json_response = response.json()
    voice_id = json_response.get("voice_id")  # use .get() method to get value of voice_id, returns None if not found

    if voice_id is None:
    # handle the case where voice_id is not present in the response
        #return 'Error: Voice ID not found in response' 
        return json_response

    # get default voice settings
    # Send a request to get default voice settings
    response = requests.get(
    "https://api.elevenlabs.io/v1/voices/settings/default",
    headers={ "Accept": "application/json" }
    ).json()

    stability, similarity_boost = response["stability"], response["similarity_boost"]

    
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

    # Add Content-Type header to the existing headers dictionary
    headers["Content-Type"] = "application/json"
    models_imp(XI_API_KEY)
    # Define the data to be sent in the request
    data = {
      "text": text,
      "model_id": "eleven_multilingual_v1",
      "voice_settings": {
        "stability": stability,
        "similarity_boost": similarity_boost
      }
    }
    response = requests.post(tts_url, json=data, headers=headers, stream=True)
    
    return response
app = Flask(__name__, static_folder='templates/dist', static_url_path='')
SelectedOption1 = ''
SelectedOption2 = ''
Text_data = ''
CHUNK_SIZE = 1024
app.secret_key = 'supersecretkey'
app.config['records']='/Users/mac/Desktop/Cloning_test/records'

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'wma', 'au', 'aiff', 'm4a'}


@app.route('/download_output')
def download_output():
    return send_file('templates/dist/output/voice.wav', as_attachment=True)

@app.route('/')
def home():
    return render_template("dist/HOME.html")

@app.route('/save-record', methods=['POST'])
def save_record():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    file_name = str(uuid.uuid4()) + ".wav"
    full_file_name = os.path.join(app.config['records'], file_name)
    file.save(full_file_name)
    return render_template("dist/page2.html")

@app.route('/save_selection',methods=['POST'])
def save_var():
    global SelectedOption1, SelectedOption2
    SelectedOption1 = request.form.get('option')
    SelectedOption2 = request.form.get('option2')
    response = {
        'selectedOption1': SelectedOption1,
        'selectedOption2': SelectedOption2
    }
    print(response)
    return jsonify(response)


@app.route('/Story', methods=['GET'])
def upload_file():
    global SelectedOption1, SelectedOption2, Text_data
    url = f"https://api.elevenlabs.io/v1/voices/add"
    records_dir = app.config['records']
    filenames = []
    filenames = os.listdir(records_dir)
    send_text_to_speech_api(XI_API_KEY, Text_data, filenames,selectedgender=SelectedOption1,selectedaccent=SelectedOption2)
    response = send_text_to_speech_api(XI_API_KEY, Text_data, filenames,selectedgender=SelectedOption1,selectedaccent=SelectedOption2)
    empty_records_folder(records_dir)
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'templates/dist/output')
    output_path = os.path.join(OUTPUT_DIR, 'voice.wav')    
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)      
    return render_template('dist/SUCCESS.html')

def empty_records_folder(records1dir):
    # Delete all files inside the records folder
    for file_name in os.listdir(records1dir):
        file_path = os.path.join(records1dir, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

@app.route('/get_data', methods=['POST'])
def process_send():
    global Text_data
    data = request.get_json()
    text = data.get('text')
    Text_data = text
    response = {
        'text': Text_data,
    }
    print(response)
    return jsonify(response)
if __name__ == '__main__':
     
      app.run(debug=True)
   
