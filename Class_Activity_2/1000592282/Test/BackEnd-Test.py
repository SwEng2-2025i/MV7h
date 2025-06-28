import requests
from fpdf import FPDF
from datetime import datetime
import os

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

def delete_user(user_id):
    r = requests.delete(f"{USERS_URL}/{user_id}")
    print(r.json())

def delete_task(task_id):
    r = requests.delete(f"{TASKS_URL}/{task_id}")
    print(r.json())

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

    #Limpieza
    delete_task(task_id)
    delete_user(user_id)

    #Verificar que no existen
    tasks = get_tasks()
    assert not any(t["id"] == task_id for t in tasks), "❌ La tarea no fue eliminada"
    r = requests.get(USERS_URL)
    assert not any(u["id"] == user_id for u in r.json()), "❌ El usuario no fue eliminado"
    print("Limpieza completada")


def generar_pdf(texto):
    if not os.path.exists("reportes"):
        os.makedirs("reportes")

    n = len([f for f in os.listdir("reportes") if f.endswith(".pdf")]) + 1
    nombre = f"reportes/reporte_{str(n).zfill(3)}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Reporte de Pruebas de Integración", ln=True)
    pdf.cell(0, 10, f"Fecha: {datetime.now()}", ln=True)
    pdf.multi_cell(0, 10, texto)
    pdf.output(nombre)



if __name__ == "__main__":
    integration_test()
    generar_pdf("Prueba completada")