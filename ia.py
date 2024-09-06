import io
import requests
from flask import request, jsonify
from PIL import Image
from db import create_connection

def recognize_species(image_data):

    response = requests.post("YOUR_AI_MODEL_API_URL", files={"file": image_data})
    return response.json()

def recognize():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        image_data = file.read()


        species_info = recognize_species(image_data)


        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO uploads (filename, image_data, species_name, species_description) VALUES (%s, %s, %s, %s)",
            (file.filename, image_data, species_info.get('name', 'Unknown'), species_info.get('wikipedia_summary', 'No description available'))
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'species_info': species_info}), 200

    return jsonify({'error': 'File type not allowed'}), 400

def allowed_file(filename):
    allowed_extensions = {'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
