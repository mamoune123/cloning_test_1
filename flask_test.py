from flask import Flask, request, jsonify, render_template, send_file, redirect, flash, url_for, session
import uuid
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
import requests
import os
import json
import shutil
import psycopg2
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
app.config['mes_voix']='/Users/mac/Desktop/Cloning_test/mes_voix'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'wma', 'au', 'aiff', 'm4a'}
db_host = 'localhost'
db_port = 5432 
db_name = 'VoiceStory'
db_user = 'postgres'
db_password = '1234'



@app.route('/fav')
def fav():
    return render_template('dist/favoris.html')


@app.route('/update_favorite', methods=['POST'])
def update_favorite():
    favorite_id = request.json.get('favoriteId')
    is_favorite = request.json.get('isFavorite')
    user_id = session.get('user_id') 
    print(user_id)

    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE favoris SET is_favori = %s WHERE id_histoire = %s AND id_utilisateur = %s;", (is_favorite, favorite_id, user_id))
        conn.commit()
        return jsonify({'message': 'Favorite status updated'})
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': 'Failed to update favorite status'})
    

@app.route('/c')
def c():

    return render_template("dist/comptes.html")
    
@app.route('/comptes',methods=['GET'])
def get_histoires():
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    user_id = session.get('user_id') if 'user_id' in session else None
    try:
        cursor = conn.cursor()
        if user_id :
            cursor.execute('SELECT h.id_histoire, h.titre, h.img, h.description, h.texte, t.nom_thème, f.is_favori ' +
               'FROM histoires h ' +
               'JOIN thèmes t ON h.id_thème = t.id_thème ' +
               'LEFT JOIN favoris f ON h.id_histoire = f.id_histoire '  +
                       'WHERE f.id_utilisateur = %s', (user_id,))
        else:
            cursor.execute('SELECT h.id_histoire, h.titre, h.img, h.description, h.texte, t.nom_thème ' +
                           'FROM histoires h ' +
                           'JOIN thèmes t ON h.id_thème = t.id_thème')
        histoires = cursor.fetchall()
        if user_id:
            histoire_data = [{'id_histoire': histoire[0], 'titre': histoire[1], 'img': histoire[2], 'description': histoire[3], 'texte': histoire[4], 'theme_nom': histoire[5], 'is_favori': histoire[6]} for histoire in histoires]
        else:
            histoire_data = [{'id_histoire': histoire[0], 'titre': histoire[1], 'img': histoire[2], 'description': histoire[3], 'texte': histoire[4], 'theme_nom': histoire[5]} for histoire in histoires]

        
       

        # Return the themes data as JSON
        return jsonify({'histoires': histoire_data})
    except psycopg2.Error as e:
        print('Error fetching data:', e)
        return 'Internal Server Error', 500
    finally:
        cursor.close()
        conn.close()        
@app.route('/page2', methods=['GET'])
def get_themes():
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id_thème, nom_thème, img FROM thèmes')
        themes = cursor.fetchall()

        # Convert the themes data to a list of dictionaries for JSON serialization
        themes_data = [{'id': theme[0], 'nom_thème': theme[1], 'img': theme[2]} for theme in themes]

        # Return the themes data as JSON
        return jsonify({'themes': themes_data})
    except psycopg2.Error as e:
        print('Error fetching data:', e)
        return 'Internal Server Error', 500
    finally:
        cursor.close()
        conn.close()

@app.route('/forgot',methods=['POST'])
def forget():
    username = request.form['user']
    password = request.form['pass']
    
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()
    select_query = "SELECT username FROM Utilisateurs WHERE username = %s"
    cursor.execute(select_query, (username,))
    result = cursor.fetchone()
    if result:
        # Username exists, perform the password change logic and update the database
        update_query = "UPDATE Utilisateurs SET password = %s WHERE username = %s"
        cursor.execute(update_query, (password, username))
        conn.commit()
        cursor.close()
        conn.close()
        success_message = "Password changed successfully!"
        return redirect(url_for('start', success_message=success_message))
    else:
        # Username doesn't exist, display an error message
        cursor.close()
        conn.close()
        print('no matching for the usernam')
        return render_template('dist/forget.html')

    
@app.route('/home')
def home():
    return render_template("dist/HOME.html")
@app.route('/login1', methods=['POST'])
def login1():
    # Get form data
    username = request.form['user']
    password = request.form['pass']

    # Connect to the database
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()

    # Check if the username and password match
    cursor.execute("SELECT * FROM Utilisateurs WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    if user:
        # Login successful, redirect to a logged-in page
        session['user_id'] = user[0]
        session['logged_in'] = True
        session['username'] = username
        cursor.close()
        conn.close()
        return redirect(url_for('home', username=username))
       
    else:
        cursor.close()
        conn.close()
        # Login failed, display an error message
        error_message = "Invalid username or password. Please try again."
        return render_template('dist/login.html', error=error_message)
@app.route('/logout')
def logout():
    session.clear()  # Clear the user session
    return redirect(url_for('home'))
@app.route('/record')
def record():
    return render_template("dist/RECORDING.html")
@app.route('/index')
def index():
    return render_template("dist/index.html")
@app.route('/download_output')
def download_output():
    return send_file('templates/dist/output/voice.wav', as_attachment=True)

@app.route('/register')
def register():
    return render_template("dist/register.html")
@app.route('/signup', methods=['POST'])
def signup():
    # Get form data
    username = request.form['user']
    password = request.form['pass']

    # Connect to the database
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()

    # Insert user data into the database
    cursor.execute("INSERT INTO Utilisateurs (username, password) VALUES (%s, %s)", (username, password))

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    # Redirect or render a success page
    return render_template('dist/login.html')
@app.route('/T')
def T():
    return render_template("dist/page2.html")
@app.route('/f')
def f():
    return render_template("dist/forget.html")
@app.route('/')
def start():
    success_message =request.args.get('success_message')
    return render_template('dist/login.html',success_message=success_message)

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
    full_file_name1 = os.path.join(app.config['mes_voix'], file_name)
    file.save(full_file_name)
    file.save(full_file_name1)
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
@app.route('/wait')
def wait():
    return render_template('dist/waiting.html')
@app.route('/suc')
def suc():
    return render_template('dist/SUCCESS.html')
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
   
