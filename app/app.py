from flask import Flask, request, jsonify
from app.face_recognition_logic import process_images_from_urls_in_batches
from app.firebase_config import get_image_urls_from_firestore
import os
import shutil
import face_recognition

app = Flask(__name__)

# Ensure upload folder exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/api/match-images/", methods=["POST"])
def match_images():
    if 'reference_image' not in request.files:
        return jsonify({"error": "No image part"}), 400

    reference_image = request.files['reference_image']
    group_id = request.form.get("group_id", "uLFXzY5qXGg23xmFoacq")

    if reference_image.content_type not in ["image/jpeg", "image/png"]:
        return jsonify({"error": "Invalid image format. Use JPEG or PNG."}), 400

    # Save reference image locally
    file_location = os.path.join(UPLOAD_FOLDER, reference_image.filename)
    reference_image.save(file_location)

    # Load the reference image and get face encoding
    reference_encoding = face_recognition.face_encodings(face_recognition.load_image_file(file_location))

    if not reference_encoding:
        return jsonify({"error": "No face found in the reference image."}), 400

    # Get image URLs from Firestore
    image_urls = get_image_urls_from_firestore(group_id)

    # Process images in batches and find matches
    matching_images = process_images_from_urls_in_batches(reference_encoding[0], image_urls)

    return jsonify({"matching_images": matching_images})
