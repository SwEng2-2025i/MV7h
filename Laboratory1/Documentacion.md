# Laboratorio 1: Sistema de Notificaciones con Flask  
**Autor:** Andrés Felipe Perdomo Uruburu

---

## 📘 Descripción

Este proyecto implementa un sistema de notificaciones como una aplicación web utilizando **Flask**. Los usuarios pueden registrarse definiendo los canales de comunicación disponibles (correo electrónico, SMS, llamada telefónica, etc.) y seleccionar uno como canal **preferido**.

Cuando se registra un nuevo usuario, el sistema intenta enviarle una notificación de bienvenida a través de su canal preferido. Si este canal falla (fallo simulado aleatoriamente), se recurre a los demás canales en el orden disponible. Esta lógica sigue el **patrón de diseño Cadena de Responsabilidad**. Cada intento de envío se registra usando un **logger centralizado implementado como Singleton**.

---

## 🧩 Características

- Aplicación web desarrollada con Flask.
- Simulación de envío de notificaciones por canales definidos.
- Prevención de usuarios duplicados.
- Uso de dos patrones de diseño:
  - **Cadena de Responsabilidad** para la gestión de canales de comunicación.
  - **Singleton** para el logger de eventos.
- Fallos de notificación simulados aleatoriamente.
- Registro de intentos de envío exitosos y fallidos.
- Arquitectura modular y escalable.
- Interfaz simple para registrar usuarios desde un formulario web.

---

## 🧱 Estructura del Proyecto

notificaciones_flask/
├── app.py
├── templates/
│ └── index.html
├── static/
│ └── styles.css
├── data/
│ └── users.json
├── logger.py
├── handlers/
│ ├── base_handler.py
│ ├── email_handler.py
│ ├── sms_handler.py
│ └── call_handler.py
├── utils/
│ └── notification_chain.py
└── README.md


---

## 🔁 Patrones de diseño utilizados

### 1. Cadena de Responsabilidad

Los canales de notificación (`EmailHandler`, `SMSHandler`, `CallHandler`) se enlazan como una cadena. Cada handler intenta enviar el mensaje y, si falla (simulado), pasa el control al siguiente handler disponible.

### 2. modelo vista controlador

Las plantillas se encuentran separadas en su carpeta respectiva con el nombre de templates y son renderizadas a travez de jinja y los controladores estan bien definidos como funciones de Flask

---
📘 Diagrama de Clases





!["Captura de pantalla 2025-06-01 182805"](https://github.com/user-attachments/assets/00f24364-c75a-402e-95eb-2fd46ad00b54)


## 🚀 Instalación y ejecución

1. Clona el repositorio:

```bash
git clone https://github.com/tuusuario/notificaciones_flask.git
cd notificaciones_flask


###📮 Uso de la App
Registro de usuario
Formulario accesible desde la raíz:

GET /

Datos requeridos:

Nombre de usuario

Selección de canales disponibles

Canal preferido

🔒 Si se intenta registrar un nombre ya existente, el sistema muestra un error.

Ejemplo de notificación (simulada automáticamente al registrar un usuario):
plaintext
Copiar
Editar
--- SIMULANDO ENVÍO DE NOTIFICACIÓN ---
Intentando enviar mensaje por canal preferido: email
❌ FALLÓ
Intentando canal alternativo: sms
✅ ÉXITO
🖥️ Interfaz
La interfaz se entrega en un formulario HTML con diseño simple, accesible en la raíz del servidor.  

📘 Diagrama de Clases





!["Captura de pantalla 2025-06-01 182805"](https://github.com/user-attachments/assets/00f24364-c75a-402e-95eb-2fd46ad00b54)
