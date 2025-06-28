# Test/BackEnd-Test.py

import os
import glob
import traceback
from datetime import datetime

import requests
from reportlab.pdfgen import canvas

# Endpoints de los microservicios
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name: str) -> int:
    r = requests.post(USERS_URL, json={"name": name})
    r.raise_for_status()
    data = r.json()
    print(f"✅ Usuario creado: {data}")
    return data["id"]

def create_task(user_id: int, title: str) -> int:
    r = requests.post(TASKS_URL, json={"title": title, "user_id": user_id})
    r.raise_for_status()
    data = r.json()
    print(f"✅ Tarea creada: {data}")
    return data["id"]

def get_tasks() -> list:
    r = requests.get(TASKS_URL)
    r.raise_for_status()
    return r.json()

def delete_task(task_id: int):
    r = requests.delete(f"{TASKS_URL}/{task_id}")
    assert r.status_code == 200, f"❌ DELETE /tasks/{task_id} devolvió {r.status_code}"
    # Verificar que ya no exista
    r2 = requests.get(f"{TASKS_URL}/{task_id}")
    assert r2.status_code == 404, f"❌ Después de DELETE, GET /tasks/{task_id} devolvió {r2.status_code}"

def delete_user(user_id: int):
    r = requests.delete(f"{USERS_URL}/{user_id}")
    assert r.status_code == 200, f"❌ DELETE /users/{user_id} devolvió {r.status_code}"
    # Verificar que ya no exista
    r2 = requests.get(f"{USERS_URL}/{user_id}")
    assert r2.status_code == 404, f"❌ Después de DELETE, GET /users/{user_id} devolvió {r2.status_code}"

def generate_pdf_report(success: bool, log_messages: list[str]):
    #Genera un reporte PDF con los resultados del test
    os.makedirs("reports", exist_ok=True)
    # Buscar cuántos reportes ya existen
    existing = glob.glob("reports/backend_report_*.pdf")
    next_index = len(existing) + 1
    filename = f"reports/backend_report_{next_index:03d}.pdf"

    c = canvas.Canvas(filename, pagesize=(595, 842))  # A4 portrait
    c.setFont("Helvetica-Bold", 16)
    title = "Informe de Test BackEnd"
    c.drawString(50, 800, title)
    c.setFont("Helvetica", 10)
    c.drawString(50, 780, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, 765, f"Resultado: {'ÉXITO' if success else 'FALLIDO'}")

    y = 740
    for msg in log_messages:
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = 800
        c.drawString(50, y, msg)
        y -= 15

    c.save()
    print(f"📄 PDF generado: {filename}")

def integration_test():
    log = []
    success = False

    try:
        log.append("🔄 Iniciando test de integración BackEnd")

        # 1) Crear usuario
        user_id = create_user("Camilo")
        log.append(f"  • Usuario ID={user_id} creado")

        # 2) Crear tarea para ese usuario
        task_id = create_task(user_id, "Test Task")
        log.append(f"  • Tarea ID={task_id} creada para Usuario {user_id}")

        # 3) Verificar que la tarea exista en la lista
        tasks = get_tasks()
        assert any(t["id"] == task_id for t in tasks), "❌ La tarea no aparece en GET /tasks"
        log.append("  • Verificado GET /tasks incluye la tarea")

        # 4) Borrar tarea y comprobar 404
        delete_task(task_id)
        log.append(f"  • DELETE /tasks/{task_id} OK y GET devuelve 404")

        # 5) Borrar usuario y comprobar 404
        delete_user(user_id)
        log.append(f"  • DELETE /users/{user_id} OK y GET devuelve 404")

        log.append("✅ Cleanup completado sin errores")
        success = True

    except AssertionError as ae:
        msg = f"💥 AssertionError: {ae}"
        print(msg)
        log.append(msg)
    except Exception as e:
        tb = traceback.format_exc().splitlines()
        log.append("💥 Exception inesperada:")
        log.extend(tb)
        print("".join(tb))
    finally:
        # Generar reporte PDF sea éxito o error
        generate_pdf_report(success, log)

if __name__ == "__main__":
    integration_test()
