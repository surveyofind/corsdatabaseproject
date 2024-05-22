import pandas as pd
import mysql.connector

# Read CSV data into a DataFrame
df = pd.read_csv('CORSFINAL2.csv')

# Establish connection to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Root@123",
    database="new"
)
cursor = connection.cursor()

# Insert data into MySQL table
for index, row in df.iterrows():
    # Limit corsid to 50 characters
    corsid = str(row['corsid'])
    state_name = str(row['state_name'])
    site_name = str(row['site_name'])
    cursor.execute("INSERT INTO cors_app_gdc_data (corsid,state_name,site_name) VALUES (%s , %s , %s)", (corsid,state_name,site_name))

# Commit changes and close connection
connection.commit()
connection.close()
