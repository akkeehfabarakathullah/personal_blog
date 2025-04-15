# Flask-based Blog Application

This is a Flask-based Blog Application that allows users to register, log in, create, edit, delete, and view blog posts. Additionally, it has a schedule management feature, a search function for posts, and basic user authentication and authorization.

---

## Key Features

### 1. User Authentication
- **Registration**: Secure user registration with password hashing using bcrypt.
- **Login**: Session-based authentication.
- **Logout**: Securely logs users out.

### 2. Post Management
- **Create Post**: Authenticated users can write blog posts.
- **Edit/Delete Post**: Only the post owner can edit or delete their posts.
- **View Post**: Each post has a detailed view page.

### 3. Schedule Management
- Create and view personal schedules with title, date, and description.

### 4. Search Functionality
- Keyword search for posts (real-time results in JSON format).

---

## Technologies Used

- **Flask** – Web framework.
- **SQLAlchemy** – ORM for database interactions.
- **Flask-Bcrypt** – Password hashing.
- **SQLite** – Database.
- **Werkzeug** – Password utilities.
- **HTML/CSS/Jinja2** – Templating and UI.

---

## Key Routes & Their Purpose

| Route | Purpose |
|-------|---------|
| `/` | Home page with all blog posts |
| `/register` | Register a new user |
| `/login` | Log in |
| `/logout` | Log out |
| `/create` | Create a new post |
| `/post/<int:post_id>` | View a single post |
| `/post/<int:post_id>/edit` | Edit a post |
| `/post/<int:post_id>/delete` | Delete a post |
| `/schedule` | View all schedules |
| `/schedule/create` | Create a new schedule |
| `/search` | Search for posts |

---

## Key Concepts

- **Authentication & Authorization**: Session management & `login_required` decorator.
- **Flash Messages**: Feedback system for user actions.
- **Password Security**: Passwords are hashed using bcrypt.
- **SQLAlchemy Models**:
  - `User`: Stores user info.
  - `Post`: Stores blog posts.
  - `Schedule`: Stores schedules.
- **Search Feature**: Case-insensitive search using `ilike`.
- **Error Handling**: Custom 404 and 500 error pages.

---

## Installation Guide

1. **Clone the repository**:
```bash
git clone <repository_url>
cd <project_directory>
```

2. **Create a virtual environment & install dependencies**:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Set the Secret Key**:
- In `app.py`, set a secure secret key for session management.

4. **Initialize the Database**:
```bash
python app.py
```
- The SQLite database will be automatically created.

---

## File Structure

```
├── app.py                # Main application code
├── templates/            # HTML templates
│   ├── index.html
│   ├── about.html
│   ├── register.html
│   ├── login.html
│   ├── create.html
│   ├── post.html
│   ├── edit.html
│   └── schedule.html
├── static/               # Static assets
├── requirements.txt      # Python dependencies
└── database.db           # SQLite database (auto-generated)
```

---

## Future Improvements

- **User Profiles**: Add profile editing & picture uploads.
- **Email Authentication**: Verify users via email upon registration.
- **Advanced Search**: Filter by date, category, or user.
- **Post Categorization**: Enable post tagging and topic-based organization.

---
