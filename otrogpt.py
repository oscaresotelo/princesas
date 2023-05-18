diccionario = ["\n3", "Hola\n", "Mundo", "Adiós\n"]

# Eliminar '\n' de la palabra específica y de todas las palabras que lo contengan


cadena_texto = "{"
for key, value in diccionario.items():
	cadena_texto += f"'{key}': '{value}', "
	cadena_texto = cadena_texto.rstrip(", ")
	cadena_texto += "}"

	cadena_texto = cadena_texto.replace('\n', '')

print(cadena_texto)