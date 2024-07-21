# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return redirect(url_for('secret_page'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('signup'))
        
        # Bonus point: Check if email already exists in the database
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already exists. Please use a different email.')
            return redirect(url_for('signup'))
        
        # If email doesn't exist, create new user
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('thankyou'))
    
    return render_template('signup.html')

@app.route('/secret')
def secret_page():
    return render_template('secretpage.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)