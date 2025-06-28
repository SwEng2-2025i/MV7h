import requests
import os 
from fpdf import FPDF

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"


def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    report = ("User created:" + str(user_data) + "\n")
    return user_data["id"], report

def delete_user(user_id):
    response = requests.delete(USERS_URL, json={"user_id": user_id})
    response.raise_for_status()
    user_data = response.json()
    print("✅ User deleted:", user_data)
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    report = ("Task created:" + str(task_data) + "\n")
    return task_data["id"], report

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def delete_task(task_id):
    response = requests.delete(TASKS_URL, json={
        "task_id": task_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task deleted:", task_data)

def generate_pdf_report(report_content, reports_dir='reports'):
    # Ensure the reports directory exists
    os.makedirs(reports_dir, exist_ok=True)
    # Find the next sequential report number
    existing = [f for f in os.listdir(reports_dir) if f.startswith('backend_reports_') and f.endswith('.pdf')]
    numbers = [int(f.split('_')[2].split('.')[0]) for f in existing if f.split('_')[2].split('.')[0].isdigit()]
    next_num = max(numbers) + 1 if numbers else 1
    filename = os.path.join(reports_dir, f'backend_reports_{next_num}.pdf')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in report_content.split('\n'):
        pdf.cell(0, 10, line, ln=True)
    pdf.output(filename)
    print(f"PDF report saved as {filename}")

def integration_test():
    # Step 1: Create user
    reports = ""
    user_id, report1 = create_user("Camilo")

    # Step 2: Create task for that user
    task_id, report2 = create_task(user_id, "Prepare presentation")

    reports += report1 + report2

    # Step 3: Verify that the task is registered and associated with the user
    tasks = get_tasks()
    user_tasks = [t for t in tasks if t["user_id"] == user_id]

    if not any(t["id"] == task_id for t in user_tasks):
        reports += "The task was not correctly registered\n"
    reports += ("Test completed: task was successfully registered and linked to the user.\n")

    generate_pdf_report(reports)

    # Step 4: Clean up 
    del_task = delete_task(task_id)
    del_user = delete_user(user_id)



if __name__ == "__main__":
    integration_test()
