CREATE TABLE IF NOT EXISTS `finalgrades` (
  `ID`                INT(11)        NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for the grade record',
  `Student_ID`        INT(11)        NOT NULL                COMMENT 'Reference to the student ID',
  `Class_ID`        INT(11)        NOT NULL                COMMENT 'Reference to the class ID',
  `Letter_Grade`      CHAR(2)        NOT NULL                COMMENT 'Letter grade (e.g., A, B, C, etc.)',
  `Grade_Level`       INT(2)         NOT NULL                COMMENT 'Grade level (e.g., 9 for 9th grade)',
  `Credit_Type`       VARCHAR(50)    NOT NULL                COMMENT 'Type of credit (e.g., elective, core)',
  `Credit_Awarded`    DECIMAL(5, 2)  NOT NULL DEFAULT 0.00   COMMENT 'Credit awarded for the course',
  `Credit_Potential`  DECIMAL(5, 2)  NOT NULL DEFAULT 0.00   COMMENT 'Maximum possible credit for the course',
  PRIMARY KEY (`ID`),
  FOREIGN KEY (`Student_ID`) REFERENCES `students`(`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`Class_ID`) REFERENCES `classes`(`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='Table for storing final grades for students in classes';
