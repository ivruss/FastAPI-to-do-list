import psycopg2

def database_creation(db_name):
    try:
        conn = psycopg2.connect(
        user='postgres',
        password='12042013',
        host='localhost',
        port='5432'
        )
        
        conn.autocommit = True
        
        cursor = conn.cursor()
        
        create_db_query = f'CREATE DATABASE {db_name};'
        cursor.execute(create_db_query)
        
        print(f"Database '{db_name}' created successfully")
        
    except psycopg2.Error as e:
        print("Error:", e)
        
    finally:
        cursor.close()
        conn.close()


def users_table_creation(table_name='users'):
    try:
        conn = psycopg2.connect(
        database='fastapi_users_test',
        user='postgres',
        password='12042013',
        host='localhost',
        port='5432'
        )
        
        conn.autocommit = True
        
        cursor = conn.cursor()
        
        create_table_query = f'''
        CREATE TABLE {table_name} (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(255),
            email VARCHAR(255),
            password VARCHAR(255)
        );
        '''
        cursor.execute(create_table_query)
        print (f"Table '{table_name}' created successfully")
        
    except psycopg2.Error as e:
        print("Error:", e)
        
    finally:
        cursor.close()
        conn.close()
 
        
def tasks_table_creation(table_name='tasks'):
    try:
        conn = psycopg2.connect(
        database='fastapi_users_test',
        user='postgres',
        password='12042013',
        host='localhost',
        port='5432'
        )
        
        conn.autocommit = True
        
        cursor = conn.cursor()
        
        create_table_query = f'''
        CREATE TABLE {table_name} (
            id SERIAL PRIMARY KEY,
            header VARCHAR(255),
            data TEXT,
            user_id INT
        );
        '''
        cursor.execute(create_table_query)
        print (f"Table '{table_name}' created successfully")
        
    except psycopg2.Error as e:
        print("Error:", e)
        
    finally:
        cursor.close()
        conn.close()
        
def table_redaction():
    try:
        conn = psycopg2.connect(
        database='fastapi_users_test',
        user='postgres',
        password='12042013',
        host='localhost',
        port='5432'
        )
        
        conn.autocommit = True
        
        cursor = conn.cursor()
        
        add_column_query = """
        ALTER TABLE users
        DROP COLUMN token;
        """

        cursor.execute(add_column_query)
        print ("Successful")
        
    except psycopg2.Error as e:
        print("Error:", e)
        
    finally:
        cursor.close()
        conn.close()
        