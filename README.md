# EduPortal — E-Learning Management System

A Django-based e-learning platform with separate dashboards for teachers and students, built for managing courses, grades, and class routines.

## Features

- **Role-based authentication** — separate registration and login flow for Teachers and Students
- **Course management** — teachers create and manage courses; students browse and enroll
- **Grade tracking** — teachers record marks; students view only their own grades
- **Class routine** — weekly schedule per course, visible to enrolled students
- **Admin panel** — full CRUD access with search, filters, and list views for all models
- **Responsive UI** — built with Bootstrap 5 and custom styling

## Tech Stack

- Python 3.x
- Django 6.1
- SQLite (default database)
- Bootstrap 5 + Bootstrap Icons

## Models

- `User` (custom, extends AbstractUser) — with `role` field (teacher/student)
- `Course` — linked to a teacher via ForeignKey
- `Enrollment` — links students to courses
- `Grade` — student marks per course
- `Routine` — weekly class schedule per course

## Setup Instructions

1. **Clone the repository**
```bash
   git clone <repository-url>
   cd elearning_project
```

2. **Create and activate a virtual environment**
```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
```

3. **Install dependencies**
```bash
   pip install django
```

4. **Apply migrations**
```bash
   python manage.py migrate
```

5. **Create a superuser (for admin access)**
```bash
   python manage.py createsuperuser
```

6. **Run the development server**
```bash
   python manage.py runserver
```

7. **Open in browser**
http://127.0.0.1:8000

## Usage

- Register as a **Teacher** to create courses, add grades, and set routines.
- Register as a **Student** to enroll in courses, view grades, and check the class schedule.
- Access `/admin` with superuser credentials to manage all data directly.

## Team

- [Ghyalpo Lama] — Authentication, Course Management, Enrollment, UI Design, Grade Module, Routine Module, Dashboard Statistics

## Project Structure
elearning_project/
├── accounts/ # User model, authentication, dashboards
├── courses/ # Course, Enrollment, Grade, Routine
├── core/ # Project settings and URLs
├── templates/ # Shared templates (base, home)
└── manage.py