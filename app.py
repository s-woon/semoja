from flask import Flask, redirect, render_template, request, jsonify, url_for, app
from pymongo import MongoClient
import requests

client = MongoClient('mongodb+srv://test:sparta@cluster0.yoehfpg.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'SPARTA'

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib


# Flask
app = Flask(__name__)

# .env
# load_dotenv()
# ID = os.environ.get('DB_ID')
# PW = os.environ.get('DB_PW')

# ========================================================================================
# 로그인 화면
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화합니다.
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요합니다.
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있습니다.
        # 아래에선 id와 exp를 담았습니다. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있습니다.
        # exp에는 만료시간을 넣어줍니다. 만료시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 납니다.
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=50000)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API입니다.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.
# (그렇지 않으면 남의 장바구니라든가, 정보를 누구나 볼 수 있겠죠?)
@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'name': userinfo['name']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': ''})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': ''})


# ========================================================================================
# 회원가입 화면
@app.route('/signup', methods=["GET"])
def signup():
    return render_template('signup.html')

# [회원가입 API]
# id, pw, name, email, num정보를 받아서 mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.

@app.route("/api/signup", methods=["POST"])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    name_receive = request.form['name_give']
    email_receive = request.form['email_give']
    num_receive = request.form['num_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {
        'id':id_receive,
        'pw': pw_hash,
        'name': name_receive,
        'email': email_receive,
        'num': num_receive
    }

    db.user.insert_one(doc)

    return jsonify({'msg': '회원가입이 완료되었습니다.'})

# ========================================================================================
# 세모자 메인 카테고리 화면
@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        print(user_info)
        return render_template('index.html', nickname=user_info["name"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route("/certificate", methods=["GET"])
def certificate_get():
    certificate_list = list(db.certificate.find({}, {'_id': False}))
    return jsonify({'certificates': certificate_list})

# # 카테고리 클릭 정보 넘기기
# @app.route('/certificateDetails/post_certificate_num', methods=["POST"])
# def post_certificate_num():
#     num_receive = request.form['_num_give']
#     index_receive = request.form['_index_give']
#     doc = {
#         'index':index_receive,
#         'num':num_receive
#     }
#     return jsonify({'msg':doc})


# ========================================================================================
# 세모자 자격증 세부정보
@app.route('/certificateDetails/<nickname>/<index>/<num>', methods=["GET"])
def certificate_Details(nickname,index,num):
    certificate = list(db.certificate.find({}, {'_id': False}))
    for i in range(0,len(certificate)):
        if int(certificate[i]['index']) == int(index) and int(certificate[i]['certificateNum']) == int(num):
            certificateNum = certificate[i]["certificateNum"]
            implNm = certificate[i]["implNm"]
            click_index = certificate[i]["index"]
            instiNm = certificate[i]["instiNm"]
            jmNm = certificate[i]["jmNm"]
            mdobligFldNm = certificate[i]["mdobligFldNm"]
            summary = certificate[i]["summary"]
    return render_template("certificateDetails.html",
                           certificateNum=certificateNum,
                           nickname=nickname,
                           implNm=implNm,
                           click_index=click_index,
                           instiNm=instiNm,
                           jmNm=jmNm,
                           mdobligFldNm=mdobligFldNm,
                           summary=summary)

# 자격증 세부정보 가져오기
@app.route('/certificateDetails/get_detail', methods=["GET"])
def get_certificate_Details():
    certificate_detail = list(db.certificate.find({}, {'_id': False}))
    # result = certificate_detail.json()
    # print(certificate_detail[1]['implNm'])
    return jsonify({'certificate_detail': certificate_detail})

# index : 01 - 기술사 , 02 - 기능장 , 03 - 기사 , 04 - 기능사

# 자격증 세부정보 > 코멘트 DB 저장
@app.route('/certificateDetails/post_comment', methods=["POST"])
def post_certificate_comment():
    comment_receive = request.form["comment_give"]
    # id_receive = "" # 어떤 아이디가 입력을 했는지 확인이 필요
    certificate_id_receive = "" # 자격증에 대한 id 부여 필요
    certificateNum_receive = request.form["certificateNum_give"]
    certificateNum_receive = request.form["click_index_give"]


    doc = {
        "certificate_id":certificate_id_receive,
        "id":id_receive,
        "comment":comment_receive
    }
    # db.certificate_comment.insert_one(doc)
    return jsonify({'msg':'코멘트 입력이 완료되었습니다.'})

# db.user.insert_one(doc)
# db.certificate.insert_one(doc)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)