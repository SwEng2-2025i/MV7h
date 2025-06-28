# Test/FrontEnd-Test.py

import time
import os
import glob
import traceback
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reportlab.pdfgen import canvas
from datetime import datetime

# URLs
FRONT_URL = "http://localhost:5000"
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

# Datos creados para cleanup
_created = {"users": [], "tasks": []}

# Prepara carpeta de reportes y contador
REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)
existing = glob.glob(f"{REPORT_DIR}/frontend_report_*.pdf")
next_idx = len(existing) + 1
REPORT_PATH = os.path.join(REPORT_DIR, f"frontend_report_{next_idx:03d}.pdf")

# Inicializa PDF
c = canvas.Canvas(REPORT_PATH, pagesize=(595, 842))
c.setFont("Helvetica-Bold", 16)
c.drawString(50, 800, "FrontEnd E2E Test Report")
c.setFont("Helvetica", 10)
c.drawString(50, 780, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
log_y = 760

def log(msg: str):
    global log_y
    if log_y < 50:
        c.showPage()
        c.setFont("Helvetica", 10)
        log_y = 800
    c.drawString(50, log_y, msg)
    log_y -= 15

def abrir_frontend(driver):
    driver.get(FRONT_URL)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    log("✔ Frontend cargado")

def crear_usuario(driver):
    # Rellena y envía el formulario de usuario
    driver.find_element(By.ID, "username").send_keys("E2EUser")
    driver.find_element(By.XPATH, "//button[contains(text(),'Crear Usuario')]").click()
    # Espera confirmación
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "user-result"), "Usuario creado con ID")
    )
    text = driver.find_element(By.ID, "user-result").text
    log(f"✔ Crear Usuario: {text}")
    uid = int("".join(filter(str.isdigit, text)))
    _created["users"].append(uid)
    return uid

def crear_tarea(driver, uid):
    # Rellena y envía el formulario de tarea
    driver.find_element(By.ID, "userid").clear()
    driver.find_element(By.ID, "userid").send_keys(str(uid))
    driver.find_element(By.ID, "task").clear()
    driver.find_element(By.ID, "task").send_keys("E2ETask")
    driver.find_element(By.XPATH, "//button[text()='Crear Tarea']").click()
    # Espera confirmación
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID")
    )
    text = driver.find_element(By.ID, "task-result").text
    log(f"✔ Crear Tarea: {text}")
    tid = int("".join(filter(str.isdigit, text)))
    _created["tasks"].append(tid)
    return tid

def ver_tareas(driver):
    # Refresca la lista y comprueba la tarea
    driver.find_element(By.XPATH, "//button[contains(text(),'Actualizar lista de tareas')]").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "tasks"))
    )
    tasks_text = driver.find_element(By.ID, "tasks").text
    log(f"✔ Lista Tareas: {tasks_text.replace(chr(10), ' | ')}")
    assert "E2ETask" in tasks_text, "❌ La tarea no aparece en la lista"

def cleanup():
    # 1) Borrar **todas** las tareas de los usuarios creados en _created
    all_tasks = requests.get(TASKS_URL).json()
    for t in all_tasks:
        if t["user_id"] in _created["users"]:
            r = requests.delete(f"{TASKS_URL}/{t['id']}")
            assert r.status_code in (200, 404), f"❌ DELETE /tasks/{t['id']} devolvió {r.status_code}"

    # 2) Borrar los usuarios
    for uid in _created["users"]:
        r = requests.delete(f"{USERS_URL}/{uid}")
        assert r.status_code in (200, 404), f"❌ DELETE /users/{uid} devolvió {r.status_code}"

    # 3) Verificar que ya no queden tareas para esos usuarios
    rem = requests.get(TASKS_URL).json()
    remaining_for_us = [t for t in rem if t["user_id"] in _created["users"]]
    log(f"✔ Cleanup: {len(remaining_for_us)} tareas restantes para usuarios de prueba")
    assert not remaining_for_us, "❌ Quedan datos de prueba: " + str(remaining_for_us)

def main():
    log("🔄 Iniciando FrontEnd E2E")
    options = Options()
    driver = webdriver.Chrome(options=options)
    try:
        abrir_frontend(driver)
        uid = crear_usuario(driver)
        tid = crear_tarea(driver, uid)
        ver_tareas(driver)
        log("✅ E2E steps completados")
    except Exception as e:
        log(f"💥 Error: {e}")
        traceback.print_exc()
    finally:
        try:
            cleanup()
            log("✔ Cleanup completado")
        except Exception as e:
            log(f"💥 Cleanup error: {e}")
        c.save()
        driver.quit()
        print(f"📄 FrontEnd report: {REPORT_PATH}")

if __name__ == "__main__":
    main()
