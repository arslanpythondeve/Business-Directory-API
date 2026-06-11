# 🚀 Business Directory API

A scalable and production-ready Business Directory API built with FastAPI.  
This project focuses on **performance optimization, secure authentication, caching, and scalable backend architecture**.

---

## 📌 Features

- 🔐 JWT Authentication
- 👥 Role-Based Access Control (Admin & User)
- ⚡ Async FastAPI architecture
- 🧠 Redis caching for high-speed responses
- 🚦 Rate limiting using Redis
- ⚙️ Celery background workers
- 📊 Pagination, filtering, and sorting
- 🔎 Search API for business data
- 🗄️ PostgreSQL with indexing and query optimization
- 🔄 Connection pooling for database efficiency
- 🧹 Clean and modular architecture

---

## 🏗️ Tech Stack

FastAPI, PostgreSQL, SQLAlchemy, Pydantic, Redis, Celery, JWT, Docker, Async/Await

---

## 🔐 Authentication

- User registration and login system
- JWT token-based authentication
- Admin and User role separation
- Protected routes using dependency injection

---

## ⚡ Performance Optimization

- Database connection pooling
- Indexing for faster query execution
- Query optimization (minimal data fetching)
- Efficient ORM usage

---

## 🧠 Caching Strategy

- Redis used for caching frequently accessed data
- Reduced database load significantly
- Cache expiration (TTL) implemented
- Smart cache invalidation on updates

---

## 🚦 Rate Limiting

- Redis-based rate limiting system
- Prevents API abuse
- Adds delay under high request load

---

## ⚙️ Background Tasks

- Celery workers for async background processing
- Improves API responsiveness
- Handles heavy tasks outside main request cycle

---

## 📂 API Endpoints

### User APIs
- POST `/user/registration`
- POST `/user/login`
- GET `/user/is_auth`

### Business APIs
- GET `/business/yelp`
- GET `/business/enroll`
- GET `/business/word_of_mouth`
- GET `/business/search/{company_name}`
- GET `/business/table/{table}/{company_name}`
- POST `/business/{source}/create`
- PUT `/business/{source}/{company_name}/update`
- DELETE `/business/{source}/{company_name}/del`

---

## 📊 Database Features

- PostgreSQL relational schema
- Indexed columns for faster search
- Foreign key relationships
- Optimized query execution

---

## 🐳 Run with Docker

```bash
docker-compose up --build