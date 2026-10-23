# Lab Equipment Booking System

## Project Overview

The Lab Equipment Booking System is a web-based application developed using Flask and Python to manage shared laboratory equipment bookings.

It helps users view available equipment and manage booking requests in an organized way.

## Features

- User accounts and login
- Equipment catalogue
- Equipment availability management
- Booking requests
- Database-backed equipment records
- Automated testing using pytest

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML and CSS
- pytest
- Ruff

## Installation

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install the required dependencies.
4. Run the application.

```bash
git clone https://github.com/nirmanijayakodi0-afk/lab-equipment-booking.git
cd lab-equipment-booking
python -m venv .venv
```

Activate the environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install flask flask-sqlalchemy pytest pytest-cov ruff
```

Run the application:

```bash
python app.py
```

## Testing

Run automated tests:

```bash
python -m pytest -v
```

Run code quality checks:

```bash
ruff check .
```

## Project Status

The system is being developed incrementally, with accounts and login, the equipment catalogue, and booking requests as key development priorities.