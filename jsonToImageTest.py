import json
from PIL import Image
import numpy as np

# Load the JSON data
with open('img2.json') as f:
    # Load the JSON data
    data = json.load(f)

# Extract the image data
image_data = data['generated_images']

# Convert the image data to a NumPy array
image_array = np.array(image_data, dtype=np.uint8)

# Reshape the array to remove the extraneous dimensions
image_array = np.squeeze(image_array)

# Create an image from the array
image = Image.fromarray(image_array)

# Save the image to a file
image.save('output.png')
