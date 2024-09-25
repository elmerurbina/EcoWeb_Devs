# Este archivo es meramente utilizado para generar el .csv desde una carpeta .zip

import os
import pandas as pd
from PIL import Image

# Ruta de acceso al folder
dataset_path = "C:\\Users\\elmer\\PycharmProjects\\EcoWeb_Devs\\static\\dataset"


# Inicializar lista para manejar los datos
image_data = []


for root, dirs, files in os.walk(dataset_path):
    for file in files:
        if file.endswith(('png', 'jpg', 'jpeg')):
            file_path = os.path.join(root, file)

            # Cargar las imagenes
            try:
                img = Image.open(file_path)

                img_resized = img.resize((64, 64))  # Recortar todas las imagenes a 64x64 pixeles


                img_data = list(img_resized.getdata())
                img_data_flat = [pixel for sublist in img_data for pixel in sublist]  # Flatten


                label = os.path.basename(root)


                image_data.append([file, label] + img_data_flat)

            except Exception as e:
                print(f"Error processing {file_path}: {e}")

# Crear un DataFrame con Pandas
columns = ['filename', 'label'] + [f'pixel_{i}' for i in range(len(image_data[0]) - 2)]
df = pd.DataFrame(image_data, columns=columns)

# Guardar los datos en un dataset .csv
csv_path = "images_data.csv"
df.to_csv(csv_path, index=False)
# Mostrar mensaje de validacion
print(f"CSV file saved to {csv_path}")
