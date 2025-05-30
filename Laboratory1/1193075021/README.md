# Multichannel Notification System

**Author:** [Tu Nombre Completo]

## 📌 Descripción

Sistema REST para gestionar usuarios y enviar notificaciones a través de múltiples canales (email, SMS, consola), con fallback automático en caso de fallos.

## 🚀 Endpoints

### POST /users

```json
{
  "name": "Juan",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"]
}
```

### GET /users

Lista todos los usuarios.

### POST /notifications/send

```json
{
  "user_name": "Juan",
  "message": "Your appointment is tomorrow.",
  "priority": "high"
}
```

## 🎯 Patrones de Diseño Usados

- **Chain of Responsibility**: Para manejar fallos y fallback entre canales.
- **Singleton**: Para manejar un logger centralizado.

## 🏗️ Diagrama de Clases

![Diagrama de clases](diagrama%de%clases.png)

## 🛠️ Instrucciones

1. Instala dependencias:

```bash
pip install -r requirements.txt
```

2. Corre el servidor:

```bash
python main.py
```

3. Usa Postman o curl para probar:

```bash
curl -X POST http://127.0.0.1:5000/users -H "Content-Type: application/json" -d '{"name":"Juan","preferred_channel":"email","available_channels":["email","sms"]}'
```

## 📘 Swagger

http://localhost:5000/docs
