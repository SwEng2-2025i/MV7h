#  Pruebas de Integración

 Pruebas de integración de microservicios con capacidades automatizadas de testing backend y frontend. Este proyecto demuestra pruebas de integración de APIs, testing automatizado de UI web, y generación de reportes en PDF.

## 🏗️ Arquitectura del Proyecto

Este proyecto consiste en una arquitectura de microservicios con los siguientes componentes:

### Servicios
- **Servicio de Usuarios** (Puerto 5001): API de gestión de usuarios
- **Servicio de Tareas** (Puerto 5002): API de gestión de tareas con validación de usuarios
- **Servicio Frontend** (Puerto 5000): Interfaz web para interacciones de usuario

### Componentes de Pruebas
- **Pruebas de Integración Backend**: Testing de APIs con limpieza automatizada
- **Pruebas Selenium Frontend**: Testing automatizado de UI web
- **Generador de Reportes**: Generación de reportes PDF de resultados de pruebas

## 📁 Estructura del Proyecto

```
├── requirements.txt           # Dependencias de Python
├── Front-End/
│   └── main.py               # Interfaz web Flask (Puerto 5000)
├── Users_Service/
│   └── main.py               # Servicio API de usuarios (Puerto 5001)
├── Task_Service/
│   └── main.py               # Servicio API de tareas (Puerto 5002)
├── Test/
│   ├── BackEnd-Test.py       # Pruebas de integración backend
│   ├── FrontEnd-Test.py      # Pruebas Selenium frontend
│   └── report_generator.py   # Generación de reportes PDF
├── instance/
│   ├── users.db              # Base de datos SQLite para usuarios
│   └── tasks.db              # Base de datos SQLite para tareas
└── reports/
    ├── backend/              # Reportes de pruebas backend
    └── frontend/             # Reportes de pruebas frontend
```

## 🚀 Inicio Rápido


### Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd "1032356041"
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Iniciar todos los servicios** (Ejecutar cada uno en una terminal separada)
   
   **Terminal 1 - Servicio de Usuarios:**
   ```bash
   cd Users_Service
   python main.py
   ```
   
   **Terminal 2 - Servicio de Tareas:**
   ```bash
   cd Task_Service
   python main.py
   ```
   
   **Terminal 3 - Servicio Frontend:**
   ```bash
   cd Front-End
   python main.py
   ```

### Ejecutar Pruebas

**Pruebas de Integración Backend:**
```bash
cd Test
python BackEnd-Test.py
```

**Pruebas Selenium Frontend:**
```bash
cd Test
python FrontEnd-Test.py
```

## 🔧 Documentación de la API

### Servicio de Usuarios (localhost:5001)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/users` | Crear un nuevo usuario |
| GET | `/users/{id}` | Obtener usuario por ID |
| GET | `/users` | Listar todos los usuarios |
| DELETE | `/users/{id}` | Eliminar usuario |
| POST | `/reset` | Eliminar todos los usuarios |

**Ejemplo de Crear Usuario:**
```json
POST /users
{
  "name": "Juan Pérez"
}
```

### Servicio de Tareas (localhost:5002)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/tasks` | Crear una nueva tarea |
| GET | `/tasks` | Listar todas las tareas |
| DELETE | `/tasks/{id}` | Eliminar tarea |
| POST | `/reset` | Eliminar todas las tareas |

**Ejemplo de Crear Tarea:**
```json
POST /tasks
{
  "title": "Completar proyecto",
  "user_id": 1
}
```

## 🧪 Características de las Pruebas

### Pruebas de Integración Backend (`BackEnd-Test.py`)

- **Pruebas de Gestión de Usuarios**: Crea y valida operaciones de usuarios
- **Pruebas de Gestión de Tareas**: Crea tareas y valida relaciones usuario-tarea
- **Integración Entre Servicios**: Prueba la comunicación entre servicios de Usuarios y Tareas
- **Limpieza Automatizada**: Limpia automáticamente los datos de prueba después de cada ejecución
- **Manejo de Errores**: Manejo integral de errores y reportes
- **Generación de Reportes PDF**: Genera reportes detallados de pruebas

**Flujo de Pruebas:**
1. Crear usuario de prueba
2. Crear tarea de prueba vinculada al usuario
3. Verificar relación tarea-usuario
4. Limpiar datos de prueba
5. Verificar finalización de limpieza
6. Generar reporte PDF

### Pruebas Selenium Frontend (`FrontEnd-Test.py`)

- **Automatización de UI Web**: Pruebas automatizadas de la interfaz web
- **Simulación de Interacción de Usuario**: Simula interacciones reales de usuario
- **Pruebas Multi-navegador**: Pruebas basadas en Chrome con framework extensible
- **Validación Visual**: Valida elementos de UI y respuestas
- **Limpieza Automatizada**: Reinicia todos los datos después de las pruebas

### Generación de Reportes

- **Reportes PDF Automatizados**: Generados para pruebas backend y frontend
- **Numeración Secuencial**: Los reportes se numeran automáticamente de forma secuencial
- **Información de Timestamp**: Cada reporte incluye timestamp de generación
- **Resultados Detallados**: Registro completo de resultados de pruebas







## 📝 Reportes de Pruebas

Los reportes de pruebas se generan automáticamente en formato PDF:
- **Reportes Backend**: `reports/backend/report_XXX.pdf`
- **Reportes Frontend**: `reports/frontend/report_XXX.pdf`


## 📋 Dependencias

- **Flask**: Framework web para servicios y frontend
- **Flask-SQLAlchemy**: ORM de base de datos
- **Flask-CORS**: Compartición de recursos de origen cruzado
- **Requests**: Cliente HTTP para pruebas de API
- **Selenium**: Framework de automatización web
- **ReportLab**: Librería de generación de PDF



#### 1. Endpoints `/reset` Agregados a Cada Microservicio

**Objetivo**: Permitir la limpieza total de las bases de datos de forma segura después de cada prueba.

**Servicios Afectados**:
- `Users_Service.py` (usuarios): se agregó `@app.route('/reset', methods=['POST'])`
- `Task_Service.py` (tareas): se agregó `@app.route('/reset', methods=['POST'])`

**Resultado**: Se elimina todo el contenido de las bases User y Task respectivamente.

En el apartado del Backend, por la construcción del código, se definieron directamente las rutas que se van a utilizar:

```python
RESET_USERS_URL = "http://localhost:5001/reset"
RESET_TASKS_URL = "http://localhost:5002/reset"
```

Al finalizar el main en el caso del Frontend, llamamos a la función creada para borrar las tareas:





