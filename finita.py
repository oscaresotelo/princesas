import asyncio
import streamlit as st
import docx
from io import BytesIO
from EdgeGPT import Chatbot, ConversationStyle
import re
import json
import time
import base64
from st_pages import Page, show_pages, add_page_title
from gtts import gTTS
import tempfile
import os

# st.set_page_config(page_title="Gpt-AutoSustentable", page_icon=":memo:")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """


st.set_page_config(page_title="Gpt-AutoSustentable", page_icon=":memo:")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css("estilos.css")
class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def text_to_speech(text):
    tts = gTTS(text=text, lang="es", tld='us')
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    tts.save(temp_file.name)
    return temp_file.name

def download_file(data, filename, file_format):
    if file_format == "txt":
        b64 = base64.b64encode(data.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">Haz clic aquí para descargar el archivo</a>'
    elif file_format == "docx":
        doc = docx.Document()
        doc.add_paragraph(data)
        doc_bytes = BytesIO()
        doc.save(doc_bytes)
        b64 = base64.b64encode(doc_bytes.getvalue()).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}" download="{filename}">Haz clic aquí para descargar el archivo en formato WORD</a>'
    else:
        return None
    return href

async def main():
    start_time = time.time()
    bot = await Chatbot.create(cookie_path='./cookies.json')
    
    session_state = SessionState(download_button=False)
    st.title("Ingresa tu Pregunta")
    show_pages([
        Page("finita.py", "Ingresar Preguntas"),
        Page("fina2.py", "Cargar Foto Tarea", ":notebook:"),
        Page("generador.py", "Crear Solucion", ":notebook:"),
        Page("ejecutarcodigo.py", "Soluciones Creadas", ":notebook:"),
        ])
    prompt = st.text_area("", height=275)
    
    if st.button("Preguntar"):
        with st.spinner('Procesando pregunta...'):
            diccionario = await bot.ask(prompt=prompt, conversation_style=ConversationStyle.creative)
           
            cadena_texto = "{"
            for key, value in diccionario.items():
                cadena_texto += f"'{key}': '{value}', "
            cadena_texto = cadena_texto.rstrip(", ")
            cadena_texto += "}"

            cadena_texto = cadena_texto.replace('\n', '')
            cadena_texto = cadena_texto.replace('\n\n', '')
            cadena_texto = cadena_texto.replace('\n\n', '')
            cadena_texto = cadena_texto.replace('**', '')
            cadena_texto = cadena_texto.replace("\n-", "")
            cadena_texto = cadena_texto.replace("Hola, este es Bing.", "")
            cadena_texto = cadena_texto.replace("</strong>", "</strong><br>")
            cadena_texto = re.sub(r'\\n', '\n', cadena_texto)
            cadena_texto = re.sub(r'\[\^.\^\]', '', cadena_texto)
            start = "'Keyboard'}, {'text': '"
            end = "', 'author':"
            cadena_texto = cadena_texto.replace('</strong>', '</strong><br>')
            result = cadena_texto.split(start)[1].split(end)[0]
            start = "'Keyboard'}, {'text': '"
            end = "', 'author':"
            cadena_texto = cadena_texto.replace('</strong>', '</strong><br>')
            result = cadena_texto.split(start)[1].split(end)[0]

            resultado = st.write(result)
            sample_rate = 44100
            audio_file = text_to_speech(result)
            st.audio(audio_file, format='audio/mp3')
            elapsed_time = time.time() - start_time
            os.remove(audio_file)
            st.write(f"Tiempo transcurrido: {elapsed_time} segundos")   

            if not session_state.download_button:
                session_state.download_button = True
                # Descargar como archivo de texto
                href_txt = download_file(result, "resultado.txt", "txt")
                st.markdown(href_txt, unsafe_allow_html=True)

                # Descargar como archivo de Word
                href_docx = download_file(result, "resultado.docx", "docx")
                st.markdown(href_docx, unsafe_allow_html=True)

if __name__ == "__main__":
    asyncio.run(main())