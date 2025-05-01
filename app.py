from flask import Flask, render_template, jsonify, request, send_file, session
import speech_recognition as sr
from gtts import gTTS
import os
from check import process_query
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'anirudh'  # Replace with a secure random key

# ROUTES TO HTML PAGES
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/freya')
def freya():
    return render_template('freya.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('login.html')


# SPEECH TO TEXT (GET request from browser mic)
@app.route('/speech-to-text', methods=['GET'])
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            transcription = recognizer.recognize_google(audio)
            print(f"Transcription: {transcription}")  # Debug print

            # Pass transcription to process_query
            response = process_query(transcription)
            print(response)  # Debug print

            # Save response in session
            session['response'] = response

            return jsonify({
                "transcription": transcription,
                "response": response
            })
        except sr.UnknownValueError:
            print("Could not understand the audio.")  # Debug print
            return jsonify({"transcription": "Sorry, I couldn't understand that."})
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")  # Debug print
            return jsonify({"transcription": "Speech recognition service is unavailable."})
        except Exception as e:
            print(f"Error: {str(e)}")  # Debug print
            return jsonify({"transcription": f"Error: {str(e)}"})


# TEXT TO SPEECH
@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    text = session.get('response')  # Retrieve the response from the session
    print(f"Text from session: {text}")  # Debug print
    if not text:
        return jsonify({"status": "error", "message": "No text provided"}), 400

    try:
        # Generate TTS
        tts = gTTS(text=text, lang='en')
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return send_file(audio_buffer, mimetype="audio/mpeg", as_attachment=False, download_name="freya.mp3")

    except Exception as e:
        print(f"Error in TTS: {e}")  # Debug print
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
