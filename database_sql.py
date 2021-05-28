# db생성
# CREATE DATABASE o2 CHARACTER SET utf8 COLLATE utf8_general_ci;
# CREATE TABLE `topic` (
# 	`id` int(11) NOT NULL AUTO_INCREMENT,
# 	`title` varchar(100) NOT NULL,
# 	`description` text NOT NULL,
# 	`author` varchar(30) NOT NULL,
# 	PRIMARY KEY (id)
# 	) ENGINE=innoDB DEFAULT CHARSET=utf8;


import pymysql


db = pymysql.connect(
            host='localhost', 
            user='root', 
            password='1234', 
            db='gangnam',
            charset='utf8mb4')

cur = db.cursor()

# query = 'SELECT * FROM topic;'

# cur.execute(query)

# db.commit()

# data = cur.fetchall()

# print(data)



query = 'INSERT INTO `gangnam`.`topic` (`id`, `title`, `description`, `author`) VALUES (2 ,"자바" ,"자바(영어: Java, 문화어: 쟈바)는 썬 마이크로시스템즈의 제임스 고슬링(James Gosling)과 다른 연구원들이 개발한 객체 지향적 프로그래밍 언어이다. 1991년 그린 프로젝트(Green Project)라는 이름으로 시작해 1995년에 발표했다.", "GARY");'

cur.execute(query)

db.commit()

db.close()


# query = "UPDATE `topic` SET `title` = 'asdfasf', `author` = 'asdfasfsa' WHERE (`id` = '2')" # WHERE : 조건문

# cur.execute(query)
# db.commit()

# db.close()

# query = "DELETE FROM `gangnam`.`topic` WHERE (`id` = '2')"

# cur.execute(query)
# db.commit()

# db.close()


