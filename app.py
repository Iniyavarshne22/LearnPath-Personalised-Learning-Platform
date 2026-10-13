
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session
from db import get_db_connection
from flask_bcrypt import Bcrypt
import mysql.connector

app = Flask(__name__)
app.secret_key = "learnpath-dev-key-change-later"

bcrypt = Bcrypt(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        career_goal = request.form.get("career_goal", "")

        if not name or not email or len(password) < 8 or not career_goal:
            flash("Please fill in all fields correctly.")
            return redirect(url_for("register"))

        password_hash = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute(
                """INSERT INTO students
                   (name, email, password_hash, career_goal)
                   VALUES (%s, %s, %s, %s)""",
                (name, email, password_hash, career_goal)
            )
            connection.commit()

            flash("Registration successful! You can now log in.")
            return redirect(url_for("register"))

        except mysql.connector.IntegrityError:
            flash("This email is already registered.")

        except mysql.connector.Error as error:
            app.logger.error("Database error: %s", error)
            flash("Unable to save your account. Please try again.")

        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM students WHERE email = %s",
                (email,)
            )
            student = cursor.fetchone()

            if student and bcrypt.check_password_hash(
                student["password_hash"], password
            ):
                session["student_id"] = student["id"]
                session["student_name"] = student["name"]
                return redirect(url_for("dashboard"))

            flash("Invalid email or password.")

        except mysql.connector.Error:
            app.logger.exception("Login database error")
            flash("Unable to log in right now. Please try again.")

        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None and connection.is_connected():
                connection.close()

    return render_template("login.html")



@app.route("/dashboard")
def dashboard():
    if "student_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """SELECT id, name, email, career_goal
               FROM students WHERE id = %s""",
            (session["student_id"],)
        )
        student = cursor.fetchone()

        if not student:
            session.clear()
            return redirect(url_for("login"))

        if student["career_goal"] == "Python Developer":
            roadmap = [
                "Python Fundamentals",
                "Data Structures and Algorithms",
                "Object-Oriented Programming",
                "SQL and MySQL",
                "Flask Web Development",
                "Build a Python Project"
            ]

        elif student["career_goal"] == "Java Developer":
            roadmap = [
                "Java Fundamentals",
                "Object-Oriented Programming",
                "Data Structures and Algorithms",
                "SQL and MySQL",
                "Java Application Development",
                "Build a Java Project"
            ]

        else:
            roadmap = [
                "HTML and CSS",
                "JavaScript Fundamentals",
                "Python or JavaScript Programming",
                "React Fundamentals",
                "Backend Development with Flask",
                "SQL and MySQL",
                "Build a Full-Stack Project"
            ]

        progress = 0

        return render_template(
            "dashboard.html",
            student=student,
            roadmap=roadmap,
            progress=progress
        )

    except mysql.connector.Error:
        app.logger.exception("Dashboard database error")
        return "Unable to load your dashboard. Please try again later.", 500

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/assessment", methods=["GET", "POST"])
def assessment():
    if "student_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            python_score = int(request.form.get("python_score", -1))
            sql_score = int(request.form.get("sql_score", -1))
            problem_score = int(
                request.form.get("problem_solving_score", -1)
            )

            if any(score not in range(4) for score in
                   [python_score, sql_score, problem_score]):
                flash("Please select valid skill levels.")
                return redirect(url_for("assessment"))

            total_score = python_score + sql_score + problem_score

            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute(
                """INSERT INTO assessments
                (student_id, python_score, sql_score,
                 problem_solving_score, total_score)
                VALUES (%s, %s, %s, %s, %s)""",
                (
                    session["student_id"],
                    python_score,
                    sql_score,
                    problem_score,
                    total_score
                )
            )
            connection.commit()

            cursor.close()
            connection.close()

            flash(f"Assessment saved! Your score is {total_score}/9.")
            return redirect(url_for("assessment_result"))

        except (ValueError, mysql.connector.Error):
            app.logger.exception("Assessment submission failed")
            flash("Unable to save your assessment. Please try again.")
            return redirect(url_for("assessment"))

    return render_template("assessment.html")


@app.route("/assessment-result")
def assessment_result():
    if "student_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """SELECT python_score, sql_score,
                      problem_solving_score, total_score, created_at
               FROM assessments
               WHERE student_id = %s
               ORDER BY id DESC LIMIT 1""",
            (session["student_id"],)
        )
        result = cursor.fetchone()

        if not result:
            return redirect(url_for("assessment"))

        return render_template("assessment_result.html", result=result)

    except mysql.connector.Error:
        app.logger.exception("Could not load assessment result")
        return "Unable to load assessment results.", 500

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


@app.route("/learning-progress", methods=["POST"])
def update_learning_progress():
    if "student_id" not in session:
        return redirect(url_for("login"))

    topic = request.form.get("topic", "").strip()
    completed = request.form.get("completed") == "yes"

    # Only allow topics belonging to the student's roadmap.
    career_goal = None
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT career_goal FROM students WHERE id = %s",
            (session["student_id"],)
        )
        student = cursor.fetchone()

        if not student:
            session.clear()
            return redirect(url_for("login"))

        career_goal = student["career_goal"]

        if career_goal == "Python Developer":
            allowed_topics = [
                "Python Fundamentals",
                "Data Structures and Algorithms",
                "Object-Oriented Programming",
                "SQL and MySQL",
                "Flask Web Development",
                "Build a Python Project"
            ]
        elif career_goal == "Java Developer":
            allowed_topics = [
                "Java Fundamentals",
                "Object-Oriented Programming",
                "Data Structures and Algorithms",
                "SQL and MySQL",
                "Java Application Development",
                "Build a Java Project"
            ]
        else:
            allowed_topics = [
                "HTML and CSS",
                "JavaScript Fundamentals",
                "Python or JavaScript Programming",
                "React Fundamentals",
                "Backend Development with Flask",
                "SQL and MySQL",
                "Build a Full-Stack Project"
            ]

        if topic not in allowed_topics:
            flash("Invalid roadmap topic.")
            return redirect(url_for("dashboard"))

        cursor.execute(
            """
            INSERT INTO learning_progress (student_id, topic, completed)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE completed = VALUES(completed)
            """,
            (session["student_id"], topic, completed)
        )
        connection.commit()

        flash("Learning progress updated successfully!")

    except mysql.connector.Error:
        app.logger.exception("Could not update learning progress")
        flash("Unable to update progress. Please try again.")

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
