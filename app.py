from flask import Flask, redirect, render_template, request, jsonify, url_for, app
# from pymongo import MongoClient
# JWT와 관련 여부 확인 필요
# from dotenv import load_dotenv
import os

# Flask
app = Flask(__name__)

# .env
# load_dotenv()
# ID = os.environ.get('DB_ID')
# PW = os.environ.get('DB_PW')

# 로그인 화면
@app.route('/login', methods=["GET"])
def login():
    return render_template('login.html')

# 회원가입 화면
@app.route('/signup', methods=["GET"])
def signup():
    return render_template('signup.html')

# 메인화면 - 카테고리
@app.route('/', methods=["GET"])
def home():
    return render_template('index.html')

# 자격증 세부정보
@app.route('/certificateDetails', methods=["GET"])
def certificate_Details():
    return render_template('certificateDetails.html')

# 자격증 세부정보 가져오기
@app.route('/certificateDetails/get_detail')
def get_certificate_Details():
    return 0

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)