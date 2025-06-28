
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests

FRONTEND_URL = "http://localhost:5000"


def generate_frontend_pdf(test_name, result, details):
    # reuse the same PDF logic
    generate_pdf_report(test_name, result, details)


def abrir_frontend(driver):
    driver.get(FRONTEND_URL)
    time.sleep(2)


def crear_usuario_ui(driver, wait, name="Ana"):
    username_input = driver.find_element(By.ID, "username")
    username_input.clear()
    username_input.send_keys(name)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    assert "Usuario creado con ID" in user_result, "User creation UI failed"
    user_id = ''.join(filter(str.isdigit, user_result))
    print("✅ UI User created, ID:", user_id)
    return user_id


def crear_tarea_ui(driver, wait, user_id, desc="Terminar laboratorio"):
    driver.find_element(By.ID, "task").send_keys(desc)
    driver.find_element(By.ID, "userid").send_keys(user_id)
    time.sleep(1)
    crear_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']")))
    crear_btn.click()
    wait.until(EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID"))
    task_id = ''.join(filter(str.isdigit, driver.find_element(By.ID, "task-result").text))
    print("✅ UI Task created, ID:", task_id)
    return task_id


def ver_tareas_ui(driver):
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)
    tasks = driver.find_element(By.ID, "tasks").text
    assert "Terminar laboratorio" in tasks, "Task not shown in UI list"
    print("✅ UI tasks listed correctly.")


def cleanup_via_api(user_id, task_id):
    # Direct API cleanup since UI might not support delete forms
    requests.delete(DELETE_TASK_URL(task_id)).raise_for_status()
    print(f"🗑️ API Task deleted: {task_id}")
    requests.delete(DELETE_USER_URL(user_id)).raise_for_status()
    print(f"🗑️ API User deleted: {user_id}")


def main():
    test_name = "Frontend E2E Flow"
    result = "PASSED"
    details = ""
    options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario_ui(driver, wait)
        task_id = crear_tarea_ui(driver, wait, user_id)
        ver_tareas_ui(driver)

        # Cleanup
        cleanup_via_api(user_id, task_id)

        # Verify cleanup via API
        remaining = requests.get(TASKS_URL).json()
        assert not any(t['id'] == task_id for t in remaining), "Cleanup failed: task still exists"
        print("✅ Cleanup verified: UI test data removed.")
        details = f"User ID: {user_id}\nTask ID: {task_id}\nCleanup: successful"
    except AssertionError as ae:
        print(f"❌ AssertionError: {ae}")
        result = "FAILED"
        details = str(ae)
    except Exception as e:
        print(f"❌ Error in UI test: {e}")
        result = "ERROR"
        details = str(e)
    finally:
        driver.quit()
        generate_frontend_pdf(test_name, result, details)

if __name__ == "__main__":
    main()
