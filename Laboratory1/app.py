from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
import json
import os
import random  # <- Importado para simular fallos

app = Flask(__name__)
app.secret_key = 'secreto'  

# Define la ruta para el archivo JSON
DATA_FILE = 'data/all_data.json'

# --- Mensajes de depuración al iniciar la aplicación y asegurar la estructura ---
print("\n--- INICIANDO APLICACIÓN FLASK ---")
print(f"Directorio de trabajo actual: {os.getcwd()}")
print(f"Ruta esperada del archivo JSON: {os.path.abspath(DATA_FILE)}")

if not os.path.exists('data'):
    try:
        os.makedirs('data')
        print(f"Carpeta 'data/' creada exitosamente en: {os.path.abspath('data')}")
    except OSError as e:
        print(f"!!! ERROR FATAL: No se pudo crear la carpeta 'data/': {e}")
        import sys
        sys.exit(1)

if os.path.exists(DATA_FILE):
    if os.path.getsize(DATA_FILE) > 0:
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                json.load(f)
            print(f"El archivo '{DATA_FILE}' existe y parece ser un JSON válido.")
        except json.JSONDecodeError:
            print(f"!!! ADVERTENCIA: El archivo '{DATA_FILE}' existe pero no es un JSON válido.")
    else:
        print(f"El archivo '{DATA_FILE}' existe pero está vacío.")
else:
    print(f"El archivo '{DATA_FILE}' no existe al inicio. Se creará cuando se envíen datos.")

print("------------------------------------\n")


@app.route("/", methods=['GET'])
def index():
    print("\n--- SOLICITUD GET RECIBIDA en '/' ---")
    return render_template("index.html")


@app.route("/users", methods=['POST'])
def register_user():
    print("\n--- SOLICITUD POST RECIBIDA en '/users' ---")
    print("Datos de request.form:", request.form)

    if not request.form:
        flash('Error: No se recibieron datos del formulario.', 'error')
        return redirect(url_for('index'))

    try:
        user_name = request.form['userName']
        num_channels_str = request.form['numChannels']

        try:
            num_channels = int(num_channels_str)
        except ValueError:
            flash('Error: El número de canales no es válido.', 'error')
            return redirect(url_for('index'))

        preferred_channel_key = request.form.get('preferredChannel') 

        contact_channels = []
        for i in range(num_channels):
            channel_key = f'contactChannel{i}'
            channel_value = request.form.get(channel_key, 'N/A') 
            contact_channels.append(channel_value)

        preferred_channel_value = ""
        if preferred_channel_key:
            try:
                preferred_index = int(preferred_channel_key.replace('contactChannel', ''))
                if 0 <= preferred_index < len(contact_channels):
                    preferred_channel_value = contact_channels[preferred_index]
                else:
                    preferred_channel_value = "N/A (Índice fuera de rango)"
            except ValueError:
                preferred_channel_value = "N/A (Clave preferida inválida)"
        else:
            print("--- [!] No se seleccionó canal preferido.")

        user_data = {
            'userName': user_name,
            'numChannels': num_channels,
            'contactChannels': contact_channels,
            'preferredChannel': preferred_channel_value
        }

        all_data = []
        if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                try:
                    all_data = json.load(f)
                except:
                    all_data = []

        all_data.append(user_data)

        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=4, ensure_ascii=False)
            flash('¡Registro de usuario exitoso!', 'success')

            # === SIMULACIÓN DE NOTIFICACIÓN ===
            print("\n--- SIMULANDO ENVÍO DE NOTIFICACIÓN ---")
            mensaje = f"Bienvenido, {user_name}. Gracias por registrarte."
            print(f"Intentando enviar mensaje por canal preferido: {preferred_channel_value}")
            envio_exitoso = random.random() > 0.3  # 70% probabilidad de éxito

            if envio_exitoso:
                print(f"[✅ ÉXITO] Notificación enviada por canal preferido: {preferred_channel_value}")
            else:
                print(f"[❌ FALLÓ] Canal preferido '{preferred_channel_value}' falló. Buscando alternativos...")

                canales_restantes = [c for c in contact_channels if c != preferred_channel_value]
                for canal_alternativo in canales_restantes:
                    print(f"Intentando canal alternativo: {canal_alternativo}")
                    if random.random() > 0.3:
                        print(f"[✅ ÉXITO] Notificación enviada por canal alternativo: {canal_alternativo}")
                        break
                else:
                    print("[❌ ERROR] Todos los canales fallaron. No se pudo enviar la notificación.")

        except Exception as e:
            flash(f'Error al guardar el usuario: {e}', 'error')

        return redirect(url_for('index'))

    except KeyError as e:
        flash(f'Error: Falta un campo requerido: {e}', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Ocurrió un error inesperado: {e}', 'error')
        return redirect(url_for('index'))


@app.route("/users", methods=['GET'])
def list_users():
    print("\n--- SOLICITUD GET en '/users' ---")
    users = []
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                users = json.load(f)
        except:
            flash('No se pudieron cargar los usuarios.', 'error')
    else:
        flash('No hay usuarios registrados aún.', 'info')
    
    return render_template("users.html", users=users)


@app.route("/send_notification", methods=['GET'])
def send_notification_form():
    print("\n--- MOSTRANDO FORMULARIO DE NOTIFICACIÓN ---")
    return render_template("notification_form.html")


@app.route("/notifications/send", methods=['POST'])
def send_notification():
    print("\n--- ENVÍO DE NOTIFICACIÓN MANUAL ---")
    print("Datos recibidos:", request.form)

    if not request.form:
        flash('Error: No se recibieron datos.', 'error')
        return redirect(url_for('send_notification_form'))

    try:
        message = request.form.get('message')
        priority = request.form.get('priority')

        if not message or not priority:
            flash('Error: El mensaje y la prioridad son obligatorios.', 'error')
            return redirect(url_for('send_notification_form'))

        print(f"Mensaje='{message}', Prioridad='{priority}'")
        flash(f'Notificación enviada con éxito: "{message}" (Prioridad: {priority})', 'success')
        return redirect(url_for('send_notification_form'))

    except Exception as e:
        flash(f'Ocurrió un error al enviar la notificación: {e}', 'error')
        return redirect(url_for('send_notification_form'))


if __name__ == '__main__':
    app.run(debug=True)
