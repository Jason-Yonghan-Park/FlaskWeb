############### main.py -> 웹서비스 시작하고 요청을 분석해서 처리하는 컨트롤러 역할

# 필요한 패키지 임포트
from flask import Flask, render_template, request, jsonify, send_file

# Flask 객체 생성
app = Flask(__name__, template_folder='D:/FlaskWeb/webservice/templates')

# 각각의 요청을 처리하는 메서드
# @app.route() -> flask가 제공하는 데코레이터 (spring의 annotation과 역할 비슷)
@app.route('/')
def home():
    method = request.args.get('method')
    print('home() - method', method)

    # 현재 들어온 요청이 post인지 get인지 구분
    print('methods: ', request.method)

    # main.py 모듈이 있는 하부의 templates/index.html 파일을 찾음
    return render_template('index.html', method=method)

@app.route('/chat', methods=['GET'])
def chat_get():
    # 현재 요청 방식이 무엇인지 출력
    print('methods', request.method)

    # get 방식의 요청 파라미터 읽기
    id = request.args.get('id')
    pass1 = request.args.get('pass')
    uId = request.args.get('uId')

    return render_template('chatting.html', id=id, pass1=pass1, uId=uId)

@app.route('/chat', methods=['POST'])
def chat_post():
    # 요청 방식이 무엇인지 출력
    print('methods', request.method)

    # post 방식의 요청 파라미터 읽기
    resData = {}
    resData['id'] = request.form.get('id')
    resData['pass1'] = request.form.get('pass')
    resData['uId'] = request.form.get('uId')
    print('resData: {}'.format(resData))

    return render_template('chatting.html', **resData)

@app.route('/chatting', methods=['POST'])
def chatting():
    req_msg = request.form.get('req_msg')
    print('req_msg: ', req_msg)

    return req_msg

# 현재 모듈이 최상위에서 실행 될때 웹 서비스 시작
if __name__ == '__main__':
    # 실제 웹서비스 시작
    # app.run(host='0.0.0.0', port=9000) -> 실제 운영할 때 사용하면 좋음
    # 개발 시 소스코드 변경되면 바로 웹서버에 갱신하는 옵션(debug)
    app.run(host='0.0.0.0', port=9000, debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)
