import csv
from PIL import Image
from flask import request, jsonify
import imagehash
from io import BytesIO
from db import create_connection

# Cargar el dataset
species_data = []

# Funcion para cargar el dataser
def load_dataset():
    global species_data
    with open('dataset.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            species_data.append({
                'image_path': row['image_path'],
                'species_name': row['species_name'],
                'species_description': row['species_description'],
                'image_hash': imagehash.average_hash(Image.open(row['image_path']))
            })

# Call this function once when the app starts to load the dataset
load_dataset()

# Function to recognize the species by comparing image hashes
def recognize_species(image_data):
    uploaded_image = Image.open(BytesIO(image_data))
    uploaded_image_hash = imagehash.average_hash(uploaded_image)

    # Compare the uploaded image hash with each image in the dataset
    for species in species_data:
        if uploaded_image_hash - species['image_hash'] < 5:  # Allow slight differences
            return {
                'name': species['species_name'],
                'description': species['species_description']
            }

    return {'name': 'Lo sentimos, esta imagen no esta dentro de nuestro dataset!', 'description': 'No hay descripcion disponible'}

# Route to handle image upload and species recognition
def recognize():
    if 'file' not in request.files:
        print("No file part in request")  # Debugging
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        print("No selected file")  # Debugging
        return jsonify({'error': 'No selected file'}), 400

    # Debugging: Print file details
    print(f"File received: {file.filename}")

    if file and allowed_file(file.filename):
        image_data = file.read()

        # Call your function to recognize species
        species_info = recognize_species(image_data)

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ia (filename, image_data, species_name, species_description) VALUES (%s, %s, %s, %s)",
            (file.filename, image_data, species_info.get('name', 'Unknown'), species_info.get('description', 'No description available'))
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'species_info': species_info}), 200

    print("File type not allowed")  # Debugging
    return jsonify({'error': 'File type not allowed'}), 400

def allowed_file(filename):
    allowed_extensions = {'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
