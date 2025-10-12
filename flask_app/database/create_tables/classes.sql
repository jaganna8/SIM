CREATE TABLE IF NOT EXISTS `classes` (
  `ID`                INT(11)        NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for the class',
  `Teacher_ID`        INT(11)        NOT NULL                COMMENT 'Reference to the teacher ID',
  `Start_Date`        DATE           NOT NULL                COMMENT 'Start date of the class',
  `End_Date`          DATE           NULL                    COMMENT 'End date of the class',
  `Possible_Credit`   DECIMAL(5, 2)  NOT NULL DEFAULT 0.00   COMMENT 'Possible credit for the class',
  `Credit_Type`       VARCHAR(50)    NOT NULL                COMMENT 'Type of credit (e.g., elective, core)',
  `Course_Name`       VARCHAR(255)   NOT NULL                COMMENT 'Name of the course',
  `School_Year`       INT(4)         NOT NULL                COMMENT 'School year associated with the class (e.g., 2023)',
  `Term`              VARCHAR(50)    NOT NULL                COMMENT 'Term (e.g., Fall, Spring)',
  `Status`            VARCHAR(50)    NOT NULL                COMMENT 'Status of the class (e.g., completed, in-progress)',
  PRIMARY KEY (`ID`),
  FOREIGN KEY (`Student_ID`) REFERENCES `users`(`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='Table for storing class information linked to students';
