# BizConnect Directory Platform

A **production-ready Business Directory Platform** built with **FastAPI**, designed to efficiently manage and search **10M+ business records**. The platform emphasizes **high performance, scalability, secure authentication, and distributed backend architecture** for handling large-scale business data and concurrent user traffic.

---

##  Key Features

*  JWT Authentication & Authorization
*  Role-Based Access Control (Admin & User)
*  Fully Asynchronous FastAPI Architecture
*  Redis Caching with Smart Cache Invalidation
*  Redis-Based API Rate Limiting
*  Celery Background Workers
*  High-Performance Business Search
*  Pagination, Filtering & Sorting
*  PostgreSQL Query Optimization & Indexing
*  Database Connection Pooling
*  Dockerized Deployment
*  Clean, Modular & Scalable Architecture


#  Architecture Highlights

Designed as a scalable backend capable of handling millions of business records through:

* Distributed service architecture
* Async request handling
* Optimized PostgreSQL queries
* Redis caching layer
* Background task processing with Celery
* Secure authentication and authorization
* Efficient database connection pooling

---

#  Core Features

##  Authentication & Authorization

* User Registration & Login
* JWT Access Token Authentication
* Role-Based Access Control (RBAC)
* Dependency Injection for Protected Routes

---

##  Business Search

Designed for large-scale datasets with:

* Company Name Search
* Source-Based Search
* Advanced Filtering
* Pagination
* Sorting
* Optimized Query Execution

---

## Performance Optimization

Performance improvements include:

* PostgreSQL Indexing
* Query Optimization
* Minimal Data Fetching
* Database Connection Pooling
* Async Request Processing

Resulting in significantly faster API response times for large datasets.

---

## Redis Caching

Frequently requested business data is cached using Redis to reduce database load.

Features include:

* Cache Frequently Accessed Records
* Configurable TTL
* Smart Cache Invalidation
* Reduced Database Queries
* Faster Response Times

---

## Rate Limiting

Implemented Redis-based rate limiting to improve API stability and prevent abuse.

* Request Limiting
* Traffic Control
* Protection Against API Abuse

---

## Background Processing

Heavy operations are executed asynchronously using Celery workers.

Examples:

* Data Processing
* Cache Refresh
* Background Jobs
* Long Running Tasks

This keeps API responses fast and responsive.

---

# Database

* PostgreSQL
* Indexed Search Columns
* Optimized SQL Queries
* Foreign Key Relationships
* Connection Pooling
* Scalable Relational Schema

Designed to efficiently manage **10M+ business records**.

---

# API Endpoints

## Authentication

| Method | Endpoint             |
| ------ | -------------------- |
| POST   | `/user/registration` |
| POST   | `/user/login`        |
| GET    | `/user/is_auth`      |

---

## Business APIs

| Method | Endpoint                                   |
| ------ | ------------------------------------------ |
| GET    | `/business/yelp`                           |
| GET    | `/business/enroll`                         |
| GET    | `/business/word_of_mouth`                  |
| GET    | `/business/search/{company_name}`          |
| GET    | `/business/table/{table}/{company_name}`   |
| POST   | `/business/{source}/create`                |
| PUT    | `/business/{source}/{company_name}/update` |
| DELETE | `/business/{source}/{company_name}/del`    |

---

#  Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Pydantic
* Redis
* Celery
* JWT Authentication
* Docker
* Async/Await

---

# Run with Docker

```bash
docker-compose up --build
```

---

# Project Highlights

* Managed and searched **10M+ business records** efficiently.
* Implemented secure **JWT Authentication** with **Role-Based Access Control (RBAC)**.
* Built a high-performance search engine with filtering, sorting, and pagination.
* Improved response times using **Redis caching**, optimized database queries, and indexing.
* Increased scalability through **Celery background workers**, **Redis rate limiting**, and asynchronous FastAPI architecture.
* Designed a production-ready backend capable of handling high-volume concurrent traffic.
