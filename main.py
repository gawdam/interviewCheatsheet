from io import BytesIO

from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from test import sample_json

from functions.generate_interview_cheatsheet import generate_interview_cheatsheet

# Initialize the Flask app
app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'tmp/'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tmp', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/')

        file = request.files['file']
        # If user does not select a file, browser also submits an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect('/')

        try:
            if file and allowed_file(file.filename):
                file_data = BytesIO(file.read())

                # Get the job description
                job_description = request.form['jobDescription']

                # Check if job description is provided
                if not job_description.strip():
                    flash('Job description is required.')
                    return redirect('/')

                # Generate the cheatsheet text
                cheatsheet_text = generate_interview_cheatsheet(file_data, job_description)

                return render_template('result.html', cheatsheet=cheatsheet_text)
            else:
                flash('Invalid file format. Only PDF files are allowed.')
                return redirect('/')

        except Exception as e:
            flash(f"Error reading the uploaded file: {e}")
            return redirect('/')

    return render_template('index.html')

@app.route('/favicon.png')
def favicon():
    return app.send_static_file('favicon.png')


if __name__ == '__main__':
    app.run()