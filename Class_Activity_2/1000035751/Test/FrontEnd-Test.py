import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fpdf import FPDF

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

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
    if user_result:
        result = "Correct"
    else:
        result = "Incorrect"
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))  # Extract numeric ID from result
    report = "Resultado usuario: " + result + " Usuario creado con ID" + str(user_id) + "\n"
    return user_id, report

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
    task_result = driver.find_element(By.ID, "task-result").text
    print("Texto en task_result:", task_result)
    assert "Tarea creada con ID" in task_result
    task_id = ''.join(filter(str.isdigit, task_result))
    
    if task_result:
        result = "Correct"
    else:
        result = "Incorrect"
    report = "Texto en task_result: " + result + " Tarea creada con ID" + str(task_id) + "\n"
    return task_id, report

def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text

    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks
    report = "Tareas:\n" + tasks
    return report

def generate_pdf_report(report_content, reports_dir='reports'):
    # Ensure the reports directory exists
    os.makedirs(reports_dir, exist_ok=True)
    # Find the next sequential report number
    existing = [f for f in os.listdir(reports_dir) if f.startswith('frontend_reports_') and f.endswith('.pdf')]
    numbers = [int(f.split('_')[2].split('.')[0]) for f in existing if f.split('_')[2].split('.')[0].isdigit()]
    next_num = max(numbers) + 1 if numbers else 1
    filename = os.path.join(reports_dir, f'frontend_reports_{next_num}.pdf')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in report_content.split('\n'):
        pdf.cell(0, 10, line, ln=True)
    pdf.output(filename)
    print(f"PDF report saved as {filename}")


def delete_user(user_id):
    response = requests.delete(USERS_URL, json={"user_id": user_id})
    response.raise_for_status()
    user_data = response.json()
    print("✅ User deleted:", user_data)
    return user_data["id"]

def delete_task(task_id):
    response = requests.delete(TASKS_URL, json={
        "task_id": task_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task deleted:", task_data)

def main():
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    reports = ""

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id, report1 = crear_usuario(driver, wait)
        task_id, report2 = crear_tarea(driver, wait, user_id)
        report3 = ver_tareas(driver)
        time.sleep(3)  # Final delay to observe results if not running headless
        reports += report1 + report2 + report3
        generate_pdf_report(reports)
        #cleanup
        delete_user(user_id)
        delete_task(int(task_id))
        
    finally:
        driver.quit()  # Always close the browser at the end

if __name__ == "__main__":
    main()
