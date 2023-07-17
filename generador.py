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
import sqlite3
from sydney import SydneyClient
os.environ["BING_U_COOKIE"] = "<your-cookie>"


conn = sqlite3.connect('codigopython.db')
c = conn.cursor()

# Crear la tabla si no existe
c.execute('''CREATE TABLE IF NOT EXISTS codigo
             (nombre TEXT, scriptcodigo TEXT)''')
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

class SessionState:
    def __init__(self):
        self.codigo = ""

def get_session_state():
    if 'session_state' not in st.session_state:
        st.session_state.session_state = SessionState()
    return st.session_state.session_state

def guardar_codigo(nombre, codigo):
    c.execute("INSERT INTO codigo (nombre, scriptcodigo) VALUES (?, ?)", (nombre, codigo))
    conn.commit()

def extract_python_code(text):

    
    if "```python" in text:
        pattern = r"```python(.*?)```"
    else:
        pattern = r"```(.*?)```"
        
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    else:
        return ""

async def main(prompt) -> None:

    async with SydneyClient() as sydney:
        response =  await sydney.compose(prompt)
        return(response)


st.title("Ingresa tu Pregunta")
session_state = get_session_state()
    
    # if "codigo" not in st.session_state:
    #     st.session_state.codigo = ""
start_time = time.time()
# bot = await Chatbot.create(cookie_path='./cookies.json')
    
    # session_state = SessionState(download_button=False)
   
    
    # show_pages([
    #     Page("finita.py", "Ingresar Preguntas"),
    #     Page("fina2.py", "Cargar Foto Tarea", ":notebook:"),
    #     Page("generar.py", "Crear Solucion", ":notebook:"),
    #     Page("ejecutarcodigo.py", "Soluciones Creadas", ":notebook:"),
    # ])
nombre = st.text_input("Nombre de la Aplicacion:")
if st.button("Guardar Aplicacion"):
        
       
    with st.spinner('Guardando Código en la Base de Datos...'):
        if len(st.session_state.codigo.strip()) == 0:
                st.warning("El código está vacío. No se guardará nada.")
        elif len(nombre.strip()) == 0:
            st.warning("Por favor, ingrese un nombre para el código.")
        else:
            guardar_codigo(nombre, st.session_state.codigo)
            st.success("Código guardado exitosamente en la base de datos.")
    # improve = """import streamlit as st, import io, escribir directamemte el codigo , no explicar,importar y controlar que se hayan importado correctamente,IMPORTANTE RECORDAR QUE El objeto 'DataFrame' no tiene el atributo 'append',
    #             as librerias necesarias para que el codigo
    #             no genere errores,IMPORTANTE GENERAR EL CODIGO EN UN SOLO ARCHIVO, Estructurawr aplicación para mejorar 
    #             su mantenibilidad y escalabilidad,Desarrollando interfaces de usuario avanzadas con funciones de UI renderizadas por st.session_state
    #             Creando elementos de UI reutilizables para varias páginas,  Agregando estilos limitados con lenguajes markdown y componentes estáticos de Streamlit
    #             Colocando elementos de Streamlit de forma programática,IMPORTANTE RECORDAR QUE El objeto 'DataFrame' no tiene el atributo 'append', importar libreria base64 para generar link de descargar,
    #             debes trabajar con la libreria pandas actualizada, IMPORTANTE ESCRIBIR EL CODIGO EN UN SOLO ARCHIVO, recordar que streamlit no usa 
    #   ,USAR COMILLAS SIMPLES PARA DELIMITAR TEXTO,
    #             REALIZAR EL SIGUIENTE  PEDIDO: """
improve = """import streamlit as st, import base64, actua como desarrollador senior de streamlit, IMPORTANTE USAR BIBLIOTECA ACTUALIZADA DE  pandas, 
usar loc en lugar de append, 
el pedido es el siguiente:  """
texto = st.text_area("", height=275)
prompt = improve + texto 
    
    
if st.button("Generar"):
    with st.spinner('Procesando Solicitud...'):
        diccionario = asyncio.run(main(prompt))
       
            # cadena_texto = "{"
            # for key, value in diccionario.items():
            #     cadena_texto += f"'{key}': '{value}', "
            # cadena_texto = cadena_texto.rstrip(", ")
            # cadena_texto += "}"

            # cadena_texto = cadena_texto.replace('\n', '')
            # cadena_texto = cadena_texto.replace('\n\n', '')
            # cadena_texto = cadena_texto.replace('\n\n', '')
            # cadena_texto = cadena_texto.replace('**', '')
            # cadena_texto = cadena_texto.replace("\n-", "")
            # cadena_texto = cadena_texto.replace("\'", "'")
            # cadena_texto = cadena_texto.replace("Hola, este es Bing.", "")
            # cadena_texto = cadena_texto.replace("</strong>", "</strong><br>")
            # cadena_texto = re.sub(r'\\n', '\n', cadena_texto)
            # cadena_texto = re.sub(r'\[\^.\^\]', '', cadena_texto)
            # start = "'Keyboard'}, {'text': '"
            # end = "', 'author':"
            # cadena_texto = cadena_texto.replace('</strong>', '</strong><br>')
            # result = cadena_texto.split(start)[1].split(end)[0]
            # start = "'Keyboard'}, {'text': '"
            # end = "', 'author':"
            # cadena_texto = cadena_texto.replace('</strong>', '</strong><br>')
            # # st.write(cadena_texto)

            # result = cadena_texto.split(start)[1].split(end)[0]
            
            # resultado = st.write(result)
        st.session_state.codigo = (extract_python_code(diccionario))
        
        elapsed_time = time.time() - start_time
            
        st.write(f"Tiempo transcurrido: {elapsed_time} segundos")   
exec(st.session_state.codigo, globals())
    

