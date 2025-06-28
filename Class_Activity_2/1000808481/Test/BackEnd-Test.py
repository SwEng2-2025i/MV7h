# Test/BackEnd-Test.py
import requests
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

# PDF Report Configuration
REPORTS_DIR = "test_reports"
REPORT_PREFIX = "report"


def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("✅ User created:", user_data)
    return user_data["id"]


def create_task(user_id, description):
    response = requests.post(
        TASKS_URL, json={"title": description, "user_id": user_id})
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task created:", task_data)
    return task_data["id"]


def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks


# Added cleanup functions
def cleanup(user_id):
    """Delete user and all associated data"""
    delete_url = f"{USERS_URL}/{user_id}"
    try:
        response = requests.delete(delete_url)
        response.raise_for_status()
        print(
            f"🧹 User {user_id} and their tasks have been cleaned up.")
        return True
    except requests.exceptions.HTTPError as e:
        print(f"⚠️ Cleanup failed for user {user_id}: {e}")
        return False


def verify_user_deleted(user_id):
    """Verify that a user has been deleted"""
    response = requests.get(f"{USERS_URL}/{user_id}")
    if response.status_code != 404:
        raise AssertionError(
            f"❌ User {user_id} still exists")
    print(f"✅ Verified user {user_id} was deleted")


def verify_tasks_deleted(user_id):
    """Verify that all tasks for a user have been deleted"""
    tasks = get_tasks()
    user_tasks = [
        t for t in tasks if t["user_id"] == user_id]
    if len(user_tasks) > 0:
        raise AssertionError(
            f"❌ Found {len(user_tasks)} tasks still associated with user {user_id}"
        )
    print(
        f"✅ Verified all tasks for user {user_id} were deleted")


# Added PDF Report functions
def get_next_report_number():
    """Get the next sequential report number"""
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)
        return 1

    existing_files = [
        f
        for f in os.listdir(REPORTS_DIR)
        if f.startswith(REPORT_PREFIX) and f.endswith(".pdf")
    ]

    existing_numbers = []
    for filename in existing_files:
        number_part = filename[len(REPORT_PREFIX): -4]
        if number_part.isdigit():
            existing_numbers.append(int(number_part))

    return max(existing_numbers, default=0) + 1


def generate_pdf_report(report_content, report_number):
    """Generate a PDF report with the given content and number"""
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    filename = f"{REPORT_PREFIX}{report_number}.pdf"
    filepath = os.path.join(REPORTS_DIR, filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50,
                 f"Backend Integration Test Report #{report_number}")

    # Date and time
    c.setFont("Helvetica", 10)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.drawString(50, height - 70, f"Generated: {timestamp}")

    # Content
    c.setFont("Helvetica", 12)
    y_position = height - 100

    for line in report_content:
        if y_position < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - 50

        c.drawString(50, y_position, str(line))
        y_position -= 20

    c.save()
    print(f"📄 Report saved as: {filepath}")
    return filepath


def integration_test():
    """Enhanced integration test with cleanup and reporting"""
    user_id = None
    report_content = []
    test_successful = False

    try:
        report_content.append(
            "=== BACKEND INTEGRATION TEST ===")
        report_content.append("")

        # Step 1: Create user
        report_content.append("Step 1: Creating user...")
        user_id = create_user("Camilo")
        report_content.append(
            f"✅ User created with ID: {user_id}")

        # Step 2: Create task for that user
        report_content.append("Step 2: Creating task...")
        task_id = create_task(
            user_id, "Prepare presentation")
        report_content.append(
            f"✅ Task created with ID: {task_id} for user {user_id}")

        # Step 3: Verify that the task is registered and associated with the user
        report_content.append(
            "Step 3: Verifying task-user integration...")
        tasks = get_tasks()
        user_tasks = [
            t for t in tasks if t["user_id"] == user_id]

        assert any(
            t["id"] == task_id for t in user_tasks
        ), "❌ The task was not correctly registered"
        print(
            "✅ Test completed: task was successfully registered and linked to the user."
        )
        report_content.append(
            "✅ Task successfully linked to user")
        report_content.append(
            "✅ Backend integration test PASSED")
        test_successful = True

    except Exception as e:
        error_msg = f"❌ Test failed: {str(e)}"
        print(error_msg)
        report_content.append(error_msg)
        test_successful = False

    finally:
        # REQUIREMENT 1: Data cleanup and verification
        report_content.append("")
        report_content.append("=== CLEANUP PHASE ===")

        if user_id is not None:
            try:
                # Cleanup
                report_content.append(
                    "Performing cleanup...")
                cleanup_success = cleanup(user_id)

                if cleanup_success:
                    report_content.append(
                        f"🧹 Cleanup completed for user ID: {user_id}"
                    )

                    # Verify cleanup
                    report_content.append(
                        "Verifying cleanup...")
                    verify_user_deleted(user_id)
                    verify_tasks_deleted(user_id)

                    report_content.append(
                        "✅ Cleanup verification PASSED")
                else:
                    report_content.append(
                        "⚠️ Cleanup failed")

            except Exception as cleanup_error:
                error_msg = f"❌ Cleanup verification failed: {str(cleanup_error)}"
                print(error_msg)
                report_content.append(error_msg)

        # REQUIREMENT 2: PDF Report generation
        report_content.append("")
        report_content.append("=== TEST SUMMARY ===")
        if test_successful:
            report_content.append(
                "Overall Result: ✅ PASSED")
        else:
            report_content.append(
                "Overall Result: ❌ FAILED")

        # Generate PDF report
        report_number = get_next_report_number()
        generate_pdf_report(report_content, report_number)

        print("🏁 Backend integration test completed")


if __name__ == "__main__":
    integration_test()
