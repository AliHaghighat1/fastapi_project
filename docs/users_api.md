# Users API Documentation

This document describes the **Users module** of the FastAPI backend project.

It demonstrates a simple CRUD-style API using an in-memory database.

---

## Base Endpoint


/users


---

## Data Model

Each user has the following structure:

```

---

# Data Model

Each user has the following structure:

```json
{
  "id": 1,
  "public_id": "550e8400-e29b-41d4-a716-446655440000",
  "first_name": "string",
  "last_name": "string",
  "gender": "male | female",
  "email": "user@example.com",
  "balance": 0.0,
  "is_active": true
}

```

---

## Features

- Get all users
- Search users (filters + partial search)
- Get single user by public_id (UUID)
- Create user (with duplicate email protection)
- Update user
- Delete user
- UUID-based public identification

---

## Email Validation

This project uses **Pydantic EmailStr** for validating email addresses.

### Why?

It ensures that all user emails:
- Are properly formatted
- Are valid email structures (e.g. contain `@` and domain)
- Prevent invalid data from entering the system

### How it is used

In the User model:

```email: EmailStr```

This automatically validates emails in:

- POST /users
- any request containing user data

---

## Get All Users (with filters + search)

### Request

```GET /users```

### Query Parameters

| Parameter  | Type    | Description               |
| ---------- | ------- | ------------------------- |
| first_name | string  | Partial match search      |
| last_name  | string  | Partial match search      |
| gender     | string  | Exact match (male/female) |
| email      | string  | Partial match search      |
| is_active  | boolean | Filter active users       |


---

### Examples

#### Get all users

```GET /users```

#### Filter by gender

```GET /users?gender=male```

#### Search by name

```GET /users?first_name=ali```

#### Search by email

```GET /users?email=gmail```

#### Combined filters

```GET /users?gender=female&is_active=true```


---


## Get Single User

### Request

```GET /users/{public_id}```

### Example

```GET /users/550e8400-e29b-41d4-a716-446655440000```

### Success Response

```{
  "id": 1,
  "public_id": "550e8400-e29b-41d4-a716-446655440000",
  "first_name": "Ali",
  "last_name": "Mohammadi",
  "gender": "male",
  "email": "ali@example.com",
  "balance": 120.5,
  "is_active": true
}```

### Error Response

```{
  "detail": "User not found"
}
```

---

## Create User

### Request

```POST /users```

### Body

```{
  "first_name": "John",
  "last_name": "Doe",
  "gender": "male",
  "email": "john@example.com",
  "balance": 100.5,
  "is_active": true
}
```

### Response

```{
  "id": 11,
  "public_id": "generated-uuid",
  "first_name": "John",
  "last_name": "Doe",
  "gender": "male",
  "email": "john@example.com",
  "balance": 100.5,
  "is_active": true
}
```

### Validation Rules

- Email must be unique
- Email format must be valid
- UUID is auto-generated
- ID is auto-incremented

---

## Update User

### Request

```PUT /users/{public_id}```

### Body

```{
  "first_name": "Updated",
  "last_name": "Name",
  "gender": "male",
  "email": "updated@example.com",
  "balance": 200,
  "is_active": true
}
```

### Response

Returns updated user object.

### Errors

- 404 → User not found
- 400 → Email already exists

---

## Delete User

### Request

```DELETE /users/{public_id}```

### Response

```{
  "message": "User deleted successfully"
}
```

---

## Architecture

- FastAPI → API layer
- SQLAlchemy → ORM
- MariaDB → Database
- UUID → Public identifiers
- Pydantic → Validation

---

## Security Design

- Internal ID (auto-increment) is NOT exposed
- Public ID uses UUID
- Email is unique
- Validation enforced at API level

---

## Summary

| Method | Endpoint           | Description     |
| ------ | ------------------ | --------------- |
| GET    | /users             | List + search   |
| GET    | /users/{public_id} | Get single user |
| POST   | /users             | Create user     |
| PUT    | /users/{public_id} | Update user     |
| DELETE | /users/{public_id} | Delete user     |

---

## Dependencies

This Users API uses the following main dependencies:

### FastAPI

```fastapi
uvicorn
```
Used to build and run the REST API.

#### Database ORM

```sqlalchemy
pymysql
```

Used to connect and interact with MariaDB using Python objects instead of raw SQL.

### Data Validation

```pydantic```

Used for request and response validation (UserCreate, UserResponse).

### Email Validation

To validate user email addresses:

```pip install "pydantic[email]"```

or:

```pip install email-validator```

Used for validating EmailStr fields.

### Environment Variables
```python-dotenv```

Used to load database credentials from .env.

---

## Installation

Install dependencies from the project root:

```bash
pip install -r requirements.txt
```
