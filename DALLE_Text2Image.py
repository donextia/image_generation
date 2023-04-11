import streamlit as st
import openai
import requests
from PIL import Image
from io import BytesIO
import os

st.title("AInnovation - Demos")

openai.api_key = st.secrets["openai_api_key"]

# Función para realizar la solicitud a la API de DALL-E
def generar_imagen(prompt):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        
        image_url = response['data'][0]['url']
        img_data = requests.get(image_url).content
        img = Image.open(BytesIO(img_data))
        return img
    except Exception as e:
        st.write(f"Error al generar la imagen: {e}")
        return None

# Crear la aplicación Streamlit
st.title("Text2Image with DALLE-2")
st.write("Escribe un texto descriptivo para generar una imagen")

# Solicitar el prompt al usuario
prompt = st.text_input("Ingrese un prompt:")

# Si el usuario proporciona un prompt, llamar a la API de DALL-E
if prompt:
    st.write("Generando imagen...")
    imagen_generada = generar_imagen(prompt)
    
    # Mostrar la imagen generada en Streamlit
    if imagen_generada:
        st.image(imagen_generada, caption="Imagen generada por DALL-E")