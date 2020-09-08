import secrets

def generate_random_id():
    return secrets.token_urlsafe(8)

def filter_tasks(global_tasks, status):
    response = []
    for task in global_tasks:
        if task["status"] == status:
            response.append(task)
    return response

def find_task(global_tasks, id: str):
    for task in global_tasks:
        if task["id"] == id:
            return task
    return None