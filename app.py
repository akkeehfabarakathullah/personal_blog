import os
from flask_bcrypt import Bcrypt
from flask import Flask, jsonify, render_template, request, redirect, send_from_directory, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




# Initialize Bcrypt and SQLAlchemy
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  # Initialize bcrypt here

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Define relationship to User
    user = db.relationship('User', backref='posts', lazy=True)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
@login_required
def index():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if the passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        # Hash the password using bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()  # Using username instead of email

        if user and bcrypt.check_password_hash(user.password, password):
            # Store the user_id in the session to keep them logged in
            session['user_id'] = user.id
            return redirect(url_for('index'))  # Redirecting to the dashboard route
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        new_post = Post(
            title=title,
            content=content,
            user_id=session['user_id']
        )
        
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('index'))
        except:
            flash('Error creating post. Please try again.', 'danger')
            
    return render_template('create.html')

@app.route('/post/<int:post_id>') 
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.user_id != session['user_id']:
        flash('You can only edit your own posts!', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        
        try:
            db.session.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('post', post_id=post.id))
        except:
            flash('Error updating post. Please try again.', 'danger')
        
    return render_template('edit.html', post=post)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Ensure the logged-in user is the one who created the post
    if post.user_id != session['user_id']:
        flash('You can only delete your own posts!', 'danger')
        return redirect(url_for('index'))

    try:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'success')
        return redirect(url_for('index'))
    except:
        flash('Error deleting post. Please try again.', 'danger')
        return redirect(url_for('index'))

@app.route('/schedule')
def schedule():
    schedules = Schedule.query.order_by(Schedule.date).all()
    return render_template('schedule.html', schedules=schedules)

@app.route('/schedule/create', methods=['GET', 'POST'])
@login_required
def create_schedule():
    if request.method == 'POST':
        title = request.form['title']
        date_str = request.form['date']
        description = request.form['description']
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
            new_schedule = Schedule(
                title=title,
                date=date,
                description=description,
                user_id=session['user_id']
            )
            
            db.session.add(new_schedule)
            db.session.commit()
            flash('Schedule created successfully!', 'success')
            return redirect(url_for('schedule'))
        except ValueError:
            flash('Invalid date format. Please try again.', 'danger')
        except:
            flash('Error creating schedule. Please try again.', 'danger')
            
    return render_template('create_schedule.html')

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Context processor for user data
@app.context_processor
def utility_processor():
    def get_current_user():
        if 'user_id' in session:
            return User.query.get(session['user_id'])
        return None
    return dict(get_current_user=get_current_user)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')  # Fetch the search query from the URL
    results = []

    if query:
        try:
            # Query the 'Post' model for titles or content containing the search term (case-insensitive)
            results = Post.query.filter(
                (Post.title.ilike(f'%{query}%')) | 
                (Post.content.ilike(f'%{query}%'))
            ).all()

            # Format results as a list of dictionaries
            results_data = [{"id": post.id, "title": post.title} for post in results]
            
            # Return results as JSON
            return jsonify(results_data)
        
        except Exception as e:
            # If there's an error, return an empty array and log the error
            print(f"Error: {str(e)}")
            return jsonify([])

    return jsonify([])  # Return an empty list if no query is provided



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)









