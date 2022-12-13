-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2022-12-13 02:44:07.304

-- tables
-- Table: FCE_records
CREATE TABLE FCE_records (
    Year int  NOT NULL,
    Sem varchar(200)  NOT NULL,
    College varchar(200)  NOT NULL,
    Dept varchar(200)  NOT NULL,
    Num int  NOT NULL,
    Section varchar(200)  NOT NULL,
    Instructor varchar(200)  NOT NULL,
    Course_name varchar(200)  NOT NULL,
    Hours decimal(4,2)  NULL,
    Rating decimal(3,2)  NULL,
    CONSTRAINT FCE_records_pk PRIMARY KEY (Year,Sem,College,Dept,Num,Section,Instructor,Course_name)
);

-- End of file.

