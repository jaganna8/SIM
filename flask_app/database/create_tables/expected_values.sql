CREATE TABLE IF NOT EXISTS `expected_values` (
    `ID` INT(11) AUTO_INCREMENT NOT NULL,
    `Baseline_GPA` DECIMAL(3,2) NOT NULL COMMENT 'Target GPA (e.g., 3.50)',
    `Baseline_Attendance` DECIMAL(5,2) NOT NULL COMMENT 'Target attendance percentage (e.g., 95.00 for 95%)',
    `Credits_Grade9` DECIMAL(4,1) NOT NULL COMMENT 'Expected cumulative credits by end of 9th grade (including current courses)',
    `Credits_Grade10` DECIMAL(4,1) NOT NULL COMMENT 'Expected cumulative credits by end of 10th grade',
    `Credits_Grade11` DECIMAL(4,1) NOT NULL COMMENT 'Expected cumulative credits by end of 11th grade',
    `Credits_Grade12` DECIMAL(4,1) NOT NULL COMMENT 'Expected cumulative credits by end of 12th grade (graduation: 19 required)',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='Table for storing expected gpa, attendance, credits, etc';