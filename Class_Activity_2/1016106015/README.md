# 🧪 Proyecto de Prueba de Integración: Microservicios con Flask

Este proyecto simula un sistema distribuido compuesto por dos microservicios desarrollados en Flask. Cada uno se encarga de una funcionalidad diferente (usuarios y tareas) y se prueban de forma automática con scripts Python que validan la comunicación entre ambos servicios, generando además reportes en PDF.

---

## 📦 Estructura del Proyecto

```
📁 Example 5 - Integration Test/
├── ServiceA/               # Microservicio A: Gestión de Usuarios
│   └── app.py              # Código del microservicio (puerto 5001)
│
├── ServiceB/               # Microservicio B: Gestión de Tareas
│   └── app.py              # Código del microservicio (puerto 5002)
│
├── Test/                   # Pruebas automáticas
│   ├── BackEnd-Test.py     # Test integración backend (API REST)
│   └── FrontEnd-Test.py    # Test E2E frontend con Selenium
│
└── reports/                # Carpeta donde se guardan los PDFs generados
    ├── backend_report_001.pdf
    └── frontend_report_001.pdf
```

---

## ⚙️ Requisitos

* Python 3.11 o superior
* Google Chrome instalado
* Dependencias Python:

```bash
pip install flask flask_sqlalchemy flask_cors requests reportlab selenium
```

> 💡 Si usas Windows, asegúrate de agregar `chromedriver.exe` a tu PATH o colócalo en el mismo directorio del script de prueba frontend.

---

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

### 3. Ejecutar Prueba Frontend (opcional)

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

## 📌 Notas

* Este proyecto no persiste los datos permanentemente (usa SQLite local).
* El frontend está pensado como una prueba mínima simulada con Selenium.
* No requiere autenticación, ni manejo de sesiones.

---

## 📚 Créditos

* Proyecto educativo con fines de práctica en pruebas de integración.
* Tecnología usada: Flask, SQLite, Requests, Selenium, ReportLab.

---

## 📬 Contacto

Si tienes dudas o sugerencias, no dudes en abrir un issue o contactarme por correo.
