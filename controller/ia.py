# Archivo para manejar la funcionalidad del reconocimiento de imagenes con IA

# Librerias y modulos
import csv
from PIL import Image
from flask import request, jsonify
import imagehash
from io import BytesIO
from models.db import create_connection

# Cargar el dataset
species_data = []

# Funcion para cargar el dataset
def load_dataset():
    global species_data
    dataset_path = 'C:/Users/elmer/PycharmProjects/EcoWeb_Devs/dataset.csv'
    with open(dataset_path, newline='', encoding='utf-8') as csvfile:
        # Your code here

        reader = csv.DictReader(csvfile)
        for row in reader:
            species_data.append({
                'image_path': row['image_path'], # Ruta de la imagen
                'species_name': row['species_name'], # Nombre de la especie
                'species_description': row['species_description'], # Descripcion de la especie
                'image_hash': imagehash.average_hash(Image.open(row['image_path'])) # Usado para comparar las imagenes
            })

# Llamar la funcion una vez se el programa comience a cargar el dataset
load_dataset()

# Reconocer las especies mediante comparacion de imaganes utilizando hashes
def recognize_species(image_data):
    uploaded_image = Image.open(BytesIO(image_data))
    uploaded_image_hash = imagehash.average_hash(uploaded_image)

    # Compara la imagen subida con cada una de las imagenes que existen en el dataset
    for species in species_data:
        if uploaded_image_hash - species['image_hash'] < 5:  # Permite pequenias diferencias
            return {
                # Si la imagen existe retornar el nombre y la descripcion
                'name': species['species_name'],
                'description': species['species_description']
            }

    # Si la imagen no existe retornar un mensaje por default
    return {'name': 'Lo sentimos, esta imagen no esta dentro de nuestro dataset!', 'description': 'No hay descripcion disponible'}

# Funcion para manejar la imagen que sube el usuario y el reconocimiento de esta
def recognize():
    if 'file' not in request.files:
        print("No file part in request")  # Esta linea es meramente depuracion
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        print("No selected file")  # Esta linea es meramente depuracion
        return jsonify({'error': 'No selected file'}), 400

    # Esta linea es meramente depuracion para saber si la imagen se subio correctamente
    print(f"File received: {file.filename}")

    if file and allowed_file(file.filename):
        image_data = file.read()

        # Llamar la funcion para reconocer la imagen mediante hashes
        species_info = recognize_species(image_data)

        # Crear conexion con la base de datos
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            # Guardar la imagen y los datos como el nombre y la descripcion en la base de datos
            "INSERT INTO ia (filename, image_data, species_name, species_description) VALUES (%s, %s, %s, %s)",
            (file.filename, image_data, species_info.get('name', 'Unknown'), species_info.get('description', 'No description available'))
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'species_info': species_info}), 200

    print("File type not allowed")  # Debugging
    return jsonify({'error': 'File type not allowed'}), 400

# Funcion para definir las extensiones o archivos permitidos
def allowed_file(filename):
    allowed_extensions = {'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
