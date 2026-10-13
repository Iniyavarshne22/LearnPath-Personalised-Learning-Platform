# LearnPath – Personalised Learning Platform

A web-based learning platform that helps students follow career-oriented learning roadmaps, track their learning progress, and assess their skills.

## Overview

LearnPath is a Python Flask and MySQL web application designed to help students organize their learning based on their selected career goals. Students can create accounts, access a personalized learning roadmap, mark topics as completed, and evaluate their skills through assessments.

## Features

- **Student Registration and Login:** Create an account and securely log in.
- **Password Hashing:** Store password hashes instead of plain-text passwords.
- **Personalized Learning Roadmaps:** Display learning topics based on the selected career goal.
- **Learning Progress Tracking:** Mark roadmap topics as completed and monitor overall progress.
- **Skill Assessment:** Submit self-assessment scores for relevant technical skills.
- **Assessment Results:** View scores and learning recommendations.
- **Database Integration:** Store student accounts, assessment results, and learning progress in MySQL.
- **Responsive User Interface:** Access the application through a web browser.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application programming |
| Flask | Web framework and routing |
| MySQL | Relational database |
| mysql-connector-python | Python–MySQL connectivity |
| Flask-Bcrypt | Password hashing |
| HTML5 | Page structure |
| CSS3 | Styling and responsive layouts |
| JavaScript | Client-side interactions |
| Git and GitHub | Version control and source-code hosting |

## Application Modules

### 1. User Authentication
Allows students to register and log in using their credentials.

### 2. Personalized Roadmap
Provides learning topics based on the student's selected career goal, such as Python Developer, Java Developer, or Full-Stack Developer.

### 3. Progress Tracking
Allows students to mark completed learning topics and view their overall progress.

### 4. Skill Assessment
Collects self-assessment scores and calculates an overall assessment score.

### 5. Results and Recommendations
Displays the latest assessment results and suggests areas for improvement.

## Project Structure

```text
Personalised Learning Platform/
├── app.py
├── db.py
├── test_db.py
├── requirements.txt
├── .gitignore
├── README.md
└── templates/
    ├── index.html
    ├── register.html
    ├── login.html
    ├── dashboard.html
    ├── assessment.html
    └── assessment_result.html
```

## Prerequisites

Before running the application, install:

- Python 3
- MySQL Server
- Git (optional, for cloning the repository)

## Installation and Setup

### 1. Clone the repository

Replace `YOUR-USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR-USERNAME/LearnPath-Personalised-Learning-Platform.git
cd LearnPath-Personalised-Learning-Platform
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure MySQL

Create a database named `learnpath_db` in MySQL.

Create the required tables for students, assessments, and learning progress using the SQL schema provided with the project.

### 5. Configure environment variables

Create a local `.env` file in the project root. Configure the database connection values expected by `db.py`.

Example:

```text
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_local_mysql_password
DB_NAME=learnpath_db
```

Use your own local MySQL credentials. Never commit `.env` or real passwords to GitHub.

### 6. Run the application

```bash
python app.py
```

Open the following address in your browser:

http://127.0.0.1:5000

## Testing

Manually test the following workflows:

- Student registration and login
- Personalized roadmap display
- Learning progress updates
- Skill assessment submission
- Assessment result display
- Logout functionality
- Database persistence

The `test_db.py` file can be used to check database connectivity.

## Security Notes

- Passwords should be stored using a password-hashing mechanism.
- Database credentials should be kept in environment variables.
- Production deployments should use a strong secret key and disable Flask debug mode.
- Validate user inputs and handle database errors appropriately.

## Future Enhancements

- Adaptive recommendations based on learning history
- Visual analytics for learning progress
- Additional career roadmaps and assessments
- Deployment to a cloud hosting platform

## Project Status

Developed as a student portfolio project.

## Author

**Iniyavarshne A**

GitHub: https://github.com/Iniyavarshne22
