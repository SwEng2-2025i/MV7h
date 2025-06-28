# Class Activity 2 - Pruebas de Integración y E2E

**Estudiante:** Juan Camilo Daza Gutierrez 
**ID:** <1004777234>  
**Fecha:** 2025-06-27

---

## Descripción

Esta actividad implementa pruebas automáticas de integración y E2E (end-to-end) en un sistema distribuido de microservicios compuesto por:

- **Users_Service:** gestión de usuarios.
- **Task_Service:** gestión de tareas asignadas a usuarios.
- **FrontEnd:** interfaz gráfica web.
- **BackEnd-Test.py:** script de prueba de integración entre microservicios.
- **FrontEnd-Test.py:** script de prueba E2E con Selenium.
- **report_utils.py:** utilitario para generación de reportes PDF.
- **reports/**: carpeta donde se guardan los reportes numerados.

---

## Estructura del proyecto
```text
Class_Activity_2/<1004777234>/
│
├── Front-End/
│    └── main.py 
├── Task_Service/ 
│    └── main.py 
├── Test/
│    ├── reports/
│    │    ├── reporte_001.pdf
│    │    └── reporte_002.pdf
│    ├── BackEnd-Test.py 
│    ├── FrontEnd-Test.py 
│    └── report_utils.py 
├── Users_Service/ 
│    ├── main.py
├── README.md 
└── requirements.txt
 ```

---

## Cambios realizados

### 1. **Microservicios**

Se añadieron rutas `DELETE` para permitir limpieza de datos luego de las pruebas:

#### En `Users_Service`:
- `DELETE /users/<id>`: elimina un usuario por ID.

#### En `Task_Service`:
- `DELETE /tasks/<id>`: elimina una tarea por ID.

---

### 2. **BackEnd-Test.py**

- Realiza una prueba de integración creando un usuario y una tarea relacionada.
- Verifica la asociación entre tarea y usuario.
- Elimina los datos creados al final.
- Confirma que los datos fueron efectivamente eliminados.
- Genera automáticamente un **reporte PDF numerado**.

---

### 3. **FrontEnd-Test.py**

- Automatiza el flujo completo desde la interfaz gráfica usando Selenium:
  - Crea usuario.
  - Crea tarea asociada.
  - Visualiza y valida tareas.
- Realiza limpieza automática de los datos al final.
- Genera reporte PDF numerado con los resultados.

---

### 4. **Generación de Reportes PDF**

- Se agregó el archivo `report_utils.py` con funciones para generar reportes numerados en `/reports`.
- Cada ejecución genera un nuevo archivo `reporte_XXX.pdf`.

