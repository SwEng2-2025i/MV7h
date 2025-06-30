# 🧪 Reporte de Pruebas de Integración - Example 5

**Autor:** Cristian David Machado Guzmán  
**Fecha:** 26 de junio de 2025

---

## 📘 Descripción

Este proyecto implementa un sistema distribuido compuesto por tres servicios principales:

- **Users_Service:** Servicio encargado de crear y consultar usuarios.
- **Task_Service:** Servicio encargado de crear y listar tareas asociadas a un usuario.
- **Front-End:** Interfaz web que consume ambos servicios para facilitar su uso.
- **Tests:** Pruebas automatizadas (con `requests` y `selenium`) para validar la integración entre servicios.

---

## ✅ Funcionalidades añadidas

Se añadieron dos funcionalidades adicionales a los archivos de pruebas, tanto desde back-end como front-end:

### 1. 🧼 Limpieza de datos al finalizar las pruebas (Data cleanup)

**Objetivo:** Asegurar que los datos de prueba (usuarios y tareas) no queden persistentes luego de ejecutar los tests.

**Dónde se implementó:**

- `BackEnd-Test.py`:  
  - Se añadieron las funciones `eliminar_usuario`, `eliminar_tarea` y `verificar_eliminacion`.
  - Estas funciones eliminan y confirman la eliminación de los datos creados durante la prueba.

### 2. 📄 Generación automática de reportes PDF numerados

**Objetivo:** Documentar los resultados de cada prueba en un archivo PDF independiente, numerado secuencialmente y almacenado sin sobrescribir anteriores.

**Dónde se implementó:**

- `BackEnd-Test.py`:  
  - Se creó la función `generar_pdf_reporte(logs)` que usa la librería `fpdf` para construir el archivo.
  - Los reportes se guardan en la carpeta `reports/` con nombre `report_001.pdf`, `report_002.pdf`, etc.
  - La función `integration_test` fue modificada para registrar los logs paso a paso y pasarlos a la función de generación del PDF.

**Ejemplo del resultado**
reports/
├── report_001.pdf
├── report_002.pdf

---

## 📂 Archivos modificados

| Archivo            | Sección modificada o añadida                | Descripción breve                               |
|--------------------|---------------------------------------------|--------------------------------------------------|
| `BackEnd-Test.py`  | `eliminar_usuario`, `eliminar_tarea`, `verificar_eliminacion` | Limpieza de datos de test |
|                    | `generar_pdf_reporte`                       | Creación automática del PDF con los resultados  |
|                    | `integration_test`                         | Integración completa del flujo + logs + reporte |
| `requirements.txt` | + `fpdf`                                    | Dependencia nueva para la generación de PDFs    |

---

## 🧪 Ejecución recomendada

1. Asegurese de tener los tres servicios (`Users_Service`, `Task_Service` y `Front-End`) corriendo.
2. Ejecutar el archivo de pruebas:

```bash
python BackEnd-Test.py
