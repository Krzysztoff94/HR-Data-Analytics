HR Data Analytics
Overview:

The HR Data Analytics project aims to provide insights into employee data using a star schema database design. This project is designed to analyze various aspects of workforce management, including demographics, job roles, compensation, and retention rates. It leverages Python for data processing and Oracle Database running in Docker for data storage and retrieval.

Key Features:

Star Schema Design: The database is structured using a star schema, ensuring efficient querying and reporting.
Data Import: Automated scripts for importing employee data from CSV files into the database.
Data Analysis: Utilize Python scripts to analyze employee trends, such as salary distribution, demographics, and turnover rates.
Visualizations: Integration with data visualization tools to represent insights in an understandable format.
Technologies Used:

Database: Oracle Database (running in Docker)
Programming Languages: PL/SQL for database procedures and Python for data analysis and manipulation.
Data Processing: Utilization of libraries such as cx_Oracle for database connections and pandas for data manipulation.
Environment: The project is set up in a virtual environment to ensure dependency management.
Getting Started:

Clone the repository:
bash
Skopiuj kod
git clone https://github.com/yourusername/HR-Data-Analytics.git
Set up the Oracle Database in Docker.
Install required Python packages:
bash
Skopiuj kod
pip install -r requirements.txt
Configure the database connection settings using a .env file.
Run the data import script to load employee data into the database.
Execute analysis scripts to generate insights.
