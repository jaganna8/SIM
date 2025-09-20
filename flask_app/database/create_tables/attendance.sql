CREATE TABLE IF NOT EXISTS `attendance` (
  `ID`          INT(11)       NOT NULL AUTO_INCREMENT COMMENT 'Unique identifier for the attendance record',
  `Student_ID`  INT(11)       NOT NULL                COMMENT 'Reference to the student ID',
  `Classes_ID`  INT(11)       NOT NULL                COMMENT 'Reference to the class ID',
  `Date`        DATE          NOT NULL                COMMENT 'Date of the attendance record',
  `Code`        VARCHAR(10)   NOT NULL                COMMENT 'Attendance code (e.g., P for present, A for absent)',
  PRIMARY KEY (`ID`),
  FOREIGN KEY (`Student_ID`) REFERENCES `students`(`ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`Classes_ID`) REFERENCES `classes`(`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='Table for storing attendance records for students in classes';
