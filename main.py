# filepath: /d:/Professional - Work/contests/open source AI/interviewCheatsheet/main.py
import json
import os
import tempfile
from io import BytesIO
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, flash, session, jsonify
import requests
from werkzeug.utils import secure_filename
import firebase_admin
from firebase_admin import auth, credentials,storage
from CRUD import (
    upload_resume,
    upload_job_description,
    upload_cheatsheet,
    get_cheatsheet,
)
from functions.candidate.generate_interview_cheatsheet import generate_interview_cheatsheet
from functions.generate_jd_summary import generate_jd_summary



# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')

# Load environment variables
load_dotenv()

# Initialize Firebase Admin SDK
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not cred_path:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS not set")
cred = credentials.Certificate(cred_path)

# Initialize Firebase for Pyrebase
firebase_admin.initialize_app(cred, {
    "storageBucket": "interviewprepzz.firebasestorage.app"
})
bucket = storage.bucket()


# Temporary directory for file uploads
TEMP_UPLOAD_FOLDER = tempfile.mkdtemp()
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    print("/")
    # Pass auth and storage to CRUD module
    session.pop('cheatsheet_URL', None)
    session.pop('job_desc_url', None)
    session.pop('resume_url', None)


    user_name = session.get('user_name') or session.get('user_email')
    return render_template('index.html', user_name=user_name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("/login")

    if request.method == 'POST':
        id_token = request.form.get('idToken')
        if not id_token:
            flash("No authentication token provided.", "error")
            return redirect('/login')
        try:
            decoded_token = auth.verify_id_token(id_token)
            user_id = decoded_token.get('uid')
            email = decoded_token.get('email')
            session['user_id'] = user_id
            session['user_email'] = email
            session['id_token'] = id_token
            return redirect('/authenticate')
        except Exception as e:
            flash("Invalid token", "error")
            return redirect('/login')
    return render_template('login.html')

@app.route('/set-token', methods=['POST'])
def set_token():
    print("/set-token")

    """ Verify Firebase ID Token and store it in the session """
    try:
        data = request.get_json()
        id_token = data.get("idToken")

        if not id_token:
            return jsonify({"error": "ID token is required"}), 400

        # Verify token using Firebase Admin SDK
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token.get('uid')
        email = decoded_token.get('email')

        if not user_id:
            return jsonify({"error": "Invalid token"}), 401

        # ✅ Store everything in the Flask session
        session['user_id'] = user_id
        session['email'] = email
        session['id_token'] = id_token  # 🔥 Store the token for later authentication

        return jsonify({"message": "User authenticated", "user_id": user_id, "email": email}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    print("/authenticate")
    """ Authenticate user from session token """
    id_token = session.get('id_token')  # 🔥 Read token from session
    if not id_token:
        return redirect('/login')

    try:
        decoded_token = auth.verify_id_token(id_token)
        session['user_id'] = decoded_token['uid']
        session['user_email'] = decoded_token.get('email', '')
        session['user_name'] = decoded_token.get('name', '')  # Store user's name if available
        return redirect('/store')
    except ValueError as e:
        flash("Invalid authentication token.", "error")
    except auth.ExpiredIdTokenError:
        flash("Your session has expired. Please log in again.", "error")
    except auth.InvalidIdTokenError:
        flash("Invalid authentication token.", "error")
    except Exception as e:
        flash("Authentication failed.", "error")

    return redirect('/login')

@app.route('/submit', methods=['POST'])
def submit():
    print("/submit")
    file = request.files.get('file')
    job_description = request.form.get('jobDescription', '').strip()

    if not job_description:
        flash('Job description is required.', 'error')
        return redirect('/')

    if file and allowed_file(file.filename):
        resume_filename = secure_filename(file.filename)
        resume_path = os.path.join(TEMP_UPLOAD_FOLDER, resume_filename)
        file.save(resume_path)

        # Save job description to a temporary file
        job_desc_path = os.path.join(TEMP_UPLOAD_FOLDER, "job_desc.txt")
        with open(job_desc_path, "w", encoding="utf-8") as f:
            f.write(job_description)

        session['resume_path'] = resume_path
        session['job_desc_path'] = job_desc_path
        session['type'] = "candidate"

        return redirect('/store')  # Redirect to store (which will now show the loading screen)

    flash('Invalid file or no file uploaded.', 'error')
    return redirect('/')

@app.route('/submitInterviewer', methods=['POST'])
def submitInterviewer():
    print("/submitInterviewer")

    job_description = request.form.get('jobDescription', '').strip()

    if not job_description:
        flash('Job description is required.', 'error')
        return redirect('/')

    # Save job description to a temporary file
    job_desc_path = os.path.join(TEMP_UPLOAD_FOLDER, "job_desc.txt")
    with open(job_desc_path, "w", encoding="utf-8") as f:
        f.write(job_description)

    session['job_desc_path'] = job_desc_path
    session['type'] = "interviewer"

    return redirect('/store')  # Redirect to store (which will now show the loading screen)




@app.route('/store')
def store():
    print("/store")

    if 'user_id' not in session:
        return redirect('/login')

    # user_id = session['user_id']
    # resume_path = session.get('resume_path')
    # job_description = session.get('job_desc_path')

    # if not resume_path or not job_description:
    #     flash("Missing data.", "error")
    #     return redirect('/')

    return render_template('loading.html', redirect_url='/process')

@app.route('/process')
def process():
    print("/process")



    if 'user_id' not in session:
        return redirect('/login')



    user_id = session['user_id']
    resume_path = session.get('resume_path')
    job_description_path = session.get('job_desc_path')

    if session['type'] == "interviewer":
        if job_description_path and os.path.exists(job_description_path):
            with open(job_description_path, "r", encoding="utf-8") as f:
                job_description = f.read()
            print(job_description)
        job_desc_url = upload_job_description(job_description, user_id)

        jd_summary = generate_jd_summary(job_description)
        jd_summmary_URL = upload_cheatsheet(user_id, jd_summary)

        session['job_desc_url'] = job_desc_url
        session['jd_summmary_URL'] = jd_summmary_URL

        return redirect('/job-dashboard')

    try:
        with open(resume_path, 'rb') as f:
            resume_data = f.read()

        if job_description_path and os.path.exists(job_description_path):
            with open(job_description_path, "r", encoding="utf-8") as f:
                job_description = f.read()
            print(job_description) 
        resume_url = upload_resume(BytesIO(resume_data), "resume.pdf", user_id)
        job_desc_url = upload_job_description(job_description, user_id)

        cheatsheet_text = generate_interview_cheatsheet(BytesIO(resume_data), job_description,type=session['type'])
        cheatsheet_URL = upload_cheatsheet(user_id, cheatsheet_text)


        session['resume_url'] = resume_url
        session['job_desc_url'] = job_desc_url
        session['cheatsheet_URL'] = cheatsheet_URL

    except Exception as e:
        flash(f"Error processing data: {e}", "error")
        return redirect('/')
    


    return redirect('/cheatsheet')

@app.route('/job-dashboard')
def job_dashboard():
    user_id = session["user_id"]

    job_desc_URL = get_cheatsheet(user_id)
    if not job_desc_URL:
        flash("No cheatsheet available.", "error")
        return redirect('/')
    job_description_text = None
    if job_desc_URL:
        try:
            response = requests.get(job_desc_URL)
            if response.status_code == 200:
                job_description_text = response.text
            else:
                flash("Failed to retrieve cheatsheet.", "error")
        except Exception as e:
            flash(f"Error retrieving cheatsheet: {str(e)}", "error")
    print(f"Cheatsheet text: {job_desc_URL}")

    job_desc_json = json.loads(job_description_text)

    # Your cheatsheet_data is already in your Flask app
    return render_template('jobDashboard.html', job_data=job_desc_json)

@app.route('/screening-results')
def screening_results():
    user_id = session["user_id"]

    cheatsheet_URL = get_cheatsheet(user_id)
    if not cheatsheet_URL:
        flash("No cheatsheet available.", "error")
        return redirect('/')
    cheatsheet_text = None
    if cheatsheet_URL:
        try:
            response = requests.get(cheatsheet_URL)
            if response.status_code == 200:
                cheatsheet_text = response.text
            else:
                flash("Failed to retrieve cheatsheet.", "error")
        except Exception as e:
            flash(f"Error retrieving cheatsheet: {str(e)}", "error")
    print(f"Cheatsheet text: {cheatsheet_URL}")

    cheatsheet_json = json.loads(cheatsheet_text)

    # Your cheatsheet_data is already in your Flask app
    return render_template('screeningResults.html', candidate_data=cheatsheet_json)


@app.route('/cheatsheet')
def cheatsheet():
    """Retrieve cheatsheet and resume download URL, then render the result page."""
    if "user_id" not in session:
        flash("User not authenticated.", "error")
        return redirect('/login')

    user_id = session["user_id"]

    # Get cheatsheet URL
    cheatsheet_URL = get_cheatsheet(user_id)
    if not cheatsheet_URL:
        flash("No cheatsheet available.", "error")
        return redirect('/')

    # Fetch and save the resume locally
    resume_url = session.get("resume_url")
    local_resume_path = None

    if resume_url:
        try:
            response = requests.get(resume_url)
            if response.status_code == 200:
                # Ensure directory exists
                resume_dir = "static/resumes/"
                os.makedirs(resume_dir, exist_ok=True)

                # Save file locally
                resume_filename = f"{user_id}_resume.pdf"
                local_resume_path = os.path.join(resume_dir, resume_filename)

                with open(local_resume_path, "wb") as f:
                    f.write(response.content)

                print(f"Resume saved at: {local_resume_path}")
            else:
                flash("Failed to download resume.", "error")
        except Exception as e:
            flash(f"Error downloading resume: {str(e)}", "error")

    # Fetch job description content
    job_desc_url = session.get("job_desc_url")
    job_description = None
    if job_desc_url:
        try:
            response = requests.get(job_desc_url)
            if response.status_code == 200:
                job_description = response.text
            else:
                flash("Failed to retrieve job description.", "error")
        except Exception as e:
            flash(f"Error retrieving job description: {str(e)}", "error")

    # Fetch cheatsheet content
    cheatsheet_text = None
    if cheatsheet_URL:
        try:
            response = requests.get(cheatsheet_URL)
            if response.status_code == 200:
                cheatsheet_text = response.text
            else:
                flash("Failed to retrieve cheatsheet.", "error")
        except Exception as e:
            flash(f"Error retrieving cheatsheet: {str(e)}", "error")

    return render_template(
        "result.html",
        cheatsheet=json.loads(cheatsheet_text) if cheatsheet_text else None,
        resume_url=local_resume_path,  # Pass local path
        job_description=job_description
    )


@app.route('/config')
def get_firebase_config():
    return jsonify({
        "apiKey": os.getenv("FIREBASE_API_KEY"),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
        "projectId": os.getenv("FIREBASE_PROJECT_ID"),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
        "appId": os.getenv("FIREBASE_APP_ID"),
        "databaseURL": os.getenv("FIREBASE_DATABASE_URL")
    })

@app.route('/logout')
def logout():
    session.clear()
    response = redirect('/')
    response.delete_cookie('firebase_id_token')
    flash("You have been logged out.", "info")
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)