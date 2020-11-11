#-- DATABASE 생성 및 선택


CREATE DATABASE IF NOT EXISTS pythondb;
use pythondb;
USE MYSQL;
DROP DATABASE pythondb;
# 테이블 생성
DROP TABLE IF EXISTS member;
CREATE TABLE IF NOT EXISTS member(
	no INTEGER PRIMARY KEY AUTO_INCREMENT,
	id VARCHAR(20) NOT NULL,
	name VARCHAR(10) NOT NULL,
	pass VARCHAR(20) NOT NULL,
	email VARCHAR(30) NOT NULL,
	phone VARCHAR(13) NOT NULL,	
	address1 VARCHAR(80) NOT NULL,
	reg_date TIMESTAMP NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

# 회원 정보 추가
INSERT INTO member(id, name, pass, email, phone, address1, reg_date) 
VALUES('midas', '홍길동', '1234', 'midastop@naver.com', '010-1234-5678', 
	'경기 부천시 오정구 수주로 18 (고강동, 동문미도아파트)', '2019-10-06 12:10:30');
INSERT INTO member(id, name, pass, email, phone, address1, reg_date) 
VALUES('admin', '이순신', '1234', 'midastop1@naver.com', '010-4321-8765', 
	'서울 구로구 구로중앙로34길 33-4(구로동, 영림빌딩)', '2019-10-11 11:20:50');
INSERT INTO member(id, name, pass, email, phone, address1, reg_date) 
VALUES('servlet', '강감찬', '1234', 'midas@daum.net', '010-5687-5678',  
	'서울 강남구 강남대로146길 28 (논현동, 논현아파트)', '2019-10-05 12:10:30');

commit;
SELECT * FROM member;
