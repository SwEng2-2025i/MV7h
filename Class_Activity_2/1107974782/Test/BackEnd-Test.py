import requests
from fpdf import FPDF
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

def eliminar_tarea(task_id):
    response = requests.delete(f'{TASKS_URL}/{task_id}')
    assert response.status_code == 200
    print("✅ Tarea eliminada")

def eliminar_usuario(user_id):
    response = requests.delete(f'{USERS_URL}/{user_id}')
    assert response.status_code == 200
    print("✅ Usuario eliminado")

def verificar_eliminacion(user_id, task_id):
    r_user = requests.get(f'{USERS_URL}/{user_id}')
    r_task = requests.get(f'{TASKS_URL}/{task_id}')
    assert r_user.status_code == 404
    assert task_id not in [t['id'] for t in requests.get(TASKS_URL).json()]
    print("✅ Verificación de eliminación completada")

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def generar_pdf_reporte(logs):
    if not os.path.exists("reports"):
        os.makedirs("reports")

    existing = [f for f in os.listdir("reports") if f.startswith("report_") and f.endswith(".pdf")]
    num = len(existing) + 1
    filename = f"reports/report_{num:03}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Reporte de Pruebas de Integración", ln=True, align='C')
    pdf.ln(10)

    for line in logs:
        # Eliminar emojis no compatibles con latin-1
        clean_line = ''.join(c for c in line if ord(c) < 256)
        pdf.multi_cell(0, 10, txt=clean_line)

    pdf.output(filename)
    print(f"📁 Reporte generado: {filename}")


def integration_test():
    logs = []

    try:
        # Crear usuario
        user_id = create_user("Marco Perez")
        logs.append(f"✅ Usuario creado con ID: {user_id}")

        # Crear tarea
        task_id = create_task(user_id, "Volver al tolima")
        logs.append(f"✅ Tarea creada con ID: {task_id} para el usuario {user_id}")

        # Verificación de existencia
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), "❌ La tarea no se registró correctamente"
        logs.append("✅ Verificación: la tarea fue registrada correctamente y asociada al usuario")

        # Limpieza
        eliminar_tarea(task_id)
        eliminar_usuario(user_id)
        logs.append("✅ Limpieza: Tarea y usuario eliminados")

        # Verificación de limpieza
        verificar_eliminacion(user_id, task_id)
        logs.append("✅ Verificación de limpieza: los datos fueron eliminados correctamente")

    except Exception as e:
        logs.append(f"❌ Error durante las pruebas: {str(e)}")
        raise

    finally:
        generar_pdf_reporte(logs)

if __name__ == "__main__":
    integration_test()
