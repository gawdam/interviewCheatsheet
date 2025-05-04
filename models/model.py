# filepath: interviewCheatsheet/app/models.py
from main import db  # Import db instance from __init__.py
from datetime import datetime

class Recruiter(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    acc_cre_dt = db.Column(db.DateTime, default=datetime.utcnow)
    tokens_left = db.Column(db.Integer)
    last_session_dt = db.Column(db.DateTime)
    organization = db.Column(db.String(100))
    username = db.Column(db.String(80), unique=True, nullable=False)

    job_reqs = db.relationship('JobReq', backref='recruiter', lazy=True)
    candidates = db.relationship('Candidate', backref='recruiter', lazy=True)

class JobReq(db.Model):
    job_req_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('recruiter.user_id'), nullable=False)
    jd_url = db.Column(db.String(255))
    reg_doc_created = db.Column(db.DateTime)
    req_doc_url = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    candidates = db.relationship('Candidate', backref='job_req', lazy=True)

class Candidate(db.Model):
    candidate_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('recruiter.user_id'), nullable=False)
    job_req_id = db.Column(db.Integer, db.ForeignKey('job_req.job_req_id'), nullable=False)
    resume_url = db.Column(db.String(255))
    cheatsheet_url = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)