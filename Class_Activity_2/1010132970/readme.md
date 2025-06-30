# Integration Test — Data Cleanup & Automatic PDF Reporting

## 📋 Overview

This repository demonstrates end-to-end integration testing for a microservice architecture (Users & Tasks), focusing on two main features:
1. **Data cleanup:** Ensuring all test data is deleted and its deletion verified.
2. **Automatic PDF reporting:** Saving the result of each test execution in a sequential, never-overwritten PDF report.

---

## 🟢 **Backend Integration Test**

### 🔧 **Added/Modified Code Sections**
- **Cleanup logic:**  
  After creating and verifying test data, the script calls the appropriate DELETE endpoints to remove both user and task.  
  The following verification functions were added to confirm deletion:
  - `verify_task_deleted(task_id)`
  - `verify_user_deleted(user_id)`

- **PDF Report Generation:**  
  - Functions for sequential report naming and PDF creation were added:
    - `get_next_report_filename()`
    - `save_report_pdf(content, filename)`
  - Test log collection (using a `log` list) to capture and store every step and result.
  - All prints are now also saved in the report.

- **Dependency:**  
  - Added [fpdf](https://pyfpdf.github.io/fpdf2/) as a requirement:
    ```
    pip install fpdf
    ```

### 📝 **Sample Test Output**
After each run, a PDF report is generated in the `reports/` folder, e.g. `test-report-1.pdf`, `test-report-2.pdf`, etc.  
The PDF will show a trace like:

```Test Result: SUCCESS

== Integration Test ==  
User created: {'id': 10, 'name': 'Camilo'}  
Task created: {'id': 15, 'title': 'Prepare presentation', 'user_id': 10}  
Test completed: task was successfully registered and linked to the user.  
--- Cleanup ---  
Task 15 deleted.  
Task 15 deletion verified.  
User 10 deleted.  
User 10 deletion verified.  
Cleanup completed and verified.

```
## 🟢 **Frontend Integration Test (Selenium-based)**

### 🔧 **Added/Modified Code Sections**
- **Cleanup:**  
  After the Selenium flow, the script now calls the backend's DELETE endpoints (via `requests`) to clean up the user and task created during the test.
- **PDF Reporting:**  
  - Uses similar helper functions for naming and creating sequential PDF reports (`get_next_report_filename()` and `save_report_pdf()`).
  - All significant log entries (actions, results, errors) are added to a log list, which is then written to the PDF.
- **Dependency:**  
  - Also it now requires [fpdf](https://pyfpdf.github.io/fpdf2/):
    ```
    pip install fpdf
    ```

