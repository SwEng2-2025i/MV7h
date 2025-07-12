import requests
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    return response.json()["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={"title": description, "user_id": user_id})
    response.raise_for_status()
    return response.json()["id"]

def get_tasks():
    return requests.get(TASKS_URL).json()

def save_report_pdf(content):
    os.makedirs("reports", exist_ok=True)
    existing = [f for f in os.listdir("reports") if f.startswith("report") and f.endswith(".pdf")]
    next_num = len(existing) + 1
    filename = f"reports/report{next_num}.pdf"

    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    text = c.beginText(40, 750)
    for line in content:
        text.textLine(line)
    c.drawText(text)
    c.save()
    print(f"📄 Report saved: {filename}")

def integration_test():
    report_lines = []
    user_id = create_user("Camilo")
    report_lines.append(f"User created with ID: {user_id}")

    task_id = create_task(user_id, "Prepare presentation")
    report_lines.append(f"Task created with ID: {task_id}")

    tasks = get_tasks()
    user_tasks = [t for t in tasks if t["user_id"] == user_id]

    assert any(t["id"] == task_id for t in user_tasks), "Task not linked to user"
    report_lines.append("Task was successfully registered and linked to the user.")

    # No hay necesidad de hacer limpieza en este caso

    # Verificación de limpieza
    tasks_after = get_tasks()
    assert not any(t["id"] == task_id for t in tasks_after), "Task still present"
    report_lines.append("Task deletion verified.")

    save_report_pdf(report_lines)

if __name__ == "__main__":
    integration_test()
