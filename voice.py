""" file for voice generation """
import elevenlabs
import api_keys
import utils
import os

API_KEY = api_keys.elevenlabs_api_key
elevenlabs.set_api_key(API_KEY)

VOICE = "british_male"

MODEL = "eleven_multilingual_v2"  # eleven_multilingual_v2 or eleven_turbo_v2

AUDIO_FILE_DIR = "./secret/voices/"

def get_speech(text: str, voice: str = VOICE) -> str:
    """Generate speech from text and returns path to audio file."""
    try:
        audio = elevenlabs.generate(
            text=text,
            voice=voice,
            model=MODEL,
        )
        # make dir if not exist
        if not os.path.exists(AUDIO_FILE_DIR):
            os.makedirs(AUDIO_FILE_DIR)

        file_path = os.path.join(AUDIO_FILE_DIR, f"{utils.get_unique_str()}.mp3")
        elevenlabs.save(audio, file_path)
    except:
        raise Exception("Could not generate speech.")
    
    return file_path
        

if __name__ == "__main__":
    get_speech(
        "This week we will go through the overview of the course, instructional plan, policies and procedures and the eConestoga setup.   Once completed, we will get started with an introduction and key terms to networking."
    )

    #voices = elevenlabs.voices()

    #print(voices[1].name)
