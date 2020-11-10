############# pymysql로 회원테이블 만들기
import pymysql

# db 연결
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='12345678', db='test', charset='utf8')

# members table 만들기
try:
    with db.cursor() as cursor:
        sql = '''
                CREATE TABLE members (
	                no INTEGER PRIMARY KEY AUTO_INCREMENT,
	                id VARCHAR(20) NOT NULL,
	                name VARCHAR(10) NOT NULL,
	                pass VARCHAR(20) NOT NULL,
	                email VARCHAR(30) NOT NULL,
	                phone VARCHAR(13) NOT NULL,	
	                address1 VARCHAR(80) NOT NULL,
	                reg_date TIMESTAMP NOT NULL
                )ENGINE=InnoDB DEFAULT CHARSET=utf8;
            '''
        cursor.execute(sql)
        db.commit()
finally:
    db.close()

# members db에 자료 추가
# db 연결
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='12345678', db='test', charset='utf8')
try:
    cursor = db.cursor()
    sql ="INSERT INTO members(id, name, pass, email, phone, address1, reg_date) VALUES(%s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql, ('midas', '홍길동', '1234', 'midastop@naver.com', '010-1234-5678', '경기 부천시 오정구 수주로 18 (고강동, 동문미도아파트)', '2019-10-06 12:10:30'))
    cursor.execute(sql, ('admin', '이순신', '1234', 'midastop1@naver.com', '010-4321-8765', '서울 구로구 구로중앙로34길 33-4(구로동, 영림빌딩)', '2019-10-11 11:20:50'))
    cursor.execute(sql, ('servlet', '강감찬', '1234', 'midas@daum.net', '010-5687-5678',' 서울 강남구 강남대로146길 28 (논현동, 논현아파트)', '2019-10-05 12:10:30'))
    db.commit()
finally:
    db.close()
