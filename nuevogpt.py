# import re

# # Abrir el archivo datos.txt en modo lectura
# with open('datos.txt', 'r') as f:
#     data = f.read()

# start = "'Keyboard'}, {'text': '"
# end = "', 'author':"

# result = data.split(start)[1].split(end)[0]
# resultnuevo = result.replace(['\n\n', "["] , ["",""])
# with open('respuesta.txt', 'w') as f:
#     f.write(resultnuevo)


import re

# Abrir el archivo datos.txt en modo lectura
with open('datos.txt', 'r') as f:
    data = f.read()

# Reemplazar los caracteres \n\n por vacío
data = data.replace('\n', '')

# Reemplazar los caracteres [^1^], [^2^] y [^3^] por vacío
data = re.sub(r'\[\^.\^\]', '', data)

start = "'Keyboard'}, {'text': '"
end = "', 'author':"

result = data.split(start)[1].split(end)[0]

with open('respuesta.txt', 'w') as f:
    f.write(result)


