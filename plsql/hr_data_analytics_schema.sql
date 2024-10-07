CREATE TABLE employees (
    employee_id NUMBER PRIMARY KEY,
    first_name VARCHAR2(50) NOT NULL,
    last_name VARCHAR2(50),
    age NUMBER,
    gender VARCHAR2(10),
    hire_date DATE,
    termination_date DATE,
    department_id NUMBER,
    position_id NUMBER,
    salary_id NUMBER,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (position_id) REFERENCES positions(position_id),
    FOREIGN KEY (salary_id) REFERENCES salary(salary_id)
);

CREATE TABLE departments (
    department_id NUMBER PRIMARY KEY,
    department_name VARCHAR2(100) NOT NULL,
    business_unit VARCHAR2(100)
);

CREATE TABLE positions (
    position_id NUMBER PRIMARY KEY,
    job_title VARCHAR2(100) NOT NULL
);

CREATE TABLE salary (
    salary_id NUMBER PRIMARY KEY,
    annual_salary NUMBER,
    bonus_percent NUMBER
);