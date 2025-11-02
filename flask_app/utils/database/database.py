import mysql.connector
import csv
from io import StringIO
import itertools
from math import pow
import os
import hashlib
import base64
from datetime import datetime, timedelta

class database:

    # init database 
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

    # create tables and seed database
    def build_db(self):
        self.create_tables()
        self.seed_database()

    # query db
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

    # create table
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

    # insert rows into specified table
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

    # hash given password
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
    
    # check if given password matches hashed password
    def check_password(self, password: str, hashed: str) -> bool:
        """
        Checks if the provided password matches the hashed password.
        """
        return self.hash_password(password) == hashed
    
    # seed database from csv files
    def seed_database(self):
        data_path = 'flask_app/database/inital_data/'
        for table in self.tables:
            csv_file = os.path.join(data_path, f"{table}.csv")
            if os.path.exists(csv_file):
                self.import_from_csv(table, csv_file)
            else:
                print(f"⚠️ CSV file for table '{table}' not found at: {csv_file}")

    # import data from csv file into specified table
    def import_from_csv(self, table_name: str, file_path: str):
        """
        Imports data from a CSV file into the given table.

        Args:
            table_name (str): The table name to import into.
            file_path (str): Full path to the CSV file.
        """
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)  # first row = column names
                rows = [row for row in reader if any(row)]  # skip empty lines

                if not rows:
                    print(f"⚠️ No data found in {file_path}")
                    return

                # Insert rows into the table using your existing insert_rows() method
                self.insert_rows(
                    table=table_name,
                    columns=headers,
                    parameters=rows
                )

                print(f"✅ Imported {len(rows)} records into '{table_name}' from {os.path.basename(file_path)}")

        except Exception as e:
            print(f"❌ Error importing {file_path} into {table_name}: {e}")