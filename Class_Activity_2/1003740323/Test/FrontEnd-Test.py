import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test_utils import TestReportGenerator

class FrontEndIntegrationTest:
    def __init__(self):
        self.report_generator = TestReportGenerator("FrontEnd Integration Test")
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Configura el driver de Selenium"""
        start_time = time.time()
        try:
            options = Options()
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 10)
            
            execution_time = time.time() - start_time
            self.report_generator.add_test_result(
                "Configurar Driver",
                "PASS",
                "Driver de Chrome configurado correctamente",
                execution_time
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.report_generator.add_test_result(
                "Configurar Driver",
                "FAIL",
                f"Error configurando driver: {str(e)}",
                execution_time
            )
            raise e

    def abrir_frontend(self):
        """Abre la aplicación frontend en el navegador"""
        start_time = time.time()
        try:
            self.driver.get("http://localhost:5000")
            time.sleep(2)  # Dar tiempo a que cargue la página
            
            execution_time = time.time() - start_time
            self.report_generator.add_test_result(
                "Abrir Frontend",
                "PASS",
                "Frontend abierto correctamente en http://localhost:5000",
                execution_time
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.report_generator.add_test_result(
                "Abrir Frontend",
                "FAIL",
                f"Error abriendo frontend: {str(e)}",
                execution_time
            )
            raise e

    def crear_usuario(self):
        """Llena el formulario de creación de usuario y lo envía"""
        start_time = time.time()
        try:
            username_input = self.driver.find_element(By.ID, "username")
            username_input.clear()
            username_input.send_keys("Ana")
            time.sleep(1)
            
            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
            time.sleep(2)

            user_result = self.driver.find_element(By.ID, "user-result").text
            print(f"Resultado usuario: {user_result}")
            
            if "Usuario creado con ID" not in user_result:
                raise AssertionError(f"Error en creación de usuario: {user_result}")
                
            user_id = ''.join(filter(str.isdigit, user_result))  # Extraer ID numérico del resultado
            user_id = int(user_id)
            
            # Registrar el usuario creado para limpieza posterior
            self.report_generator.track_created_user(user_id)
            
            execution_time = time.time() - start_time
            self.report_generator.add_test_result(
                "Crear Usuario via Frontend",
                "PASS",
                f"Usuario 'Ana' creado con ID {user_id}",
                execution_time
            )
            
            return user_id
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.report_generator.add_test_result(
                "Crear Usuario via Frontend",
                "FAIL",
                f"Error creando usuario: {str(e)}",
                execution_time
            )
            raise e

    def crear_tarea(self, user_id):
        """Llena el formulario de creación de tarea con una tarea y user ID, luego lo envía"""
        start_time = time.time()
        try:
            task_input = self.driver.find_element(By.ID, "task")
            task_input.clear()
            task_input.send_keys("Terminar laboratorio")
            time.sleep(1)

            userid_input = self.driver.find_element(By.ID, "userid")
            userid_input.clear()
            userid_input.send_keys(str(user_id))
            userid_input.send_keys('\t')  # Forzar focus fuera del input para activar validación
            time.sleep(1)

            crear_tarea_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))
            )
            crear_tarea_btn.click()
            time.sleep(2)

            self.wait.until(
                EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID")
            )
            task_result = self.driver.find_element(By.ID, "task-result")
            print(f"Texto en task_result: {task_result.text}")
            
            if "Tarea creada con ID" not in task_result.text:
                raise AssertionError(f"Error en creación de tarea: {task_result.text}")
                
            task_id = ''.join(filter(str.isdigit, task_result.text))
            task_id = int(task_id)
            
            # Registrar la tarea creada para limpieza posterior
            self.report_generator.track_created_task(task_id)
            
            execution_time = time.time() - start_time
            self.report_generator.add_test_result(
                "Crear Tarea via Frontend",
                "PASS",
                f"Tarea 'Terminar laboratorio' creada con ID {task_id} para usuario {user_id}",
                execution_time
            )
            
            return task_id
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.report_generator.add_test_result(
                "Crear Tarea via Frontend",
                "FAIL",
                f"Error creando tarea: {str(e)}",
                execution_time
            )
            raise e

    def ver_tareas(self):
        """Hace clic en el botón para actualizar la lista de tareas y verifica que aparezca la nueva tarea"""
        start_time = time.time()
        try:
            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
            time.sleep(2)

            tasks = self.driver.find_element(By.ID, "tasks").text
            print(f"Tareas: {tasks}")
            
            if "Terminar laboratorio" not in tasks:
                raise AssertionError(f"La tarea 'Terminar laboratorio' no aparece en la lista: {tasks}")
            
            execution_time = time.time() - start_time
            self.report_generator.add_test_result(
                "Verificar Tareas en Frontend",
                "PASS",
                "La tarea 'Terminar laboratorio' aparece correctamente en la lista",
                execution_time
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.report_generator.add_test_result(
                "Verificar Tareas en Frontend",
                "FAIL",
                f"Error verificando tareas: {str(e)}",
                execution_time
            )
            raise e

    def run_integration_test(self):
        """Ejecuta el flujo completo de pruebas E2E"""
        print("🚀 Iniciando prueba de integración del FrontEnd...")
        
        try:
            self.setup_driver()
            self.abrir_frontend()
            user_id = self.crear_usuario()
            task_id = self.crear_tarea(user_id)
            self.ver_tareas()
            time.sleep(3)  # Pausa final para observar resultados si no está en modo headless
            
            print("✅ Prueba de integración del FrontEnd completada exitosamente")
            
        except Exception as e:
            print(f"❌ Error en la prueba de integración del FrontEnd: {str(e)}")
            raise e
        finally:
            # Cerrar el navegador
            if self.driver:
                self.driver.quit()
                
            # Paso 4: Limpieza de datos
            print("\n🧹 Iniciando limpieza de datos...")
            cleanup_results = self.report_generator.cleanup_test_data()
            
            for result in cleanup_results:
                print(result)
            
            # Paso 5: Verificar limpieza
            print("\n🔍 Verificando limpieza de datos...")
            verification_results = self.report_generator.verify_data_cleanup()
            
            for result in verification_results:
                print(result)
            
            # Paso 6: Generar reporte PDF
            print("\n📄 Generando reporte PDF...")
            report_file = self.report_generator.generate_pdf_report(
                cleanup_results, 
                verification_results
            )
            
            print(f"✅ Prueba completada. Reporte generado: {report_file}")

def main():
    """Función principal que ejecuta las pruebas"""
    test = FrontEndIntegrationTest()
    test.run_integration_test()

if __name__ == "__main__":
    main()
