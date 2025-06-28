import os
import glob
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"
DELETE_USER_URL = lambda uid: f"{USERS_URL}/{uid}"
DELETE_TASK_URL = lambda tid: f"{TASKS_URL}/{tid}"

PDF_DIR = "reports"
PDF_TEMPLATE = "report_{}.pdf"


def generate_pdf_report(test_name, result, details):
    os.makedirs(PDF_DIR, exist_ok=True)
    existing = glob.glob(os.path.join(PDF_DIR, "report_*.pdf"))
    # determine next sequence number
    nums = [int(os.path.splitext(os.path.basename(f))[0].split('_')[1]) for f in existing if f.split('_')[1].isdigit()]
    next_num = max(nums) + 1 if nums else 1
    filename = os.path.join(PDF_DIR, PDF_TEMPLATE.format(next_num))

    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, f"Test Report #{next_num}")
    c.drawString(50, 730, f"Test Name: {test_name}")
    c.drawString(50, 710, f"Result: {result}")
    text = c.beginText(50, 690)
    text.setFont("Helvetica", 10)
    text.textLines(details)
    c.drawText(text)
    c.save()
    print(f"📄 PDF report generated: {filename}")


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
    return response.json()


def delete_task(task_id):
    response = requests.delete(DELETE_TASK_URL(task_id))
    response.raise_for_status()
    print(f"🗑️ Task deleted: {task_id}")


def delete_user(user_id):
    response = requests.delete(DELETE_USER_URL(user_id))
    response.raise_for_status()
    print(f"🗑️ User deleted: {user_id}")


def integration_test():
    test_name = "Integration User-Task Flow"
    try:
        # Create user and task
        user_id = create_user("Camilo")
        task_id = create_task(user_id, "Prepare presentation")

        # Verify task exists
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), "The task was not correctly registered"
        print("✅ Test passed: task registered and linked.")

        # Cleanup
        delete_task(task_id)
        delete_user(user_id)

        # Verify cleanup
        tasks_after = get_tasks()
        assert not any(t["id"] == task_id for t in tasks_after), "Cleanup failed: task still exists"
        print("✅ Cleanup verified: test data removed.")

        result = "PASSED"
        details = f"User ID: {user_id}\nTask ID: {task_id}\nCleanup: successful"
    except AssertionError as ae:
        print(f"❌ AssertionError: {ae}")
        result = "FAILED"
        details = str(ae)
    except Exception as e:
        print(f"❌ Error during test: {e}")
        result = "ERROR"
        details = str(e)
    finally:
        generate_pdf_report(test_name, result, details)


if __name__ == "__main__":
    integration_test()