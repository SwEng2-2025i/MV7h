import requests
from report_utils import save_report

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

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

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
    print(f"Task {task_id} deleted.")

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
    print(f"User {user_id} deleted.")

def integration_test():
    # Step 1: Create user
    user_id = create_user("Camilo")

    # Step 2: Create task for that user
    task_id = create_task(user_id, "Prepare presentation")

    # Step 3: Verify that the task is registered and associated with the user
    tasks = get_tasks()
    user_tasks = [t for t in tasks if t["user_id"] == user_id]

    assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
    print("✅ Test completed: task was successfully registered and linked to the user.")
    
    # Limpieza
    delete_task(task_id)
    delete_user(user_id)

    # Verificación de limpieza
    tasks_after = get_tasks()
    assert all(t["id"] != task_id for t in tasks_after), "❌ Task was not deleted"
    print("✅ Task was deleted")

    try:
        requests.get(f"{USERS_URL}/{user_id}").raise_for_status()
        raise Exception("❌ User still exists")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print("✅ User was deleted")
        else:
            raise
    
    report_lines = [
        "INTEGRATION TEST BACKEND",
        f"User ID: {user_id}",
        f"Task ID: {task_id}",
        "✔ Usuario creado",
        "✔ Tarea creada",
        "✔ Asociación verificada",
        "✔ Datos eliminados correctamente"
    ]
    save_report(report_lines)

if __name__ == "__main__":
    integration_test()