# FastAPI Backend Project

A modern, scalable FastAPI backend starter template.

## Project Structure

```
fastapi_project/
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration and settings
│   ├── routes/                # API route handlers
│   │   ├── __init__.py
│   │   └── health.py          # Health check endpoints
│   └── models/                # Data models and schemas
│       ├── __init__.py
│       └── schemas.py         # Pydantic models
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── install_requirements.md    # Installation guide
└── README.md                  # This file
```

## Prerequisites

- Python 3.12
- UV (Python package manager) - See `install_requirements.md` for installation

## Installation

1. **Follow the Python 3.12 + UV installation guide:**
   ```bash
   cat install_requirements.md
   ```

2. **Create a virtual environment:**
   ```bash
   uv venv --python 3.12
   ```

3. **Activate the virtual environment:**
   ```bash
   # macOS/Linux
   source .venv/bin/activate
   
   # Windows
   .venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```

5. **Create environment file:**
   ```bash
   cp .env
   ```

### note:

Windows File Explorer does not let you name files starting with a dot, use a code editor or the command line to create it.

#### Using VS Code:

- Open your project folder in VS Code.
- Click the New File icon in the Explorer panel.
- Name the file exactly: .env 

#### Using Command Prompt:

- Open the Command Prompt or PowerShell.
- Go to your project folder using the cd command (e.g., cd C:\Users\Name\Projects\MyProject).
- Type echo. > .env and press Enter.

## Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

**Interactive API documentation:** `http://localhost:8000/docs` (Swagger UI)
**Alternative documentation:** `http://localhost:8000/redoc` (ReDoc)

## Health Check

Test the API is running:
```bash
curl http://localhost:8000/health
```

## Development Workflow

1. Create new routes in `app/routes/`
2. Define data models in `app/models/schemas.py`
3. Import and include routers in `main.py`
4. Test using the interactive API docs or curl

## Adding New Endpoints

Example: Creating a new `users` router

1. **Create `app/routes/users.py`:**
   ```python
   from fastapi import APIRouter
   
   router = APIRouter(
       prefix="/users",
       tags=["users"]
   )
   
   @router.get("/")
   def get_users():
       return {"users": []}
   ```

2. **Include in `main.py`:**
   ```python
   from app.routes import users
   app.include_router(users.router)
   ```

## Sample API Documentation

- Users API → docs/users_api.md

## Environment Variables

Configure the application using the `.env` file. See `.env.example` for available options.

## Next Steps

- Add more routes in `app/routes/`
- Define your data models in `app/models/schemas.py`
- Configure database connection when needed
- Add request validation and error handling
- Implement authentication/authorization as needed

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
