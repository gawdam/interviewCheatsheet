# InterviewPrepz: AI-Powered Interview Cheatsheet Generator

This project provides a web application that generates a comprehensive interview cheatsheet based on a candidate's resume and the job description.  The application leverages AI to analyze the input documents and create a tailored resource to help candidates prepare for interviews.
![banner](https://github.com/user-attachments/assets/46777ab0-964f-4993-8f13-a7d2e032cf6a)


## Features

* **Resume Upload:** Upload your resume in PDF format.
* **Job Description Input:**  Paste the job description into the provided text area.
* **AI-Powered Analysis:** The application uses an AI model to analyze the resume and job description.
* **Cheatsheet Generation:** A detailed cheatsheet is generated, including:
    * SWOT analysis of the candidate's strengths, weaknesses, opportunities, and threats.
    * A comparison of required skills and candidate skills.
    * A curated list of interview concepts with related YouTube video links (if available), and sample interview questions and answers.
    * A list of potential questions and answers related to projects listed on the resume.
    * Relevant insights about the target company (if available).
* **Firebase Integration:**  Resumes, job descriptions, and cheatsheets are stored securely using Firebase Storage.
* **Secure Authentication:** User authentication is handled securely using Firebase Authentication.


## Usage

1. Navigate to the application's web interface.
2. Log in using your Google account.
3. Upload your resume (PDF format only).
4. Paste the job description.
5. Click "Generate your interview cheatsheet".
6. The generated cheatsheet will be displayed, along with download links for your resume and job description.


## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   ```
2. **Navigate to the project directory:**
   ```bash
   cd interviewCheatsheet
   ```
3. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/macOS
   venv\Scripts\activate  # On Windows
   ```
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Set environment variables:** Create a `.env` file in the root directory and add the following (replace with your actual keys):
   ```
   GOOGLE_APPLICATION_CREDENTIALS="<path_to_your_google_credentials_json>"
   GEMINIAPIKEY="<your_google_gemini_api_key>"
   YTAPIKEY="<your_youtube_data_api_key>"
   FLASK_SECRET_KEY="<your_flask_secret_key>"
   FIREBASE_API_KEY="<your_firebase_api_key>"
   FIREBASE_AUTH_DOMAIN="<your_firebase_auth_domain>"
   FIREBASE_PROJECT_ID="<your_firebase_project_id>"
   FIREBASE_STORAGE_BUCKET="<your_firebase_storage_bucket>"
   FIREBASE_MESSAGING_SENDER_ID="<your_firebase_messaging_sender_id>"
   FIREBASE_APP_ID="<your_firebase_app_id>"
   FIREBASE_DATABASE_URL="<your_firebase_database_url>"

   ```

6. **Run the application:**
   ```bash
   python main.py
   ```


## Technologies Used

* **Python:** The backend is built using Python 3.10.  It handles file processing, AI interaction, and Firebase communication.
* **Flask:** A lightweight Python web framework for building the web application.
* **Firebase:** Used for user authentication, file storage, and database management.
* **Google Gemini API:** Used for generating the interview cheatsheet.
* **YouTube Data API:** Used to fetch YouTube video links for concepts.
* **PyPDF2:** Used for extracting text from uploaded resumes.
* **HTML, CSS, JavaScript:** Used for creating the frontend user interface.
* **Docker:**  A Dockerfile is provided for easy containerization and deployment.
* **Gunicorn:** A WSGI HTTP server for deploying the Flask application.

## Configuration

The application requires several environment variables to be set.  These are defined in a `.env` file.  See the "Installation" section for details.

## API Documentation

The application uses the Google Gemini API and YouTube Data API.  Refer to their respective documentation for details.  No direct REST API is exposed.  

## Dependencies

The `requirements.txt` file lists all necessary Python packages.

## Contributing

Contributions are welcome!  Please open an issue or submit a pull request.

## Gallery
* Homepage
![image](https://github.com/user-attachments/assets/37fa01d4-54bb-4d38-b0d5-5e0997a75652)
* Cheatsheet -
![image](https://github.com/user-attachments/assets/830e89ee-c45c-4ee5-b877-abd468f537dc)
![image](https://github.com/user-attachments/assets/f5b1b43c-4c48-4eef-b923-09eb8cfa1c12)
![image](https://github.com/user-attachments/assets/5c0f6fc2-fff9-4054-8986-5254d4f6b3cb)
![image](https://github.com/user-attachments/assets/04b67ef8-b296-4854-8c6e-b7e04f8e9d8b)
![image](https://github.com/user-attachments/assets/88ec3e71-089b-4804-8d96-83040fff4b77)


* 


## Testing

No formal testing framework is currently implemented.



*README.md was made with [Etchr](https://etchr.dev)*
