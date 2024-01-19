from elevenlabs import generate
import configparser

voiceoverDir = "Voiceovers"

config = configparser.ConfigParser()
config.read('config.ini')
API_KEY = config["ElevenLabs"]["API_KEY"]

def create_voice_over(fileName, text):
    filePath = f"{voiceoverDir}/{fileName}.mp3"
    audio = generate(
        text=text,
        voice="Callum",
        model="eleven_multilingual_v2",
        api_key=API_KEY
    )

    with open(filePath, "wb") as audio_file:
        audio_file.write(audio)

    return filePath