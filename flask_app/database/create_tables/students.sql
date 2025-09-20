CREATE TABLE IF NOT EXISTS `students` (
  `ID`                           INT(11)        NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for the student',
  `First_Name`                   VARCHAR(255)   NOT NULL                COMMENT 'First name of the student',
  `Last_Name`                    VARCHAR(255)   NOT NULL                COMMENT 'Last name of the student',
  `Grade`                        VARCHAR(10)    NOT NULL                COMMENT 'Grade level of the student',
  `Expected_Graduation`          VARCHAR(10)           NOT NULL                COMMENT 'Expected graduation date of the student',
  `Gender`                       VARCHAR(10)    NOT NULL                COMMENT 'Gender of the student',
  `School`                       VARCHAR(255)   NOT NULL                COMMENT 'School the student is enrolled in',
  `Flag_FosterCare`              BOOLEAN        NOT NULL DEFAULT 0      COMMENT 'Indicates if the student is in foster care (0 or 1)',
  `Flag_EnglishLanguageLearner`  BOOLEAN        NOT NULL DEFAULT 0      COMMENT 'Indicates if the student is an English language learner (0 or 1)',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='Table for storing student information';
