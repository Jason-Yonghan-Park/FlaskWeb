'''
Created on 2019. 10. 29.
@author: inc-1class
VO(Value Object) 클래스를 정의하는 모듈)
'''
import email

class Member:
    
    def __init__(self, *args, **kwargs):
        self.no = kwargs["no"]
        self.id = kwargs["id"]
        self.name = kwargs["name"]
        self.pw = kwargs["pw"]
        self.email = kwargs["email"]
        self.phone = kwargs["phone"]
        self.address1 = kwargs["address1"]
        self.regDate = kwargs["regDate"]
   
    def getNo(self):
        return self.no
    
    def setNo(self, no):
        self.no = no
        
    def getId(self):
        return self.id
    
    def setId(self, id):
        self.id = id
    
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
    
    def getPw(self):
        return self.pw
    
    def setPw(self, pw):
        self.pw = pw
    
    def getEmail(self):
        return self.email;
    
    def setEmail(self, email):
        self.email = email
    
    def getPhone(self):
        return self.phone
    
    def setPhone(self, phone):
        self.phone = phone
    
    def getAddress1(self):
        return self.address1
    
    def setAddress1(self, address1):
        self.address1 = address1
        
    def getRegDate(self):
        return self.regDate
    
    def setRegDate(self, regDate):
        self.regDate = regDate


# 기본 패키지에 json 모듈과 flask 패키지의 json 모듈이 있음
# 두 모듈은 거의 비슷한 기능을 제공함
from flask import json
import json

# json 모듈의 JSONEncoder 
from json import JSONEncoder

from datetime import datetime

# JSONEncoder를 상속 받아서 json을 인코딩 해주는 클래스
class MemberEncoder(JSONEncoder):
    def default(self, obj):
        
        # json으로 인코딩 하려면 __dict__ 함수가 객체에 있어야 하는데
        # datetime.datetime 객체에는 __dict__ 함수가 없어서 별도의 처리가 필요 
        if isinstance(obj, datetime):
            return obj.replace(microsecond=0).isoformat()
        return obj.__dict__


# 현재 모듈이 main으로 실행되면 웹 서비스를 시작한다.
if __name__ == "__main__":    
    
    # Member 객체를 생성해 직렬화 테스트 하는 코드
    m = Member(no=1, id='midas', name='홍길동', 
                        pw='1234', email="hong@naver.com", 
                        phone='010-8917-6683', 
                        address1="서울 마포구 노고산동", 
                        regDate=datetime.now())
    
    # 한 명의 Member 객체를 직렬화 하는 코드
    print(MemberEncoder().encode(m))
    
    # 한 명의 Member 객체를 json 문자열로 변환하여 출력
    print(json.dumps(m, cls=MemberEncoder, ensure_ascii=False))
        
    #dt = datetime.now()
    #print(dt)
    #print(dir(dt))
