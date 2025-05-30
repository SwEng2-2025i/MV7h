# Sistema de Notificaciones Multicanal (API REST)

**Autor:** Juan Camilo Daza Gutierrez  
**Fecha:** Mayo 2025

## Descripción del sistema

Este proyecto es un sistema de notificaciones multicanal construido como una API REST utilizando **Flask**. Permite registrar usuarios con múltiples canales de comunicación (email, SMS, consola) y enviar notificaciones utilizando su canal preferido. Si el canal preferido falla (simulado aleatoriamente), se intentan los canales secundarios usando el patrón **Chain of Responsibility**.

Adicionalmente, se aplica el patrón **Singleton** para mantener una única instancia del logger durante toda la ejecución de la aplicación.

---

## Tecnologías utilizadas

- Python 3.10+
- Flask
- Flasgger (Swagger UI para documentación interactiva)
- logging (con patrón Singleton)
- random (simulación de fallos)

---

## Endpoints disponibles

###  `POST /users`
Registra un nuevo usuario.

- **Headers requeridos**: `Authorization: Bearer <token>`
- **Payload de ejemplo**:
```json
{
  "name": "Juan",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"]
}
```
- **Respuesta 201**:
```json
{
  "message": "User registered"
}
```

###  `GET /users`
Lista todos los usuarios registrados.

- **Headers requeridos**: `Authorization: Bearer <token>`
- **Respuesta 200**:
```json
[
  {
    "name": "Juan",
    "preferred_channel": "email",
    "available_channels": ["email", "sms"]
  }
]
```

###  `POST /notifications/send`
Envía una notificación a un usuario usando su canal preferido y haciendo fallback si falla.

- **Headers requeridos**: `Authorization: Bearer <token>`
- **Payload de ejemplo**:
```json
{
  "user_name": "Juan",
  "message": "Tu cita es mañana.",
  "priority": "alta"
}
```
- **Respuesta si se envía exitosamente**:
```json
{
  "message": "Notification sent via email"
}
```
- **Respuesta si fallan todos los canales**:
```json
{
  "message": "All channels failed"
}
```
---

## Patrones de diseño aplicados

### Chain of Responsibility
- Implementado para probar múltiples canales de comunicación.
- Cada canal intenta enviar el mensaje y, si falla (usando `random.choice`), pasa al siguiente.

### Singleton
- Aplicado al `logger` para asegurar que solo exista una instancia central de registro de eventos.
---

## Diagrama de clases/módulos

``` text
+-----------------------+           +---------------------+
|        User           |           |       Channel       |
|-----------------------|           |---------------------|
| - name: str           |<>-------->| - name: str         |
| - preferred_channel   |           | - next_channel      |
| - available_channels  |           +---------------------+
|                       |           | +send(message):bool |
+-----------------------+           +---------------------+

+---------------------------+
|       NotificationLogger  |  <<Singleton>>
|---------------------------|
| +get_instance(): logger   |
+---------------------------+
```
## Instrucciones de instalación y ejecución
### 1. Clonar el repositorio
``` bash
git clone https://github.com/tuusuario/sistema-notificaciones.git
cd sistema-notificaciones
``` 
### 2. Instalar dependencias
``` bash
pip install -r requirements.txt
``` 
### 3. Ejecutar el servidor
``` bash
python app.py
```
### 4. Abrir la documentación Swagger
``` bash
http://127.0.0.1:5000/apidocs
```
## Pruebas con `curl`:
### Crear usuario:
``` bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test" \
  -d '{
    "name": "Juan",
    "preferred_channel": "email",
    "available_channels": ["email", "sms"]
}'
```
### Enviar notificación:
``` bash
curl -X POST http://localhost:5000/notifications/send \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test" \
  -d '{
    "user_name": "Juan",
    "message": "Tu cita es mañana.",
    "priority": "alta"
}'
```
