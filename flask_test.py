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
import random
import string
from premailer import transform
from bs4 import BeautifulSoup
import copy
XI_API_KEY = "067b3f82874d1f95f8ba0945f192d5bd"

def sendEmail(recipient_email,updated_content): #Fonction d'envoie d'email de bienvenue
    # Create the email headers
    sender_email = "voicestorykidsstory@gmail.com"
    sender_password = "lohlwfqevcdifnpr"
    subject = 'Registration Succesful to VoiceStory, Welcome !!'
    headers = f"From: {sender_email}\r\nTo: {recipient_email}\r\nSubject: {subject}\r\nMIME-Version: 1.0\r\nContent-Type: text/html\r\n"
    html_file = '/Users/mac/Desktop/Cloning_test/templates/dist/EMAIL.html'
    with open(html_file,'r') as file : #La page de bienvenue
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
    #Configuration du serveur smtp

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
def send_text_to_speech_api(XI_API_KEY, text, filenames,selectedgender,selectedaccent):   #Fonction pour envoyer les informations qu'il faut pour l'API ELEVENLAB
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
app.config['mes_voix']='/Users/mac/Desktop/Cloning_test/templates/dist/mes_voix'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'wma', 'au', 'aiff', 'm4a'}
db_host = 'localhost'
db_port = 5432 
db_name = 'VoiceStory'
db_user = 'postgres'    #A changer si different dans votre base de donnée (Utiliser POSTGRES)
db_password = '1234'    #ca aussi


@app.route('/update_selected', methods=['POST']) 
def update_selected():
    data = request.get_json() 
    voix_id = data['voixId'] #Extraction des valeurs des clés 'voixId' et 'selected' à partir des données.
    selected = data['selected']  
    user_id = session.get('user_id') #Récupération de l'identifiant de l'utilisateur à partir de la session.

    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password) #Fonction de connection a la base de données
    print(selected)
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE voix SET selected = %s WHERE id_voix = %s AND id_utilisateur = %s;", (selected,voix_id, user_id))#Mise a jours de la table voix
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


@app.route('/fav') #toute les fonctions qui sont simple comme ca c'est pour afficher les templates avec jinja2
def fav():
    return render_template('dist/favoris.html')


@app.route('/update_favorite', methods=['POST']) #Pour la mise a jours de la table favoris et donc sauvegarder pour l'utilisateur ces choix
def update_favorite():
    favorite_id = request.json.get('favoriteId')
    is_favorite = request.json.get('isFavorite')
    user_id = session.get('user_id') 
    print(user_id)

    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)#connection a la base de donées
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE favoris SET is_favori = %s WHERE id_histoire = %s AND id_utilisateur = %s;", (is_favorite, favorite_id, user_id))
        conn.commit()
        return jsonify({'message': 'Favorite status updated'})
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': 'Failed to update favorite status'})
    
@app.route('/recoute/<id_clone>') #fonction pour l'historique
def recoute(id_clone):
    user_id = session.get('user_id')
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    try:
        cursor = conn.cursor()
        if user_id : #si l'utilisateur est connecter
            cursor.execute("SELECT c.id_clone, c.chemin_fichier, h.titre, h.texte FROM clone c INNER JOIN histoires h ON c.id_histoire = h.id_histoire AND c.id_clone=%s;", (id_clone,))
            results = cursor.fetchall() #collecte des informations de la base de données
            ecoute_data = [{'chemin_fichier':ec[1],'titre':ec[2], 'texte':ec[3]} for ec in results]  #mettre ces données dans le dictionnaire Json ecoute_date
            return render_template("dist/recoute.html",ecoute_data=ecoute_data)
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': 'Failed to update favorite status'})
    return
@app.route('/c')
def c():

    return render_template("dist/comptes.html")#affichage de la partie histoires

@app.route ('/voice_card')
def voice_card():
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    user_id = session.get('user_id') if 'user_id' in session else None
    try:
        cursor = conn.cursor()
        if user_id :
            cursor.execute('SELECT c.id_clone, c.nom_file, c.date_ajout, c.id_histoire, h.titre, h.img FROM clone c JOIN histoires h ON c.id_histoire = h.id_histoire WHERE c.id_utilisateur = %s', (user_id,))
            histoires = cursor.fetchall()
            # Convert the themes data to a list of dictionaries for JSON serialization
            histoires_data = [{'id_clone': histoire[0], 'nom_file': histoire[1], 'date_ajout' : histoire[2], 'id_histoire': histoire[3], 'titre' : histoire[4],'img':histoire[5]} for histoire in histoires]

            # Return the themes data as JSON
            return jsonify({'mes_histoires': histoires_data})
    except psycopg2.Error as e:
        print('Error fetching data:', e)
        return 'Internal Server Error', 500
    finally:
        cursor.close()
        conn.close()



@app.route('/comptes',methods=['GET'])#Fonction qui permet de recolter les informations sur les histoires de la base de donées
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
@app.route('/voixget') #fonction qui permet la recolte des infos sur la voix de l'utilisateur et donc permetre de les recuperers apres
def voixge():
    user_id = session.get('user_id')
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM voix WHERE id_utilisateur = %s", (user_id,))
    voix = cursor.fetchall()
    voix_data = [{'id_voix' : voi[0], 'chemin_fichier': voi[2],'nom_file': voi[3], 'date_ajout': voi[4], 'selected':voi[5]} for voi in voix]
    return jsonify({'voix': voix_data})

@app.route('/voix1')#si on accedere depuis une histoires il y'a le bouton generate story
def voix1():
    show_button = True 
    if 'show_button1' in request.args:
        show_button = False     
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()

    # Get the user's ID
    user_id = session.get('user_id') 

    # Query the database to check if the user has any voice
    cursor.execute("SELECT * FROM voix WHERE id_utilisateur = %s", (user_id,))
    result = cursor.fetchone()

    if result is None:
        # User has no voice
        message = True
    else:
        # User has at least one voice
        message = False

    return render_template('dist/mes_voix.html', show_button=show_button, message=message)

@app.route('/voix') #si on accede depuis le page Themes y'a pas de bouton generate
def voix():
    show_button1 = False
    return redirect(url_for('voix1',show_button1=show_button1))
@app.route('/page2', methods=['GET'])#fonction qui permet de generer les cartes des themes grace a la collecte d'informations de la base de données
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
@app.route('/f')#Route pour la page forget.html
def f():
    return render_template("dist/forget.html")
@app.route('/reset', methods=['POST']) #fonction qui part l'entrer de l'email envoie un mail de reset password
def reset():
    email = request.form['email_reset']
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM utilisateurs WHERE email = %s", (email,)) 
    result = cursor.fetchone()
    if result : 
            username = result[0]
            print(username)
            Send_Reset(email,username)#fonction qui envoie le mail de reset password
            return render_template('dist/login.html',error_message='Email sent Successfully')
    else : 
            
            return render_template('dist/login.html',error_message='user not found (unknown email)')
@app.route('/reset_password/<username>', methods=['GET', 'POST'])#route pour la renitialisation du motdepasse
def reset_password(username):
    #  Retrieve the user's email associated with the provided username from the database
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM utilisateurs WHERE username = %s", (username,)) 
    result = cursor.fetchone()
    email = result[0] if result else None
    print(email)
    if email:
        if request.method == 'POST':
            #  Process the password reset form submission
            new_password = request.form['pass']
            confirm_password = request.form['new_pass']

            if new_password == confirm_password:
                # Update the user's password in the database
                update_query = "UPDATE Utilisateurs SET password = %s WHERE username = %s"
                cursor.execute(update_query, (new_password, username))
                conn.commit()
                cursor.close()
                conn.close()
                success_message = "Password changed successfully!"
                return redirect(url_for('start', success_message=success_message))
            else:
                cursor.close()
                conn.close()
                error_message = 'Passwords do not match.'
                return render_template('dist/forget.html',username=username, error_message=error_message)
        else:
            cursor.close()
            conn.close()
            return render_template('dist/forget.html', username=username)
    else:
        return render_template('forget.html')
    
def Send_Reset(recipient_email, Username): # Ce que recoie dans l'utilisateur dans la messagerie
    # Create the email headers
    sender_email = "voicestorykidsstory@gmail.com"
    sender_password = "lohlwfqevcdifnpr"
    subject = 'Reset Password'
    headers = f"From: {sender_email}\r\nTo: {recipient_email}\r\nSubject: {subject}\r\nMIME-Version: 1.0\r\nContent-Type: text/html\r\n"
    
    with app.app_context():
        reset_password_link = url_for('reset_password', username=Username, _external=True) #grace l'url_for creation du liens de reset password avec le nom d'utilisateur dans le liens
    
    # Create the body of the email
    body = f'''
    <html>
    <body>
        <h1>Reset Password</h1>
        <p>Dear {Username},</p>
        <p>Please click the following link to reset your password:</p>
        <p><a href="{reset_password_link}">{reset_password_link}</a></p>
        <p>If you are not responsible for this action, please ignore this message.</p>
    </body>
    </html>
    '''
  
    # Create the full email message
    email_message = headers + "\r\n" + body
    smtp_server = 'smtp.gmail.com'
    smtp_port = '587'
    
    try:
        # Create an SMTP session
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

    
@app.route('/home')
def home():
    return render_template("dist/HOME.html")
@app.route('/login1', methods=['POST'])#Connection de l'utilisateur
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
    return redirect(url_for('bien_inscrit')) #apres bonne inscription on est redirecter vers la route bien_inscrit qui elle dirige vers la page de succes
@app.route('/T')
def T():
    return render_template("dist/page2.html")
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
def add_to_database(user_id,chemin_fichier,texte): #fonction permet de nommer les histoires clonner et sauvegarder dans la base de données
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password) 
    cursor = conn.cursor() 
    cursor.execute("SELECT username FROM utilisateurs WHERE id_utilisateur = %s", (user_id,))
    result = cursor.fetchone()
    if result:
        nom_utilisateur = result[0]  # Récupérer le nom de l'utilisateur
    else:
        nom_utilisateur = 'John Doe'

    chiffre_aleatoire = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4)) #nommage de l'histoire clonnées
    nom_fichier = nom_utilisateur.replace(" ", "") + chiffre_aleatoire + '.wav'
    cursor.execute("SELECT id_histoire FROM histoires WHERE texte = %s",(texte,))
    result = cursor.fetchone()
    if result:
        id_histoire = result[0]
    else:
        id_histoire = None
    cursor.execute("INSERT INTO clone (id_utilisateur, chemin_fichier, nom_file, id_histoire) VALUES (%s, %s, %s, %s)", (user_id, chemin_fichier, nom_fichier, id_histoire))
    conn.commit()#insertion des valeurs au dessus dans la base de données
    cursor.close()
    conn.close()
    print("L'insertion dans la table clone a été effectuée avec succès !")
    return
@app.route('/Story', methods=['GET'])
def upload_file():#Fonction qui Recolte et envoie tout ce dont l'api ELEVENLAB a besoin
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
        response = send_text_to_speech_api(XI_API_KEY, Text_data, filenames1,selectedgender=SelectedOption1,selectedaccent=SelectedOption2)  
        response2 = copy.copy(response)
        OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'templates/dist/output')  
        output_path1 = os.path.join(OUTPUT_DIR, 'voice.wav') 
        output_filename = str(uuid.uuid4()) + '.wav'   
        output_path = os.path.join(OUTPUT_DIR, output_filename) 
        add_to_database(user_id,output_path,Text_data) #Ajout a la base de donées le nouveau fichier clonnées
        with open(output_path, 'wb') as f: #Creations du fichier audio grace a la response de l'API d'ElevenLabs qui est un fichier Json
                    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                     if chunk:
                        f.write(chunk)   
        with open(output_path1, 'wb') as f:
                    for chunk in response2.iter_content(chunk_size=CHUNK_SIZE):
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
@app.route('/bien_inscrit') 
def bien_inscrit():
    return render_template('dist/inscritreussie.html')
@app.route('/h')
def h():
    return render_template('dist/mes_histoires.html')
@app.route('/get_data', methods=['POST'])# permet la recolte du texte de l'histoire
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
   
