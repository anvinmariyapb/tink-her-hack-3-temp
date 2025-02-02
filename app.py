from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash  # For password hashing
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

# ==============================
# 🔹 MySQL Database Connection
# ==============================
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='anvin',  # Your MySQL username
            password='Anvin@2001',  # Your MySQL password
            database='home_fix',  # Your database name
            port=3306
        )
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

# ==============================
# 🔹 Home Route
# ==============================
@app.route('/')
def home():
    return render_template('index.html')

# ==============================
# 🔹 Services Route (Fetching from MySQL)
# ==============================
@app.route('/services', methods=['GET', 'POST'])
def services():
    connection = get_db_connection()
    if connection is None:
        flash("Database connection failed. Please try again later.", "error")
        return render_template('services.html', services=[])

    category = request.form.get("category", "all")

    with connection.cursor(dictionary=True) as cursor:
        if category == "all":
            cursor.execute("SELECT * FROM services")
        else:
            cursor.execute("SELECT * FROM services WHERE category = %s", (category,))
        services = cursor.fetchall()

    connection.close()
    return render_template('services.html', services=services, selected_category=category)

# ==============================
# 🔹 Contact Route (Saving Messages to DB)
# ==============================
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    connection = get_db_connection()
    if connection is None:
        flash("Database connection failed.", "error")
        return render_template('contact.html', contacts=[])

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
            connection.commit()
        
        flash("Message sent successfully!", "success")
        return redirect(url_for('contact'))

    with connection.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM contacts ORDER BY id DESC")
        contacts = cursor.fetchall()

    connection.close()
    return render_template('contact.html', contacts=contacts)

# ==============================
# 🔹 User Registration Route
# ==============================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Password Validation
        if len(password) < 8 or not any(char.isupper() for char in password) or not any(char.islower() for char in password) or not any(char.isdigit() for char in password) or not any(char in "!@#$%^&*()" for char in password):
            flash("Password must be at least 8 characters, contain an uppercase, lowercase, number, and special character.", "error")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        connection = get_db_connection()
        if connection is None:
            flash("Database connection failed.", "error")
            return redirect(url_for('register'))

        with connection.cursor(dictionary=True) as cursor:
            # Check if username already exists
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                flash("Username already exists. Choose another one.", "error")
                return redirect(url_for('register'))

            # Insert user
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            connection.commit()

        connection.close()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# ==============================
# 🔹 User Login Route
# ==============================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        if connection is None:
            flash("Database connection failed. Please try again later.", "error")
            return redirect(url_for('login'))

        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

        connection.close()

        if user and check_password_hash(user["password"], password):
            session['username'] = username
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password", "error")

    return render_template('login.html')

# ==============================
# 🔹 User Dashboard Route (Protected)
# ==============================
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash("Please log in first.", "error")
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

# ==============================
# 🔹 User Logout Route
# ==============================
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))


@app.route('/service/<int:service_id>')
def service_detail(service_id):
    connection = get_db_connection()
    if connection is None:
        flash("Database connection failed.", "error")
        return redirect(url_for('services'))

    with connection.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM services WHERE id = %s", (service_id,))
        service = cursor.fetchone()

        if service is None:
            flash("Service not found.", "error")
            return redirect(url_for('services'))

    connection.close()
    return render_template('service_detail.html', service=service)


# ==============================
# 🔹 Run the Flask App
# ==============================
if __name__ == "__main__":
    app.run(debug=True)
