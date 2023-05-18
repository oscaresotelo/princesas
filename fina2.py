import asyncio
import streamlit as st
from EdgeGPT import Chatbot, ConversationStyle
import re
import json
import time
import base64
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# st.set_page_config(page_title="Gpt-AutoSustentable", page_icon=":memo:")
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
st.title("Gpt-AutoSustentable")





async def main():

    start_time = time.time()
    bot = await Chatbot.create(cookie_path='./cookies.json')
    
    session_state = SessionState(download_button=False)
    st.title("Ingresa tu Pregunta")
    
    


    
    # prompt = st.text_input("")
    st.sidebar.title("Seleccionar Foto De La Tarea")
    imagem = st.sidebar.file_uploader("", type=["png","jpg"])
        #se selecionar alguma imagem...
    if imagem:
        img = Image.open(imagem)
        
        st.sidebar.info("Foto Cargada")
        st.sidebar.image(img, width=350)
        st.info("Por Favor Solo Dejar las Preguntas")
            
        texto = pytesseract.image_to_string(img, lang="spa")
        
        #prompt = st.write("{}".format(texto))
        
        textoprocesado = texto
        preguntas = st.text_area("Editar La Pregunta:",textoprocesado, height=275)
        if st.button("Preguntar"):

            with st.spinner('Procesando pregunta...'):
                
                # time.sleep(1)
                
                diccionario = await bot.ask(prompt= preguntas, conversation_style=ConversationStyle.creative)

                cadena_texto = "{"
                for key, value in diccionario.items():
                    cadena_texto += f"'{key}': '{value}', "
                cadena_texto = cadena_texto.rstrip(", ")
                cadena_texto += "}"

                # cadena_texto = cadena_texto.replace('\n', '')
                # cadena_texto = cadena_texto.replace("Hola, este es Bing.", "")
                cadena_texto = cadena_texto.replace("Hola, este es Bing.", "")
                cadena_texto = cadena_texto.replace("</strong>", "</strong><br>")
                cadena_texto = re.sub(r'\[\^.\^\]', '', cadena_texto)
                start = "'Keyboard'}, {'text': '"
                end = "', 'author':"
                cadena_texto = cadena_texto.replace('</strong>', '</strong><br>')
                result = cadena_texto.split(start)[1].split(end)[0]

                st.write(result)

                elapsed_time = time.time() - start_time
                st.write(f"Tiempo transcurrido: {elapsed_time} segundos")

                if not session_state.download_button:
                    session_state.download_button = True
                    download_data = base64.b64encode(result.encode()).decode()
                    href = f'<a href="data:file/txt;base64,{download_data}" download="resultado.txt">Haz clic aquí para descargar la informacion</a>'
                    st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    asyncio.run(main())
