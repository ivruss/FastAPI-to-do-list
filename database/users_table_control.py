import psycopg2
from passlib.hash import bcrypt_sha256
      
        
def post_user(data):
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
        INSERT INTO users (first_name, email, password)
        VALUES (%s, %s, %s);
        """
        
        password = bcrypt_sha256.hash(data['password'])
        
        data_to_insert = (
            data['first_name'],
            data['email'],
            password
        )
        
        cursor.execute(insert_query, data_to_insert)
        conn.commit()

    except psycopg2.Error as e:
        print("Error:", e)
        
    finally:
        cursor.close()
        conn.close()


def get_user(user_id=None):
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
                result.append({'id': row[0], 'first_name': row[1], 'email': row[2], 'password': row[3]})
                
        
        if user_id:
            
            select_query = f'SELECT * FROM users WHERE id = {user_id};'
            cursor.execute(select_query, user_id)
            rows = cursor.fetchall()
            
            for row in rows:
                result = {'id': row[0], 'first_name': row[1], 'email': row[2], 'password': row[3]}

        return result
            
    except psycopg2.Error as e:
        print("Error:", e)
        
    finally:
        cursor.close()
        conn.close()


def delete_user(user_id):
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


def update_user(user_id, data):
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
    

