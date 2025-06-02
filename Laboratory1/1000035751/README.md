# REST API for managing users and notifications

**By:** Santiago Villota Alava

## 📕 Description

This proyect implements a REST API in flask, for managing users and sending notifications. Users can register depending on their prefered method of communications (SMS, email, phonecall, etc).

In case of communication failure, the system tries again with a fallback communication method, if availible.

All user notifications are logged.

## 🎯 Features

- Flask for REST API.
- Swagger documentation.
- Chain of responsability pattern.
- Singleton pattern.
- System response for channel failure and retry fallback.
- User creation, specifing name, preffered_channel, available_channels.
- Send notifications, specifing username of receiver, message, and priority of message.
- Logger for notifications.
- No database.
- Modular, clean and documented code.

## 🔧 REST API Endpoints

| Method | Endpoint              | Description                                      |
|--------|-----------------------|--------------------------------------------------|
| POST   | `/users`              | Register a user with name, preferred and available channels |
| GET    | `/users`              | List all users                                   |
| POST   | `/notifications/send` | Send a notification with message and priority    |

### Example Payloads

#### POST /users

```json
{
  "name": "Juan",
  "preferred_channel": "email",
  "available_channels": ["email", "sms"]
}
```

#### POST /notifications/send

```json
{
  "user_name": "Juan",
  "message": "Your appointment is tomorrow.",
  "priority": "high"
}
```

## Design decisions

### Why use chain of responsability?

Chain of responsability is used because it allows for clean, modular design. When getting the different handlers to do the work of ensuring communications, order matters, and sometimes some handlers are not used. If we did this code in if statements, addign a new service would be problem.

### Why use singleton?

Singleton is used for the logger. Basically we want to call a centralized logger accross python files and classes, without worring about passing the instance. Singleton helps with that.

## Setup

### 1. Clone the repo

  ```bash
  git clone git@github.com:SwEng2-2025i/MV7h.git
  ```

### 2. Install requirements

```bash
pip install -r requirements.txt
```

### 3. Run app

```bash
python3 app.py
```

Works on Python 3.12.3

For documentation check [here](http://127.0.0.1:5000/apidocs) while app is running.

## Tests

Create a user

```bash
curl -X POST "http://localhost:5000/users" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"avalible_channels\": [    \"sms\",    \"email\",    \"phonecall\"  ],  \"name\": \"Pedro\",  \"preferred_channel\": \"sms\"}"
```

List all users

```bash
curl -X GET "http://localhost:5000/users" 
```

Send a notification

```bash
curl -X POST "http://localhost:5000/notifications/send" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{  \"message\": \"The toilet is clogged again\",  \"priority\": \"high\",  \"user_name\": \"Pedro\"}"
```
