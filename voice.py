""" file for voice generation """
import elevenlabs
import api_keys

API_KEY = api_keys.elevenlabs_api_key
elevenlabs.set_api_key(API_KEY)

VOICE = 'voice_a'

MODEL = "eleven_multilingual_v2"  # eleven_multilingual_v2 or eleven_turbo_v2

AUDIO_FILE_NAME = "./secret/voice.mp3"


def get_speech(text: str, voice: str = VOICE) -> bool:
    """Generate speech from text and save to AUDIO_FILE_NAME."""
    try:
        audio = elevenlabs.generate(
            text=text,
            voice=voice,
            model=MODEL,
        )
        elevenlabs.save(audio, AUDIO_FILE_NAME)
    except Exception as e:
        print(e)
        return False
    return True


if __name__ == "__main__":
    get_speech('This week we will go through the overview of the course, instructional plan, policies and procedures and the eConestoga setup.   Once completed, we will get started with an introduction and key terms to networking.')

    voices = elevenlabs.voices()
    # print only voice name

    print(voices[1].name)
