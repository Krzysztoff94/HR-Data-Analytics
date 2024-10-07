-- oracle access to docker with import .csv files
CREATE OR REPLACE DIRECTORY csv_dir AS '/tmp';
GRANT READ, WRITE ON DIRECTORY csv_dir TO system;

-- SALARY import
-- data load to ext table from csv
CREATE OR REPLACE PROCEDURE import_salary_data AS
v_check NUMBER;
BEGIN
    -- import only when table is empty
    SELECT COUNT(salary_id) into v_check from salary;
    IF v_check = 0 THEN

    -- create ext table
    EXECUTE IMMEDIATE 'CREATE TABLE salary_ext (
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
            FIELDS TERMINATED BY '','' OPTIONALLY ENCLOSED BY ''"'' 
            (annual_salary CHAR(10), bonus_percent CHAR(10))
        )
        LOCATION (''salary.csv'')
    )
    REJECT LIMIT UNLIMITED';

    -- insert data to target table
    EXECUTE IMMEDIATE 'INSERT INTO salary (
        annual_salary, 
        bonus_percent
    )
    SELECT 
        TO_NUMBER(annual_salary), 
        TO_NUMBER(bonus_percent)
    FROM salary_ext';

    -- delete ext temp table
    EXECUTE IMMEDIATE 'DROP TABLE salary_ext';
    COMMIT;
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        RAISE; 
END import_salary_data;
/
-- use procedure
BEGIN
    import_salary_data;
END;
/
