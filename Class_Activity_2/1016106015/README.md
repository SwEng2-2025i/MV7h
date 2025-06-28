# 🧪 Proyecto de Prueba de Integración: Microservicios con Flask

Este proyecto simula un sistema distribuido compuesto por dos microservicios desarrollados en Flask. Cada uno se encarga de una funcionalidad diferente (usuarios y tareas) y se prueban de forma automática con scripts Python que validan la comunicación entre ambos servicios, generando además reportes en PDF.

---

## ⚙️ Requisitos

* Python 3.11 o superior
* Google Chrome instalado
* Dependencias Python:

```bash
pip install flask flask_sqlalchemy flask_cors requests reportlab selenium
```


## 🚀 Cómo ejecutar

### 1. Iniciar Microservicios

En terminales separadas:

```bash
# Terminal 1
cd ServiceA
python app.py  # Ejecuta en localhost:5001

# Terminal 2
cd ServiceB
python app.py  # Ejecuta en localhost:5002
```

### 2. Ejecutar Prueba Backend

```bash
cd Test
python BackEnd-Test.py
```

Esto probará:

* Crear un usuario
* Crear una tarea asociada
* Consultar tareas
* Eliminar la tarea y el usuario
* Verificar que hayan sido eliminados
* Generar un reporte PDF con los resultados en la carpeta `reports`

### 3. Ejecutar Prueba Frontend

```bash
python FrontEnd-Test.py
```

Esto abrirá un navegador real, simulará interacciones, y generará un reporte visual en PDF.

---

## 📄 Reportes

Cada vez que se ejecutan los tests, se genera un PDF con los pasos realizados, resultados, y posibles errores:

* `backend_report_001.pdf`, `backend_report_002.pdf`, ...
* `frontend_report_001.pdf`, `frontend_report_002.pdf`, ...

---

## 🚼 Limpieza Automática

Cada prueba incluye una fase de *cleanup* que elimina los usuarios y tareas creados durante la prueba, para garantizar un entorno limpio en cada ejecución.

---
