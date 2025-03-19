# Database/User/Authentication Branch

This demo branch shows off: Python, Flask, LoginManager, WTForms, Werkzeug, Flask-SQLAlchemy, Flask-Migrate, matplotlib and psycopg2.
It is in the form of a basic business web space with B2B and B2C features.

You will need to ensure you install PostgreSQL on your computer. You can do so by installing PostgreSQL from the link below and following the instructions:

<https://www.postgresql.org/download/>

When installing PostgreSQL, select the **PostgreSQL Server**, **pgAdmin 4** and **Command Line Tools** components.
Ensure you deselect the _Stack Builder_ component during the installation as it is not necessary for this course.

Create a database and ensure you have a database user that you can use to connect to the database.

To begin using this app you can do the following:

1. Clone the repository to your local machine.
2. Create a Python virtual environment e.g. `python -m venv venv` (You may need to use `python3` instead)
3. Enter the virtual environment using `source venv/bin/activate` (or `./venv/Scripts/activate` on Windows)
4. Install the dependencies using Pip. e.g. `pip install -r requirements.txt`. Note: Ensure you have PostgreSQL already installed and a database created. If there are errors during PIP install, then remove all ==version numbers from the requirements.txt file and try again.
5. Change/Rename the `.env.sample` to `.env`
6. Edit the `.env` file and enter your database credentials and database username.
6. Run the migrations by typing `flask db upgrade`
7. Ensure you add a user to your database to test the login system.
8. Start the development server using `flask --debug run`.

```python
# from .config import Config
...
# app.config.from_object(Config)
```

Using the separate config file will also require you to set environment variables on your local computer or server at the command line. For example on Linux or MacOS:

```bash
export SECRET_KEY="my-super-secret-key"
export DATABASE_URL="postgresql://yourusername:yourpassword@localhost/databasename"
```

Or on Windows:

```powershell
set SECRET_KEY="my-super-secret-key"
set DATABASE_URL="postgresql://yourusername:yourpassword@localhost/databasename"
```
