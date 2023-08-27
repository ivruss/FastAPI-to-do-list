import psycopg2
from passlib.hash import bcrypt_sha256


def names_data_generator():
    names = ['Glenn', 'Dave', 'Duke', 'Alex', 'Lindy', 'Bart', 'Lisa']

    for name in names:

        data = {'first_name': name, 'email': f'{name}@gmail.com', 'password': f'{name}123', 'token': f'{name}token'}



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


def table_creation(table_name):
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
            password VARCHAR(255),
            token TEXT
        );
        '''
        cursor.execute(create_table_query)
        print (f"Table '{table_name}' created successfully")
        
    except psycopg2.Error as e:
        print("Error:", e)
        
    finally:
        cursor.close()
        conn.close()
      
        
def post_data(data):
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
        
        insert_query = """
        INSERT INTO users (first_name, email, password, token)
        VALUES (%s, %s, %s, %s);
        """
        
        password = bcrypt_sha256.hash(data['password'])
        
        data_to_insert = (
            data['first_name'],
            data['email'],
            password,
            data['token']
        )
        
        cursor.execute(insert_query, data_to_insert)
        conn.commit()

    except psycopg2.Error as e:
        print("Error:", e)
        
    finally:
        cursor.close()
        conn.close()


def get_data(user_id=None):
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
        
        result = []
        
        if not user_id:
            
            select_query = "SELECT * FROM users;"
            
            cursor.execute(select_query)
            
            rows = cursor.fetchall()
            for row in rows:
                result.append({'id': row[0], 'first_name': row[1], 'email': row[2], 'password': row[3], 'token': row[4]})
                
        
        if user_id:
            
            select_query = f'SELECT * FROM users WHERE id = {user_id};'
            cursor.execute(select_query, user_id)
            rows = cursor.fetchall()
            
            for row in rows:
                result = {'id': row[0], 'first_name': row[1], 'email': row[2], 'password': row[3], 'token': row[4]}

        return result
            
    except psycopg2.Error as e:
        print("Error:", e)
        
    finally:
        cursor.close()
        conn.close()


def delete_data(user_id):
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
        
        delete_query = f"DELETE FROM users WHERE id = {user_id};"
        
        cursor.execute(delete_query)
        conn.commit()

        
    except psycopg2.Error as e:
        print("Error:", e)
        
    finally:
        cursor.close()
        conn.close()


def update_data(user_id, data):
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
        
        update_string = ', '.join([f"{key} = %s" for key in data.keys()])
        update_query = f"""
        UPDATE users
        SET {update_string}
        WHERE id = %s;
        """
        
        query_params = list(data.values())
        query_params.append(user_id)
        
        cursor.execute(update_query, query_params)
        conn.commit()
        
    except psycopg2.Error as e:
        print("Error:", e)
        
    finally:
        cursor.close()
        conn.close()


def log_in(data):
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
        
        result = []
            
        user_email = data['email']
        password = data['password']    
            
        select_query = 'SELECT password, id FROM users WHERE email = %s;'
        cursor.execute(select_query, (user_email,))
        rows = cursor.fetchall()
            
        for row in rows:
            if bcrypt_sha256.verify(password, row[0]):
                return row[1]
            else:
                return False
            
    except psycopg2.Error as e:
        print("Error:", e)
        
    finally:
        cursor.close()
        conn.close()


def if_user_id_in_database(user_id):
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

        select_query = f'SELECT id FROM users WHERE id = {user_id};'
        cursor.execute(select_query)
        rows = cursor.fetchall()
            
        if rows:
            return True
        
        else:
            return False
            
    except psycopg2.Error as e:
        print('Error: ', e)
        
    finally:
        cursor.close()
        conn.close()
        
        
        

