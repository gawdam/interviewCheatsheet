import json
import os
import tempfile
from io import BytesIO

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, flash, session, jsonify
import requests
from werkzeug.utils import secure_filename
import firebase_admin
from firebase_admin import auth, credentials
from authentication import (
    upload_resume_to_firebase,
    upload_job_description_to_firebase,
    upload_cheatsheet_to_firebase,
    get_cheatsheet_from_firebase
)
from functions.generate_interview_cheatsheet import generate_interview_cheatsheet

# Load environment variables
load_dotenv()

# Initialize Firebase Admin SDK
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not cred_path:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS not set")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')

# Temporary directory for file uploads
TEMP_UPLOAD_FOLDER = tempfile.mkdtemp()
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    session.pop('cheatsheet_URL', None)
    user_name = session.get('user_name') or session.get('user_email')
    return render_template('index.html', user_name=user_name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id_token = request.form.get('idToken')
        if not id_token:
            flash("No authentication token provided.", "error")
            return redirect('/login')
        response = jsonify({"message": "Login successful"})
        response.set_cookie("firebase_id_token", id_token, httponly=True, secure=True, samesite='None')
        return response
    return render_template('login.html')

@app.route('/submit', methods=['POST'])
def submit():
    file = request.files.get('file')
    job_description = request.form.get('jobDescription', '').strip()
    
    if not job_description:
        flash('Job description is required.', 'error')
        return redirect('/')

    if file and allowed_file(file.filename):
        resume_filename = secure_filename(file.filename)
        resume_path = os.path.join(TEMP_UPLOAD_FOLDER, resume_filename)
        file.save(resume_path)
        session['resume_path'] = resume_path
        session['job_desc'] = job_description
        return redirect('/store')  # Redirect to store (which will now show the loading screen)
    
    flash('Invalid file or no file uploaded.', 'error')
    return redirect('/')

@app.route('/store')
def store():
    print("Storing data...")
    if 'user_id' not in session:
        flash("You must log in first.", "error")
        return redirect('/login')
    
    user_id = session['user_id']
    resume_path = session.get('resume_path')
    job_description = session.get('job_desc')
    
    if not resume_path or not job_description:
        print("Missing data.")
        flash("Missing data.", "error")
        return redirect('/')
    
    return render_template('loading.html', redirect_url='/process')

@app.route('/process')
def process():
    print("Processing data...")
    if 'user_id' not in session:
        flash("You must log in first.", "error")
        return redirect('/login')
    
    user_id = session['user_id']
    resume_path = session.get('resume_path')
    job_description = session.get('job_desc')
    
    try:
        with open(resume_path, 'rb') as f:
            resume_data = f.read()
        resume_url = upload_resume_to_firebase(BytesIO(resume_data), "resume.pdf", user_id)
        print("RESUME URL: " + resume_url)
        job_desc_url = upload_job_description_to_firebase(job_description, user_id)
        
        cheatsheet_text = generate_interview_cheatsheet(BytesIO(resume_data), job_description)
        cheatsheet_url = upload_cheatsheet_to_firebase(user_id, cheatsheet_text)
        
        session['resume_url'] = resume_url
        session['job_desc_url'] = job_desc_url
        session['cheatsheet_URL'] = cheatsheet_url
    
    except Exception as e:
        flash(f"Error processing data: {e}", "error")
        return redirect('/')
    
    return redirect('/cheatsheet')

@app.route('/cheatsheet')
def cheatsheet():
    cheatsheet_url = session.get('cheatsheet_URL')
    if not cheatsheet_url:
        flash("No cheatsheet available.", "error")
        return redirect('/')
    
    response = requests.get(cheatsheet_url)
    if response.status_code == 200:
        cheatsheet_text = response.json()
        return render_template('result.html', cheatsheet=cheatsheet_text, resume_url=session['resume_url'])
    else:
        flash("Failed to retrieve cheatsheet.", "error")
        return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    response = redirect('/')
    response.delete_cookie('firebase_id_token')
    flash("You have been logged out.", "info")
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
