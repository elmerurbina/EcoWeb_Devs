"""
File to manage the functionality of the AI model to acknowledge
the name and a brief description of an animal or plant species.
"""

# Packages and Modules
import csv
from PIL import Image
from flask import request, jsonify
import imagehash
from io import BytesIO
from models.ai_model import create_connection

# Class to handle AI functionalities
class SpeciesRecognizer:
    def __init__(self):
        self.species_data = []
        self.dataset_path = 'C:/Users/elmer/PycharmProjects/EcoWeb_Devs/dataset.csv'
        self.load_dataset()

    def load_dataset(self):
        """Loads species data from the dataset.csv file."""
        try:
            with open(self.dataset_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    image_path = row['image_path']
                    species_name = row['species_name']
                    species_description = row['species_description']
                    image_hash_value = imagehash.average_hash(Image.open(image_path))

                    self.species_data.append({
                        'image_path': image_path,
                        'species_name': species_name,
                        'species_description': species_description,
                        'image_hash': image_hash_value
                    })
        except FileNotFoundError:
            print(f"Dataset file not found at path: {self.dataset_path}")
        except Exception as e:
            print(f"Error loading dataset: {e}")

    def recognize_species(self, image_data):
        """Recognizes the species by comparing image hashes."""
        try:
            uploaded_image = Image.open(BytesIO(image_data))
            uploaded_image_hash = imagehash.average_hash(uploaded_image)

            for species in self.species_data:
                # Allows small differences
                if uploaded_image_hash - species['image_hash'] < 5:
                    return {
                        'name': species['species_name'],
                        'description': species['species_description']
                    }
        except Exception as e:
            print(f"Error recognizing species: {e}")

        # If there are no images like the provided on the dataset show a default message
        return {
            'name': 'Lo sentimos, esta imagen no está dentro de nuestro dataset!',
            'description': 'No hay descripción disponible'
        }

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    allowed_extensions = {'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def recognize():
    """Handle the uploaded image and perform species recognition."""
    if 'file' not in request.files:
        print("No file part in request")
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        print("No selected file")
        return jsonify({'error': 'No selected file'}), 400

    print(f"File received: {file.filename}")

    if file and allowed_file(file.filename):
        image_data = file.read()

        # Instantiate SpeciesRecognizer and recognize species
        recognizer = SpeciesRecognizer()
        species_info = recognizer.recognize_species(image_data)

        # Save to database using the stored procedure
        try:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.callproc(
                'insert_species_data',
                (file.filename, image_data, species_info.get('name', 'Unknown'),
                 species_info.get('description', 'No description available'))
            )
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({'error': 'Database error'}), 500

        return jsonify({'species_info': species_info}), 200

    print("File type not allowed")
    return jsonify({'error': 'File type not allowed'}), 400
