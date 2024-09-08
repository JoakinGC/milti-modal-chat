import requests
import base64
from docx import Document
from PIL import Image
from PIL import ImageDraw, ImageFont
import io
import json
import time

# Configuración
API_URL = "https://api-inference.huggingface.co/models/impira/layoutlm-invoices"
headers = {"Authorization": "Bearer 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"}

def docx_to_images(file_path):
    # Cargar el documento DOCX
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    
    # Crear una imagen suficientemente grande para contener el texto
    img = Image.new('RGB', (1200, 1600), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Utilizar una fuente más apropiada
    try:
        font = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        font = ImageFont.load_default()

    # Escribir el texto en la imagen, ajustando el salto de línea
    margin = 10
    offset = 10
    for line in text.split('\n'):
        draw.text((margin, offset), line, font=font, fill=(0, 0, 0))
        offset += draw.textbbox((margin, offset), line, font=font)[3] - draw.textbbox((margin, offset), line, font=font)[1] + 5  # espacio entre líneas
    
    # Guardar la imagen en bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    
    return [img_bytes.getvalue()]

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def fetch_result_with_retry(file_path, question, max_retries=5):
    retries = 0
    while retries < max_retries:
        if file_path.endswith(".docx"):
            images = docx_to_images(file_path)
        else:
            raise ValueError("Formato de archivo no soportado. Usa PDF o DOCX.")
        
        for image in images:
            img_base64 = base64.b64encode(image).decode("utf-8")

            payload = {
                "inputs": {
                    "image": img_base64,
                    "question": question
                }
            }

            response = query(payload)
            
            if "error" in response:
                if "loading" in response["error"]:
                    estimated_time = response.get("estimated_time", 10)  # tiempo por defecto si no está disponible
                    print(f"El modelo está cargando. Esperando {estimated_time} segundos antes de reintentar...")
                    time.sleep(estimated_time)
                    retries += 1
                else:
                    print(f"Error en la consulta: {response['error']}")
                    return None
            else:
                return response

    print("Superado el número máximo de reintentos.")
    return None

def fetch_result_with_image(image_path, question, max_retries=5):
    retries = 0
    while retries < max_retries:
        with open(image_path, "rb") as f:
            img = f.read()
            img_base64 = base64.b64encode(img).decode("utf-8")

        payload = {
            "inputs": {
                "image": img_base64,
                "question": question
            }
        }

        response = query(payload)

        if "error" in response:
            if "loading" in response["error"]:
                estimated_time = response.get("estimated_time", 10)  # tiempo por defecto si no está disponible
                print(f"El modelo está cargando. Esperando {estimated_time} segundos antes de reintentar...")
                time.sleep(estimated_time)
                retries += 1
            else:
                print(f"Error en la consulta: {response['error']}")
                return None
        else:
            return response

    print("Superado el número máximo de reintentos.")
    return None

def main(file_path, question):
    result = fetch_result_with_retry(file_path, question)
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("No se pudo obtener una respuesta del modelo.")

# Ejemplo de uso con documento DOCX
#main("prueba.docx", "What is this document about?")

# Ejemplo de uso con imagen directamente
result = fetch_result_with_image("prueba2.png", "¿De que trata de este documento? ¿y que es una clausula?")
if result:
    print(json.dumps(result, indent=2))
    print(result)
else:
    print("No se pudo obtener una respuesta del modelo.")
