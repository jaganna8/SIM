### Student Information Management System ###
# A web-based management systems designed for teachers and administrators of a school district to quickly view, manage, and analyze student data across multiple schools
# Built with Flask (Python), MySQL, and HTML/CSS/JS
# Provides secure, role-based access

### Features ###
# User Roles
    # Teachers:
        # View all students across schools
        # Access individual student details (attendance, classes, grades)
        # Search specific students
    # Admin
        # All teacher privileges
        # Add new students, teachers, and classes
        # Manage system wide data

# Pages
    # Student Dashboard
        # Displays an overview of all students and their demographic Information
        # Highlights students of concern (e.g. Low GPA)
        # Ability to filter by grade, school, etc.
        # Allows navigation to a detailed student profile page upon clicking on a student row
    # Student Detail Page
        # Displays attendance records, class enrollments and drops, and academic performance


### Tech Stack ###
# Frontend - HTML/CSS/JS
# Backend - Flask (Python)
# Database - MySQL
# Containerization - Docker + Docker Compose

### Structure ###
project/
│
├── app.py                 # Main Flask application
├── templates/             # HTML templates (Jinja2)
├── static/                # CSS and JS files
├── database/              # SQL scripts, initialization, or models
├── Dockerfile             # Flask app container setup
├── docker-compose.yml     # Multi-container configuration (Flask + MySQL)
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

### Running the project with Docker ###
1. Clone the repository
    git clone https://github.com/jaganna8/SIM.git
2. Build and Start the containers
    docker-compose up --Build
3. Access the application
    http://localhost:8080


### Future Improvements ###
# Add data visualization (GPA trends, attendance patterns, etc.)
# Add tools for logging attendance and final grades for teachers
# Add other elements of concern to be highlighted (low number of credits for grade level, etc.)
# Make CSS cohesive across all pages