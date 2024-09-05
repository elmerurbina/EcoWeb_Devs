import os
import pandas as pd
from PIL import Image

# Path to your dataset folder
dataset_path = "C:\\Users\\elmer\\PycharmProjects\\EcoWeb_Devs\\static\\dataset"


# Initialize a list to hold data
image_data = []

# Loop through folders and files
for root, dirs, files in os.walk(dataset_path):
    for file in files:
        if file.endswith(('png', 'jpg', 'jpeg')):
            file_path = os.path.join(root, file)

            # Load image
            try:
                img = Image.open(file_path)
                # Optional: Resize or preprocess image if necessary
                img_resized = img.resize((64, 64))  # Resize all images to 64x64 pixels

                # Convert image to a flattened array (Optional for pixel data)
                img_data = list(img_resized.getdata())
                img_data_flat = [pixel for sublist in img_data for pixel in sublist]  # Flatten

                # Get label from folder name or filename (depending on your organization)
                label = os.path.basename(root)  # Assumes folder name is the label

                # Append image file path, label, and optionally image data
                image_data.append([file, label] + img_data_flat)

            except Exception as e:
                print(f"Error processing {file_path}: {e}")

# Create a pandas DataFrame
# Modify this if you don't want pixel data and only file paths/labels
columns = ['filename', 'label'] + [f'pixel_{i}' for i in range(len(image_data[0]) - 2)]
df = pd.DataFrame(image_data, columns=columns)

# Save to CSV
csv_path = "images_data.csv"
df.to_csv(csv_path, index=False)
print(f"CSV file saved to {csv_path}")
