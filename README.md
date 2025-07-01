# aaread

> **Note**: This `README.md` was generated with the help of AI and will be updated later once the application is fully developed.

---

# 📚 Flask Novel Reading Web App

This is a Flask-based web application browsing and reading novels with user authentication and admin features. Users can sign up, log in, and manage their personal library, while admin(me) have access to an upload section to manage novel content.

---

## 🚀 Features

- 🔐 User authentication (signup, login, logout)
- 🧑‍💻 Role-based access (admin vs regular users)
- 📖 View all novels (`/novels`)
- 📚 Personal library section (`/library`)
- 📤 File upload section for admins only (`/upload`)
- 🔔 Flash messages for error/success feedback
- 🗃️ SQLite database for storing user information

---

## 🛠 Tech Stack

- **Backend**: Python + Flask
- **Frontend**: HTML + Jinja2 + Bootstrap
- **Database**: SQLite
- **Session Management**: `flask-session`
- **Security**: `werkzeug.security` for password hashing

---

## 🧰 Requirements

- Python 3.x
- pip

### Install dependencies:

```bash
pip install -r requirements.txt

