import time
import requests  # Para limpieza de datos
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

BACKEND_USERS_URL = "http://localhost:5001/users"
BACKEND_TASKS_URL = "http://localhost:5002/tasks"

def abrir_frontend(driver):
    # Opens the frontend application in the browser
    driver.get("http://localhost:5000")
    time.sleep(2)  # Give the page time to load

def crear_usuario(driver, wait):
    # Fills out the user creation form and submits it
    # Then retrieves and returns the newly created user ID
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    print("Resultado usuario:", user_result)
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))  # Extract numeric ID from result
    return user_id

def crear_tarea(driver, wait, user_id):
    # Fills out the task creation form with a task and user ID, then submits it
    # Waits until the confirmation text appears and asserts the result
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys("Terminar laboratorio")
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
    userid_input.send_keys(user_id)
    userid_input.send_keys('\t')  # Force focus out of the input to trigger validation
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
    print("Texto en task_result:", task_result.text)
    assert "Tarea creada con ID" in task_result.text

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks

def borrar_tarea(task_id):
    response = requests.delete(f"{BACKEND_TASKS_URL}/{task_id}")
    response.raise_for_status()
    print(f"✅ Tarea {task_id} eliminada")

def borrar_usuario(user_id):
    response = requests.delete(f"{BACKEND_USERS_URL}/{user_id}")
    response.raise_for_status()
    print(f"✅ Usuario {user_id} eliminado")

def generar_pdf_reporte(test_results):
    reports_dir = "test_reports"
    os.makedirs(reports_dir, exist_ok=True)
    existing = [f for f in os.listdir(reports_dir) if f.startswith("frontend_report_") and f.endswith(".pdf")]
    nums = [int(f.split("_")[2].split(".")[0]) for f in existing if f.split("_")[2].split(".")[0].isdigit()]
    next_num = max(nums) + 1 if nums else 1
    filename = os.path.join(reports_dir, f"frontend_report_{next_num}.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, f"Frontend Test Report #{next_num}")
    c.drawString(50, 735, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y = 710
    for line in test_results:
        c.drawString(50, y, line)
        y -= 20
        if y < 50:
            c.showPage()
            y = 750
    c.save()
    print(f"✅ PDF report generated: {filename}")

def main():
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    user_id = None
    task_id = None
    test_log = []
    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait)
        test_log.append(f"Usuario creado con ID: {user_id}")
        crear_tarea(driver, wait, user_id)
        test_log.append("Tarea creada y asociada correctamente.")
        # Obtener el ID de la tarea creada desde backend para limpieza
        tasks = requests.get(BACKEND_TASKS_URL).json()
        task_id = max((t["id"] for t in tasks if str(t["user_id"]) == str(user_id)), default=None)
        ver_tareas(driver)
        test_log.append("Verificación visual de tarea en frontend exitosa.")
        time.sleep(3)  # Final delay to observe results if not running headless
    except Exception as e:
        test_log.append(f"❌ Test failed: {str(e)}")
        raise
    finally:
        # Limpieza de datos
        if task_id:
            try:
                borrar_tarea(task_id)
                test_log.append(f"Tarea {task_id} eliminada")
                # Verificar que la tarea fue eliminada
                tasks = requests.get(BACKEND_TASKS_URL).json()
                assert not any(t["id"] == task_id for t in tasks), "❌ La tarea no fue eliminada"
                test_log.append("Eliminación de tarea verificada.")
            except Exception as e:
                test_log.append(f"❌ Error al eliminar/verificar tarea: {str(e)}")
        if user_id:
            try:
                borrar_usuario(user_id)
                test_log.append(f"Usuario {user_id} eliminado")
                # Verificar que el usuario fue eliminado
                r = requests.get(f"{BACKEND_USERS_URL}/{user_id}")
                assert r.status_code == 404, "❌ El usuario no fue eliminado"
                test_log.append("Eliminación de usuario verificada.")
            except Exception as e:
                test_log.append(f"❌ Error al eliminar/verificar usuario: {str(e)}")
        generar_pdf_reporte(test_log)
        driver.quit()  # Always close the browser at the end

if __name__ == "__main__":
    main()
