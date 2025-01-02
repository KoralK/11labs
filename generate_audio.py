import requests
import dropbox
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_audio():
    API_URL = "https://api.elevenlabs.io/v1/text-to-speech/oWAxZDx7w5VEj9dCyTzz"
    API_KEY = os.getenv("ELEVEN_API_KEY")  # Retrieve API key

    if not API_KEY:
        raise ValueError("ELEVEN_API_KEY is not set")

    payload = {
        "text": "Hello from GitHub Codespaces!"
    }

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        with open("GeneratedAudio.mp3", "wb") as f:
            f.write(response.content)
        print("Audio generated successfully!")
    else:
        print(f"Failed to generate audio: {response.status_code}, {response.text}")
        return False

    return "GeneratedAudio.mp3"

def upload_to_dropbox(file_path):
    ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")  # Retrieve access token
    if not ACCESS_TOKEN:
        raise ValueError("DROPBOX_ACCESS_TOKEN is not set")

    DROPBOX_PATH = "/n8n_audio_uploads/GeneratedAudio.mp3"
    dbx = dropbox.Dropbox(ACCESS_TOKEN)

    with open(file_path, "rb") as f:
        dbx.files_upload(f.read(), DROPBOX_PATH, mode=dropbox.files.WriteMode.overwrite)

    print("File uploaded to Dropbox successfully!")

if __name__ == "__main__":
    audio_file = generate_audio()
    if audio_file:
        upload_to_dropbox(audio_file)