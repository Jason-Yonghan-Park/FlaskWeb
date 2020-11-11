"""
    실행하기 
    
    먼저 아래와 같이 웹 서비스에 필요한 파이썬 패키지와 MySQL 접속에 필요한 패키지를 설치한다.    
    
    pip3 install flask   
    pip3 install pymysql
    
    크로스 도메인에 대한 Ajax 처리를 위한 Access-Control-Allow-Origin에 대한 처리 패키지
    pip3 install -U flask-cors    
    
     
    이클립스에서는 main.py 모듈을 화면에 띄우고 Ctrl + F11 키로 실행하면 
    다음과 같은 메시지가 뜨면서 웹 서버가 실행된다.
    
    * Serving Flask app "main" (lazy loading)
    * Environment: production
       WARNING: This is a development server. Do not use it in a production deployment.
      Use a production WSGI server instead.
    * Debug mode: off
    * Running on http://0.0.0.0:9000/ (Press CTRL+C to quit)
    
    웹 서비스가 에러 없이 실행되면 웹브라우저를 실행하고 다음 주소를 입력해 접속하면
    "채팅 테스트"라는 제목을 가진 화면이 나타나는데 이 화면에서 아이디, 비밀번호 
    입력 양식에 아무거나 입력하고 로그인 버튼을 클릭하면 "대화하기" 창으로 이동한다.

    http://localhost:9000
     
    ##############################################
    Flask 참고 사이트 
    
    * Flask 한글 번역문서 
    https://flask-docs-kr.readthedocs.io/ko/latest/

    * Flask 기초
    https://www.fun-coding.org/flask_basic-1.html

    * Flask DB 연동 참고
    https://www.fun-coding.org/mysql_basic6.html
    https://godoftyping.wordpress.com/2017/05/27/python-mysql/
    http://pythonstudy.xyz/python/article/202-MySQL-%EC%BF%BC%EB%A6%AC

    * Flask-matplot 연동하기
    https://frhyme.github.io/python-lib/flask_matplotlib/
     
"""

# 웹 요청을 처리하는 파이썬 모듈
# flask 웹 프레임워크 사용
from flask import Flask, render_template, request, json, jsonify, send_file, redirect, url_for, Response

# matplotlib를 이용해 차트를 출력하는 모듈 임포트
from webservice.visual.matplotlib_chart import chartLineStyle, multiSizeScatter

from io import BytesIO, StringIO

from webservice.db.db_connector import MySqlDbConnector
from webservice.db.value_object import Member, MemberEncoder

# Access-Control-Allow-Origin에 대한 처리
# pip3 install -U flask-cors 
from flask_cors import CORS

# Flask 객체 생성
app = Flask(__name__)

# Access-Control-Allow-Origin에 대한 처리
CORS(app)

# Flask(app)가 제공하는 route 데코레이터(decorator)를 사용해 
# 루트(/)로 들어오는 요청을 처리하는 home() 함수를 엔드포인트로 등록
# SpringFramework에서 @RequestMapping과 비슷한 역할을 함
@app.route("/")
def home():
    
    # get 방식 요청 파라미터를 읽어온다. 지정한 요청 파라미터가 없으면 None이 넘어온다.
    method = request.args.get("method")
    print("home() - method : ", method)
    
    # 요청 방식이 GET 방식인지 POST 방식인지 다음과 같이 확인할 수 있다.     
    print("methods : ", request.method)
        
    # 화면에 출력할 템플릿 페이지를 반환하면서 모델 데이터를 인수로 지정할 수 있다. 
    # 현재 모듈이 실행되는 위치에서 templates/index.html 파일을 찾는다.
    # 뷰 페이지에서 사용할 모델 데이터를 method 이름으로 같이 보낸다.
    return render_template("index.html", method = method)

    # 프로그램 요소가 없는 정적 파일이라면 아래와 같이 지정해도 된다.
    # 현재 모듈이 실행되는 위치에서 static/home.html 파일을 찾는다. 
    # @app.route("/", static_folder=".", static_url_path="")
    # return app.send_static_file("home.html")


# /chat 으로 들어오는 get 방식 요청을 처리하는 chat_get() 함수를 엔드포인트로 등록
@app.route("/chat", methods=["GET"])
def chat_get():
    
    # 요청 방식이 GET 방식인지 POST 방식인지 다음과 같이 확인할 수 있다.
    print("methods : ", request.method)
    
    # get 방식 요청 파라미터를 읽어온다. 지정한 요청 파라미터가 없으면 None이 반환된다.
    id = request.args.get("id")
    pass1 = request.args.get("pass")
    uId = request.args.get("uId")
        
    # 템플릿 페이지(뷰 페이지)를 반환하면서 모델 정보를 인수로 지정할 수 있다.
    # 현재 모듈이 실행되는 위치에서 templates/chatting.html을 찾는다.
    # 뷰 페이지로 보낼 모델이 여러 개라면 아래와 같이 가변인수를 사용할 수 있다.
    return render_template("chatting.html", id = id, pass1 = pass1, uId = uId)


# /chat 으로 들어오는 post 방식 요청을 처리하는 chat_post() 함수를 엔드포인트로 등록
@app.route("/chat", methods=["POST"])
def chat_post():
    
    # post 방식의 요청 파라미터를 읽어온다.
    print("methods : ", request.method)
    resData={}
    resData["id"] = request.form.get("id")
    resData["pass1"] = request.form.get("pass")
    resData["uId"] = request.form.get("uId")
    
    # 웹 서버 콘솔에 출력
    print("resData : ", resData)
        
    # 템플릿 페이지(뷰 페이지)를 반환하면서 모델 정보를 인수로 지정할 수 있다.
    # chat_get() 함수에서 사용했던 가변인수 방식과 동일하게 동작한다.
    # 템플릿으로 보내야 하는 모델 데이터가 많을 경우 유용하게 사용할 수 있다.
    # 뷰 페이지에서 resData 지정한 key 값으로 데이터에 접근할 수 있다.
    return render_template("chatting.html", **resData)


# /chatting 으로 들어오는 post 방식 요청을 처리하는 함수를 엔드포인트로 등록
@app.route("/chatting", methods=["POST"])
def chatting():
    
    # post 방식으로 넘어오는 요청 파라미터를 읽어온다.
    req_msg = request.form.get("req_msg")
    print("req_msg : ",  req_msg)
    
    # 요청 파라미터에서 읽어온 데이터를 그대로 응답으로 반환한다.
    # Ajax 요청에 대한 응답으로 뷰 페이지 없이 반환 값만 그대로 전달된다.
    return req_msg

    # 사전 데이터를 JSON 형식으로 변환해 반환할 수 있음
    #return jsonify({"msg": req_msg})


# 회원 리스트 보기 요청을 처리하는 함수
@app.route("/memberList")
def memberList():
    
    # DB 접속 객체 생성 - host, user, pw, db
    dao = MySqlDbConnector("localhost", "root", "12345678", "pythondb")
    
    memberList = dao.getMemberList()
    
    return render_template("memberList.html", memberList=memberList)
    

# 회원 등록 폼 요청을 처리하는 함수
@app.route("/joinForm")
def joinForm():
    return render_template("joinForm.html")
    
    
# joinForm에서 들어오는 요청을 받아 DB에 회원정보를 등록하는 함수
@app.route("/addMember", methods=["POST"])
def addMember():
    # DB 접속 객체 생성 - host, user, pw, db
    dao = MySqlDbConnector("localhost", "root", "12345678", "pythondb")
    
    # no는 테이블에 회원정보가 추가되면서 생성되는 것으로 None를 지정했다.
    # regDate도 마찬가지로 SYSDATE() 함수를 사용할 것이므로 None를 지정했다.
    member = Member(
                    no=None,
                    id=request.form.get("id"), name=request.form.get("name"),
                    pw=request.form.get("pw"), email=request.form.get("email"),
                    phone=request.form.get("phone"), address1=request.form.get("address1"),
                    regDate=None)
    
    dao.addMember(member)
    
    return redirect(url_for("memberList"))
    
    
# 회원정보 상세 보기 - RestAPI를 이용해 파라미터 받기
@app.route("/memberDetail/<no>")
def memberDetail(no):
    
    print("main.getMember() - no : ", no)
    
    # DB 접속 객체 생성 - host, user, pw, db
    dao = MySqlDbConnector("localhost", "root", "12345678", "pythondb")
    
    member = dao.getMember(no)
    
    return render_template("memberDetail.html", member=member)   


# 회원 정보 수정 폼 요청을 처리하는 함수
@app.route("/updateMemberForm/<no>")
def updateMemberForm(no):
    
    print("main.updateMemberForm() - no : ", no)
    
    # DB 접속 객체 생성 - host, user, pw, db
    dao = MySqlDbConnector("localhost", "root", "12345678", "pythondb")
    
    member = dao.getMember(no)
    
    return render_template("updateMemberForm.html", member=member) 


# 회원 정보 수정 폼으로부터 들어오는 회원 정보 수정 요청을 처리하는 함수
@app.route("/updateMember", methods=["POST"])
def updateMember():
    # DB 접속 객체 생성 - host, user, pw, db
    dao = MySqlDbConnector("localhost", "root", "12345678", "pythondb")
    
    # id, name, pw은 수정 가능한 데이터가 아니므로 None로 지정해 객체를 생성함
    member = Member(
                    no=request.form.get("no"),
                    id=None, name=None, pw=None, email=request.form.get("email"),
                    phone=request.form.get("phone"), address1=request.form.get("address1"),
                    regDate=None)
    
    dao.updateMember(member)
    
    return redirect(url_for("memberList"))


# 회원 정보 삭제 요청을 처리하는 함수
@app.route("/deleteMember/<no>")
def deleteMember(no):
    print("main.updateMemberForm() - no : ", no)
    
    # DB 접속 객체 생성 - host, user, pw, db
    dao = MySqlDbConnector("localhost", "root", "12345678", "pythondb")
    
    dao.deleteMember(no)
    
    return redirect(url_for("memberList"))


# 스프링에서 오는 회원 리스트 요청을 json으로 응답하는 함수
@app.route("/mListJson", methods=["POST"])
def mListJson():
    
    # DB 접속 객체 생성 - host, user, pw, db
    dao = MySqlDbConnector("localhost", "root", "12345678", "pythondb")
    
    memberList = dao.getMemberList()
    
    no = request.form.get("no")
    print("no : ", no)
    #print(jsonify(memberList))
    
    # 사용자 정의 객체를 직렬화 해주는 객체가 필요함 - value_object 모듈에 정의되
    #return jsonify(memberList)
    
    # dumps() 함수는 json 형식의 문자열로 변환 - 클라이언트에서 eval() 함수 필요
    # return json.dumps(memberList, cls=MemberEncoder, ensure_ascii=False)
    
    # 클라이언트에서 바로 json(자바스크립트 객체)로 받으려면 아래와 같이 반환
    return jsonify(json.loads(json.dumps(memberList, cls=MemberEncoder, ensure_ascii=False)))



# 응답 데이터의 header를 설정하고 json 형식으로 반환
def getRequestHeader():
    
    res = Response()
    
    # 크로스 도메인에 대한 Ajax 요청 처리 
    res.headers.add("Access-Control-Allow-Origin", "*")
    
    result = "파이썬 객체"
    # 아래 두 가지 방식 테스트
    #return render_template("result.html", data=result)
    #return jsonify(result)
    
    # 결과 데이터를 직렬화 해서 문자열이나 json 형식으로 응답
    res.set_data(str(result))
    return  res
    
    # 별도의 header 설정을 적용해 템플릿을 통해 html 문석 형식으로 응답
    # return res.set_data(render_template("result.html", data=result))
    

# /sendFileChart 로 들어오는 get 방식 요청을 처리하는 함수를 엔드포인트로 등록
@app.route("/sendFileChart", methods=["GET"])
def sendFileChart():
    
    # get 방식 요청 파라미터를 읽는다.
    kind = request.args.get("chart")
    print("sendFile Chart - kind : ", kind)
    plt = None
    
    if kind in 'line':
        plt = chartLineStyle()
        
    elif kind in 'scatter':
        plt = multiSizeScatter()
        
    # file로 저장하는 것이 아니라 BinaryObject에 저장해서 이미지 
    # 정보를 임시 파일로 넘겨준다고 생각하면 된다.         
    img = BytesIO()
    plt.savefig(img, format='png', dpi=200)
        
    # svg로 저장할 수도 있지만 이 경우 html에서 다른 방식으로 저장해야 함.
    # plt.savefig(img, format='svg')
    # return send_file(img, mimetype='image/svg')    
    #img.seek(0)
    
    # 임시로 만들어진 이미지 파일을 응답으로 전송한다.
    # send_file() 함수는 url 요청이 왔을 때 그에 대응되는 파일을 내부에서
    # 생성해 반환하는 함수 즉, 내부에서 BinaryObject에 파일을 저장하고 
    # 그 값을 send_file() 함수에 넘기면 파일로 만들어서 반환해 준다.
    # 단순히 이미지 파일을 반환해 브라우저에 이미지만 출력된다.
    return send_file(img, mimetype='image/png')


# /chartView 로 들어오는 get 방식 요청을 처리하는 함수를 엔드포인트로 등록
@app.route("/chartView", methods=["GET"])
def chartView(): 
    
    kind = request.args.get("chart")   
    
    # 뷰 페이지로 보낼 모델 데이터를 사전 데이터로 저장
    resData = {}
    resData["title"] = kind;   
    resData["width"] = 800
    resData["height"] = 600
    
    # 모델과 함께 뷰 페이지 정보를 반환한다.
    # 뷰 페이지에서 resData의 key로 데이터에 접근할 수 있다.
    # chart.html로 이동해 모델이 뷰에 출력되고 클라이언트로 응답되며
    # chart.html 에서 "{{ url_for('fig', chart=title) }}"에 의해서
    # /fig/line 와 같이 출력되며 img 태그의 src 속성에 이미지 정보가
    # "/fig/line"과 같이 되므로 브라우저에서 이 주소로 이미지를 요청한다.
    # 그러면 아래 fig(chart) 함수가 실행되고 이미지가 브라우저로 응답된다.
    return render_template("chart.html", **resData)


# /fig/line 형식으로 들어오는 요청을 처리하는 함수
# REST API를 이용해서 요청 파라미터인 chart를 함수의 인수로 받는다.
@app.route("/fig/<string:chart>")
def fig(chart):
    
    plt = None    
    print("fig - kind : ", chart)
    
    if chart in 'line':
        plt = chartLineStyle()
        
    elif chart in 'scatter':
        plt = multiSizeScatter()
    
    # file로 저장하는 것이 아니라 BinaryObject에 저장해서 이미지 
    # 정보를 임시 파일로 넘겨준다고 생각하면 된다.
    img = BytesIO()    
    plt.savefig(img, format='png', dpi=72)
    img.seek(0)
    
    # 이미지 파일을 생성해 반환
    return send_file(img, mimetype='image/png')

    
# 현재 모듈이 main으로 실행되면 웹 서비스를 시작한다.
if __name__ == "__main__":    

    # host 옵션을 생략하거나 "localhost"로 지정하면 현재 모듈을 로컬 서버로 실행한다.
    # host를 아래와 같이 "0.0.0.0"으로 지정하면 다른 컴퓨터에서 접근가능하다.
    #app.run(host="0.0.0.0", port=9000)
    
    # 개발 할 때만 debug 옵션을 지정하고 실제 운영에서는 debug 옵션을 제거한다.
    # debug=True 옵션은 파이써 코드가 수정되는 것을 자동으로 감지해 갱신 시켜준다.
    app.run(host="0.0.0.0", port=9000, debug=True)
    
    