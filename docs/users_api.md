# Users API Documentation

This document describes the **Users module** of the FastAPI backend project.

It demonstrates a simple CRUD-style API using an in-memory database.

---

## Base Endpoint


/users


---

## Data Model

Each user has the following structure:

```json id="model1"
{
  "id": 1,
  "first_name": "string",
  "last_name": "string",
  "gender": "male | female",
  "email": "user@example.com",
  "balance": 0.0,
  "is_active": true
}

```

## Get All Users

Returns all users in the system.

### Request

```GET /users```

## Filtering Users

You can filter users using query parameters:

### By gender
```GET /users?gender=male```

### By active status
```GET /users?is_active=true```

### Combined filters
```GET /users?gender=female&is_active=true```


## Get Single User

Retrieve a specific user by ID.

```GET /users/{id}```

### Example Request
```GET /users/1```

### Success Response

```
{
  "id": 1,
  "first_name": "Ali",
  "last_name": "Mohammadi",
  "gender": "male",
  "email": "ali@example.com",
  "balance": 120.5,
  "is_active": true
}
```

### Error Response (User Not Found)

```
{
  "detail": "User not found"
}
```

## Create User

Create a new user in the system.

```POST /users```

### Request Body

```
{
  "first_name": "John",
  "last_name": "Doe",
  "gender": "male",
  "email": "john@example.com",
  "balance": 100.5,
  "is_active": true
}
```

### Response

```
{
  "id": 11,
  "first_name": "John",
  "last_name": "Doe",
  "gender": "male",
  "email": "john@example.com",
  "balance": 100.5,
  "is_active": true
}
```

## Auto ID Generation

When creating a new user:

- The system automatically assigns an ID
- ID = (highest existing ID + 1)
- Ensures uniqueness without a database

### Example:

- Existing IDs: 1 → 10
- New user ID: 11

## Summary

| Method | Endpoint            | Description      |
| ------ | ------------------- | ---------------- |
| GET    | `/users`            | Get all users    |
| GET    | `/users/{id}`       | Get single user  |
| POST   | `/users`            | Create user      |
| GET    | `/users?gender=`    | Filter by gender |
| GET    | `/users?is_active=` | Filter by status |
