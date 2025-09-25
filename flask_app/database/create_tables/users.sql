CREATE TABLE IF NOT EXISTS `users` (
    ID SERIAL PRIMARY KEY,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Password_Hash VARCHAR(255) NOT NULL,
    `Role` VARCHAR(10) NOT NULL CHECK (`Role` IN ('teacher', 'admin'))
);