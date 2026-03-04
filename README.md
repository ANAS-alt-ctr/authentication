### Overview

This project is a simple **Authentication API** built with **FastAPI (Python)**.
It allows users to:

* Register a new account
* Log in with username and password
* Receive a secure access token (JWT)
* Store user data in a JSON file (no database)
* Track login and registration history

This project is mainly for learning and practice.

---

## Main Features

* User Registration
* User Login
* Password hashing (passwords are not saved as plain text)
* JWT token generation for authentication
* JSON file storage
* Authentication history tracking

---

## Project Structure (Simple Explanation)

* **main file** – Starts the FastAPI application
* **Authentication router** – Handles register and login
* **Security module** – Hashes passwords and creates tokens
* **Models & Schemas** – Define how user data should look
* **users.json** – Stores users and login history

---

## User Registration

Users can create an account by providing:

* Username
* Password
* Name
* Email
* Age
* City

### What happens during registration:

1. The system checks if the username already exists.
2. If it does not exist, the password is encrypted (hashed).
3. The user information is saved in `users.json`.
4. A registration event is recorded in the history.
5. A success message is returned.

---

## User Login

Users log in using:

* Username
* Password

### What happens during login:

1. The system checks if the username exists.
2. It verifies the password using hashing.
3. If correct, it creates a JWT access token.
4. A login event is recorded in the history.
5. The token is returned to the user.

The token can be used to access protected endpoints (if added later).

---

## Data Storage

All data is stored in a file called:

**users.json**

It contains:

* A list of registered users
* A list of authentication history (register and login events with timestamps)

This means:

* No database is required
* Data is stored locally
* It is simple but not suitable for large production systems

---

## Security

* Passwords are encrypted (hashed) before storage
* JWT tokens are used for authentication
* Login and register activities are recorded

⚠ Important:
This is a basic learning project. For real production use, you would need:

* A real database
* Strong secret key protection
* Token expiration management
* HTTPS
* Better validation and security controls

---

## How to Access the API

After running the server, you can open:

`http://localhost:8000/docs`

This page shows interactive API documentation where you can test register and login.

---

## Summary

This project is a simple authentication system that:

* Registers users
* Logs users in
* Generates secure tokens
* Stores data in a JSON file
* Records authentication history

It is a good example for beginners learning how authentication works in FastAPI.

I have face some errors:
1.the login endpoint is not work 
2. Authenticator is authenticate the user
3.Not save the login history
