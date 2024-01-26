import elevenlabs
import elevenlabs 
import api_keys

API_KEY = api_keys.elevenlabs_api_key
elevenlabs.set_api_key(API_KEY)

MODEL = 'eleven_multilingual_v2' # eleven_multilingual_v2 or eleven_turbo_v2

AUDIO_FILE_NAME = './secret/audio/voice.mp3'

def get_speech(text: str, voice: str = 'british_male') -> bool:
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
    
    #get_speech('test')
    
    voices = elevenlabs.voices()
    #print only voice name
    
    print(voices[1].name)
