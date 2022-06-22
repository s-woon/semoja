from flask import Flask, redirect, render_template, request, jsonify, url_for, app
from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.yoehfpg.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

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

# db.user.insert_one(doc)

# 메인화면 - 카테고리 상단 select 구현

# 자격증 세부정보
@app.route('/certificateDetails', methods=["GET"])
def certificate_Details():
    return render_template('certificateDetails.html')

# 자격증 세부정보 가져오기
@app.route('/certificateDetails/get_detail', methods=["GET"])
def get_certificate_Details():
    certificate_detail = list(db.certificate.find({}, {'_id': False}))
    # result = certificate_detail.json()
    print(certificate_detail[1]['implNm'])
    return jsonify({'certificate_detail': certificate_detail})

# index : 01 - 기술사 , 02 - 기능장 , 03 - 기사 , 04 - 기능사

# 자격증 세부정보 > 코멘트 남기기
@app.route('/certificateDetails/post_comment', methods=["POST"])
def post_certificate_comment():
    comment_receive = request.form["comment_give"]
    id_receive = "" # 어떤 아이디가 입력을 했는지 확인이 필요
    certificate_id_receive = "" # 자격증에 대한 id 부여 필요
    doc = {
        "certificate_id":certificate_id_receive,
        "id":id_receive,
        "comment":comment_receive
    }
    # db.certificate_comment.insert_one(doc)
    return jsonify({'msg':'코멘트 입력이 완료되었습니다.'})

# db.certificate.insert_one(doc)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)