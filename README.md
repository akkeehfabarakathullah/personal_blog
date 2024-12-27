Flask-based Blog Application
This is a Flask-based Blog Application that allows users to register, log in, create, edit, delete, and view blog posts. Additionally, it has a schedule management feature, a search function for posts, and basic user authentication and authorization.

Key Features
1. User Authentication:
Registration: Users can create an account by providing a username and password. The password is securely hashed using bcrypt to ensure safety.
Login: Users can log in using their username and password. If credentials match, they are logged in and a session is created.
Logout: The app supports user logout by clearing the session data.
2. Post Management:
Create Post: After logging in, users can create new posts with a title and content.
Edit Post: Users can edit their own posts. The app ensures users can only edit posts they created.
Delete Post: Users can delete their own posts. The app checks if the user owns the post before deletion.
View Post: Each post has a dedicated page showing its details (title, content, date posted).
3. Schedule Management:
Users can create schedules with a title, date, and description. This feature can be useful for time management or event planning.
A list of all created schedules is available for users to view.
4. Search Functionality:
The app includes a search bar where users can search for posts based on keywords in the title or content.
Search results are shown in real-time as JSON.
Technologies Used:
Flask: The main web framework. It handles routing, rendering templates, and managing user sessions.
SQLAlchemy: ORM used to interact with the SQLite database. This is where data about users, posts, and schedules is stored.
Flask-Bcrypt: A library used to securely hash passwords. Ensures user credentials are protected.
SQLite: The database used to store user, post, and schedule information. It is lightweight and suitable for this project.
Werkzeug: Used for password management (hashing and checking passwords).
Key Routes & Their Purpose:
/ (Home Page): Displays all blog posts sorted by the most recent ones. Only logged-in users can access this page.
/register: A form for new users to create an account. It includes validation for matching passwords and checks if the username already exists.
/login: A login form that allows users to authenticate using their username and password.
/logout: Logs the user out by removing their user_id from the session.
/create: A form where authenticated users can create new posts. Users enter the post's title and content.
/post/int:post_id: A page displaying the full details of a post, including title, content, and the posting date.
/post/int:post_id/edit: Allows users to edit their own posts. A user cannot edit someone else’s post.
/post/int:post_id/delete: Deletes the selected post after ensuring the logged-in user is the owner.
/schedule: Displays a list of all schedules created by users.
/schedule/create: Allows users to create a new schedule by providing a title, date, and description.
/search: Users can search for posts based on keywords. It returns results in JSON format, which is useful for dynamic search features.
Key Concepts:
1. Authentication and Authorization:
Session Management: The app uses Flask's session to store the logged-in user's ID (user_id). This ensures that the user stays logged in across pages.
Login Required Decorator: A custom decorator (login_required) is used to protect routes from unauthenticated users. It redirects to the login page if the user is not logged in.
2. Flask Flash Messages:
Flash messages are used to display feedback to the user (e.g., success, error, or warning messages). For example, when a post is successfully created, a success message is shown: flash('Post created successfully!', 'success').
3. Password Security:
Passwords are hashed using bcrypt to ensure user security. When users log in, the hashed password is compared to the input password.
4. SQLAlchemy Models:
User Model: Contains the user’s username and password.
Post Model: Contains the blog post's title, content, date_posted, and a foreign key to the user table.
Schedule Model: Contains the schedule's title, date, and description, with a foreign key to the user table.
5. Search Feature:
The search bar allows users to search for posts by title or content. The search query is executed using ilike, which performs a case-insensitive search in SQLAlchemy.
6. Error Handling:
Custom error pages for 404 and 500 errors ensure a better user experience in case of missing routes or server errors.
Key Functions and Decorators:
1. Login Decorator (login_required):
This decorator is applied to routes that require user authentication. If the user is not logged in, it redirects them to the login page and shows a flash message.
2. Utility Processor:
The utility processor get_current_user() is used to fetch the current logged-in user and make it available globally in the templates. This is useful for rendering user-specific content like the "Create Post" button, which is shown only to logged-in users.


Installation
To run this project, you'll need Python 3 and the following dependencies:

1.Clone the repository:
git clone <repository_url>
cd <project_directory>

2.Install dependencies:
Create a virtual environment and install required packages.
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt

3.Set the secret key:
In the app.py file, replace 'your_secret_key_here' with a secure key for session management.

4.Initialize the Database:
The application uses SQLite as the database. 
The database file will be automatically created when you run the application for the first time.
python app.py



File Structure.
├── app.py                # Main application code
├── templates/            # HTML templates for various routes
│   ├── index.html        # Home page displaying all posts
│   ├── about.html        # About page
│   ├── register.html     # Registration page
│   ├── login.html        # Login page
│   ├── create.html       # Create post page
│   ├── post.html         # Single post view
│   ├── edit.html         # Edit post page
│   └── schedule.html     # View schedules page
├── static/               # Static files (CSS, JS, images)
├── requirements.txt      # List of Python dependencies
└── database.db           # SQLite database file (auto-generated)


Technologies Used
Python 3 - Programming language
Flask - Web framework
SQLAlchemy - ORM for database interaction
Bcrypt - Password hashing
SQLite - Lightweight relational database
HTML/CSS - Frontend templates
Jinja2 - Templating engine for Flask
Werkzeug - Utilities for handling security

Improvements for Future Development:
User Profile: Add functionality for users to view and update their profile information (e.g., change password, profile picture).
Email Authentication: Implement email verification upon registration to ensure user authenticity.
Advanced Search: Enhance the search feature by adding more filters (e.g., searching by date or user).
Post Categorization: Allow posts to be categorized into different topics or tags.