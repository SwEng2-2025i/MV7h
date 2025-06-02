# Sistema de Notificación

**Autor:** Jesus David Giraldo Gomez

Este proyecto implementa una API REST modular para gestionar usuarios y enviar notificaciones a través de múltiples canales (email, SMS, consola), utilizando patrones de diseño para garantizar escalabilidad y mantenibilidad.

## Características Principales

✔ **Gestión de usuarios**: Registro de preferencias de canales de comunicación  
✔ **Envío inteligente**: Priorización automática usando el canal preferido  
✔ **Resiliencia**: Fallover automático a canales alternativos cuando falla el principal  
✔ **Registro centralizado**: Historial completo de todos los intentos de notificación  

## Patrones Implementados

| Patrón | Ubicacion | Aplicación |
|--------|------------|-----------|
| **Chain of Responsibility** | channels | Escalabilidad para añadir nuevos canales |
| **Singleton** | notification_logger | Registro consistente desde cualquier componente |

## Estructura del Proyecto

```bash
1013676367/
├── channels/                               
│   ├── base_channel.py          
│   ├── email_channel.py         
│   ├── sms_channel.py           
│   └── console_channel.py       
│
├── core/                                   
│   ├── notification_logger.py   
│   └── notification_service.py  
│
├── models/                    
│   ├── user.py                  
│   └── notification.py          
│
├── README.md                  
├── requirements.txt           
└── run.py                     
```


## API Endpoints
### User
#### `POST /users`
Crea un nuevo usuario en el sistema.

**Request Body:**
```json
{
  "name": "Juan",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"]
}
```
**Response:**
```json
{
  "message": "User created successfully"
}
```

#### `GET /users`
**Request Body: Does not require**

**Response:**
```json
{
  [
  {
    "available_channels": [
      "sms",
      "console"
    ],
    "name": "Alice",
    "preferred_channel": "email"
  },
  {
    "available_channels": [
      "sms",
      "console"
    ],
    "name": "Pedro",
    "preferred_channel": "sms"
  }
  ]
}
```

### Notifications

#### `POST /notifications/send`
Crea un nuevo usuario en el sistema.

**Request Body:**
```json
{
  "message": "Your appointment is tomorrow.",
  "priority": "high",
  "user_name": "Juan"
}
```
**Response:**
```json
{
  "status": "sent"
}
```
### Logs

#### `GET /logs`

**Request Body: Does not require**

**Response:**
```json
{
    "channel": "EmailChannel",
    "message": "Hola",
    "success": false,
    "timestamp": "2025-05-29T20:53:35.693151",
    "user": "Alice"
}
```

## Configuración

### Clonar el repositorio:
```
git clone https://github.com/SwEng2-2025i/MV7h.git
```
### Acceder al sistema:
```
cd Laboratory1
cd 1013676367
```
### Instalar dependencias:
```
pip install -r requirements.txt
```
### Ejecutar la aplicación:
```
python app.py
```
### Acceder a la documentación interactiva:
```
http://localhost:5000/apidocs
```

## Testing con CURL

### Crear usuario
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Maria",
    "preferred_channel": "sms",
    "available_channels": ["sms", "email"]
  }'
```

### Obtener todos los usuarios
```bash
curl -X GET "http://localhost:5000/users" -H "accept: application/json"
```
### Enviar notificación
```bash
curl -X POST http://localhost:5000/notifications/send \
  -H "Content-Type: application/json" \
  -d '{
        "user_name": "Juan",
        "message": "Tu cita es mañana.",
        "priority": "high"
      }'
```

### Obtener logs de notificaciones
```bash
curl -X GET "http://localhost:5000/logs" -H "accept: application/json"
```


## Diagrama de clases

![alt text](<assets/esquema de archivos.png>)
