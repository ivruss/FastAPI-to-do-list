import psycopg2

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
        ALTER TABLE tasks
        ADD COLUMN date TIMESTAMP;
        """

        cursor.execute(add_column_query)
        print ("Успешно")
        
    except psycopg2.Error as e:
        print("Error:", e)
        
    finally:
        cursor.close()
        conn.close()

def post_task(data):
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
        INSERT INTO tasks (header, data, user_id, date)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP);
        """
    
        data_to_insert = (
            data['header'],
            data['data'],
            data['user_id'],
        )
        
        cursor.execute(insert_query, data_to_insert)
        conn.commit()
        return 200
        
    except psycopg2.Error as e:
        print("Error:", e)
        
    finally:
        cursor.close()
        conn.close()
        

def get_task(user_id=None):
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
            
            select_query = "SELECT * FROM tasks;"
            
            cursor.execute(select_query)
            
            rows = cursor.fetchall()
            for row in rows:
                result.append({'id': row[0], 'header': row[1], 'data': row[2], 'date': row[4]})
                
        
        if user_id:
            
            select_query = f'SELECT * FROM tasks WHERE user_id = {user_id};'
            cursor.execute(select_query, user_id)
            rows = cursor.fetchall()
            
            for row in rows:
                result.append({'id': row[0], 'header': row[1], 'data': row[2], 'date': row[4]})

        return result
        
    except psycopg2.Error as e:
        print("Error:", e)
        
    finally:
        cursor.close()
        conn.close()


def if_task_id_in_database(task_id):
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
            
        select_query = f'SELECT id FROM tasks WHERE id = {task_id};'
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


def if_task_belongs_to(user_id, task_id):
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

        select_query = f'SELECT user_id FROM tasks WHERE id = {task_id};'
        cursor.execute(select_query)
        rows = cursor.fetchall()
        
        if if_task_id_in_database(task_id):
            if rows[0][0] == user_id:
                return True
            else:
                return False
            
        else:
            return ('There\'s no such task ID in the database')
            
    except psycopg2.Error as e:
        print('Error: ', e)
        
    finally:
        cursor.close()
        conn.close()
        

def delete_task(task_id):
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
        
        delete_query = f"DELETE FROM tasks WHERE id = {task_id};"
        
        if if_task_id_in_database(task_id):
            cursor.execute(delete_query)
            conn.commit()
            
        else:
            return ('There\'s no such task ID in the database')

        
    except psycopg2.Error as e:
        print("Error:", e)
        
    finally:
        cursor.close()
        conn.close()
        
def update_task(task_id, data):
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
        UPDATE tasks
        SET {update_string}
        WHERE id = %s;
        """
        
        query_params = list(data.values())
        query_params.append(task_id)
        
        cursor.execute(update_query, query_params)
        conn.commit()
        
    except psycopg2.Error as e:
        print("Error:", e)
        
    finally:
        cursor.close()
        conn.close()
        
    
        
