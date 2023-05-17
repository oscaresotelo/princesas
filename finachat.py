import asyncio
from EdgeGPT import Chatbot, ConversationStyle
import re
import json
import time

async def main():
    start_time = time.time()
    bot = await Chatbot.create(cookie_path='./cookies.json')
    diccionario = await bot.ask(prompt="resumir el siguiente link https://es.wikipedia.org/wiki/Antiperuanismo,  en español ", conversation_style=ConversationStyle.creative)
   
    cadena_texto = "{"
    for key, value in diccionario.items():
        cadena_texto += f"'{key}': '{value}', "
    cadena_texto = cadena_texto.rstrip(", ")
    cadena_texto += "}"

    # Imprimir la cadena de texto resultante
    
    cadena_texto = cadena_texto.replace('\n', '')
    cadena_texto = re.sub(r'\[\^.\^\]', '', cadena_texto)
    start = "'Keyboard'}, {'text': '"
    end = "', 'author':"
    result = cadena_texto.split(start)[1].split(end)[0]
    print(result)
    elapsed_time = time.time() - start_time
    print(f"Tiempo transcurrido: {elapsed_time} segundos")
    # with open('datos.txt', 'w') as f:
    #     f.write(json.dumps(result))
    # await bot.close()

if __name__ == "__main__":
    asyncio.run(main())



