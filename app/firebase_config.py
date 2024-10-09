import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate('imageria-a09ae-firebase-adminsdk-whbrs-cb68800962.json')
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

def get_image_urls_from_firestore(group_id: str):
    # Fetch image URLs from Firestore based on the group ID
    image_urls = []
    docs = db.collection('groups').document(group_id).collection('photos').stream()
    
    for doc in docs:
        data = doc.to_dict()
        image_urls.append(data.get('photoURL'))  # Assuming 'photoURL' field contains the image URL
    
    return image_urls
