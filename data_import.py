import pandas as pd
import cx_Oracle
from dotenv import load_dotenv
import os

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

# Pobierz dane połączeniowe z pliku .env
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_service_name = os.getenv('DB_SERVICE_NAME')

# Utwórz DSN (Data Source Name)
dsn = cx_Oracle.makedsn(db_host, db_port, service_name=db_service_name)

# Połącz się z bazą danych
connection = cx_Oracle.connect(user=db_user, password=db_password, dsn=dsn)
cursor = connection.cursor()

# 1. Wczytaj dane z plików CSV do DataFrame
df_employees = pd.read_csv("employees.csv", encoding="ISO-8859-1")
df_departments = pd.read_csv("departments.csv", encoding="ISO-8859-1")
df_positions = pd.read_csv("positions.csv", encoding="ISO-8859-1")
df_salary = pd.read_csv("salary.csv", encoding="ISO-8859-1")

# Debug: Wyświetl pierwsze kilka wierszy DataFrame
print("Employees DataFrame:")
print(df_employees.head())

# 2. Import danych do tabeli departments
for index, row in df_departments.iterrows():
    cursor.execute("""
        INSERT INTO departments (department_name, business_unit) 
        VALUES (:department_name, :business_unit)
    """, [row['department_name'], row['business_unit']])

connection.commit()  # Zatwierdź zmiany w tabeli departments

# 3. Import danych do tabeli positions
for index, row in df_positions.iterrows():
    cursor.execute("""
        INSERT INTO positions (job_title) 
        VALUES (:job_title)
    """, [row['job_title']])

connection.commit()  # Zatwierdź zmiany w tabeli positions

# 5. Import danych do tabeli salary
for index, row in df_salary.iterrows():
    cursor.execute("""
        INSERT INTO salary (annual_salary, bonus_percent) 
        VALUES (:annual_salary, :bonus_percent)
    """, [row['annual_salary'], row['bonus_percent']])

connection.commit()  # Zatwierdź zmiany w tabeli salary

# 4. Import danych do tabeli employees
for index, row in df_employees.iterrows():
    try:
        # Debug: Sprawdzenie wartości ID
        print(f"Inserting row {index}: {row}")

        # Upewnij się, że id są poprawne i nie są NaN
        department_id = int(row['department_id']) if pd.notna(row['department_id']) else None
        position_id = int(row['position_id']) if pd.notna(row['position_id']) else None
        salary_id = int(row['salary_id']) if pd.notna(row['salary_id']) else None

        # Debug: Sprawdź wartości przed wstawieniem
        print(f"department_id: {department_id}, position_id: {position_id}, salary_id: {salary_id}")

        # Sprawdź, czy klucze obce istnieją
        cursor.execute("SELECT COUNT(*) FROM departments WHERE department_id = :id", [department_id])
        if cursor.fetchone()[0] == 0:
            print(f"Department ID {department_id} does not exist. Skipping row {index}.")
            continue

        cursor.execute("SELECT COUNT(*) FROM positions WHERE position_id = :id", [position_id])
        if cursor.fetchone()[0] == 0:
            print(f"Position ID {position_id} does not exist. Skipping row {index}.")
            continue

        cursor.execute("SELECT COUNT(*) FROM salary WHERE salary_id = :id", [salary_id])
        if cursor.fetchone()[0] == 0:
            print(f"Salary ID {salary_id} does not exist. Skipping row {index}.")
            continue

        cursor.execute("""
            INSERT INTO employees (first_name, last_name, age, gender, hire_date, termination_date, 
                    department_id, position_id, salary_id)
            VALUES (:first_name, :last_name, :age, :gender, 
                    TO_DATE(:hire_date, 'YYYY-MM-DD'), 
                    TO_DATE(:termination_date, 'YYYY-MM-DD'), 
                    :department_id, :position_id, :salary_id)
        """, [
            row['first_name'], row['last_name'], row['age'], row['gender'], 
            row['hire_date'], row['termination_date'], 
            department_id, position_id, salary_id  # Wstaw wartości jako int
        ])
    except cx_Oracle.DatabaseError as e:
        print(f"Error inserting row {index}: {row}. Error: {str(e)}")

connection.commit()  # Zatwierdź zmiany w tabeli employees

# Zamknięcie połączenia z bazą danych
cursor.close()
connection.close()

print("Dane zostały załadowane do bazy.")
