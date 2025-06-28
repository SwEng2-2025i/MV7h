# Test/FrontEnd-Test.py
import time
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

# Endpoints for cleanup
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

# PDF Report Configuration
REPORTS_DIR = "test_reports"
REPORT_PREFIX = "report"


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
    driver.find_element(
        By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(
        By.ID, "user-result").text
    print("Resultado usuario:", user_result)
    assert "Usuario creado con ID" in user_result
    user_id = "".join(
        filter(str.isdigit, user_result)
    )  # Extract numeric ID from result
    return user_id


def crear_tarea(driver, wait, user_id):
    # Fills out the task creation form with a task and user ID, then submits it
    # Waits until the confirmation text appears and asserts the result
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys("Terminar laboratorio")
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
    userid_input.send_keys(user_id)
    # Force focus out of the input to trigger validation
    userid_input.send_keys("\t")
    time.sleep(1)

    crear_tarea_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[text()='Crear Tarea']"))
    )
    crear_tarea_btn.click()
    time.sleep(2)

    wait.until(
        EC.text_to_be_present_in_element(
            (By.ID, "task-result"), "Tarea creada con ID")
    )
    task_result = driver.find_element(By.ID, "task-result")
    print("Texto en task_result:", task_result.text)
    assert "Tarea creada con ID" in task_result.text


def ver_tareas(driver):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(
        By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]"
    ).click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks


# Added Cleanup functions (same as backend)
def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    return response.json()


def cleanup(user_id):
    """Delete user and all associated data"""
    delete_url = f"{USERS_URL}/{user_id}"
    try:
        response = requests.delete(delete_url)
        response.raise_for_status()
        print(
            f"🧹 User {user_id} and their tasks have been cleaned up.")
        return True
    except requests.exceptions.HTTPError as e:
        print(f"⚠️ Cleanup failed for user {user_id}: {e}")
        return False


def verify_user_deleted(user_id):
    """Verify that a user has been deleted"""
    response = requests.get(f"{USERS_URL}/{user_id}")
    if response.status_code != 404:
        raise AssertionError(
            f"❌ User {user_id} still exists")
    print(f"✅ Verified user {user_id} was deleted")


def verify_tasks_deleted(user_id):
    """Verify that all tasks for a user have been deleted"""
    tasks = get_tasks()
    user_tasks = [
        t for t in tasks if t["user_id"] == user_id]
    if len(user_tasks) > 0:
        raise AssertionError(
            f"❌ Found {len(user_tasks)} tasks still associated with user {user_id}"
        )
    print(
        f"✅ Verified all tasks for user {user_id} were deleted")


# Added PDF Report functions (same as backend)
def get_next_report_number():
    """Get the next sequential report number"""
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)
        return 1

    existing_files = [
        f
        for f in os.listdir(REPORTS_DIR)
        if f.startswith(REPORT_PREFIX) and f.endswith(".pdf")
    ]

    existing_numbers = []
    for filename in existing_files:
        number_part = filename[len(REPORT_PREFIX): -4]
        if number_part.isdigit():
            existing_numbers.append(int(number_part))

    return max(existing_numbers, default=0) + 1


def generate_pdf_report(report_content, report_number):
    """Generate a PDF report with the given content and number"""
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    filename = f"{REPORT_PREFIX}{report_number}.pdf"
    filepath = os.path.join(REPORTS_DIR, filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50,
                 f"Frontend Integration Test Report #{report_number}")

    # Date and time
    c.setFont("Helvetica", 10)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.drawString(50, height - 70, f"Generated: {timestamp}")

    # Content
    c.setFont("Helvetica", 12)
    y_position = height - 100

    for line in report_content:
        if y_position < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - 50

        c.drawString(50, y_position, str(line))
        y_position -= 20

    c.save()
    print(f"📄 Report saved as: {filepath}")
    return filepath


def main():
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    user_id = None
    report_content = []
    test_successful = False

    try:
        report_content.append(
            "=== FRONTEND INTEGRATION TEST ===")
        report_content.append("")

        wait = WebDriverWait(driver, 10)

        abrir_frontend(driver)
        report_content.append(
            "✅ Frontend page opened successfully.")

        user_id = crear_usuario(driver, wait)
        report_content.append(
            f"✅ User created successfully with ID: {user_id}")

        crear_tarea(driver, wait, user_id)
        report_content.append(
            "✅ Task created successfully for the user.")

        ver_tareas(driver)
        report_content.append(
            "✅ Tasks displayed successfully on the frontend.")

        test_successful = True
        # Final delay to observe results if not running headless
        time.sleep(3)

    except Exception as e:
        error_msg = f"❌ Frontend test failed: {str(e)}"
        print(error_msg)
        report_content.append(error_msg)
        test_successful = False

    finally:
        driver.quit()  # Always close the browser at the end

        # REQUIREMENT 1: Data cleanup and verification
        report_content.append("")
        report_content.append("=== CLEANUP PHASE ===")

        if user_id is not None:
            try:
                # Cleanup
                report_content.append(
                    "Performing cleanup...")
                cleanup_success = cleanup(int(user_id))

                if cleanup_success:
                    report_content.append(
                        f"🧹 Cleanup completed for user ID: {user_id}"
                    )

                    # Verify cleanup
                    report_content.append(
                        "Verifying cleanup...")
                    verify_user_deleted(int(user_id))
                    verify_tasks_deleted(int(user_id))

                    report_content.append(
                        "✅ Cleanup verification PASSED")
                else:
                    report_content.append(
                        "⚠️ Cleanup failed")

            except Exception as cleanup_error:
                error_msg = f"❌ Cleanup verification failed: {str(cleanup_error)}"
                print(error_msg)
                report_content.append(error_msg)

        # REQUIREMENT 2: PDF Report generation
        report_content.append("")
        report_content.append("=== TEST SUMMARY ===")
        if test_successful:
            report_content.append(
                "Overall Result: ✅ PASSED")
        else:
            report_content.append(
                "Overall Result: ❌ FAILED")

        # Generate PDF report
        report_number = get_next_report_number()
        generate_pdf_report(report_content, report_number)

        print("🏁 Frontend integration test completed")


if __name__ == "__main__":
    main()
