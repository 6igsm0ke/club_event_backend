# 🎉 ClubEvent Backend

ClubEvent Backend is the backend service for the ClubEvent app, built using Django, Django REST Framework, and Django Channels. It handles users, events, clubs, and provides WebSocket-based chat functionality.
> ⚠️ This project is configured to run locally only. For deployment, additional setup is required.
---

## 📦 Tech Stack

* **Django 5.1.5** — main web framework
* **Django REST Framework** — for RESTful APIs
* **SQLite** — default database
* **JWT (djangorestframework-simplejwt)** — authentication
* **Django Channels + Redis** — for WebSocket chat
* **Pillow** — image processing
* **Decouple** — for environment variables

---

## 📁 API Modules

| Endpoint          | Description                         |
| ----------------- | ----------------------------------- |
| `/api/v1/auth/`   | Registration, login, profile, roles |
| `/api/v1/events/` | Event creation and management       |
| `/api/v1/clubs/`  | Club browsing and member management |
| `/api/v1/chat/`   | WebSocket-based real-time chat      |

---

#🔗 Related Repository
This backend project works together with the frontend: 👉 [ClubEvent Frontend Repository](https://github.com/6igsm0ke/club_event_frontend)

## 🚀 Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/6igsm0ke/club_event_backend.git
cd club_event_backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Redis via Docker

```bash
docker run --rm -p 6379:6379 redis:7
```

### 5. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver 0.0.0.0:8000
```

---

## 🌐 WebSocket Chat

The chat system uses Django Channels and Redis. Connect via:

```
ws://<host>/ws/chat/lobby/
```

---

## 🔐 Environment Variables

Use a `.env.local` file in your project root. Example:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_USE_TLS=True
EMAIL_HOST=smtp.example.com
EMAIL_HOST_USER=your@example.com
EMAIL_HOST_PASSWORD=yourpassword
EMAIL_PORT=587
```

---

## 🖼️ Media Files

Uploaded media (e.g. images) are stored in the `/media/` directory.

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 📬 Feedback

Feel free to open [Issues](https://github.com/your-6igsm0k3/club_event_backend/issues) or submit a Pull Request.

---

**License:** MIT
