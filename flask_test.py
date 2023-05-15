from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField, StringField
from flask_wtf import FlaskForm
import requests
import os
from werkzeug.datastructures import FileStorage

XI_API_KEY = "067b3f82874d1f95f8ba0945f192d5bd"
def models_imp(XI_API_KEY):
    url = "https://api.elevenlabs.io/v1/models"
    headers = {
  "Accept": "application/json",
  "xi-api-key": XI_API_KEY
  }
    response = requests.get(url, headers=headers)
    return response
def send_text_to_speech_api(XI_API_KEY, text, filenames):   
    url = f"https://api.elevenlabs.io/v1/voices/add"
        
    headers = {
      "Accept": "application/json",
      "xi-api-key": XI_API_KEY
    }

    data = {
            'name': 'Sample1',
    'labels': '{"accent": "American", "gender": "Male"}',
    'description': 'An old man'
        }
    
     
    files = []
    for filename in filenames:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
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
CHUNK_SIZE = 1024
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = '/Users/mac/Desktop/Cloning_test/static/files'


ALLOWED_EXTENSIONS = {'mp3', 'wav', 'wma', 'au', 'aiff', 'm4a'}


@app.route('/download_output')
def download_output():
    return send_file('templates/dist/output/voice.wav', as_attachment=True)
@app.route('/Stories')
def Stories_reading():

    return
@app.route('/')
def home():
    return render_template("dist/index.html")


@app.route('/', methods=['POST'])
def upload_file():
    text = request.form['text']
    uploaded_files = request.files.getlist('file')
    url = f"https://api.elevenlabs.io/v1/voices/add"
    filenames = []
    files = []
    for file in uploaded_files:
        if file:
            files.append(file)

    
    for file in files: 
        assert isinstance(file, FileStorage)
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        filenames.append(filename)

    send_text_to_speech_api(XI_API_KEY, text, filenames)
    response = send_text_to_speech_api(XI_API_KEY, text, filenames)

    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'templates/dist/output')
    output_path = os.path.join(OUTPUT_DIR, 'voice.wav')    
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)      


    return render_template("dist/index.html",message = "your voice is generatted succesfully !!")



if __name__ == '__main__':
    app.run(debug=True)
