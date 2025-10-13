import sqlite3
import mysql.connector
import csv
from io import StringIO
import itertools
from math import pow
import os
import hashlib
import base64
from datetime import datetime, timedelta
import random

class database:

    def __init__(self, purge = False):

        self.database = os.environ.get('DB_NAME', 'mydb')
        self.host     = os.environ.get('DB_HOST', 'db')  # Use docker-compose service name
        self.user     = os.environ.get('DB_USER', 'root')
        self.port     = int(os.environ.get('DB_PORT', 3306))
        self.password = os.environ.get('DB_PASSWORD', 'rootpass')
        self.tables   = ['students', 'users', 'classes', 'enrollment', 'attendance', 'finalgrades']
        
        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                                }
        #-----------------------------------------------------------------------------

    def build_db(self):
        self.create_tables()
        self.seed_database()


    def query(self, query = "SELECT * FROM students", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def create_tables(self, purge=False, data_path = 'flask_app/database/'):
        ''' FILL ME IN WITH CODE THAT CREATES YOUR DATABASE TABLES.'''

        #should be in order or creation - this matters if you are using forign keys.
         
        if purge:
            for table in self.tables[::-1]:
                self.query(f"""DROP TABLE IF EXISTS {table}""")
            
        # Execute all SQL queries in the /database/create_tables directory.
        for table in self.tables:
            
            sql_path = os.path.join(data_path, f"create_tables/{table}.sql")
            try:
                with open(sql_path, 'r') as file:
                    sql_script = file.read()
                    self.query(sql_script)
            except FileNotFoundError:
                print(f"SQL file for table '{table}' not found at path: {sql_path}")
            except Exception as e:
                print(f"An error occurred while creating table '{table}': {e}")

    def insert_rows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        
        # Check if there are multiple rows present in the parameters
        has_multiple_rows = any(isinstance(el, list) for el in parameters)
        keys, values      = ','.join(columns), ','.join(['%s' for x in columns])
        
        # Construct the query we will execute to insert the row(s)
        query = f"""INSERT IGNORE INTO {table} ({keys}) VALUES """
        if has_multiple_rows:
            for p in parameters:
                query += f"""({values}),"""
            query     = query[:-1] 
            parameters = list(itertools.chain(*parameters))
        else:
            query += f"""({values}) """                      
        
        insert_id = self.query(query,parameters)[0]['LAST_INSERT_ID()']         
        return insert_id

    def hash_password(self, password: str) -> str:
        """
        Hashes a password using PBKDF2-HMAC-SHA256 with a salt and returns the base64-encoded hash.
        """
        salt = self.encryption['oneway']['salt']
        n = self.encryption['oneway']['n']
        r = self.encryption['oneway']['r']
        p = self.encryption['oneway']['p']
        # Using PBKDF2-HMAC-SHA256 for password hashing
        dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return base64.b64encode(dk).decode('utf-8')
    
    def check_password(self, password: str, hashed: str) -> bool:
        """
        Checks if the provided password matches the hashed password.
        """
        return self.hash_password(password) == hashed
    
    def seed_database(self):
        # add a default admin user if one does not exist
        admin_email = "admin@example.com"
        existing = self.query("SELECT * FROM users WHERE Email = %s", (admin_email,))

        if not existing:
            # Hash the password using your existing method
            admin_password = "AdminPass123"  # choose a secure default
            hashed = self.hash_password(admin_password)

            self.insert_rows(
                table="users",
                columns=["Email", "Password_Hash", "Role"],
                parameters=[[admin_email, hashed, "admin"]]
            )

        #add a default teacher user if one does not exist
        teacher_email = "teacher@example.com"
        teacher_password = self.hash_password("TeacherPass123")
        existing = self.query("SELECT * FROM users WHERE Email = %s", (teacher_email,))
        if not existing:
            self.insert_rows(
                table="users",
                columns=["Email", "Password_Hash", "Role"],
                parameters=[[teacher_email, teacher_password, "teacher"]]
            )

        #add sample students
        students = [
            ["Alice", "Johnson", "9", "2028", "F", "Wood HS", 0, 1],
            ["Bob", "Smith", "10", "2027", "M", "Unified HS", 0, 0],
            ["Charlie", "Lee", "11", "2026", "M", "Green HS", 1, 0],
            ["Diana", "Garcia", "12", "2025", "F", "Wood HS", 1, 1]
        ]
        
        for student in students:
            self.insert_rows(
                table="students",
                columns=["First_Name", "Last_Name", "Grade", "Expected_Graduation", "Gender",
                         "School", "Flag_FosterCare", "Flag_EnglishLanguageLearner"], parameters=[student]
            )
            
        #add sample classes
        teacher_id = self.query("SELECT ID FROM users WHERE Email = %s", (teacher_email,))[0]['ID']
        classes = [
            [teacher_id, "2025-09-01", "2026-06-01", 1.0, "Core", "Math 101", 2025, "Fall", "in-progress"],
            [teacher_id, "2025-09-01", "2026-06-01", 1.0, "Core", "English 101", 2025, "Fall", "in-progress"]
        ]

        for c in classes: 
            self.insert_rows(
                table="classes",
                columns=["Teacher_ID", "Start_Date", "End_Date", "Possible_Credit", "Credit_Type",
                         "Course_Name", "School_Year", "Term", "Status"], parameters=[c]
            )