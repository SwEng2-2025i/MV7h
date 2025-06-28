import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Reports'))
from Reports.Report import generar_reporte

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"
DEL_TASKS_URL="http://localhost:5002/cleanTestingTask"
DEL_USERS_URL="http://localhost:5001/cleanTestingUser"

#Memory data
testing_data=dict()
testing_data["users_id"]=[]
testing_data["tasks_id"]=[]

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("✅ User created:", user_data)
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task created:", task_data)
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def integration_test():
    resultados = []
    user_id = None
    user_data = None
    task_id = None
    task_data = None
    try:
        # Crear usuario
        try:
            response = requests.post(USERS_URL, json={"name": "Camilo"})
            response.raise_for_status()
            user_data = response.json()
            user_id = user_data["id"]
            testing_data["users_id"].append(user_id)
            resultados.append(f"Se agregó el usuario con nombre '{user_data['name']}' e id {user_id}.")
        except Exception as e:
            resultados.append(f"Error al crear usuario: {str(e)}")
            user_id = None

        # Crear tarea
        try:
            if user_id is not None:
                response = requests.post(TASKS_URL, json={"title": "Prepare presentation", "user_id": user_id})
                response.raise_for_status()
                task_data = response.json()
                task_id = task_data["id"]
                testing_data["tasks_id"].append(task_id)
                resultados.append(f"Se agregó la tarea con id {task_id} y título '{task_data['title']}' para el usuario {user_id}.")
            else:
                resultados.append("No se pudo crear la tarea porque no se creó el usuario.")
                task_id = None
        except Exception as e:
            resultados.append(f"Error al crear tarea: {str(e)}")
            task_id = None

        # Verificar tarea
        try:
            if user_id is not None and task_id is not None:
                tasks = get_tasks()
                user_tasks = [t for t in tasks if t["user_id"] == user_id]
                if any(t["id"] == task_id for t in user_tasks):
                    resultados.append(f"La tarea con id {task_id} está correctamente registrada y asociada al usuario {user_id}.")
                else:
                    resultados.append(f"La tarea con id {task_id} NO está correctamente registrada para el usuario {user_id}.")
            else:
                resultados.append("No se pudo verificar la tarea porque no se creó usuario o tarea.")
        except Exception as e:
            resultados.append(f"Error al verificar tareas: {str(e)}")
    except Exception as e:
        resultados.append(f"Error general en el test: {str(e)}")
    finally:
        generar_reporte("BackEnd", resultados)

def clean_test_task():
    for task_id in testing_data.get("tasks_id"):
        print(task_id)
        response=requests.delete(DEL_TASKS_URL,json={"id":task_id})
        response.raise_for_status()
        tarea_eliminada=response.json()
        print(f"💢Tarea con id {tarea_eliminada["id"]} y titulo {tarea_eliminada["title"]} Borrada")

def clean_test_users():
    for user_id in testing_data.get("users_id"):
        response=requests.delete(DEL_USERS_URL,json={"id":user_id})
        response.raise_for_status()
        user_elim=response.json()
        print(f"💢 Usuario con id {user_elim["id"]} y nombre {user_elim["name"]} eliminado.")

if __name__ == "__main__":
    integration_test()
    clean_test_task()
    clean_test_users()