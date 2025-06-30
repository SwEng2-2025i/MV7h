import requests
from fpdf import FPDF
import os
import re

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    msg = f"User created: {user_data}"
    print(msg)
    return user_data["id"], msg

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    msg = f"Task created: {task_data}"
    print(msg)
    return task_data["id"], msg

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    if response.status_code == 404:
        msg = f"Warning: Task {task_id} not found (already deleted?)"
    else:
        response.raise_for_status()
        msg = f"Task {task_id} deleted."
    print(msg)
    return msg

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    if response.status_code == 404:
        msg = f"Warning: User {user_id} not found (already deleted?)"
    else:
        response.raise_for_status()
        msg = f"User {user_id} deleted."
    print(msg)
    return msg

def verify_task_deleted(task_id):
    response = requests.get(f"{TASKS_URL}/{task_id}")
    assert response.status_code == 404, f"ERROR: Task {task_id} was NOT deleted!"

def verify_user_deleted(user_id):
    response = requests.get(f"{USERS_URL}/{user_id}")
    assert response.status_code == 404, f"ERROR: User {user_id} was NOT deleted!"

def get_next_report_filename(base_folder="reports", base_name="test-report"):
    os.makedirs(base_folder, exist_ok=True)
    pattern = re.compile(rf"{re.escape(base_name)}-(\d+)\.pdf")
    max_num = 0
    for fname in os.listdir(base_folder):
        match = pattern.match(fname)
        if match:
            max_num = max(max_num, int(match.group(1)))
    return os.path.join(base_folder, f"{base_name}-{max_num+1}.pdf")

def save_report_pdf(content, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    def clean(line):
        return line.encode('latin-1', 'replace').decode('latin-1')
    for line in content.splitlines():
        pdf.cell(0, 10, clean(line), ln=True)
    pdf.output(filename)
    print(f"PDF report saved as {filename}")

def integration_test():
    log = []
    try:
        log.append("== Integration Test ==")
        # Step 1: Create user
        user_id, msg1 = create_user("Camilo")
        log.append(msg1)

        # Step 2: Create task for that user
        task_id, msg2 = create_task(user_id, "Prepare presentation")
        log.append(msg2)

        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), "ERROR: The task was not correctly registered"
        msg3 = "Test completed: task was successfully registered and linked to the user."
        print(msg3)
        log.append(msg3)

        # ---- CLEANUP ----
        log.append("--- Cleanup ---")
        msg4 = delete_task(task_id)
        log.append(msg4)
        verify_task_deleted(task_id)
        log.append(f"Task {task_id} deletion verified.")
        msg5 = delete_user(user_id)
        log.append(msg5)
        verify_user_deleted(user_id)
        log.append(f"User {user_id} deletion verified.")
        log.append("Cleanup completed and verified.")
        status = "SUCCESS"
    except Exception as e:
        err = f"ERROR: {str(e)}"
        print(err)
        log.append(err)
        status = "FAIL"
    finally:
        report_text = f"Test Result: {status}\n\n" + "\n".join(log)
        filename = get_next_report_filename()
        save_report_pdf(report_text, filename)

if __name__ == "__main__":
    integration_test()
