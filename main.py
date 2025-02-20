# filepath: /d:/Professional - Work/contests/open source AI/interviewCheatsheet/main.py
import json
import os
import tempfile
from io import BytesIO

from flask import Flask, render_template, request, redirect, flash, session, url_for
from werkzeug.utils import secure_filename

from authentication import (
    upload_resume_to_firebase,
    upload_job_description_to_firebase,
    get_resume_from_firebase,
    get_job_description_from_firebase, get_cheatsheet_from_firebase, upload_cheatsheet_to_firebase,
)
from functions.generate_interview_cheatsheet import generate_interview_cheatsheet

# Initialize the Flask app
app = Flask(__name__)

# Configure app secret key
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')

# Temporary directory for storing uploaded files
TEMP_UPLOAD_FOLDER = tempfile.mkdtemp()

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        id_token = request.form['idToken']
        try:
            decoded_token = auth.verify_id_token(id_token)
            user_id = decoded_token['uid']
            session['user_id'] = user_id
            session['user_email'] = decoded_token['email']
            return redirect('/authenticate')
        except Exception as e:
            flash("Invalid token", "error")
            return redirect('/login')



    return render_template('login.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission from the homepage."""
    if request.method == 'POST':
        # Store resume and job description in temporary files
        file = request.files.get('file')
        job_description = request.form.get('jobDescription', '').strip()

        if not job_description:
            flash('Job description is required.', 'error')
            return redirect('/')

        if file and allowed_file(file.filename):
            try:
                # Save the resume to a temporary file
                resume_filename = secure_filename(file.filename)
                resume_path = os.path.join(TEMP_UPLOAD_FOLDER, resume_filename)
                file.save(resume_path)

                # Save the job description to a temporary file
                job_desc_path = os.path.join(TEMP_UPLOAD_FOLDER, 'job_description.txt')
                with open(job_desc_path, 'w') as f:
                    f.write(job_description)

                # Store file paths in session
                session['resume_path'] = resume_path
                session['job_desc_path'] = job_desc_path

                return redirect('/authenticate')
            except Exception as e:
                flash(f"Error processing the uploaded file: {e}", "error")
                return redirect('/')
        else:
            flash('Invalid file or no file uploaded.', 'error')
            return redirect('/')

@app.route('/authenticate')
def authenticate():
    """Check if the user is logged in and redirect accordingly."""
    if 'user_id' not in session:
        return redirect('/login')
    return redirect('/store')

@app.route('/store')
def store():
    """Store resume and job description in Firebase."""
    if 'user_id' not in session:
        flash("You must log in first.", "error")
        return redirect('/login')

    user_id = session['user_id']
    resume_path = session.get('resume_path')
    job_desc_path = session.get('job_desc_path')

    if not resume_path or not job_desc_path:
        flash("No resume or job description found in session.", "error")
        return redirect('/')

    try:
        # Read the resume file
        with open(resume_path, 'rb') as f:
            resume_data = f.read()

        # Read the job description file
        with open(job_desc_path, 'r') as f:
            job_description = f.read()

        # Upload resume to Firebase
        resume_url = upload_resume_to_firebase(BytesIO(resume_data), "resume.pdf", user_id)
        print(f"Resume uploaded: {resume_url}")
        session['resume_url'] = resume_url

        # Upload job description to Firebase
        job_desc_url = upload_job_description_to_firebase(job_description, user_id)
        print(f"Job description uploaded: {job_desc_url}")
        session['job_desc_url'] = job_desc_url

        # Generate cheatsheet
        return redirect('/cheatsheet')
    except Exception as e:
        flash(f"Error processing data: {e}", "error")
        return redirect('/')

@app.route('/config')
def get_firebase_config():
    """Return Firebase config for frontend initialization."""
    firebase_config = {
        "apiKey": os.getenv("FIREBASE_API_KEY"),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
        "projectId": os.getenv("FIREBASE_PROJECT_ID"),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
        "appId": os.getenv("FIREBASE_APP_ID"),
        "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    }
    return json.dumps(firebase_config), 200, {"Content-Type": "application/json"}


@app.route('/cheatsheet')
def cheatsheet():
    """Generate and display the interview cheatsheet."""
    if 'user_id' not in session:
        flash("You must log in first.", "error")
        return redirect('/login')

    user_id = session['user_id']

    # Check if cheatsheet file path is already in the session
    if 'cheatsheet_path' in session:
        cheatsheet_path = session['cheatsheet_path']
        try:
            # Read the cheatsheet from the local file
            with open(cheatsheet_path, 'r') as f:
                cheatsheet_text = json.load(f)

            return render_template(
                'result.html',
                cheatsheet=cheatsheet_text,
                resume_url=session.get('resume_url'),
                job_desc=session.get('job_desc')
            )
        except Exception as e:
            flash(f"Error reading cheatsheet file: {e}", "error")
            return redirect('/')

    # If cheatsheet data is not in the session, generate it
    resume_path = session.get('resume_path')
    job_desc_path = session.get('job_desc_path')

    if not resume_path or not job_desc_path:
        flash("Failed to retrieve data from session.", "error")
        return redirect('/')

    try:
        # Read the resume file
        with open(resume_path, 'rb') as f:
            resume_data = f.read()

        # Read the job description file
        with open(job_desc_path, 'r') as f:
            job_description = f.read()

        # Generate cheatsheet
        cheatsheet_text = generate_interview_cheatsheet(BytesIO(resume_data), job_description)

        if isinstance(cheatsheet_text, str):
            try:
                cheatsheet_text = json.loads(cheatsheet_text)
            except json.JSONDecodeError:
                flash("Invalid response from cheatsheet generation.", "error")
                return redirect('/')

        # Save the cheatsheet to a local file
        cheatsheet_path = os.path.join(tempfile.gettempdir(), f"cheatsheet_{user_id}.json")
        with open(cheatsheet_path, 'w') as f:
            json.dump(cheatsheet_text, f)

        # Store the file path in the session
        session['cheatsheet_path'] = cheatsheet_path

        return render_template(
            'result.html',
            cheatsheet=cheatsheet_text,
            resume_url=session['resume_url'],
            job_desc=session['job_desc']
        )
    except Exception as e:
        flash(f"Error generating cheatsheet: {e}", "error")
        return redirect('/')

@app.route('/logout', methods=['GET'])
def logout():
    """Log out the user and clear the session."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect('/')

@app.route('/favicon.png')
def favicon():
    """Serve the favicon."""
    return app.send_static_file('favicon.png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)