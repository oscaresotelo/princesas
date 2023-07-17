import streamlit as st
import pandas as pd
import base64

# Definir función para crear DataFrame de empleados
def crear_df_empleados():
    # Crear lista vacía para guardar los datos
    datos = []
    # Crear un bucle para pedir los datos al usuario
    while True:
        # Mostrar un título
        st.subheader(\'Ingrese los datos del empleado\')
        # Crear campos de entrada para cada dato
        nombre = st.text_input(\'Nombre\')
        apellido = st.text_input(\'Apellido\')
        edad = st.number_input(\'Edad\', min_value=18, max_value=100)
        salario = st.number_input(\'Salario\', min_value=0, max_value=1000000)
        # Crear un botón para agregar el empleado al DataFrame
        agregar = st.button(\'Agregar empleado\')
        # Si el botón se presiona, validar los datos y agregarlos a la lista
        if agregar:
            # Validar que los campos no estén vacíos
            if nombre and apellido and edad and salario:
                # Crear un diccionario con los datos del empleado
                empleado = {\'Nombre\': nombre, \'Apellido\': apellido, \'Edad\': edad, \'Salario\': salario}
                # Agregar el diccionario a la lista
                datos.append(empleado)
                # Mostrar un mensaje de éxito
                st.success(f\'Empleado {nombre} {apellido} agregado correctamente.\')
            else:
                # Mostrar un mensaje de error
                st.error(\'Por favor, complete todos los campos.\')
        # Crear un botón para finalizar el ingreso de datos
        finalizar = st.button(\'Finalizar\')
        # Si el botón se presiona, salir del bucle
        if finalizar:
            break
    # Crear un DataFrame con la lista de datos
    df_empleados = pd.DataFrame(datos)
    # Retornar el DataFrame
    return df_empleados

# Definir función para mostrar el DataFrame de empleados
def mostrar_df_empleados(df_empleados):
    # Mostrar un título
    st.subheader(\'Lista de empleados\')
    # Mostrar el DataFrame en una tabla
    st.dataframe(df_empleados)
    # Crear un botón para descargar el DataFrame como CSV
    descargar = st.button(\'Descargar como CSV\')
    # Si el botón se presiona, generar un link de descarga
    if descargar:
        # Convertir el DataFrame a CSV y codificarlo en base64
        csv = df_empleados.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        # Crear el link de descarga con el contenido codificado
        href = f\'<a href="data:file/csv;base64,{b64}" download="empleados.csv">Descargar CSV</a>\'
        # Mostrar el link usando markdown
        st.markdown(href, unsafe_allow_html=True)

# Definir función principal de la aplicación
def main():
    # Mostrar un título principal
    st.title(\'Aplicación para dar de alta empleados\')
    # Crear una barra lateral con opciones de navegación
    menu = st.sidebar.selectbox(\'Seleccione una opción\', [\'Inicio\', \'Crear empleados\', \'Ver empleados\'])
    # Si se selecciona la opción Inicio, mostrar una introducción
    if menu == \'Inicio\':
        st.markdown(\'Bienvenido a esta aplicación para dar de alta empleados. Puede usar el menú de la izquierda para navegar entre las opciones disponibles.\')
    # Si se selecciona la opción Crear empleados, llamar a la función para crear el DataFrame de empleados
    elif menu == \'Crear empleados\':
        # Si no existe el estado de la aplicación, crearlo con un DataFrame vacío
        if \'df_empleados\' not in st.session_state:
            st.session_state.df_empleados = pd.DataFrame()
        # Llamar a la función para crear el DataFrame de empleados y asignarlo al estado de la aplicación
        st.session_state.df_empleados = crear_df_empleados()
    # Si se selecciona la opción Ver empleados, llamar a la función para mostrar el DataFrame de empleados
    elif menu == \'Ver empleados\':
        # Si existe el estado de la aplicación, llamar a la función para mostrar el DataFrame de empleados
        if \'df_empleados\' in st.session_state:
            mostrar_df_empleados(st.session_state.df_empleados)
        # Si no existe el estado de la aplicación, mostrar un mensaje de advertencia
        else:
            st.warning(\'No hay empleados registrados. Por favor, vaya a la opción Crear empleados para ingresar los datos.\')

# Llamar a la función principal de la aplicación
if __name__ == \'__main__\':
    main()