# Class Activity 2 – Pruebas de Integración y E2E

Este proyecto extiende los ejemplos de pruebas de integración y pruebas end-to-end (E2E) revisados en clase, incorporando dos funcionalidades clave:

1. **Limpieza de datos (Data cleanup)**
2. **Generación automática de reportes PDF**

---

## 1. Limpieza de datos

Al finalizar cada prueba (tanto en Back-end como en Front-end), se eliminan los datos creados durante la ejecución del test. Esto incluye:

- **Usuario**: se borra el usuario creado con un `DELETE` a la API.
- **Tarea**: se borra la tarea vinculada al usuario.

Además, las pruebas verifican que la limpieza sea exitosa, haciendo una nueva llamada al endpoint de lectura y comprobando que los IDs de usuario y tarea ya no existen.

## 2. Generación automática de reportes PDF

Cada ejecución de prueba genera un reporte en formato PDF con la siguiente información básica:

- Número de reporte secuencial (no se sobrescriben los anteriores).
- Nombre de la prueba.
- Resultado (PASSED / FAILED / ERROR).
- Detalles relevantes (ID de usuario, ID de tarea, mensajes de error si aplica).

Los archivos PDF se guardan en la carpeta `reports/`, con nombres `report_1.pdf`, `report_2.pdf`, etc.

## Estructura de archivos

```
project-root/
├── reports/                # Directorio donde se guardan los PDFs
│   ├── report_1.pdf
│   ├── report_2.pdf
│   └── ...
├── tests_integration.py    # Script de prueba de integración Back-end
├── tests_frontend.py       # Script de prueba E2E Front-end con Selenium
└── README.md               # Este documento
```

## Requisitos previos

- Python 3.x

- Librerías Python:

  - `requests`
  - `reportlab`
  - `selenium`

- Servicios en ejecución:

  - Back-end de usuarios en `http://localhost:5001`
  - Back-end de tareas en `http://localhost:5002`
  - Front-end en `http://localhost:5000`

- Chromedriver instalado y en PATH (para pruebas E2E)

## Cómo ejecutar

1. **Prueba de integración Back-end**

   ```bash
   python tests_integration.py
   ```

2. **Prueba E2E Front-end**

   ```bash
   python tests_frontend.py
   ```

Ambos scripts generarán automáticamente un PDF en `reports/` al finalizar.

## Notas finales

- La limpieza de datos garantiza que no queden residuos de pruebas anteriores.
- Los reportes PDF permiten llevar un historial de ejecución y resultados.

¡Listo! Con esto tendrás pruebas más robustas y trazabilidad de resultados.

