import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def save_report_pdf(content):
    os.makedirs("reports", exist_ok=True)
    existing = [f for f in os.listdir("reports") if f.startswith("frontend-report") and f.endswith(".pdf")]
    next_num = len(existing) + 1
    filename = f"reports/frontend-report{next_num}.pdf"

    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    text = c.beginText(40, 750)
    for line in content:
        text.textLine(line)
    c.drawText(text)
    c.save()
    print(f"📄 FrontEnd Report saved: {filename}")

def abrir_frontend(driver):
    driver.get("http://localhost:5000")
    time.sleep(2)

def crear_usuario(driver, wait):
    driver.find_element(By.ID, "username").send_keys("Ivan")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)
    result = driver.find_element(By.ID, "user-result").text
    user_id = ''.join(filter(str.isdigit, result))
    return user_id

def crear_tarea(driver, wait, user_id):
    driver.find_element(By.ID, "task").send_keys("Lab Test Ivan")
    driver.find_element(By.ID, "userid").send_keys(user_id)
    time.sleep(1)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))).click()
    time.sleep(2)

def ver_tareas(driver):
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)
    return driver.find_element(By.ID, "tasks").text

def main():
    report_lines = []
    options = Options()
    driver = webdriver.Chrome(options=options)

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait)
        report_lines.append(f"Usuario creado: {user_id}")
        crear_tarea(driver, wait, user_id)
        report_lines.append("Tarea creada para el usuario.")
        tareas = ver_tareas(driver)
        report_lines.append("Lista de tareas:\n" + tareas)
        assert "Lab Test Ivan" in tareas
        report_lines.append("Tarea verificada en el listado.")

        # No implementamos aquí la limpieza porque Selenium no tiene botón para eliminar
        # Idealmente agregarías botones de eliminar en la UI o usarías API REST para borrar directamente

    except Exception as e:
        report_lines.append(f"❌ ERROR: {str(e)}")
    finally:
        driver.quit()
        save_report_pdf(report_lines)

if __name__ == "__main__":
    main()
