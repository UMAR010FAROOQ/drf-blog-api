# DRF Blog API 🚀

![Django CI](https://github.com/UMAR010FAROOQ/drf-blog-api/actions/workflows/django.yml/badge.svg)

> A production-oriented Blog REST API built with Django REST Framework — featuring JWT authentication, service-layer architecture, nested comments, API versioning, and automated testing.

---

## ✨ Features

- ✅ API Versioning (`/api/v1/`)
- 🔐 JWT Authentication (Login + Refresh)
- 🛡️ Permission-based Access Control
- 📝 Blog Posts CRUD with filtering, search & ordering
- 💬 Nested Comment System (threaded replies)
- ♻️ Soft Delete (no permanent data loss)
- 🧠 Service Layer Architecture
- 📦 Custom Consistent API Response Format
- ⚡ Query Optimization (`select_related`, `prefetch_related`)
- 🧪 Automated API Testing
- 🚀 CI Pipeline (GitHub Actions)
- 📘 Swagger API Documentation (drf-spectacular)

---

## ⚙️ Tech Stack

| Category | Technology |
|---|---|
| Backend | Django, Django REST Framework |
| Auth | SimpleJWT |
| Database | SQLite (dev) / PostgreSQL (prod) |
| API Docs | drf-spectacular (Swagger UI) |
| Testing | Django APITestCase |
| CI/CD | GitHub Actions |

---

## 🚀 Local Setup

```bash
git clone https://github.com/UMAR010FAROOQ/drf-blog-api.git
cd drf-blog-api
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🔐 Authentication

JWT-based authentication:

| Endpoint | Method | Description |
|---|---|---|
| `/api/auth/login/` | POST | Get access + refresh token |
| `/api/auth/refresh/` | POST | Refresh access token |

**Header format:**
Authorization: Bearer <access_token>

---

## 📌 API Endpoints

**Base URL:** `/api/v1/`

| Endpoint | Method | Description |
|---|---|---|
| `/posts/` | GET | List all posts |
| `/posts/` | POST | Create a post |
| `/posts/{id}/` | GET | Get single post |
| `/posts/{id}/` | PUT | Update post |
| `/posts/{id}/` | DELETE | Soft delete post |
| `/posts/my_posts/` | GET | Current user's posts |
| `/posts/{id}/comments/` | GET | Post comments |
| `/comments/` | POST | Add comment / reply |

---

## 📘 API Documentation

Swagger UI available at:
http://localhost:8000/api/docs/

---

## 🧪 Testing

```bash
python manage.py test
```

Covers: endpoint testing, authentication, permission validation.

---

## 🧠 Architecture Decisions

**Service Layer** — business logic separated from views for maintainability and testability.

**Soft Delete** — records marked inactive instead of permanently deleted, allowing data recovery.

**API Versioning** — all routes under `/api/v1/` ensuring backward compatibility.

**Query Optimization** — `select_related` and `prefetch_related` used throughout to minimize DB hits.

---

## 📦 Example Request

```json
POST /api/v1/posts/
{
  "title": "My First Post",
  "content": "Content here...",
  "is_published": true,
  "category_ids": [1]
}
```

---

## 👨‍💻 Author

**Umar Farooq** — Backend Developer (Django / DRF)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/umar-farooq-developer)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/UMAR010FAROOQ)
