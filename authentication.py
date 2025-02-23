import json
import os
import pyrebase
from dotenv import load_dotenv
import tempfile
import io

from google.auth.transport import requests


def initialize():
    load_dotenv()

    firebase_config = {
        "apiKey": os.getenv("FIREBASE_API_KEY"),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
        "projectId": os.getenv("FIREBASE_PROJECT_ID"),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
        "appId": os.getenv("FIREBASE_APP_ID"),
        "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    }

    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth()
    storage = firebase.storage()
    return auth,storage
# firebase_admin.initialize_app(cred, {
    # 'storageBucket': 'PROJECT_ID.firebasestorage.app'
# })


def firebase_authenticate(email, password):
    auth,_ = initialize()

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except Exception as e:
        print(f"Authentication error: {e}")
        return None


def upload_resume_to_firebase(file_data, filename, user_id):
    """ Uploads the resume to Firebase Storage inside user's folder. """
    _, storage = initialize()
    try:
        file_path = f"users/{user_id}/pdfs/{filename}"

        # Convert FileStorage to bytes
        file_bytes = file_data.read()

        # Wrap bytes in a file-like object
        file_stream = io.BytesIO(file_bytes)

        # Upload to Firebase Storage
        storage.child(file_path).put(file_stream)

        return storage.child(file_path).get_url(None)
    except Exception as e:
        print(f"Error uploading resume: {e}")
        return None


def upload_job_description_to_firebase(job_description, user_id):
    """ Uploads the job description as a text file inside user's folder. """
    _, storage = initialize()
    try:
        job_desc_path = f"users/{user_id}/job_description/job_desc.txt"

        # Convert string to file-like object
        job_desc_bytes = io.BytesIO(job_description.encode('utf-8'))

        # Upload file
        storage.child(job_desc_path).put(job_desc_bytes)
        print("STORAGE URL: " + storage.child(job_desc_path).get_url(None))
        return storage.child(job_desc_path).get_url(None)
    except Exception as e:
        print(f"Error uploading job description: {e}")
        return None


def get_resume_from_firebase(user_id,filename):
    """ Retrieves the resume from Firebase Storage. """

    _, storage = initialize()
    try:

        file_path = f"users/{user_id}/pdfs/{filename}"
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        storage.child(file_path).download(path=temp_file.name, filename=temp_file.name)


        with open(temp_file.name, "rb") as file:
            content = file.read()

        return content
    except Exception as e:
        print(f"Error retrieving resume: {e}")
        return None

def get_job_description_from_firebase(user_id,filename):
    """ Retrieves the job description from Firebase Storage. """
    _, storage = initialize()
    try:
        job_desc_path = f"users/{user_id}/job_description/{filename}"
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        storage.child(job_desc_path).download(path=temp_file.name, filename=temp_file.name)

        with open(temp_file.name, "r", encoding="utf-8") as file:
            content = file.read()

        return content
    except Exception as e:
        print(f"Error retrieving job description: {e}")
        return None

def get_cheatsheet_from_firebase(user_id):
    """Retrieves the cheatsheet from Firebase Storage."""
    _, storage = initialize()
    try:
        # Define the path for the cheatsheet file
        cheatsheet_path = f"users/{user_id}/cheatsheet/cheatsheet.json"

        # Create a temporary file to store the downloaded content
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")

        # Download the file from Firebase
        storage.child(cheatsheet_path).download(path=temp_file.name, filename=temp_file.name)

        # Read the content of the file
        with open(temp_file.name, "r") as file:
            content = file.read()

        # Parse the JSON content
        cheatsheet_text = json.loads(content)

        return cheatsheet_text
    except Exception as e:
        print(f"Error retrieving cheatsheet: {e}")
        return None

def upload_cheatsheet_to_firebase(user_id, cheatsheet_text):
    """Uploads the cheatsheet as a JSON file inside the user's folder."""
    _, storage = initialize()
    try:
        # Define the path for the cheatsheet file
        cheatsheet_path = f"users/{user_id}/cheatsheet/cheatsheet.json"

        # Convert the cheatsheet text (dictionary) to a JSON string
        cheatsheet_json = json.dumps(cheatsheet_text)
        print("pass 0")

        # Convert the JSON string to a file-like object
        cheatsheet_bytes = io.BytesIO(cheatsheet_json.encode('utf-8'))
        print("pass 1")
        # Upload the file to Firebase
        storage.child(cheatsheet_path).put(cheatsheet_bytes)
        print("pass 2")

        print("CHEATSHEET STORAGE URL: " + storage.child(cheatsheet_path).get_url(None))
        # Return the public URL of the uploaded file
        return storage.child(cheatsheet_path).get_url(None)
    except Exception as e:
        print(f"Error uploading cheatsheet: {e}")
        return None