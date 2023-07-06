# blogFrog 

This project is a simple blogging platform built with Flask, a lightweight and powerful web framework for Python. Users can create an account, sign in, and start creating and sharing their blog posts.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Understanding the Codebase and Folder Structure](#understanding-the-codebase-and-folder-structure)
3. [Further Development](#further-development)

## Getting Started

To start working on this project:

1. Clone the repository using Git:
    ```
    git clone https://github.com/NamanSudan/blogFrog.git
    ```

2. Install the required packages using pip:
    ```
    pip install -r requirements.txt
    ```
    This command reads the `requirements.txt` file and installs all the Python packages listed in it. This project's dependencies are Flask and its extensions like Flask-SQLAlchemy and Flask-Login, which help with database management and user authentication.

3. Run the application:
    ```
    python app.py
    ```
    This command starts the Flask development server. You can access the application by navigating to `http://localhost:5000` in your web browser.

4. To debug the application, set the environment variable `FLASK_ENV` to `development` before running the application:
    ```
    export FLASK_ENV=development
    python app.py
    ```
    This enables Flask's development features like debugger and code reloading.

5. To deploy the application, follow the deployment guide for the platform you are using (like Heroku, AWS, GCP, etc.). You will generally need to provide a WSGI server (like Gunicorn or uWSGI), reverse proxy (like Nginx), and probably a process manager (like Supervisor or systemd).

## Understanding the Codebase and Folder Structure

The project is structured following the application factory pattern recommended for Flask applications. Here's an overview:

- `app.py`: This is the entry point of the application. It creates an instance of the Flask application and runs it.
- `website/__init__.py`: This file contains the application factory function `create_app`. It creates and configures the application, and registers the blueprints for views and authentication.
- `website/views.py`: This file contains the views for the main pages of the application, like the home page.
- `website/auth.py`: This file contains the views for authentication, like sign-in, sign-up, and sign-out.
- `website/templates`: This directory contains the Jinja2 templates for the HTML pages. They include base templates, page templates, and component templates.
- `website/static`: (if applicable) This directory would contain the static files like CSS and JavaScript.

Modifying any file will change the corresponding part of the application. For example, modifying a template will change the structure of the HTML pages, and modifying a view function will change the behavior of a route.

## Further Development

You can extend this application in many ways:

1. Add a database model for blog posts in a `models.py` file, and use Flask-SQLAlchemy to handle database operations.
2. Add routes and views for creating, reading, updating, and deleting blog posts.
3. Improve the user interface by adding CSS and JavaScript files in the `static` directory, and linking to them in the base template.
4. Add error handling for HTTP error codes like 404 and 500.
5. Add user-friendly features like password resetting, email confirmation, and user profiles.

Remember that every change you make can have impacts on other parts of the application. Always thoroughly test your changes, and use version control to keep track of them
