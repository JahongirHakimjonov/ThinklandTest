# ThinklandTest

A **Django + DRF + Elasticsearch** based project.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/JahongirHakimjonov/ThinklandTest.git
cd ThinklandTest
cp .env.example .env
```

### 2. Run with Docker (recommended)

```bash
docker compose up -d --build
```

This will start:

* Django app (`web`)
* PostgreSQL (`db`)
* Elasticsearch (`elasticsearch`)

Access the app at:
👉 [http://localhost:8000](http://localhost:8000)

### 3. Run this command in Docker container

Start PostgreSQL and Elasticsearch manually, then create a superuser:

```bash
python manage.py createsuperuser
```

### 4. Generate fake data

```bash
python manage.py generate_fake_data --categories 10 --products 100
```

### 5. Rebuild Elasticsearch index

```bash
python manage.py search_index --rebuild
```

---

## 📖 API Documentation

This project uses **DRF Spectacular** for OpenAPI docs.

* Swagger UI: [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)
* Redoc: [http://localhost:8000/api/schema/redoc/](http://localhost:8000/api/schema/redoc/)

---

## Test login and password

* username: jahongirhakimjonov@gmail.com
* password: 1253
* role: ADMIN

## 📦 Tech Stack

* **Backend**: Django, Django REST Framework
* **Search**: Elasticsearch
* **Database**: PostgreSQL
* **Docs**: DRF Spectacular
* **Containerization**: Docker & Docker Compose
