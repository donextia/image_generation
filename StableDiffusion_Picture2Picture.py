import streamlit as st
import requests
import json
from PIL import Image
import io

st.title("AInnovation - Demos")

def pix_to_pix(prompt, init_image_url, image_guidance_scale, steps, guidance_scale):
    api_key = st.secrets["stable_diffusion_api_key"]

    headers = {
        "Content-Type": "application/json",
    }

    data = {
        "key": api_key,
        "prompt": prompt,
        "init_image": init_image_url,
        "image_guidance_scale": image_guidance_scale,
        "steps": steps,
        "guidance_scale": guidance_scale
    }

    response = requests.post("https://stablediffusionapi.com/api/v5/pix2pix", headers=headers, data=json.dumps(data))
    result = json.loads(response.content)

    if 'status' not in result:
        raise Exception(f"Error al generar la imagen: Respuesta inesperada de la API\n\nRespuesta completa de la API: {result}")

    if result['status'] == 'success':
        image_url = result['output']
        st.write(f"<div>Accede a tu imagen generada aqui: <a href='{image_url}' target='_blank'>{image_url}</a></div>", unsafe_allow_html=True) # Agregar esta línea para imprimir la URL en pantalla

    else:
        raise Exception(f"Error al generar la imagen: {result.get('message', 'Error desconocido')}\n\nRespuesta completa de la API: {result}")

    return image_url


def load_image_from_url(url):
    response = requests.get(url)
    img_data = response.content
    img = None
    try:
        img = Image.open(io.BytesIO(img_data))
    except:
        pass
    return img


st.title("Pix2Pix with Stable Diffusion")

prompt = st.text_input("Introduce una descripción para la imagen que quieres generar (prompt):")
init_image_url = st.text_input("Introduce la URL de una imagen de referencia:")
image_guidance_scale = st.slider("Escala de guía de imagen", 0, 10, 1)
steps = st.slider("Pasos", 1, 100, 50)
guidance_scale = st.slider("Escala de guía", 0, 10, 7)

if init_image_url:
    try:
        init_image = load_image_from_url(init_image_url)
        st.image(init_image, caption="Imagen de referencia:", use_column_width=True)
    except Exception as e:
        st.error(f"No se pudo cargar la imagen de referencia: {str(e)}")

if st.button("Generar imagen"):
    try:
        img_url = pix_to_pix(prompt, init_image_url, image_guidance_scale, steps, guidance_scale)
      
        # Obtén los datos de la imagen a partir de la URL
        img_data = requests.get(img_url).content
 
        # Muestra la imagen en Streamlit
        st.image(img_url) 
   
    except Exception as e:
        st.error(f"No se pudo generar la imagen. Error: {str(e)}")
