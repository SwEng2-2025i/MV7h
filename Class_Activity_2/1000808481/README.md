# Class Activity 2 - Integration Testing Enhancement
## Sergio Nicolás Siabatto Cleves - ID: 1000808481

### Overview
This project extends the basic integration testing example with data cleanup and PDF reporting functionality as required by Class Activity 2.

### Requirements Implementation

#### 1. Data Cleanup ✅
**Requirement:** All data added during test execution must be deleted afterward and verified.

**Implementation:**

**Modified Services:**
- **Users Service (`Users_Service/main.py`)**: Added DELETE endpoint `/users/<user_id>`
  - Deletes user from database
  - Calls Task Service to delete associated tasks
  - Added error handling and timeout protection

- **Task Service (`Task_Service/main.py`)**: Added DELETE endpoint `/tasks/user/<user_id>`
  - Deletes all tasks for a specific user
  - Returns count of deleted tasks

**Enhanced Test Files:**
- **BackEnd-Test.py**: Added cleanup functions:
  - `cleanup(user_id)` - Deletes user and tasks
  - `verify_user_deleted(user_id)` - Confirms user deletion (404 response)
  - `verify_tasks_deleted(user_id)` - Confirms no tasks remain for user

- **FrontEnd-Test.py**: Same cleanup functions for Selenium-based tests

#### 2. PDF Report Generation ✅
**Requirement:** Automatic PDF generation with sequential numbering, no overwrites.

**Implementation:**
- **Sequential Numbering System**: `get_next_report_number()` function
  - Scans existing reports in `test_reports/` folder
  - Finds highest number and increments
  - Creates report1.pdf, report2.pdf, etc.

- **PDF Generation**: `generate_pdf_report()` function using ReportLab
  - Comprehensive test reports with timestamps
  - Test steps, results, cleanup verification
  - Separate reports for backend and frontend tests

### Code Sections Added

#### Users_Service/main.py
```python
# Lines 45-69: DELETE endpoint for user deletion
@service_a.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    # Implementation with cascading task deletion
```

#### Task_Service/main.py  
```python
# Lines 42-55: DELETE endpoint for tasks by user
@service_b.route("/tasks/user/<int:user_id>", methods=["DELETE"])
def delete_tasks_by_user(user_id):
    # Implementation to delete all user tasks
```

#### Test/BackEnd-Test.py
```python
# Lines 30-65: Cleanup and verification functions
def cleanup(user_id): # Delete user and tasks
def verify_user_deleted(user_id): # Verify deletion
def verify_tasks_deleted(user_id): # Verify no tasks remain

# Lines 66-95: PDF reporting functions  
def get_next_report_number(): # Sequential numbering
def generate_pdf_report(): # PDF creation with ReportLab
```

#### Test/FrontEnd-Test.py
```python
# Lines 75-165: Same cleanup and PDF functions as backend
# Integrated into Selenium test workflow
```

### Test Execution Results

#### Data Cleanup Testing:
- ✅ Backend test creates user ID 1, task ID 1
- ✅ Cleanup deletes user via DELETE /users/1
- ✅ Verification confirms user returns 404
- ✅ Verification confirms no tasks remain for user 1
- ✅ Frontend test follows same pattern with different user

#### PDF Report Generation:
- ✅ First backend run creates `test_reports/report1.pdf`
- ✅ First frontend run creates `test_reports/report2.pdf`
- ✅ Subsequent runs increment numbers automatically
- ✅ All previous reports preserved

### Dependencies Added
```txt
flask
flask_sqlalchemy
requests
selenium
flask_cors
reportlab  # Added for PDF generation
```

### How to Test
1. Start services: `python Users_Service/main.py` (port 5001)
2. Start services: `python Task_Service/main.py` (port 5002)  
3. Start frontend: `python Front-End/main.py` (port 5000)
4. Run tests: `python Test/BackEnd-Test.py`
5. Run tests: `python Test/FrontEnd-Test.py`
6. Check generated reports in `test_reports/` folder

### Conclusion
Both requirements have been fully implemented:
- **Data cleanup** with verification works for both backend and frontend tests
- **PDF reports** generate sequentially without overwriting previous reports
- All original functionality preserved while adding enhanced test capabilities