import jwt
import datetime
from fastapi import FastAPI, HTTPException
from database.users_table_control import get_user, post_user, delete_user, update_user, if_user_id_in_database, log_in
from database.tasks_table_control import post_task, get_task, delete_task, update_task, if_task_id_in_database, if_task_belongs_to

app = FastAPI()


@app.get("/get")
def get_all_users():
    data = get_user()
    return data


@app.get("/get/{user_id}")
def query_user_by_id(user_id:int):
    if not if_user_id_in_database(user_id):
        raise HTTPException(status_code=404, detail="Item not found")

    data = get_user(user_id)
    return data
    
    
@app.delete('/delete/{user_id}')
def delete_user(user_id:int):
    delete_user(user_id)
    return 200
    
        
@app.patch('/patch/{user_id}')
def patch_user(user_id:int, user_data: dict):
    if not if_user_id_in_database(user_id):
        raise HTTPException(status_code=404, detail="Item not found")
    
    update_user(user_id, user_data)        
    return 200


@app.post('/post')
def add_user(user: dict):
    post_user(user)
    return 200


@app.post('/login')
def log_in_user(data: dict):
    if not log_in(data):
       raise HTTPException(status_code=401, detail="Wrong password") 
   
    user_id = log_in(data)
        
    payload = {
    "user_id": user_id,
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
        
    secret_key = 'qwad1bb67nqy'
        
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token
    
    
@app.post('/{user_id}/post')
def add_task(user_id, data:dict):
    if not if_user_id_in_database(user_id):
        raise HTTPException(status_code=404, detail="Item not found")
    
    data['user_id'] = user_id
    post_task(data)
    return 200


@app.get('/{user_id}/get')
def get_users_task(user_id):
    if not if_user_id_in_database(user_id):
        raise HTTPException(status_code=404, detail="Item not found")
    
    
    return get_task(user_id)


@app.delete('/{user_id}/delete/{task_id}')
def delete_user(user_id:int, task_id:int):
    if not if_user_id_in_database(user_id):
        raise HTTPException(status_code=404, detail="Item not found")
    if not if_task_id_in_database(task_id):
        raise HTTPException(status_code=404, detail="Item not found")
    if not if_task_belongs_to(user_id, task_id):
        raise HTTPException(status_code=403, detail="Forbidden action for this user")
    
    delete_task(task_id)
    return 200


@app.patch('/{user_id}/patch/{task_id}')
def patch_user(user_id:int, task_data:dict, task_id:int):
    if not if_user_id_in_database(user_id):
        raise HTTPException(status_code=404, detail="Item not found")
    if not if_task_id_in_database(task_id):
        raise HTTPException(status_code=404, detail="Item not found")
    if not if_task_belongs_to(user_id, task_id):
        raise HTTPException(status_code=403, detail="Forbidden action for this user")
    
    update_task(task_id, task_data)        
    return 200

    
        