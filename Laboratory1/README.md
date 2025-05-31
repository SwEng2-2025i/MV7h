# 🧪 Advanced Individual Lab: Multichannel Notification System (REST API)

**Autor:** Jacel Thomás Enciso Pinzón

---

## 🧠 Descripción del Sistema

Este sistema REST permite registrar usuarios con múltiples canales de comunicación (`email`, `SMS`, `llamada`, `consola`). Cuando se envía una notificación, el sistema intenta primero con el canal **preferido** del usuario. Si ese canal falla (simulado aleatoriamente), recurre a los canales alternativos usando una **cadena de responsabilidad**. Todos los intentos de envío se registran usando un **logger Singleton**.

---

## 🧩 Patrones de Diseño Usados

### 🔗 Chain of Responsibility

Cada canal de comunicación (Email, SMS, Llamada, Consola) actúa como un **handler** en una cadena. Si un canal falla, el mensaje se pasa al siguiente.

### 🧱 Singleton

El logger implementa el patrón Singleton para asegurar que todas las notificaciones sean registradas por una sola instancia global.

---

## 📦 Estructura del Proyecto

```text
├── app.py
├── controllers/
│   ├── __init__.py
│   ├── user_controller.py
│   └── notification_controller.py
├── services/
│   ├── __init__.py
│   ├── user_service.py
│   └── notification_service.py
├── notifications/
│   ├── __init__.py
│   ├── channels.py
│   ├── chain.py
│   └── logger.py
├── models/
│   ├── __init__.py
│   └── user.py
│
└── README.md
```
