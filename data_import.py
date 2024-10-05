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

# Wczytaj dane z CSV do DataFrame
df = pd.read_csv("employees.csv")

# 1. Import danych do tabeli wymiarów: departments
unique_departments = df[['Department']].drop_duplicates()

for index, row in unique_departments.iterrows():
    cursor.execute("""
        INSERT INTO departments (department_name) 
        VALUES (:department_name)
    """, [row['Department']])

# 2. Import danych do tabeli wymiarów: job_titles
unique_job_titles = df[['Job Title']].drop_duplicates()

for index, row in unique_job_titles.iterrows():
    cursor.execute("""
        INSERT INTO job_titles (job_title) 
        VALUES (:job_title)
    """, [row['Job Title']])

# Pobranie zaktualizowanych danych z tabeli departments i job_titles
connection.commit()

# 3. Import danych do tabeli employees
for index, row in df.iterrows():
    # Pobierz ID departamentu
    cursor.execute("""
        SELECT department_id FROM departments WHERE department_name = :department_name
    """, [row['Department']])
    department_id = cursor.fetchone()[0]
    
    # Pobierz ID stanowiska
    cursor.execute("""
        SELECT job_title_id FROM job_titles WHERE job_title = :job_title
    """, [row['Job Title']])
    job_title_id = cursor.fetchone()[0]

    # Wstaw dane do tabeli employees (bez wynagrodzeń i bonusów)
    cursor.execute("""
        INSERT INTO employees (employee_id, full_name, department_id, job_title_id, gender, ethnicity, age, hire_date, country, city, exit_date)
        VALUES (:employee_id, :full_name, :department_id, :job_title_id, :gender, :ethnicity, :age, :hire_date, :country, :city, :exit_date)
    """, [
        row['Employee ID'], row['Full Name'], department_id, job_title_id, row['Gender'], 
        row['Ethnicity'], row['Age'], row['Hire Date'], row['Country'], row['City'], row['Exit Date']
    ])

# 4. Import danych do tabeli salaries
for index, row in df.iterrows():
    # Wstaw dane do tabeli salaries
    cursor.execute("""
        INSERT INTO salaries (employee_id, annual_salary, bonus_percent, effective_date)
        VALUES (:employee_id, :annual_salary, :bonus_percent, :effective_date)
    """, [
        row['Employee ID'], row['Annual Salary'], row['Bonus %'], row['Hire Date']
    ])

# Zatwierdzenie wszystkich operacji
connection.commit()

# Zamknięcie połączenia z bazą danych
cursor.close()
connection.close()

print("Dane zostały załadowane do bazy.")
