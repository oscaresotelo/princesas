import speech_recognition as sr
import epitran

# Initialize Epitran for English
epi = epitran.Epitran("spa-Latn")

# Initialize the speech recognizer
r = sr.Recognizer()

# Set the source of audio input
mic = sr.Microphone()

# Function to transcribe audio
def transcribe_audio():
    with mic as source:
        print("Listening...")

        # Adjust for ambient noise levels
        r.adjust_for_ambient_noise(source)

        # Record the audio
        audio = r.listen(source)

    print("Transcribing...")

    # Use the speech recognition library to convert speech to text
    try:
        text = r.recognize_google(audio, language = "es-AR")
        print("Original text:", text)

        # Transliterate the text using Epitran
        translit_text = epi.transliterate(text)
        print("Transliterated text:", translit_text)

    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Speech Recognition service; {0}".format(e))

# Call the function to start transcription
transcribe_audio()
