import time
import os
import re
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# --- PDF HELPERS ---

def get_next_report_filename(base_folder="reports", base_name="frontend-report"):
    os.makedirs(base_folder, exist_ok=True)
    pattern = re.compile(rf"{re.escape(base_name)}-(\d+)\.pdf")
    max_num = 0
    for fname in os.listdir(base_folder):
        match = pattern.match(fname)
        if match:
            max_num = max(max_num, int(match.group(1)))
    return os.path.join(base_folder, f"{base_name}-{max_num+1}.pdf")

def save_report_pdf(content, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in content.splitlines():
        pdf.cell(0, 10, line, ln=True)
    pdf.output(filename)
    print(f"✅ PDF report saved as {filename}")

# --- TEST FUNCTIONS ---

def abrir_frontend(driver, log):
    driver.get("http://localhost:5000")
    time.sleep(2)
    log.append("Frontend opened at http://localhost:5000")

def crear_usuario(driver, wait, log):
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)
    user_result = driver.find_element(By.ID, "user-result").text
    log.append(f"Resultado usuario: {user_result}")
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))
    log.append(f"User ID created: {user_id}")
    return user_id

def crear_tarea(driver, wait, user_id, log):
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys("Terminar laboratorio")
    time.sleep(1)
    userid_input = driver.find_element(By.ID, "userid")
    userid_input.send_keys(user_id)
    userid_input.send_keys('\t')
    time.sleep(1)
    crear_tarea_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))
    )
    crear_tarea_btn.click()
    time.sleep(2)
    wait.until(
        EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID")
    )
    task_result = driver.find_element(By.ID, "task-result")
    log.append(f"Texto en task_result: {task_result.text}")
    assert "Tarea creada con ID" in task_result.text
    task_id = ''.join(filter(str.isdigit, task_result.text))
    log.append(f"Task ID created: {task_id}")
    return task_id

def ver_tareas(driver, log):
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)
    tasks = driver.find_element(By.ID, "tasks").text
    log.append(f"Tareas: {tasks}")
    assert "Terminar laboratorio" in tasks

def delete_task(task_id, log):
    TASKS_URL = "http://localhost:5002/tasks"
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    if response.status_code == 404:
        log.append(f"⚠️ Task {task_id} not found (already deleted?)")
    else:
        response.raise_for_status()
    log.append(f"🗑️ Task {task_id} deleted.")

def delete_user(user_id, log):
    USERS_URL = "http://localhost:5001/users"
    response = requests.delete(f"{USERS_URL}/{user_id}")
    if response.status_code == 404:
        log.append(f"⚠️ User {user_id} not found (already deleted?)")
    else:
        response.raise_for_status()
    log.append(f"🗑️ User {user_id} deleted.")

def main():
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)
    log = []
    user_id = None
    task_id = None

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver, log)
        user_id = crear_usuario(driver, wait, log)
        task_id = crear_tarea(driver, wait, user_id, log)
        ver_tareas(driver, log)
        log.append("Test completed successfully!")
        time.sleep(3)
    except Exception as e:
        log.append(f"❌ ERROR: {str(e)}")
    finally:
        # --- CLEANUP: Borra los datos creados vía API ---
        if task_id:
            delete_task(task_id, log)
        if user_id:
            delete_user(user_id, log)
        driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
        driver.quit()
        # --- SAVE PDF REPORT ---
        report_text = "\n".join(log)
        filename = get_next_report_filename()
        save_report_pdf(report_text, filename)

if __name__ == "__main__":
    main()
