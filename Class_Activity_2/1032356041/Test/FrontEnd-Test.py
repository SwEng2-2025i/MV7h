
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from report_generator import create_pdf_report

def cleanup_all_data():
    """Clean up all test data using reset endpoints"""
    results = []
    try:
        # Reset users
        resp = requests.post("http://localhost:5001/reset")
        if resp.status_code == 200:
            results.append("✅ All users cleaned up successfully")
        else:
            results.append(f"❌ User cleanup failed: {resp.status_code}")
    except Exception as e:
        results.append(f"❌ Error cleaning users: {str(e)}")
    
    try:
        # Reset tasks
        resp = requests.post("http://localhost:5002/reset")
        if resp.status_code == 200:
            results.append("✅ All tasks cleaned up successfully")
        else:
            results.append(f"❌ Task cleanup failed: {resp.status_code}")
    except Exception as e:
        results.append(f"❌ Error cleaning tasks: {str(e)}")
    
    return results

def abrir_frontend(driver, results):
    driver.get("http://localhost:5000")
    time.sleep(2)
    results.append("✅ Frontend opened successfully")

def crear_usuario(driver, wait, results):
    try:
        username_input = driver.find_element(By.ID, "username")
        username_input.send_keys("TestUser")
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
        time.sleep(2)

        user_result = driver.find_element(By.ID, "user-result").text
        results.append(f"User creation result: {user_result}")
        
        if "Usuario creado con ID" in user_result:
            user_id = ''.join(filter(str.isdigit, user_result))
            results.append(f"✅ User created with ID: {user_id}")
            return user_id
        else:
            results.append("❌ User creation failed")
            return None
    except Exception as e:
        results.append(f"❌ Error creating user: {str(e)}")
        return None

def crear_tarea(driver, wait, user_id, results):
    try:
        task_input = driver.find_element(By.ID, "task")
        task_input.send_keys("Test Frontend Task")
        time.sleep(1)

        userid_input = driver.find_element(By.ID, "userid")
        userid_input.send_keys(user_id)
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
        results.append(f"Task creation result: {task_result}")
        
        if "Tarea creada con ID" in task_result:
            task_id = ''.join(filter(str.isdigit, task_result))
            results.append(f"✅ Task created with ID: {task_id}")
            return task_id
        else:
            results.append("❌ Task creation failed")
            return None
    except Exception as e:
        results.append(f"❌ Error creating task: {str(e)}")
        return None

def ver_tareas(driver, results):
    try:
        driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
        time.sleep(2)

        tasks = driver.find_element(By.ID, "tasks").text
        results.append(f"Tasks displayed: {tasks}")
        
        if "Test Frontend Task" in tasks:
            results.append("✅ Task verification successful")
        else:
            results.append("❌ Task verification failed")
    except Exception as e:
        results.append(f"❌ Error verifying tasks: {str(e)}")

def main():
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    results = []
    try:
        wait = WebDriverWait(driver, 10)
        
        # Clean up any existing data first
        results.append("Starting frontend E2E test...")
        cleanup_results = cleanup_all_data()
        results.extend(cleanup_results)
        
        # Run tests
        abrir_frontend(driver, results)
        user_id = crear_usuario(driver, wait, results)
        
        if user_id:
            task_id = crear_tarea(driver, wait, user_id, results)
            if task_id:
                ver_tareas(driver, results)
                results.append("✅ Frontend E2E test completed successfully")
            else:
                results.append("❌ Frontend E2E test failed at task creation")
        else:
            results.append("❌ Frontend E2E test failed at user creation")
        
        time.sleep(3)
        
    except Exception as e:
        results.append(f"❌ Frontend test failed with error: {str(e)}")
    
    finally:
        # Final cleanup
        results.append("Starting final cleanup...")
        cleanup_results = cleanup_all_data()
        results.extend(cleanup_results)
        
        # Generate PDF report
        try:
            report_file = create_pdf_report(results, "frontend")
            results.append(f"✅ PDF report generated: {report_file}")
        except Exception as e:
            results.append(f"❌ Failed to generate PDF report: {str(e)}")
        
        driver.quit()
        
        # Print final results
        print("\n" + "="*50)
        print("FRONTEND TEST RESULTS:")
        print("="*50)
        for result in results:
            print(result)

if __name__ == "__main__":
    main()
