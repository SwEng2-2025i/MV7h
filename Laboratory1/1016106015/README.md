# 🧪 MultiChannel Notification System
Autor: Nicolas Cortes Gutierrez

## 📝 Context

In today's software architecture, building modular and scalable systems is essential. Design patterns play a key role in helping developers write cleaner, more maintainable, and extensible code.

In this individual lab, you will implement a REST API for a notification system where users can register with multiple communication channels (e.g., email, SMS, console). When sending a notification, the system should first attempt to deliver it through the user's preferred channel. If delivery fails (simulated randomly), the system should attempt backup channels using a chain of responsibility.

The lab requires the use of at least two design patterns (chain of responsibility and one additional pattern of your choice). You will simulate notification logic, model system behavior, and structure the solution into clean, reusable components.

---

## 🎯 Objective

Develop a modular REST API to manage users and send notifications using **at least two advanced design patterns**, in addition to detailed design patterns.

---

## 🔁 Notification Logic

You will simulate delivery attempts via a **Chain of Responsibility**. For example:

1. A user has preferred channel = `email`, available = `[email, sms]`
2. Email channel is attempted (random failure simulated)
3. If it fails, the next channel (sms) is attempted

Use `random.choice([True, False])` to simulate failures.

---
## 💡System Deescription
Multichannel Notification System is a modular REST API developed in Python using Flask-RESTX. 
It allows managing users with multiple communication channels (email, SMS) and sending notifications using
a Chain of Responsibility pattern. If the preferred channel fails, the system automatically attempts backup channels. 
Additionally, the Singleton pattern is applied for event logging (Logger).

---
## 💡Endpoints
| Method | Endpoint              | Description                                      |
|--------|-----------------------|--------------------------------------------------|
| POST   | `/users`              | Register a user with name, preferred and available channels |
| GET    | `/users`              | List all users                                   |
| POST   | `/notifications/send` | Send a notification with message and priority    |

---
## 💡Example Payloads
**POST /users**
`
curl -X POST http://127.0.0.1:5000/users \
     -H "Content-Type: application/json" \
     -d '{"name":"Juan","preferred_channel":"email","available_channels":["email","sms"]}'
`

**GET /users**
`
curl http://127.0.0.1:5000/users
`

**POST /notifications/send**
`
curl -X POST http://127.0.0.1:5000/notifications/send \
     -H "Content-Type: application/json" \
     -d '{"user_name":"Juan","message":"Tu cita es mañana","priority":"high"}'
`

---
## 💡Class/module diagram
![image](https://github.com/user-attachments/assets/af75652f-2ab4-4915-9b8d-a7cfabd14154)

---
## 💡Design Pattern Justification
* Chain of Responsibility: Allows chaining objects that process notification sending through
  different channels in a flexible way and without nested conditionals.

* Singleton (Logger): Ensures a single instance of the event logging component,
  centralizing logs and preventing multiple instances.

---
## 💡Setup and Testing Instructions

* Clone the repository into laboratories/laboratory_1/1016106015/.

* Open a terminal and navigate to the project folder.

* Create a virtual environment:

`
py -3 -m venv venv
`

* Activate the environment:

`
Windows CMD: venv\Scripts\activate
`

`
PowerShell: Set-ExecutionPolicy -Scope Process Bypass y luego venv\Scripts\Activate.ps1
`

* Install dependencies:

`
pip install -r requirements.txt
`

* Run the server:

`
python app.py
`

* Test endpoints using curl, Postman, or Swagger UI:

`
Swagger UI: http://127.0.0.1:5000/
`

* Example cURL commands are provided in the "Example Payloads" 

---

## 📄 Deliverable

- Complete source code in organized structure
- A `README.md` that includes:
  - README.md with the full name.
  - System explanation and endpoint documentation
  - Class/module diagram
  - Design pattern justifications
  - Setup and testing instructions (e.g., curl/Postman examples)
- Documentation using Swagger should be included
- Well-commented code

---



## Submission Format- 
It must be delivered **via a pull request to the main branch of the repository**, which must be merged before the delivery date. In the folder laboratories/laboratory_1, create an X folder (where X = your identity document number), which must include the deliverable.


## ⏱️ Delivery date -> MAY 30, 2025 -> 23:59 GTM-5
