```markdown
# 📊 ResourceOptima

**ResourceOptima** is a Django-based project for managing resources, tasks, and assignments under managers and projects. It includes a REST API for CRUD operations, intelligent task allocation based on resource skills and availability, and modular app separation for clarity and scalability.

---

## 🚀 Features

- CRUD APIs for:
  - Managers
  - Resources
  - Skills
  - Projects
  - Tasks
  - Resource Availabilities
- Automatic task-to-resource assignment based on skill matching and availability
- REST API powered by Django REST Framework
- Support for nested routes with `drf-nested-routers`
- Auto-generated API schema with `drf-spectacular`
- Dockerized deployment setup

---

## 🗂️ Project Structure

```

.
├── docker/                      # Docker setup
│   └── scripts/                 # Startup scripts
├── docker-compose.yaml         # Docker orchestration
├── scripts/                    # Initialization scripts for sample data
├── src/
│   ├── api/                    # Core API app
│   │   ├── common/             # Shared models/utilities
│   │   └── v1/                 # Versioned API (v1)
│   │       ├── manager/        # Manager-specific APIs
│   │       ├── project/        # Project-specific APIs
│   │       ├── resource/       # Resource-specific APIs
│   │       └── urls.py         # API routing
│   ├── app/                    # Django settings and WSGI entrypoints
│   ├── cmds/                   # Custom management commands
│   ├── manage.py               # Django CLI entrypoint
│   └── requirements.txt        # Python dependencies

````

---

## ⚙️ Setup Instructions

### 1️⃣ Prerequisites

- Docker + Docker Compose
- Python 3.9+ (if running locally without Docker)
- PostgreSQL

### 2️⃣ Running with Docker

```bash
# Build and start all services
docker-compose up --build
````

### 3️⃣ Apply Migrations & Seed Data

In a new terminal:

```bash
docker exec -it <web_container_name> bash

# Inside container
python manage.py migrate
python manage.py initapp        # Custom command to initialize core setup
python manage.py createsuperuser
```

### 4️⃣ API Access

* Base URL: `http://localhost:8000/api/v1/`
* Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
* Redoc: `http://localhost:8000/api/schema/redoc/`

---

## 📌 Key API Example: Assigning Tasks

```http
POST /api/v1/projects/<project_id>/assign_tasks/
```

* Automatically assigns tasks to suitable resources
* Matching is based on required skills and resource availability

---

## 🔧 Tech Stack

* Django 4.2
* Django REST Framework
* PostgreSQL
* Gunicorn
* Docker
* drf-spectacular (for schema generation)

---

## 💡 Todo / Future Improvements

* Add filtering and search to list endpoints
* Implement pagination and rate limiting
* Build frontend dashboard (React/Vue)

```
