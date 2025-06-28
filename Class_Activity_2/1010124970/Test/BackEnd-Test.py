import requests
from fpdf import FPDF
import os
import datetime

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("✅ User created:", user_data)
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task created:", task_data)
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks
def data_cleanup(user_id, task_id):
    print("\n--- Starting Data Cleanup ---")

    # Delete Task
    if task_id:
        try:
            response = requests.delete(f"{TASKS_URL}/{task_id}")
            response.raise_for_status()
            print(f"✅ Tarea con ID {task_id} eliminada correctamente.")

        except requests.exceptions.RequestException as e:
            print(f"❌ No se ha podido eliminar la tarea con ID {task_id}: {e}")
        except Exception as e:
            print(f"❌ Error inesperado al eliminar tarea con ID {task_id}: {e}")
    else:
        print("ℹ️ No se proporcionó ID de tarea para eliminar.")

    # Delete User
    if user_id:
        try:
            response = requests.delete(f"{USERS_URL}/{user_id}")
            response.raise_for_status()
            print(f"✅ Usuario con ID {user_id} eliminado correctamente.")

        except requests.exceptions.RequestException as e:
            print(f"❌ No se ha podido eliminar al usuario con ID {user_id}: {e}")
        except Exception as e:
            print(f"❌ Error inesperado al eliminar usuario con ID {user_id}: {e}")
    else:
        print("ℹ️ No se proporcionó ID de usuario para eliminar.")

    print("--- Data Cleanup Complete ---")

def integration_test():
    user_id = None
    task_id = None
    test_result = False
    test_message = ""

    try:
        # Step 1: Create user
        user_id = create_user("Camilo")

        # Step 2: Create task for that user
        task_id = create_task(user_id, "Prepare presentation")

        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]

        assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
        test_message = "✅ Test completado: la tarea se registró y vinculó al usuario exitosamente."
        print(test_message)
        test_result = True

    except requests.exceptions.RequestException as e:
        test_message = f"❌ Error de conexión o HTTP durante el test: {e}"
        print(test_message)
    except AssertionError as e:
        test_message = str(e)
        print(test_message)
    except Exception as e:
        test_message = f"❌ Error inesperado durante el test: {e}"
        print(test_message)
    finally:
        data_cleanup(user_id, task_id)
        return {"success": test_result, "message": test_message}


def data_cleanup(user_id, task_id):
    print("\n--- Starting Data Cleanup ---")

    # Delete Task
    if task_id:
        try:
            response = requests.delete(f"{TASKS_URL}/{task_id}")
            response.raise_for_status()
            print(f"✅ Tarea con ID {task_id} eliminada correctamente.")

        except requests.exceptions.RequestException as e:
            print(f"❌ No se ha podido eliminar la tarea con ID {task_id}: {e}")
        except Exception as e:
            print(f"❌ Error inesperado al eliminar tarea con ID {task_id}: {e}")
    else:
        print("ℹ️ No se proporcionó ID de tarea para eliminar.")

    # Delete User
    if user_id:
        try:
            response = requests.delete(f"{USERS_URL}/{user_id}")
            response.raise_for_status()
            print(f"✅ Usuario con ID {user_id} eliminado correctamente.")

        except requests.exceptions.RequestException as e:
            print(f"❌ No se ha podido eliminar al usuario con ID {user_id}: {e}")
        except Exception as e:
            print(f"❌ Error inesperado al eliminar usuario con ID {user_id}: {e}")
    else:
        print("ℹ️ No se proporcionó ID de usuario para eliminar.")

    print("--- Data Cleanup Complete ---")


def report(results):
    """
    Crea un informe PDF con los resultados del test.

    Args:
        results (dict): Un diccionario que contiene el resultado del test
                        (ej. {"success": True, "message": "Test passed successfully."}).
    """
    pdf = FPDF()
    pdf.add_page()

    # Título del informe
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Informe de Resultados de la Prueba de Integración", 0, 1, "C")
    pdf.ln(10) # Salto de línea

    # Fecha y Hora
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, f"Fecha y Hora del Informe: {now}", 0, 1, "L")
    pdf.ln(5)

    # Resultados del Test
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Detalles del Test:", 0, 1, "L")
    pdf.ln(2)

    # Estado del Test
    pdf.set_font("Arial", "B", 12)
    status_text = "APROBADO" if results["success"] else "FALLIDO"
    status_color = (0, 128, 0) if results["success"] else (255, 0, 0) # Verde para aprobado, Rojo para fallido
    pdf.set_text_color(*status_color)
    pdf.cell(0, 10, f"Estado General del Test: {status_text}", 0, 1, "L")
    pdf.set_text_color(0, 0, 0) # Volver al color negro

    pdf.ln(5)

    # Mensaje del Test
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 10, f"Mensaje del Test:\n{results['message']}")
    pdf.ln(10)

    # Guardar el PDF
    pdf_filename = "informe_test_integracion.pdf"
    pdf.output(pdf_filename)
    print(f"\n📄 Informe PDF generado exitosamente: {pdf_filename}")


if __name__ == "__main__":
    print("--- Iniciando Prueba de Integración ---")
    test_results = integration_test()
    print("--- Prueba de Integración Finalizada ---")
    report(test_results)