 # 🧪 Actividad de Clase 2 – Pruebas de Integración

## 🎯 Objetivo

Implementar pruebas de integración entre los microservicios de usuarios y tareas, con dos funcionalidades adicionales:
1. Limpieza de datos generados durante la prueba (solo los creados por el test).
2. Generación automática de reportes en PDF con los resultados de las pruebas.

---

## 🛠️ Modificaciones realizadas

### En los microservicios:
- Se agregaron los endpoints:
  - `DELETE /users/<id>` en `users_service.py`
  - `DELETE /tasks/<id>` en `tasks_service.py`

### En `BackEnd-Test.py`:
- Se agregaron funciones `delete_user()` y `delete_task()` para eliminar por API.
- Se integró `generar_pdf()` al final de la prueba.

### En `requirements.txt`:
- Se añadió la dependencia `fpdf` para generar el PDF.

---

## Funcionalidad Implementada

### 1. Limpieza de datos
Al final del test BackEnd-Test:
- Se elimina la tarea usando un endpoint `DELETE /tasks/<id>`.
- Se elimina el usuario usando un endpoint `DELETE /users/<id>`.
- Se valida que ambos ya no existen consultando los endpoints GET.

### 2. Generación automática de PDF
- Al terminar la prueba, se genera un archivo PDF con los resultados en la carpeta `reportes/`.
- Los reportes son numerados secuencialmente (ej. `reporte_001.pdf`) y no se sobrescriben.

---

## 🖥️ Requisitos

Instalar dependencias con:

```bash
pip install -r requirements.txt

