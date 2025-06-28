import requests
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("✅ User created:", user_data)
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task created:", task_data)
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
    print(f"✅ Task {task_id} deleted")

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
    print(f"✅ User {user_id} deleted")

def generate_pdf_report(test_results):
    reports_dir = "test_reports"
    os.makedirs(reports_dir, exist_ok=True)
    # Buscar el siguiente número secuencial
    existing = [f for f in os.listdir(reports_dir) if f.startswith("test_report_") and f.endswith(".pdf")]
    nums = [int(f.split("_")[2].split(".")[0]) for f in existing if f.split("_")[2].split(".")[0].isdigit()]
    next_num = max(nums) + 1 if nums else 1
    filename = os.path.join(reports_dir, f"test_report_{next_num}.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, f"Test Report #{next_num}")
    c.drawString(50, 735, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y = 710
    for line in test_results:
        c.drawString(50, y, line)
        y -= 20
        if y < 50:
            c.showPage()
            y = 750
    c.save()
    print(f"✅ PDF report generated: {filename}")

def integration_test():
    test_log = []
    try:
        # Step 1: Create user
        user_id = create_user("Camilo")
        test_log.append(f"User created with ID: {user_id}")

        # Step 2: Create task for that user
        task_id = create_task(user_id, "Prepare presentation")
        test_log.append(f"Task created with ID: {task_id}")

        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
        test_log.append("Task was successfully registered and linked to the user.")

        # Step 4: Delete the created task and user
        delete_task(task_id)
        test_log.append(f"Task {task_id} deleted")
        delete_user(user_id)
        test_log.append(f"User {user_id} deleted")

        # Step 5: Verify deletion
        tasks_after = get_tasks()
        assert not any(t["id"] == task_id for t in tasks_after), "❌ The task was not deleted"
        test_log.append("Task deletion verified.")
        user_response = requests.get(f"{USERS_URL}/{user_id}")
        assert user_response.status_code == 404, "❌ The user was not deleted"
        test_log.append("User deletion verified.")
        test_log.append("✅ Cleanup completed and verified.")
    except Exception as e:
        test_log.append(f"❌ Test failed: {str(e)}")
        raise
    finally:
        generate_pdf_report(test_log)


if __name__ == "__main__":
    integration_test()