
import requests
import traceback
from report_generator import create_pdf_report


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

def verify_user_deleted(user_id):
    """Verify that a user has been deleted"""
    response = requests.get(f"{USERS_URL}/{user_id}")
    if response.status_code == 404:
        print(f"✅ User {user_id} successfully deleted")
        return True
    else:
        print(f"❌ User {user_id} still exists")
        return False

def verify_task_deleted(task_id):
    """Verify that a task has been deleted"""
    try:
        tasks = get_tasks()
        task_exists = any(t["id"] == task_id for t in tasks)
        if not task_exists:
            print(f"✅ Task {task_id} successfully deleted")
            return True
        else:
            print(f"❌ Task {task_id} still exists")
            return False
    except Exception as e:
        print(f"Error verifying task deletion: {e}")
        return False

def cleanup_data(user_id, task_id):
    """Clean up test data and verify deletion"""
    results = []
    

    try:
        response = requests.delete(f"{TASKS_URL}/{task_id}")
        if response.status_code == 204:
            results.append(f"✅ Task {task_id} deletion request successful")
        else:
            results.append(f"❌ Task {task_id} deletion failed with status {response.status_code}")
    except Exception as e:
        results.append(f"❌ Error deleting task {task_id}: {str(e)}")
    

    try:
        response = requests.delete(f"{USERS_URL}/{user_id}")
        if response.status_code == 204:
            results.append(f"✅ User {user_id} deletion request successful")
        else:
            results.append(f"❌ User {user_id} deletion failed with status {response.status_code}")
    except Exception as e:
        results.append(f"❌ Error deleting user {user_id}: {str(e)}")
    

    if verify_user_deleted(user_id):
        results.append(f"✅ User {user_id} verified as deleted")
    else:
        results.append(f"❌ User {user_id} verification failed")
    
    if verify_task_deleted(task_id):
        results.append(f"✅ Task {task_id} verified as deleted")
    else:
        results.append(f"❌ Task {task_id} verification failed")
    
    return results

def integration_test():
    test_results = []
    user_id = None
    task_id = None
    
    try:

        test_results.append("Starting integration test...")
        user_id = create_user("TestUser")
        test_results.append(f"✅ User created with ID: {user_id}")


        task_id = create_task(user_id, "Test Task")
        test_results.append(f"✅ Task created with ID: {task_id}")


        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        
        if any(t["id"] == task_id for t in user_tasks):
            test_results.append("✅ Task successfully registered and linked to user")
        else:
            test_results.append("❌ Task was not correctly registered")
            
        test_results.append("✅ Integration test completed successfully")
        
    except Exception as e:
        test_results.append(f"❌ Test failed with error: {str(e)}")
        test_results.append(f"❌ Traceback: {traceback.format_exc()}")
    
    finally:

        if user_id and task_id:
            test_results.append("Starting data cleanup...")
            cleanup_results = cleanup_data(user_id, task_id)
            test_results.extend(cleanup_results)
            test_results.append("✅ Data cleanup completed")
        

        try:
            report_file = create_pdf_report(test_results, "backend")
            test_results.append(f"✅ PDF report generated: {report_file}")
        except Exception as e:
            test_results.append(f"❌ Failed to generate PDF report: {str(e)}")
    
    return test_results

if __name__ == "__main__":
    results = integration_test()
    print("\n" + "="*50)
    print("FINAL TEST RESULTS:")
    print("="*50)
    for result in results:
        print(result)
