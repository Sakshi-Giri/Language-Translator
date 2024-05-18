# Importing the libraries
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import session
import yt_dlp
import speech_recognition as sr

from flask_migrate import Migrate
#from pocketsphinx import LiveSpeech
from moviepy.editor import VideoFileClip

#from flask import Flask, render_template, request
from googletrans import Translator
from gtts import gTTS
import os
#from pydub import AudioSegment


app = Flask(__name__)

app.secret_key = '31206b7b80bb51fafd95fcea504e7edc'
app.config['UPLOAD_FOLDER'] = 'static'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# # Initialize Flask-Migrate
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


###### Play Audio Extracted Text
import pygame
import time

def play_audio(file_path):
    pygame.init()
    pygame.mixer.init()

    try:
        pygame.mixer.music.load(file_path)
        print(f"Playing {file_path}")
        pygame.mixer.music.play()

        # Allow time for the audio to play
        while pygame.mixer.music.get_busy():
            time.sleep(2)

    except pygame.error as e:
        print(f"Error: {e}")

    finally:
        pygame.mixer.quit()


####### Convert Speech to Text
def audio(audio_path):
        # Install and import the necessary libraries
    import speech_recognition as sr

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    
    # Function to convert audio speech to text
   # def speech_to_text(audio_path):
    with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            print("Text from video speech:", text)
    return text


    
###############3 Convert Vedio to Audio
@app.route("/video_to_audio_input")
def video_to_audio_input():
    if "logged_in" in session:  # Check if user is logged in
        return render_template("vedio_to_audio.html")  # Render the template if user is logged in
    else:
        return redirect(url_for("login"))  # Redirect to login page if user is not logged in



@app.route('/extract_text_from_video', methods=['POST'])
def extract_text_from_video():
    # Handle uploaded video file
    video_file = request.files['fileInput']
    video_file_path = "static/video_file.mp4"  # Save the uploaded video file
    video_file.save(video_file_path)
    # Initialize moviepy video file
    video_clip = VideoFileClip(video_file_path)

    # Extract audio file
    audio_clip = video_clip.audio
    audio_clip.write_audiofile("static/video_audio.wav")
    
    # Initialize audio file for playing separately
    audio_path = "static/video_audio.wav"

    # Implement functionality to extract text from the audio file
    # (Replace this with your actual code for text extraction)
    extracted_text = audio(audio_path)
    
    # Translate the extracted text
    language = request.form['language']
    translator = Translator()
    translated = translator.translate(extracted_text, dest=language)
    translated_text = translated.text

    # Save translated text to an audio file
    tts = gTTS(text=translated_text, lang=language, slow=False)
    audio_output_path = os.path.join("static", "video_audio_text.mp3")
    tts.save(audio_output_path)
    
    # Play the audio file
    play_audio(audio_output_path)

    # Render the template with the extracted and translated text
    return render_template('vedio_to_audio.html', translated_text=translated_text, extracted_text=extracted_text)


####### Perform speech-to-text conversion on the extracted audio  
@app.route("/audio_to_text_input")
def audio_to_text_input():
    if "logged_in" in session:  # Check if user is logged in
        return render_template("audio.html")  # Render the template if user is logged in
    else:
        return redirect(url_for("login"))  # Redirect to login page if user is not logged in


@app.route('/audio_to_text', methods=['POST'])

def audio_to_text():
    # Handle uploaded audio file
    audio_file = request.files['fileInput']
    audio_file_path = "static/audio_text_file.wav"  # Save the uploaded audio file
    audio_file.save(audio_file_path)

    
    # Implement functionality to extract text from the audio file
    extracted_text = audio(audio_file_path)
    print(type(extracted_text))
    # Translate the extracted text
    language = request.form['language']
    translator = Translator()
    translated = translator.translate(extracted_text, dest=language)
    translated_text = translated.text
    print(translated_text)

    # Save translated text to an audio file
    tts = gTTS(text=translated_text, lang=language, slow=False)
    audio_output_path = "static/audio_text.mp3"
    tts.save(audio_output_path)

    # Play the audio file
    play_audio(audio_output_path)

    return render_template('audio.html', translated_text=translated_text,extracted_text=extracted_text)

############# Convert Text to different Languages 


@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    language = request.form['language']
    
    translator = Translator()
    translated = translator.translate(text, dest=language)
    translated_text = translated.text
    
    tts = gTTS(text=translated_text, lang=language, slow=False)
    tts.save("static/text_output.mp3")
    play_audio("static/text_output.mp3")

    return render_template('index.html', translated_text=translated_text)

#########3 input as Youtube Link convert to audio-text 
@app.route("/youtube_to_audio_input")
def youtube_to_audio_input():
    if "logged_in" in session:  # Check if user is logged in
        return render_template("youtube.html")  # Render the template if user is logged in
    else:
        return redirect(url_for("login"))  # Redirect to login page if user is not logged in


@app.route('/youtube_to_audio', methods=['POST'])
def youtube_to_audio():
    youtube_link = request.form['youtubeLink']
    
    # Initialize the yt-dlp downloader
    ydl = yt_dlp.YoutubeDL()

    # Download the video
    info_dict = ydl.extract_info(youtube_link, download=True)
    print("Video downloaded successfully!")
    
    # Get the filename of the downloaded video
    video_filename = ydl.prepare_filename(info_dict)
    
    # Initialize moviepy video file
    video_clip = VideoFileClip(video_filename)

    # Extract audio file
    audio_clip = video_clip.audio
    audio_path = "static/youtube_audio.wav"
    audio_clip.write_audiofile(audio_path)

    print("Audio extracted successfully!")
    
    # # Close the video clip
    # video_clip.close()
                                                                                                                                                                        
    audio_file_path = "static/youtube_audio.wav"
    # Implement functionality to extract text from the audio file

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    
    # Function to convert audio speech to text
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio = recognizer.record(source)
            extracted_text = recognizer.recognize_google(audio)
            print("Text from video speech:", extracted_text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    #extracted_text = audio(audio_file_path)
    print(type(extracted_text))
    # Translate the extracted text
    language = request.form['language']
    translator = Translator()
    translated = translator.translate(extracted_text, dest=language)
    translated_text = translated.text
    print(translated_text)

    # Save translated text to an audio file
    tts = gTTS(text=translated_text, lang=language, slow=False)
    audio_output_path = "static/youtube_audio_text.mp3"
    tts.save(audio_output_path)

    # Play the audio file
    play_audio(audio_output_path)

    return render_template('youtube.html', translated_text=translated_text,extracted_text=extracted_text)



# Render the HTML file for home page

@app.route("/homenew")
def homenew():
    return render_template("home.html")

@app.route("/")
def homemain():
    return render_template("home.html")

@app.route("/hometrial")
def hometrial():
    return render_template("hometrial.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/home")
def home():
    if "logged_in" in session:  # Check if user is logged in
        return render_template("index.html")  # Render the template if user is logged in
    else:
        return redirect(url_for("login"))  # Redirect to login page if user is not logged in

    #return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Check if the username or email already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'Username already exists!'
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return 'Email already exists!'

        # Create a new user instance and add it to the database
        new_user = User(full_name=full_name, email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

       # return 'Registration successful!'

    #return render_template('registration.html')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            # Store the user's ID in the session
            session['user_id'] = user.id
            # # Redirect the user to the home page
            # return redirect(url_for('home'))
            #if credentials_are_valid(request.form["username"], request.form["password"]):
            session["logged_in"] = True  # Set session variable to indicate user is logged in
            return redirect(url_for("hometrial"))  # Redirect to the restricted page
            # else:
            # return render_template("login.html", error="Invalid username or password")
        else:
            message = 'Invalid username or password'
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    # Redirect the user to the login page
    return redirect(url_for('login'))


   
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# # For AWS
# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=8080)