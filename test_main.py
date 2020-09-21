from fastapi.testclient import TestClient
from helpers.models import InTask
from main import app

client = TestClient(app)

def test_read_main_returns_not_found():
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

def test_post_task_successful():
    in_task = {"title": "Titulo teste", "subtitle": "Subtitulo teste"}
    response = client.post("/tasks", json=in_task)
    assert response.status_code == 201
    in_task["status"] = "to-do"
    in_task["id"] = response.json()["id"]
    assert response.json() == in_task
    client.delete(f"/tasks/{in_task['id']}")

def test_post_task_failed():
    in_task = {"subtitle": "Subtitulo teste"}
    response = client.post("/tasks", json=in_task)
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 'title'], 'msg': 'field required', 'type': 'value_error.missing'}]}

def test_get_task_by_id_successful():
    in_task = {"title": "Titulo teste", "subtitle": "Subtitulo teste"}
    response = client.post("/tasks", json=in_task)
    in_task["status"] = response.json()["status"]
    in_task["id"] = response.json()["id"]

    response = client.get(f"/tasks?task_id={in_task['id']}")
    assert response.status_code == 200
    assert response.json() == [in_task]

    client.delete(f"/tasks/{in_task['id']}")

def test_get_all_tasks_successful():
    tasks = []
    for i in range(3):
        tasks.append({"title": f"Titulo teste{i}", "subtitle": f"Subtitulo teste{i}"})
        response = client.post("/tasks", json=tasks[i])
        tasks[i]["status"] = response.json()["status"]
        tasks[i]["id"] = response.json()["id"]

    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == tasks
    for task in tasks:
        client.delete(f"/tasks/{task['id']}")

def test_get_tasks_by_status():
    tasks = []
    for i in range(3):
        tasks.append({"title": f"Titulo teste{i}", "subtitle": f"Subtitulo teste{i}"})
        response = client.post("/tasks", json=tasks[i])
        tasks[i]["status"] = response.json()["status"]
        tasks[i]["id"] = response.json()["id"]

    response = client.get("/tasks?status=to-do")
    assert response.status_code == 200
    assert response.json() == tasks
    
    for task in tasks:
        client.delete(f"/tasks/{task['id']}")

def test_get_task_by_inexistent_id():
    response = client.get("/tasks?task_id=unknown__id")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Tarefa unknown__id não encontrada'}    

def test_get_task_by_invalid_status():
    response = client.get("/tasks?status=unknown_status")
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['query', 'status'], 'msg': "value is not a valid enumeration member; permitted: 'to-do', 'done'", 'type': 'type_error.enum', 'ctx': {'enum_values': ['to-do', 'done']}}]}

def test_patch_task_successful():
    in_task = {"title": "Titulo teste", "subtitle": "Subtitulo teste"}
    response = client.post("/tasks", json=in_task)
    in_task["status"] = response.json()["status"]
    in_task["id"] = response.json()["id"]

    response = client.patch(f"/tasks/{in_task['id']}", json={"status": "done"})

    in_task["status"] = "done"

    assert response.status_code == 200
    assert response.json() == in_task

def test_patch_task_invalid_status():
    in_task = {"title": "Titulo teste", "subtitle": "Subtitulo teste"}
    response = client.post("/tasks", json=in_task)
    in_task["status"] = response.json()["status"]
    in_task["id"] = response.json()["id"]

    response = client.patch(f"/tasks/{in_task['id']}", json={"status": "sei la"})

    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 'status'], 'msg': "value is not a valid enumeration member; permitted: 'to-do', 'done'", 'type': 'type_error.enum', 'ctx': {'enum_values': ['to-do', 'done']}}]}

def test_patch_by_invalid_id():
    response = client.patch("/tasks/unknown__id", json={"subtitle": "teste"})
    assert response.status_code == 404
    assert response.json() == {'detail': 'Tarefa não encontrada'}  

def test_delete_task_successful():
    in_task = {"title": "Titulo teste", "subtitle": "Subtitulo teste"}
    response = client.post("/tasks", json=in_task)
    in_task["status"] = response.json()["status"]
    in_task["id"] = response.json()["id"]

    response = client.delete(f"/tasks/{in_task['id']}")
    response.status_code == 200
    response.json() == in_task

def test_delete_by_invalid_id():
    response = client.delete("/tasks/unknown__id")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Tarefa não encontrada'}  


