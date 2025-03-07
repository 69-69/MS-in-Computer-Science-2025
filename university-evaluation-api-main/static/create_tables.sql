CREATE DATABASE IF NOT EXISTS degree_evaluation;
USE degree_evaluation;

CREATE TABLE Semester (
    semester_code ENUM('Spring', 'Summer', 'Fall'),
    PRIMARY KEY (semester_code)
    )
    ENGINE = INNODB;

INSERT INTO `Semester` VALUES ('Spring'),('Summer'),('Fall');

CREATE TABLE Degree_Level (
	level VARCHAR(50),
    PRIMARY KEY (level)
	)
    ENGINE = INNODB;
INSERT INTO Degree_Level VALUES ('Undergraduate'), ('Graduate');

CREATE TABLE Department (
	department_name VARCHAR(100),
    PRIMARY KEY (department_name)
	)
    ENGINE = INNODB;


CREATE TABLE Degree (
    degree_name VARCHAR(100),
    level VARCHAR(50),
    department_name VARCHAR(100),
    PRIMARY KEY (degree_name, level),
    FOREIGN KEY (department_name) REFERENCES Department(department_name),
    FOREIGN KEY (level) REFERENCES Degree_Level(level)
    )
    ENGINE = INNODB;

CREATE TABLE Course (
    course_number VARCHAR(8),
    course_name VARCHAR(200),
    PRIMARY KEY (course_number)
    )
    ENGINE = INNODB;

CREATE TABLE Degree_Course_Requirement (
    degree_name VARCHAR(100),
    degree_level VARCHAR(50),
    course_number VARCHAR(8),
    is_core BOOLEAN,
    PRIMARY KEY (degree_name, degree_level, course_number),
    FOREIGN KEY (degree_name, degree_level) REFERENCES Degree(degree_name, level),
    FOREIGN KEY (course_number) REFERENCES Course(course_number)
    )
    ENGINE = INNODB;

CREATE TABLE Instructor (
    instructor_id VARCHAR(8),
    name VARCHAR(100),
    PRIMARY KEY (instructor_id)
    )
    ENGINE = INNODB;

CREATE TABLE Section (
    section_id INT(3),
    course_number VARCHAR(8),
    instructor_id VARCHAR(8),
    year VARCHAR(4),
    semester ENUM('Spring', 'Summer', 'Fall'),
    enrollment INT,
    PRIMARY KEY (section_id, course_number, year, semester),
    FOREIGN KEY (course_number) REFERENCES Course(course_number),
    FOREIGN KEY (instructor_id) REFERENCES Instructor(instructor_id)
    )
    ENGINE = INNODB;

CREATE TABLE Goal (
    goal_code VARCHAR(4),
    degree_name VARCHAR(100),
    degree_level VARCHAR(50),
    course_number VARCHAR(8),
    goal_description TEXT,
    PRIMARY KEY (goal_code),
    FOREIGN KEY (degree_name, degree_level) REFERENCES Degree(degree_name, level),
    FOREIGN KEY (course_number) REFERENCES Course(course_number)
    )
    ENGINE = INNODB;

CREATE TABLE Section_Evaluation (
    goal_code VARCHAR(4),
    section_id INT(3),
    instructor_notes TEXT,
    number_of_a INT,
    number_of_b INT,
    number_of_c INT,
    number_of_d INT,
    number_of_f INT,
    course_number VARCHAR(8),
    year VARCHAR(4),
    semester ENUM('Spring', 'Summer', 'Fall'),
    PRIMARY KEY (goal_code, section_id, course_number, year, semester),
    FOREIGN KEY (goal_code) REFERENCES Goal(goal_code),
    FOREIGN KEY (section_id, course_number, year, semester) REFERENCES Section(section_id, course_number, year, semester)
    )
    ENGINE = INNODB;


LOCK TABLES `Department` WRITE;
/*!40000 ALTER TABLE `Department` DISABLE KEYS */;
INSERT INTO `Department` VALUES ('Biology'),('Business'),('Chemistry'),('Computer Science'),('Education'),('Engineering'),('Law'),('Mathematics'),('Medicine'),('Physics');
/*!40000 ALTER TABLE `Department` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `Degree` WRITE;
/*!40000 ALTER TABLE `Degree` DISABLE KEYS */;
INSERT INTO `Degree` VALUES ('BSc Biology','Undergraduate','Biology'),('MSc Biology','Graduate','Biology'),('BSc Chemistry','Undergraduate','Chemistry'),('MSc Chemistry','Graduate','Chemistry'),('BSc Computer Science','Undergraduate','Computer Science'),('MSc Computer Science','Graduate','Computer Science'),('BSc Mathematics','Undergraduate','Mathematics'),('MSc Mathematics','Graduate','Mathematics'),('BSc Physics','Undergraduate','Physics'),('MSc Physics','Graduate','Physics');
/*!40000 ALTER TABLE `Degree` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `Course` WRITE;
/*!40000 ALTER TABLE `Course` DISABLE KEYS */;
INSERT INTO `Course` VALUES ('CS101','Intro to Programming'),('CS102','Data Structures'),('CS103','Algorithms'),('CS104','Databases'),('CS105','Operating Systems'),('MA101','Calculus I'),('MA102','Linear Algebra'),('MA103','Discrete Mathematics'),('PH101','Mechanics'),('PH102','Electromagnetism');
/*!40000 ALTER TABLE `Course` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `Degree_Course_Requirement` WRITE;
/*!40000 ALTER TABLE `Degree_Course_Requirement` DISABLE KEYS */;
INSERT INTO `Degree_Course_Requirement` VALUES ('BSc Computer Science','Undergraduate','CS101',1),('BSc Computer Science','Undergraduate','CS102',1),('BSc Mathematics','Undergraduate','MA101',1),('BSc Mathematics','Undergraduate','MA102',1),('BSc Physics','Undergraduate','PH101',1),('BSc Physics','Undergraduate','PH102',1),('MSc Computer Science','Graduate','CS103',1),('MSc Computer Science','Graduate','CS104',1),('MSc Mathematics','Graduate','CS105',1),('MSc Mathematics','Graduate','MA103',1);
/*!40000 ALTER TABLE `Degree_Course_Requirement` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `Goal` WRITE;
/*!40000 ALTER TABLE `Goal` DISABLE KEYS */;
INSERT INTO `Goal` VALUES ('G001','BSc Computer Science','Undergraduate','CS101','Understand programming basics'),('G002','BSc Computer Science','Undergraduate','CS102','Implement efficient algorithms'),('G003','MSc Computer Science','Graduate','CS103','Master algorithm design'),('G004','MSc Computer Science','Graduate','CS104','Design scalable databases'),('G005','BSc Mathematics','Undergraduate','MA101','Grasp calculus concepts'),('G006','BSc Mathematics','Undergraduate','MA102','Understand linear algebra'),('G007','MSc Mathematics','Graduate','MA103','Develop discrete math skills'),('G008','MSc Mathematics','Graduate','CS105','Master OS principles'),('G009','BSc Physics','Undergraduate','PH101','Understand mechanics fundamentals'),('G010','BSc Physics','Undergraduate','PH102','Learn electromagnetism basics');
/*!40000 ALTER TABLE `Goal` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `Instructor` WRITE;
/*!40000 ALTER TABLE `Instructor` DISABLE KEYS */;
INSERT INTO `Instructor` VALUES ('INS001','Dr. Smith'),('INS002','Dr. Johnson'),('INS003','Dr. Brown'),('INS004','Dr. Taylor'),('INS005','Dr. Miller'),('INS006','Dr. Wilson'),('INS007','Dr. Moore'),('INS008','Dr. Lee'),('INS009','Dr. Harris'),('INS010','Dr. Clark');
/*!40000 ALTER TABLE `Instructor` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `Section` WRITE;
/*!40000 ALTER TABLE `Section` DISABLE KEYS */;
INSERT INTO `Section` VALUES (1,'CS101','INS001','2024','Fall',30),(2,'CS102','INS002','2024','Fall',40),(3,'CS103','INS003','2024','Fall',50),(4,'CS104','INS004','2024','Fall',35),(5,'CS105','INS005','2024','Fall',25),(6,'MA101','INS006','2024','Fall',45),(7,'MA102','INS007','2024','Fall',30),(8,'MA103','INS008','2024','Fall',20),(9,'PH101','INS009','2024','Fall',25),(10,'PH102','INS010','2024','Fall',40),(11,'CS101','INS010','2023','Spring',100),(12,'CS101','INS010','2023','Summer',100),(13,'CS101','INS009','2023','Spring',100),(14,'CS101','INS008','2023','Fall',52);
/*!40000 ALTER TABLE `Section` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `Section_Evaluation` WRITE;
/*!40000 ALTER TABLE `Section_Evaluation` DISABLE KEYS */;
INSERT INTO `Section_Evaluation` VALUES ('G001',1,'Engaging class',5,10,15,2,1,'CS101','2024','Fall'),('G002',2,'Challenging material',6,9,12,3,2,'CS102','2024','Fall'),('G003',3,'Complex algorithms',7,8,10,4,3,'CS103','2024','Fall'),('G004',4,'Practical examples',8,7,10,5,4,'CS104','2024','Fall'),('G005',5,'Mathematical rigor',9,6,8,3,2,'CS105','2024','Fall'),('G006',6,'Clear concepts',10,5,10,2,1,'MA101','2024','Fall'),('G007',7,'Detailed proofs',11,4,9,3,2,'MA102','2024','Fall'),('G008',8,'Practical applications',12,3,8,4,3,'MA103','2024','Fall'),('G009',9,'Physical insights',13,2,7,3,1,'PH101','2024','Fall'),('G010',10,'Theoretical depth',14,1,6,2,1,'PH102','2024','Fall');
/*!40000 ALTER TABLE `Section_Evaluation` ENABLE KEYS */;
UNLOCK TABLES;
