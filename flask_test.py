from flask import Flask, request, jsonify, render_template, send_file, redirect, flash, url_for, session
import uuid
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
import requests
import os
import json
import shutil
import psycopg2
import smtplib
from premailer import transform
from bs4 import BeautifulSoup
XI_API_KEY = "067b3f82874d1f95f8ba0945f192d5bd"
def sendEmail(recipient_email,updated_content):
    # Create the email headers
    sender_email = "voicestorykidsstory@gmail.com"
    sender_password = "lohlwfqevcdifnpr"
    subject = 'Registration Succesful to VoiceStory, Welcome !!'
    headers = f"From: {sender_email}\r\nTo: {recipient_email}\r\nSubject: {subject}\r\nMIME-Version: 1.0\r\nContent-Type: text/html\r\n"
    html_file = '/Users/mac/Desktop/Cloning_test/templates/dist/EMAIL.html'
    with open(html_file,'r') as file : 
        data = file.read()
    
    htmlc = transform(data)

    soup = BeautifulSoup(htmlc, 'html.parser')
    h1_element = soup.find('h1', {'class': 'name'})  # Replace with the appropriate selector
    h1_element.string = updated_content

    # Get the updated HTML
    updated_html = str(soup)

    # Create the full email message
    email_message = headers + "\r\n" + updated_html
    smtp_server = 'smtp.gmail.com'
    smtp_port = '587'
    try:
        # Create a SMTP session
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Start TLS encryption if needed
            server.starttls()
            # Login to the SMTP server
            server.login(sender_email, sender_password)
            # Send the email
            server.sendmail(sender_email, recipient_email, email_message.encode('utf-8'))
        print("Email sent successfully!")
    except Exception as e:
        print("An error occurred while sending the email:", str(e))



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
    user_id = session.get('user_id')
    if user_id :
        for filename in filenames:
            file_path = os.path.join(app.config['mes_voix'], filename)
            files.append(('files', (filename, open(file_path, 'rb'), 'audio/mpeg')))
    else : 
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


@app.route('/update_selected', methods=['POST'])
def update_selected():
    data = request.get_json()
    voix_id = data['voixId']
    selected = data['selected']
    user_id = session.get('user_id') 

    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    print(selected)
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE voix SET selected = %s WHERE id_voix = %s AND id_utilisateur = %s;", (selected,voix_id, user_id))
        conn.commit()
        return jsonify({'message': 'selected status updated'})
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': 'Failed to update favorite status'})
    
    




@app.route('/delete-file', methods=['POST'])
def delete_file():
    data = request.get_json()
    file_name = data['fileName']
    print(file_name)
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()

    # Retrieve the chemin_file for the given file name
    cursor.execute("SELECT chemin_fichier FROM voix WHERE nom_file = %s", (file_name,))
    result = cursor.fetchone()

    if result:
        chemin_file = result[0]
        # Delete the file from the folder
        file_path = os.path.join(app.config['mes_voix'], chemin_file)
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print('File not found:', file_path)

    # Delete the row from the voix table
    cursor.execute("DELETE FROM voix WHERE nom_file = %s", (file_name,))
    conn.commit()

    cursor.close()
    conn.close()

    return '', 200


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
# get voice 
@app.route('/voixget')
def voixge():
    user_id = session.get('user_id')
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM voix WHERE id_utilisateur = %s", (user_id,))
    voix = cursor.fetchall()
    voix_data = [{'id_voix' : voi[0], 'chemin_fichier': voi[2],'nom_file': voi[3], 'date_ajout': voi[4], 'selected':voi[5]} for voi in voix]
    return jsonify({'voix': voix_data})

@app.route('/voix')
def voix():
    return render_template('dist/mes_voix.html')
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
    email = request.form['email']
    password = request.form['pass']

    # Connect to the database
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()

    # Check if the username and password match
    cursor.execute("SELECT * FROM Utilisateurs WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    if user:
        # Login successful, redirect to a logged-in page
        session['user_id'] = user[0]
        session['logged_in'] = True
        session['username'] = user[1]
        username = user[1]
        print(username)
        cursor.close()
        conn.close()
        return redirect(url_for('home', username=username))
       
    else:
        cursor.close()
        conn.close()
        # Login failed, display an error message
        error_message = "Invalid mail or password. Please try again."
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
    mail = request.form['email']
    print(mail)
    # Connect to the database
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()

    try : 
        # Insert user data into the database
        cursor.execute("INSERT INTO Utilisateurs (username, password, email) VALUES (%s, %s, %s)", (username, password, mail))
        sendEmail(mail,username)
    # Commit the transaction
        conn.commit()
    except psycopg2.IntegrityError as e:
        error_message = str(e)
        if 'unique_username' in error_message:
            error_message = "Username already existe. Please try different one."
            return render_template('dist/register.html',error_message=error_message)
        if 'unique_mail' in error_message:
            error_message = "Email already existe. Please try different one."
            return render_template('dist/register.html',error_message=error_message)
        else:

            error_message = "Username and email already exist. Please try different ones."
            return render_template('dist/register.html', error_message=error_message)
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
@app.route('/save_mesvoix',methods=['POST'])
def save_mesvoix():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    file_name = str(uuid.uuid4()) + ".wav"
    full_file_name = os.path.join(app.config['mes_voix'], file_name)
    file.save(full_file_name)
    user_id = session.get('user_id') 
    filename1 = file.filename
    print(filename1)
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()
    if user_id :
        insert_query = "INSERT INTO voix (id_utilisateur, nom_file, chemin_fichier) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (user_id, filename1, full_file_name))
    conn.commit()
    cursor.close()

    return render_template("dist/page2.html")

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
    user_id = session.get('user_id') 

    if user_id : 
        conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password) 
        cursor = conn.cursor() 
        cursor.execute('SELECT chemin_fichier FROM voix WHERE selected = TRUE AND id_utilisateur=%s',(user_id,)) 
        result = cursor.fetchall()
        file_remove = '.DS_Store'
        filenames1 = [os.path.basename(row[0]) for row in result]
        if file_remove in filenames1 :
            filenames1.remove(file_remove)
        print(filenames1)
        conn.close() 
        send_text_to_speech_api(XI_API_KEY, Text_data, filenames1,selectedgender=SelectedOption1,selectedaccent=SelectedOption2)  
        response = send_text_to_speech_api(XI_API_KEY, Text_data, filenames1,selectedgender=SelectedOption1,selectedaccent=SelectedOption2)  
        OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'templates/dist/output')  
        output_path = os.path.join(OUTPUT_DIR, 'voice.wav')    
        with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                     if chunk:
                        f.write(chunk)   

        return render_template('dist/SUCCESS.html')

    else :   
            filenames = []
            filenames = os.listdir(records_dir)
            file_remove = '.DS_Store'
            if file_remove in filenames :
                filenames.remove(file_remove)
            print(filenames)
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
   
