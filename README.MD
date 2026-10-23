# JobTrack — Job Application Tracker

JobTrack is a web-based job application tracking and placement analytics platform that helps users organize job applications and monitor their job search progress in one place.

## Features

- Add job applications with company name, role, status, and application date.
- View all saved applications in a dashboard.
- Update application details and status.
- Delete applications.
- Track application statistics and interview/offer progress.
- REST API built with FastAPI.
- Persistent data storage using MySQL.

## Tech Stack

**Backend:** Python, FastAPI, SQLAlchemy, Pydantic  
**Database:** MySQL  
**Frontend:** HTML, CSS, JavaScript  
**Deployment:** Render  
**API Testing:** Swagger UI

## Live Demo

- **Frontend:** https://jobtrack-frontend-fpi7.onrender.com
- **Backend API:** https://jobtrack-api-9elj.onrender.com
- **API Documentation:** https://jobtrack-api-9elj.onrender.com/docs

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Adityaaa29-coder/JobTrack.git
cd JobTrack
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=jobtrack_db
```

Use your own MySQL credentials. Never commit your `.env` file or expose database passwords.

### 5. Create database tables

Make sure MySQL is running and the `jobtrack_db` database exists, then run:

```bash
python create_tables.py
```

### 6. Start the backend

```bash
uvicorn app.main:app --reload
```

Open the API documentation at http://127.0.0.1:8000/docs.

To run the frontend locally, serve the `Frontend` folder using VS Code Live Server.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check API health |
| POST | `/applications` | Create an application |
| GET | `/applications` | List applications |
| PATCH | `/applications/{application_id}` | Update an application |
| DELETE | `/applications/{application_id}` | Delete an application |
| GET | `/analytics` | Retrieve application statistics |

## Learning Outcomes

- Building REST APIs with FastAPI.
- Using SQLAlchemy to interact with MySQL.
- Implementing CRUD operations.
- Validating requests with Pydantic.
- Connecting a JavaScript frontend to a backend API.
- Configuring environment variables and deploying a web application.

## Future Improvements

- User authentication and individual user dashboards.
- Advanced filtering and analytics.
- Automated reminders for application follow-ups.

---

**Note:** This is a learning project built to practice backend development, database integration, and full-stack application deployment.