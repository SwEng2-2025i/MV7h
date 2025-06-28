## Julian Esteban Mendoza Wilches: Testing Activity

## Nuevos Endpoints

### 1. Endpoint para limpiar tareas de testing

- **Ruta:** `/cleanTestingTask`
- **Método:** `DELETE`
- **Descripción:** Elimina una tarea específica de la base de datos de tareas, útil para limpiar datos generados durante pruebas automáticas.
- **Uso:**  
  Envía una petición DELETE con un JSON que incluya el ID de la tarea a eliminar.
  ```json
  {
    "id": 123
  }
  ```
- **Respuesta exitosa:**
  ```json
  {
    "id": 123,
    "title": "Nombre de la tarea"
  }
  ```
- **Código relacionado:**  
  Función `clean_test_tasks()` en `Task_Service/main.py`.


- **Ruta:** `/cleanTestingUser`
- **Método:** `DELETE`
- **Descripción:** Elimina un usuario específico de la base de datos de usuarios, útil para limpiar datos generados durante pruebas automáticas.
- **Uso:**  
  Envía una petición DELETE con un JSON que incluya el ID del usuario a eliminar.
  ```json
  {
    "id": 123
  }
  ```
- **Respuesta exitosa:**
  ```json
  {
    "id": 123,
    "name": "Nombre del usuario"
  }
  ```
- **Código relacionado:**  
  Función `clean_test_user()` en `Users_Service/main.py`.

## Funciones auxiliares para limpieza de datos en tests

En el archivo `Test/BackEnd-Test.py` se añadieron dos funciones auxiliares para limpiar la información generada por los tests en la base de datos:

- **clean_test_task()**: Elimina las tareas creadas durante los tests usando el endpoint `/cleanTestingTask`.
- **clean_test_users()**: Elimina los usuarios creados durante los tests usando el endpoint `/cleanTestingUser`.

Para esto, también se añadieron las siguientes URLs:

- `DEL_TASKS_URL = "http://localhost:5002/cleanTestingTask"`
- `DEL_USERS_URL = "http://localhost:5001/cleanTestingUser"`

En el archivo `Test/FrontEnd-Test.py` también se añadieron funciones auxiliares para limpiar los datos generados por los tests:

- **detele_test_tasks()**: Elimina las tareas creadas durante los tests usando el endpoint `/cleanTestingTask`.
- **delete_test_users()**: Elimina los usuarios creados durante los tests usando el endpoint `/cleanTestingUser`.

Para esto, también se añadieron las siguientes URLs:

- `DEL_TASKS_URL = "http://localhost:5002/cleanTestingTask"`
- `DEL_USERS_URL = "http://localhost:5001/cleanTestingUser"`

## Generación de reportes en PDF

Se añadió el archivo `Test/Reports/Report.py` que permite generar reportes automáticos en formato PDF con los resultados de los tests.

- Utiliza la librería `reportlab` para crear el PDF.
- La función principal es `generar_reporte(nombre_reporte, resultados)`.
- El reporte se guarda en la carpeta `Test/Reports/Generated` y el nombre del archivo incluye la fecha y hora para evitar sobreescrituras.
- Cada línea de la lista `resultados` se agrega como una línea en el PDF, permitiendo registrar de forma clara los pasos y resultados de cada prueba.
- El archivo PDF se genera automáticamente al finalizar la ejecución de los scripts de test.

## Registro y reporte de resultados de los tests

En los scripts de testing (`Test/BackEnd-Test.py` y `Test/FrontEnd-Test.py`), los resultados de cada paso de las pruebas se van guardando en una lista llamada `resultados`.

- Cada vez que una operación importante (crear usuario, crear tarea, verificar tarea, etc.) se ejecuta, se añade un mensaje descriptivo a la lista `resultados`.
- Si ocurre un error, también se agrega un mensaje con la descripción del error.
- Al finalizar el test, la lista `resultados` se pasa a la función `generar_reporte` para crear un reporte PDF detallado.

Esto permite que cada reporte PDF contenga un resumen claro y específico de lo que ocurrió en cada prueba, incluyendo los datos relevantes (IDs, nombres, títulos, etc.) y cualquier error encontrado.


