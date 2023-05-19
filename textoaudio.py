# import streamlit as st
# import pyttsx3

# def main():
#     st.title("Aplicación de Texto a Voz")

#     # Obtén el texto de entrada del usuario
#     input_text = st.text_input("Ingresa el texto para convertir a voz")

#     # Crea un botón para convertir el texto a voz
#     if st.button("Convertir a Voz"):
#         # Crea un motor de texto a voz
#         engine = pyttsx3.init()

#         # Configura el idioma del motor como español
#         engine.setProperty("voice", "spanish-latin-am")
#         rate = engine.getProperty("rate")
#         engine.setProperty("rate", rate = 50)
#         # Establece el texto de entrada como discurso
#         engine.say(input_text)

#         # Reproduce el discurso
#         engine.runAndWait()

# if __name__ == "__main__":
#     main()
import streamlit as st
from gtts import gTTS
import tempfile
import os

# Configurar idioma
language = 'es'

# Función para generar el audio a partir del texto
def text_to_speech(text):
    tts = gTTS(text=text, lang="es", tld='us')
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    tts.save(temp_file.name)
    return temp_file.name

# Configuración de la aplicación Streamlit
st.title("Texto a Audio")

# Input de texto
text = st.text_area("Ingrese el texto en español", "")

# Botón para generar el audio
if st.button("Generar audio"):
    if text:
        # Generar el audio
        audio_file = text_to_speech(text)

        # Reproducir el audio
        st.audio(audio_file, format='audio/mp3')
        
        # Eliminar el archivo temporal
        os.remove(audio_file)
    else:
        st.warning("Por favor, ingrese texto")
