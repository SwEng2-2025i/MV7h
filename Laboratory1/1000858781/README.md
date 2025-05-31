# Advanced Individual Lab: Multichannel Notification System (REST API)

## Autor

**Daniel ALejandro Acosta Avila**

## Descripción del sistema

Esta API REST permite registrar usuarios con múltiples canales de comunicación y enviar notificaciones usando patrones de diseño:

1. **Chain of Responsibility** para delegar intentos de entrega entre canales.
2. **Singleton** para el logger global de intentos.
3. **Strategy** (o Factory) para encapsular la lógica de cada canal.

## Endpoints

- `POST /users`  
  Registra un usuario.
  ```json
  {
    "name": "Juan",
    "preferred_channel": "email",
    "available_channels": ["email", "sms"]
  }
  ```
