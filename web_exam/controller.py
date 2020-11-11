############### main.py -> 웹서비스 시작하고 요청을 분석해서 처리하는 컨트롤러 역할

# 필요한 패키지 임포트
from flask import Flask, render_template, request, jsonify, send_file
from pymysql import *

# Flask 객체 생성
app = Flask(__name__, template_folder='D:/FlaskWeb/web_exam/templates')

# 각각의 요청을 처리하는 메서드
# @app.route() -> flask가 제공하는 데코레이터 (spring의 annotation과 역할 비슷)
@app.route('/')
# 회원 리스트 뿌려주는 페이지
def memberList():
    method = request.args.get('method')
    print('home() - method', method)

    # 현재 들어온 요청이 post인지 get인지 구분
    print('methods: ', request.method)

    # 회원 리스트 가지고 오기 위한 db 접속
    db = connect(host='localhost', port=3306, user='root', passwd='12345678', db='test', charset='utf8')
    curs = db.cursor()
    # 회원 리스트 가지고 오는 쿼리
    sql = "SELECT * FROM members"
    print(curs)
    curs.execute(sql)
    result = curs.fetchall()
    db.commit()
    db.close()

    # main.py 모듈이 있는 하부의 templates/index.html 파일을 찾음
    return render_template('memberList.html', method=method, result=result)

# 현재 모듈이 최상위에서 실행 될때 웹 서비스 시작
if __name__ == '__main__':
    # 실제 웹서비스 시작
    # app.run(host='0.0.0.0', port=9000) -> 실제 운영할 때 사용하면 좋음
    # 개발 시 소스코드 변경되면 바로 웹서버에 갱신하는 옵션(debug)
    app.run(host='0.0.0.0', port=9000, debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)
