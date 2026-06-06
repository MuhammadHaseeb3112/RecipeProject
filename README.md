# Recipe Project 🍽️

A feature-rich Recipe Sharing Web Application built with Django that allows users to discover, create, manage, and share recipes with others. The platform includes user authentication, recipe management, favorites, profiles, categories, and a modern responsive interface.

---

## Features

### User Authentication

* User Registration
* User Login & Logout
* Password Reset System
* Password Change Functionality
* User Profiles

### Recipe Management

* Create Recipes
* Edit Recipes
* Delete Recipes
* View Recipe Details
* Browse All Recipes
* Personal Recipe Dashboard

### Community Features

* Favorite Recipes
* Recipe Categories
* Recipe Views Counter
* User Recipe Collection

### Pages Included

* Home Page
* Recipes Page
* Recipe Detail Page
* Submit Recipe Page
* Profile Page
* My Recipes Page
* About Page
* Authentication Pages

### Security Features

* Authentication Protected Views
* User Ownership Validation
* Secure Form Handling
* CSRF Protection

---

## Tech Stack

### Backend

* Python
* Django 5

### Frontend

* HTML5
* CSS3
* Bootstrap
* Django Templates

### Database

* SQLite

### Authentication

* Django Authentication System

---

## Project Structure

```text
RecipeProject/
│
├── RecipeApp/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── templatetags/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
│
├── RecipeProject/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   └── registration/
│
├── manage.py
└── requirements.txt
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/MuhammadHaseeb3112/RecipeProject.git
cd RecipeProject
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Run Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Admin Panel:

```text
http://127.0.0.1:8000/admin/
```

---

## Screenshots

Add screenshots of:

* Home Page
* Recipe Listing Page
* Recipe Detail Page
* Submit Recipe Page
* User Profile
* Login Page
* My Recipes Page

---

## Key Learning Concepts

This project demonstrates:

* Django Models
* Django Forms
* Authentication & Authorization
* CRUD Operations
* Template Inheritance
* Custom Template Tags
* URL Routing
* Class-Based and Function-Based Views
* Database Relationships
* User Profile Management
* Secure Web Development

---

## Future Improvements

* Django REST Framework API
* Recipe Rating System
* Recipe Comments
* Recipe Search & Filtering
* Recipe Recommendations
* JWT Authentication
* Redis Caching
* Docker Deployment
* PostgreSQL Integration
* Image Optimization

---

## Author

**Muhammad Haseeb**

GitHub:
https://github.com/MuhammadHaseeb3112

---

## License

This project is created for educational, learning, and portfolio purposes.
