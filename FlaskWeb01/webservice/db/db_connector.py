'''
Created on 2019. 10. 29.
@author: inc-1class
DB Connecting 모듈

먼저 SQL 패키지에 있는 member.sql을 이용해 DB 스키마를 생성하고
회원 정보에 대한 데이터를 추가한다.  

그리고 pymysql 패키지를 아래와 같이 설치한다.
pip3 install pymysql

flask DB 연동 참고 사이트 
https://www.fun-coding.org/mysql_basic6.html

'''
import pymysql
from webservice.db.value_object import Member

class MySqlDbConnector:
    
    def __init__(self, host, user, pw, db):
        
        # pymysql을 이용해 DB에 접속
        self.conn = pymysql.connect(
            host=host, user=user, password=pw, db=db, charset="utf8")
               
        
    def getMemberList(self):
        
        memberList = []
        
        try:
            # DB 접속 객체로 부터 커서 객체를 구함
            with self.conn.cursor() as cursor:
                
                sql = "SELECT * FROM member"
        
                # 쿼리를 DB에 발행
                cursor.execute(sql)
        
                # DB로 부터 읽어온 데이터를 추출
                """
                    튜플 -> 튜플로 반환
                (
                (1, 'admin', '이순신', '1234', 'midastop1@naver.com', '010-4321-8765', '서울 구로구 구로중앙로34길 33-4(구로동, 영림빌딩)', datetime.datetime(2016, 5, 11, 11, 20, 50)), 
                (2, 'midas', '홍길동', '1234', 'midastop@naver.com', '010-1234-5678', '경기 부천시 오정구 수주로 18 (고강동, 동문미도아파트)', datetime.datetime(2016, 6, 6, 12, 10, 30)), 
                (3, 'servlet', '강감찬', '1234', 'midas@daum.net', '010-5687-5678', '서울 강남구 강남대로146길 28 (논현동, 논현아파트)', datetime.datetime(2016, 6, 5, 12, 10, 30))
                )                
                """
                # SELECT 질의 결과 데이터 전체를 한 번에 추출
                rows = cursor.fetchall()
                    
                for row in rows:
                          
                    m = Member(no=row[0], id=row[1], name=row[2], 
                            pw=row[3], email=row[4], phone=row[5], 
                            address1=row[6], regDate=row[7] )
                    
                    memberList.append(m)
            
        finally:
            # DB 연결 종료
            self.conn.close()
        
        # 회원 리스트 반환
        return memberList  
    
    
    # 회원 추가
    def addMember(self, member):
        
        try:
            # DB 접속 객체로 부터 커서 객체를 구함
            with self.conn.cursor() as cursor:
                
                """
                   실무에서는 대부분의 SQL 문장에 동적으로 컬럼의 데이타 값을 지정하는 경우가 많다.
                   동적 SQL 문을 구성할 때 실제 데이터가 들어가는 위치에 Parameter Placeholder를
                   사용하는데  MySQL의 경우 Parameter Placeholder로 %s를 사용한다.
                   그리고 execute() 메서드를 호출해 DB에 쿼리를 발행 할 때 실제 데이터를 %s를 지정한
                   순서에 맞게 아래와 같이 튜플로 만들어 이 메서드의 두 번째 인수로 지정하면 된다.
                %s는 Parameter Placeholder를 지정하는 문자로써 문자열 포맷팅에 사용되는 %s, 
                %d와는 다른 것이다. 그러므로 모든 데이터 타입에 %s를 사용해 쿼리를 작성하면 된다.   
                """  
                sql = """
                    INSERT INTO member(id, name, pass, email, phone, address1, reg_date) 
                    VALUES(%s, %s, %s, %s, %s, %s, SYSDATE())
                    """
                
                # 쿼리를 DB에 발행
                cursor.execute(sql, (member.getId(), member.getName(), 
                                     member.getPw(), member.getEmail(), 
                                     member.getPhone(), member.getAddress1()))        
                
                # DB 파일에 적용
                self.conn.commit()
                
        finally:
            # DB 연결 종료
            self.conn.close()
            print(member.getName(), " 회원 등록 완료")
    
    
    # 회원 상세정보
    def getMember(self, no):        
        
        try:
            # DB 접속 객체로 부터 커서 객체를 구함
            with self.conn.cursor() as cursor:
                
                sql = "SELECT * FROM member WHERE no=%s"
        
                # 쿼리를 DB에 발행
                cursor.execute(sql, (no))
        
                # DB로 부터 읽어오 데이터를 추출
                """
                    튜플 -> 튜플로 반환                
                (1, 'admin', '이순신', '1234', 'midastop1@naver.com', '010-4321-8765', '서울 구로구 구로중앙로34길 33-4(구로동, 영림빌딩)', datetime.datetime(2016, 5, 11, 11, 20, 50))                
                
                """
                # 커서가 가리키고 있는 다음 행의 데이터를 추출 - 첫 번째 행의 데이터 추출
                row = cursor.fetchone()
                print(row)
                m = Member(no=row[0], id=row[1], name=row[2], 
                        pw=row[3], email=row[4], phone=row[5], 
                        address1=row[6], regDate=row[7] )
            
        finally:
            # DB 연결 종료
            self.conn.close()
        
        # no에 해당하는 회원정보 반환
        return m
    
    
    # 회원정보 수정
    def updateMember(self, member):
        try:
            # DB 접속 객체로 부터 커서 객체를 구함
            with self.conn.cursor() as cursor:
                
                sql = """
                        UPDATE member 
                            SET email=%s, phone=%s, address1=%s, reg_date=SYSDATE()
                        WHERE no = %s
                        """
                
                # 쿼리를 DB에 발행
                cursor.execute(sql, (member.getEmail(), member.getPhone(), 
                                     member.getAddress1(), member.getNo()))        
                
                # DB 파일에 적용
                self.conn.commit()
                
        finally:
            # DB 연결 종료
            self.conn.close()
            print(member.getName(), " 회원 정보 수정 완료")
    
    
    # 회원정보 삭제
    def deleteMember(self, no):
        try:
            # DB 접속 객체로 부터 커서 객체를 구함
            with self.conn.cursor() as cursor:
                
                sql = "DELETE FROM member WHERE no = %s"
                
                # 쿼리를 DB에 발행
                cursor.execute(sql, no)
                
                # DB 파일에 적용
                self.conn.commit()
                
        finally:
            # DB 연결 종료
            self.conn.close()
            print(no, " 회원 정보 삭제 완료")
        
        
