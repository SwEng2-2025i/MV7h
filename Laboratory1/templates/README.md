📄 Documento HTML: index.html  
🎯 Propósito  
Este archivo representa la vista principal de la aplicación Flask para registrar usuarios. Permite al usuario:
Ingresar su nombre.

Especificar cuántos canales de contacto quiere registrar (hasta 5).  

Ingresar los datos de contacto (correo, teléfono, etc.).  

Seleccionar uno de los canales como canal preferido.  

También incluye navegación a otras vistas del sistema y muestra mensajes flash de éxito o error.  

🧱 Estructura General  
Encabezado (<head>):  

Define codificación UTF-8 y escala responsive.  

Aplica estilos embebidos para apariencia profesional (contenedor centrado, botones estilizados, mensajes flash, etc.).  

Cuerpo (<body>):  

Contenedor principal .container con título y navegación.  

Bloque de mensajes flash ({% with messages = get_flashed_messages(...) %}) para mostrar errores o confirmaciones desde Flask.  

Formulario de registro de usuario:  

Campo de texto para el nombre del usuario.  

Selector desplegable para elegir cuántos canales de contacto se desean agregar.  

Área dinámica para agregar campos de entrada según la selección.  

Botón de envío.  

Script (<script>):  

La función generateContactFields() genera dinámicamente campos de contacto.  

Cada campo incluye:  

Entrada de texto para el canal de contacto.  

Radio button para marcarlo como canal preferido.  

Se ejecuta al cambiar la cantidad de canales seleccionados.  

🔄 Interacción con Flask  
Ruta asociada en Flask:  
El formulario hace un POST a /users, que debería ser gestionado por el controlador que maneja el registro (@app.route("/users", methods=['POST'])).  

Mensajes flash:  
Los mensajes como "Registro exitoso" o "Faltan datos" se muestran gracias a get_flashed_messages() de Flask, que se renderizan automáticamente en esta plantilla.  

🧪 Validaciones  
Todos los campos de entrada (input) están marcados como required para evitar envíos incompletos desde el lado del cliente.  

La validación adicional (como formatos de contacto) debe manejarse en el servidor.  

🧭 Navegación incluida  
Registrar Usuario → Página actual (/)  

Ver Usuarios Registrados → /users  

Enviar Notificación → /send_notification  

Esto permite al usuario interactuar con las demás funcionalidades del sistema de forma intuitiva.  

📄 Documento HTML: users.html  
🎯 Propósito  
Este archivo sirve como vista en el patrón Modelo-Vista-Controlador (MVC) y está diseñado para:  

Mostrar todos los usuarios registrados en el sistema.  

Visualizar la cantidad y detalles de los canales de contacto de cada usuario.  

Navegar fácilmente a otras partes de la aplicación (registro y envío de notificaciones).  

Mostrar mensajes de éxito, advertencia o error provenientes del backend Flask.  

🧱 Estructura General  
Encabezado (<head>):  

Define la codificación UTF-8 y diseño responsive.  

Incluye estilos embebidos para el diseño visual: contenedor centrado, listas estilizadas, mensajes flash, enlaces de navegación, etc.  

Cuerpo (<body>):  

Contenedor principal .container:  

Título: "Usuarios Registrados".  

Barra de navegación a otras vistas de la aplicación.  

Línea divisoria (<hr>).  

Bloque de mensajes flash:  

Usando bloques Jinja {% with %}, {% if %}, {% for %} para mostrar mensajes flash enviados por Flask.  

Bloque de visualización condicional de usuarios:  

Si hay usuarios ({% if users %}), se recorre cada uno con for y se muestra:  

Nombre del usuario (user.userName).  

Cantidad de canales de contacto (user.numChannels).  

Lista de canales (user.contactChannels, usando join(', ') para visualización).  

Canal preferido (user.preferredChannel).  

Si no hay usuarios, se muestra el mensaje "No hay usuarios registrados aún.".  

🔄 Interacción con Flask  
Variables renderizadas:  

users: lista pasada por el backend Flask que contiene los usuarios registrados.  

Cada user es un objeto (posiblemente un diccionario o una instancia de clase personalizada) con atributos:  

userName  

numChannels  

contactChannels (lista de strings)  

preferredChannel (string)  

Mensajes flash:  

Se muestran mensajes usando el sistema de flash() de Flask.  

Cada mensaje tiene una categoría (success, error, warning, info) para aplicar diferentes estilos visuales.  

🧭 Navegación incluida  
Registrar Usuario → /  

Ver Usuarios Registrados → /users  

Enviar Notificación → /send_notification  

Esto permite al usuario volver al formulario o a la funcionalidad de notificación fácilmente.  

🧪 Validaciones y visualización  
No se realiza validación desde esta plantilla.  

Se asume que los datos ya fueron validados al momento de ser registrados.  

Se usa un enfoque condicional para evitar mostrar una lista vacía si no hay usuarios.  

💡 Observaciones  
El uso de join(', ') para mostrar los canales de contacto es eficiente y legible.  

El diseño es claro, accesible y fácil de leer.  

Esta plantilla depende completamente del backend Flask para proveer los datos.  

📄 Documento HTML: notification_form.html  
🎯 Propósito  
Esta plantilla HTML actúa como vista dentro del patrón Modelo-Vista-Controlador (MVC). Su objetivo principal es permitir que el usuario:  

Escriba un mensaje de notificación.  

Seleccione su prioridad.  

Envíe la notificación al backend (ruta /notifications/send).  

Navegue a otras secciones de la aplicación.  

Reciba retroalimentación visual mediante mensajes flash.  

🧱 Estructura del Documento  
🧠 Encabezado (<head>)  
Metaetiquetas:  

charset="UTF-8": codificación de caracteres.  

viewport: asegura que el diseño sea responsive.  

Título de la página: Enviar Notificación.  

Estilos embebidos (<style>):  

Define diseño estético y responsivo.  

Estilo para contenedor principal, etiquetas, inputs, botones, navegación y mensajes flash.  

Colores y sombras para mejorar la experiencia visual del usuario.  

🧍‍♂️ Cuerpo (<body>)  
✅ Contenedor principal .container  
Encabezado principal: Enviar Notificación.  

🧭 Barra de Navegación  
html  
Copiar  
Editar  
<a href="/">Registrar Usuario</a> |  
<a href="/users">Ver Usuarios Registrados</a> |  
<a href="/send_notification">Enviar Notificación</a>  
Permite al usuario moverse entre las tres funcionalidades principales de la aplicación.  

🔁 Mensajes Flash  
Bloque Jinja que evalúa si hay mensajes flash del backend:  

jinja2  
Copiar  
Editar  
{% with messages = get_flashed_messages(with_categories=true) %}  
Si existen, los muestra en una lista con clases dinámicas (success, error, warning, info) para dar retroalimentación visual clara.  

📤 Formulario de Envío de Notificación  
html
Copiar
Editar
<form action="/notifications/send" method="POST">
Envía datos vía POST a la ruta /notifications/send, que debería estar manejada por el controlador Flask correspondiente.

Campos del formulario:

Textarea para mensaje:

name="message", obligatorio.

Permite escribir el contenido de la notificación.

Estilo claro y amigable.

Selector de prioridad:

name="priority", obligatorio.

Ofrece opciones predeterminadas (Baja, Media, Alta, Urgente) en formato value.

Botón de envío:

Llama a la acción del formulario para registrar la notificación.

🔄 Integración con Flask
Utiliza Jinja2 ({% ... %}) para integrar mensajes flash dinámicamente.

Los datos del formulario son enviados a la ruta /notifications/send, que debería:

Validar los datos.

Enviar la notificación.

Redireccionar de vuelta a esta vista con un mensaje flash.

🎨 Diseño y UX
Enfocado en simplicidad y claridad.

Altamente accesible.

Diseño responsive sin necesidad de frameworks externos.

📚 Dependencias y Observaciones
No utiliza JavaScript (todo es funcionalidad HTML + backend).

Espera que el backend maneje correctamente las validaciones de mensaje y prioridad.

Se puede extender fácilmente para soportar destinatarios, archivos adjuntos, etc.

