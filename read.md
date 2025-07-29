# Task Manager API (FastAPI + JWT Auth)

This is a simple asynchronous backend project built with FastAPI, using JWT authentication and SQLModel for ORM. It allows users to sign up, log in, and manage tasks securely via a RESTful API.

## How to Run the Project

0) Install dependencies:

```pip install -r requirements.txt```

1) Navigate to the backend directory:

```cd backend/api```

2) Run the FastAPI app using Uvicorn:

```uvicorn main:app --reload```

3) Use the API via Postman:

```https://web.postman.co/workspace/My-Workspace~4d7eaacc-c8db-4e5e-83bf-58084daff0f1/collection/21822809-ef43e245-2aea-4d80-b046-2b517a963be4?action=share&source=copy-link&creator=21822809```

4) Note:
- All CRUD operations for tasks require a Bearer token.
- If the token expires, call the login route again to get a new token and use it in the Authorization header like:

Authorization: Bearer <your_token>
