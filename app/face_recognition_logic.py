import requests
from PIL import Image
import numpy as np
import face_recognition
from io import BytesIO

def process_images_from_urls_in_batches(reference_encoding, image_urls, batch_size=5, tolerance=0.6):
    matching_images = []

    for i in range(0, len(image_urls), batch_size):
        batch_urls = image_urls[i:i + batch_size]
        batch_images = []

        for url in batch_urls:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))

            if img.mode != 'RGB':
                img = img.convert('RGB')

            batch_images.append(np.array(img))

        # Get face encodings for all images in the batch
        for img_array in batch_images:
            encodings = face_recognition.face_encodings(img_array)

            # Compare faces in batch with the reference face encoding
            for unknown_encoding in encodings:
                results = face_recognition.compare_faces([reference_encoding], unknown_encoding, tolerance=tolerance)
                if results[0]:
                    matching_images.append(url)
                    break  # Stop checking if one match is found per image

    return matching_images
