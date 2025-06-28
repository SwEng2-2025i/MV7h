import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Reports'))
from Reports.Report import generar_reporte
data_front_test=dict()
data_front_test["users_id"]=[]
data_front_test["tasks_id"]=[]

DEL_TASKS_URL="http://localhost:5002/cleanTestingTask"
DEL_USERS_URL="http://localhost:5001/cleanTestingUser"

def abrir_frontend(driver):
    driver.get("http://localhost:5000")
    time.sleep(2)  

def crear_usuario(driver, wait):
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    print("Resultado usuario:", user_result)
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))  
    data_front_test["users_id"].append(user_id)
    return user_id

def crear_tarea(driver, wait, user_id):
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
    task_id = ''.join(filter(str.isdigit, task_result.text))
    data_front_test["tasks_id"].append(task_id)
    print("Texto en task_result:", task_result.text)
    assert "Tarea creada con ID" in task_result.text

def ver_tareas(driver):
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    assert "Terminar laboratorio" in tasks


def detele_test_tasks():
    for task_id in data_front_test.get("tasks_id"):
        print(task_id)
        response=requests.delete(DEL_TASKS_URL,json={"id":task_id})
        response.raise_for_status()
        tarea_eliminada=response.json()
        print(tarea_eliminada)
        print(f"💢Tarea con id {tarea_eliminada["id"]} y titulo {tarea_eliminada["title"]} Borrada")


def delete_test_users():
    for user_id in data_front_test.get("users_id"):
        response=requests.delete(DEL_USERS_URL,json={"id":user_id})
        response.raise_for_status()
        user_elim=response.json()
        print(user_elim)
        print(f"💢 Usuario con id {user_elim["id"]} y nombre {user_elim["name"]} eliminado.")


def main():
    options = Options()
    driver = webdriver.Chrome(options=options)

    resultados = []
    user_id = None
    task_id = None
    user_result = None
    task_result = None
    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        # Crear usuario
        try:
            username_input = driver.find_element(By.ID, "username")
            username_input.send_keys("Ana")
            time.sleep(1)
            driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
            time.sleep(2)
            user_result = driver.find_element(By.ID, "user-result").text
            assert "Usuario creado con ID" in user_result
            user_id = ''.join(filter(str.isdigit, user_result))
            data_front_test["users_id"].append(user_id)
            resultados.append(f"Se agregó el usuario con nombre 'Ana' e id {user_id}.")
        except Exception as e:
            resultados.append(f"Error al crear usuario: {str(e)}")
            user_id = None

        # Crear tarea
        try:
            if user_id is not None:
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
                task_result = driver.find_element(By.ID, "task-result").text
                task_id = ''.join(filter(str.isdigit, task_result))
                data_front_test["tasks_id"].append(task_id)
                resultados.append(f"Se agregó la tarea con id {task_id} y título 'Terminar laboratorio' para el usuario {user_id}.")
            else:
                resultados.append("No se pudo crear la tarea porque no se creó el usuario.")
                task_id = None
        except Exception as e:
            resultados.append(f"Error al crear tarea: {str(e)}")
            task_id = None

        # Ver tareas
        try:
            if user_id is not None and task_id is not None:
                driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
                time.sleep(2)
                tasks = driver.find_element(By.ID, "tasks").text
                if "Terminar laboratorio" in tasks:
                    resultados.append(f"La tarea con id {task_id} y título 'Terminar laboratorio' aparece correctamente en la lista de tareas del usuario {user_id}.")
                else:
                    resultados.append(f"La tarea con id {task_id} y título 'Terminar laboratorio' NO aparece en la lista de tareas del usuario {user_id}.")
            else:
                resultados.append("No se pudo verificar la tarea porque no se creó usuario o tarea.")
        except Exception as e:
            resultados.append(f"Error al verificar tareas: {str(e)}")
        time.sleep(3)  
    except Exception as e:
        resultados.append(f"Error general en el test: {str(e)}")
        driver.quit()  
    finally:
        generar_reporte("FrontEnd", resultados)
        driver.quit()  

if __name__ == "__main__":
    main()
    detele_test_tasks()
    delete_test_users()
