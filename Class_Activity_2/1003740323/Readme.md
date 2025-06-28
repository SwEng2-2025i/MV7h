## Actividad Testing - Javier Andrés Carrillo 

# Funcionalidades Implementadas

Características desarrolladas:

- 🎯 **Limpieza automática de datos**  
  - Aplicada tanto en el Back-End como en el Front-End.
- 📄 **Generación automática de informes PDF**

---

## Codigo relevante

### 1. Endpoints DELETE

**`Users_Service/main.py`** y **`Task_Service/main.py`**

```python
@service_a.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Elimina usuario por ID

@service_b.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Elimina tarea por ID
```

### 2. Sistema de Reportes

**`Test/test_utils.py`** - Archivo nuevo

```python
class TestReportGenerator:
    def track_created_user(user_id)      # Registra usuarios para limpieza
    def track_created_task(task_id)      # Registra tareas para limpieza
    def cleanup_test_data()              # Elimina datos de prueba
    def verify_data_cleanup()            # Verifica eliminación
    def generate_pdf_report()            # Genera reporte PDF numerado
```

### 3. Script Principal

**`Test/run_all_tests.py`** - Archivo nuevo

- Ejecuta todas las pruebas
- Verifica servicios
- Genera reporte 

## Archivos Modificados/Creados

```
├── Users_Service/main.py        
├── Task_Service/main.py         
├── Test/test_utils.py           
├── Test/BackEnd-Test.py         
├── Test/FrontEnd-Test.py        
├── Test/run_all_tests.py        
├── Test/README.md               
├── requirements.txt             
└── README.md                    
```

## Resultados

### Registro Consola

```text
✔️ Usuario creado: {'id': 1, 'name': 'Javier'}
✔️ Tarea creada: {'id': 1, 'title': 'Preparar presentación'}
🧼 Iniciando limpieza de datos...
✔️ Tarea 1 eliminada con éxito
✔️ Usuario 1 eliminado correctamente
📝 Reporte PDF generado en: Test/reports/test_report_001.pdf
```

## Puntos de Verificación

- ✔️ Eliminación automática de datos  
- ✔️ Confirmación de la limpieza realizada  
- ✔️ Creación de informes PDF con numeración correlativa  
- ✔️ Preservación de reportes anteriores  
- ✔️ Integración en Back-End y Front-End  ## Validación
