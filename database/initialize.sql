
drop database if exists fce_db;

create database fce_db;

\connect fce_db

\i database/create.sql

\copy FCE_records FROM 'database/FCE_raw.csv' csv header

-- create an aggregate from raw records for querying 
CREATE TABLE FCE_info AS 
    (
        SELECT Num as "cnum", Instructor AS "instructor", Course_name AS "cname", 
               AVG(Hours)::decimal(4,2) AS "hours", AVG(Rating)::decimal(3,2) AS "rating" 
          FROM FCE_records
         GROUP BY Num, Instructor, Course_name
    ); 
