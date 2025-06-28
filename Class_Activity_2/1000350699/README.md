# Sistema de Pruebas de Integración y Reportes Automáticos

Este proyecto contiene ejemplos de arquitectura de software y un sistema de pruebas de integración automatizadas para servicios de usuarios y tareas, incluyendo generación automática de reportes PDF.

## Estructura relevante
- `Example 5 - Integration Test/`
  - `Users_Service/main.py`: Servicio Flask para gestión de usuarios (alta, consulta, borrado).
  - `Task_Service/main.py`: Servicio Flask para gestión de tareas (alta, consulta, borrado, validación de usuario).
  - `Test/BackEnd-Test.py`: Prueba de integración backend (usuarios y tareas), limpieza de datos y generación de PDF.
  - `Test/FrontEnd-Test.py`: Prueba end-to-end con Selenium, limpieza de datos y generación de PDF.
  - `Test/test_reports/`: Carpeta donde se guardan los reportes PDF generados automáticamente.

## Funcionalidades implementadas

### 1. Limpieza de datos de prueba
- Todos los datos creados durante las pruebas (usuarios y tareas) se eliminan automáticamente al finalizar cada prueba.
- Se verifica que los datos hayan sido efectivamente eliminados.
- Esto se implementa tanto en las pruebas backend como frontend.

### 2. Generación automática de informes PDF
- Al finalizar cada ejecución de prueba, se genera un informe PDF con los resultados y pasos de la prueba.
- Los informes se guardan en la carpeta `test_reports/` con nombres secuenciales (`test_report_1.pdf`, `frontend_report_1.pdf`, etc.), sin sobrescribir los anteriores.
- Los informes incluyen fecha, número de reporte y el log de pasos/resultados de la prueba.

### 3. Pruebas backend (`BackEnd-Test.py`)
- Crea un usuario y una tarea asociada.
- Verifica la correcta asociación.
- Elimina ambos y verifica la eliminación.
- Genera un PDF con el resultado de cada paso.

### 4. Pruebas frontend (`FrontEnd-Test.py`)
- Usa Selenium para simular la interacción de un usuario en la interfaz web.
- Crea usuario y tarea desde el frontend.
- Verifica visualmente la creación.
- Elimina los datos creados y verifica la limpieza.
- Genera un PDF con el resultado de cada paso.

## Requisitos para ejecutar
- Python 3.x
- Flask, Flask-CORS, Flask-SQLAlchemy, requests, selenium, reportlab
- ChromeDriver para Selenium (y Google Chrome instalado)

Instala dependencias con:
```
pip install flask flask-cors flask-sqlalchemy requests selenium reportlab
```

## Ejecución
1. Inicia los servicios de usuarios y tareas:
   - `python Example 5 - Integration Test/Users_Service/main.py`
   - `python Example 5 - Integration Test/Task_Service/main.py`
2. Ejecuta las pruebas:
   - Backend: `python Example 5 - Integration Test/Test/BackEnd-Test.py`
   - Frontend: `python Example 5 - Integration Test/Test/FrontEnd-Test.py`
3. Revisa los reportes PDF generados en `Example 5 - Integration Test/Test/test_reports/`

---

Este sistema asegura que los datos de prueba no persisten y que cada ejecución queda documentada automáticamente en un informe PDF.
