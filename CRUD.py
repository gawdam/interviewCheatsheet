from datetime import timedelta
import io
import json
import tempfile
from flask import session
from firebase_admin import storage

def upload_file_to_firebase(file_data, file_path):
    """Uploads a file to Firebase Storage."""
    try:
        bucket = storage.bucket()
        blob = bucket.blob(file_path)
        blob.upload_from_file(file_data, content_type='application/octet-stream')
        blob.make_public()
        return blob.public_url
    except Exception as e:
        print(f"Error uploading file to {file_path}: {str(e)}")
        return None

def download_file_from_firebase(file_path, file_suffix):
    """Downloads a file from Firebase Storage."""
    try:
        bucket = storage.bucket()
        blob = bucket.blob(file_path)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix)
        blob.download_to_filename(temp_file.name)
        with open(temp_file.name, "rb") as file:
            return file.read()
    except Exception as e:
        print(f"Error retrieving file from {file_path}: {str(e)}")
        return None
    
def generate_signed_url(file_path, expiration_minutes=60):
    """Generates a signed URL for accessing a file in Firebase Storage."""
    try:
        bucket = storage.bucket()
        blob = bucket.blob(file_path)
        url = blob.generate_signed_url(expiration=timedelta(minutes=expiration_minutes))
        return url
    except Exception as e:
        print(f"Error generating signed URL for {file_path}: {str(e)}")
        return None

def upload_resume(file_data, filename, user_id):
    """Uploads a resume to Firebase Storage inside the user's folder."""
    file_path = f"users/{user_id}/pdfs/{filename}"
    return upload_file_to_firebase(file_data, file_path)

def upload_job_description(job_description, user_id):
    """Uploads job description as a text file inside the user's folder."""
    file_path = f"users/{user_id}/job_description/job_desc.txt"
    job_desc_bytes = io.BytesIO(job_description.encode('utf-8'))
    return upload_file_to_firebase(job_desc_bytes, file_path)

def upload_cheatsheet(user_id, cheatsheet_data):
    """Uploads cheatsheet as a JSON file inside the user's folder."""
    file_path = f"users/{user_id}/cheatsheet/cheatsheet.json"
    cheatsheet_json = json.dumps(cheatsheet_data)
    cheatsheet_bytes = io.BytesIO(cheatsheet_json.encode('utf-8'))
    return upload_file_to_firebase(cheatsheet_bytes, file_path)

def get_resume(user_id, filename):
    """Returns a signed URL for accessing the resume."""
    file_path = f"users/{user_id}/pdfs/{filename}"
    return generate_signed_url(file_path)


def get_job_description(user_id):
    """Returns a signed URL for accessing the job description."""
    file_path = f"users/{user_id}/job_description/job_desc.txt"
    return generate_signed_url(file_path)


def get_cheatsheet(user_id):
    """Retrieves cheatsheet from Firebase Storage."""
    file_path = f"users/{user_id}/cheatsheet/cheatsheet.json"
    return generate_signed_url(file_path)