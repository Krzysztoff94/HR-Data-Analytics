-- oracle access to docker salary.csv
CREATE OR REPLACE DIRECTORY csv_dir AS '/tmp';
GRANT READ, WRITE ON DIRECTORY csv_dir TO system;

-- insert data do ext table from csv
CREATE TABLE salary_ext (
    annual_salary CHAR(10),
    bonus_percent CHAR(10)
)
ORGANIZATION EXTERNAL
(
    TYPE ORACLE_LOADER
    DEFAULT DIRECTORY csv_dir
    ACCESS PARAMETERS
    (
        RECORDS DELIMITED BY NEWLINE
        FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
        (annual_salary CHAR(10), bonus_percent CHAR(10))
    )
    LOCATION ('salary.csv')
)
REJECT LIMIT UNLIMITED;

-- insert data to target table
INSERT INTO salary (
    annual_salary, 
    bonus_percent
)
SELECT 
    TO_NUMBER(annual_salary), 
    TO_NUMBER(bonus_percent)
FROM salary_ext;
