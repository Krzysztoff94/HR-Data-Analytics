CREATE OR REPLACE TRIGGER trg_employees_before_insert
BEFORE INSERT ON employees
FOR EACH ROW
BEGIN
    :NEW.employee_id := employee_id_seq.NEXTVAL;
END;

CREATE OR REPLACE TRIGGER trg_departments_before_insert
BEFORE INSERT ON departments
FOR EACH ROW
BEGIN
    :NEW.department_id := departments_id_seq.NEXTVAL;
END;

CREATE OR REPLACE TRIGGER trg_positions_before_insert
BEFORE INSERT ON positions
FOR EACH ROW
BEGIN
    :NEW.position_id := positions_id_seq.NEXTVAL;
END;

CREATE OR REPLACE TRIGGER trg_salary_before_insert
BEFORE INSERT ON salary
FOR EACH ROW
BEGIN
    :NEW.salary_id := salary_id_seq.NEXTVAL;
END;

