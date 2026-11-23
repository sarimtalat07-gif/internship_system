# Student Internship & Career Management System

Django + Oracle Database term project. All 15 tables from the proposal are
implemented as Django models (portal/models.py). Students browse internships
and apply; administrators manage everything through the built-in admin panel.

## Requirements (already installed in your venv)
- Python 3.12
- Django 5.x, python-oracledb, jupyter

## How to run (do this every time you work on the project)

1. Open cmd and activate the virtual environment:
       cd C:\projects\internship_system
       venv\Scripts\activate
2. Make sure Oracle XE is running (it starts automatically with Windows).
3. Open the folder in VS Code:
       code .
4. Set your credentials as environment variables (nothing secret is stored
   in the code). In the same cmd window, BEFORE opening VS Code:
       set ORACLE_USER=your_oracle_user
       set ORACLE_PASSWORD=your_oracle_password
       set DJANGO_SUPERUSER_USERNAME=admin
       set DJANGO_SUPERUSER_PASSWORD=choose-a-strong-password
       set DJANGO_SUPERUSER_EMAIL=admin@example.com
   Optional: ORACLE_DSN (default 127.0.0.1:1521/XE).
   Oracle XE 21c is recommended (Django 5 needs Oracle 19c+). If you must use
   an older Oracle, set ORACLE_THICK=1 and install Oracle Instant Client.
5. In VS Code open 00_setup.ipynb and run all cells top to bottom
   (Shift+Enter). The last cell starts the website - it keeps "running",
   that is normal.
   NOTE: if your database already has tables from an earlier run, use
   `python manage.py migrate --fake-initial` instead of a plain migrate.
6. Open the browser:
   - Website : http://127.0.0.1:8000
   - Admin   : http://127.0.0.1:8000/admin  (use the superuser you set above)
7. Run 01_seed_data.ipynb to fill the database with demo data, then refresh
   the website.
8. Run 02_reports.ipynb for the SQL / PL/SQL reports.

## Project structure
- internship_system/  -> project settings + urls (DB settings read from env vars)
- portal/             -> all 15 models, admin, views, forms, pages
- templates/portal/   -> HTML pages (Bootstrap 5)
- fake_resumes/       -> demo resume PDFs used by the seed notebook
- media/              -> created automatically; uploaded resumes go here
- 00_setup.ipynb      -> connect to Oracle, create tables, create admin, run site
- 01_seed_data.ipynb  -> fills the database with realistic demo data
- 02_reports.ipynb    -> SQL + PL/SQL reports from the proposal

## Notes for the viva
- One Django app (portal) holds everything - normal for small projects.
- Tables were created by Django's migration system from the model classes.
- Junction tables (StudentSkill, InternshipSkill) are written as normal
  models because the proposal asked for them explicitly.
- The admin panel is Django's built-in CRUD interface - we used it as the
  "administrator side" of the system, and wrote custom pages for students.

## Running the tests (no Oracle needed)
    python manage.py test --settings=internship_system.settings_test

## Known limitations / future work
- Students pick their roll number from a dropdown (no login yet). A real
  deployment should link Student to Django's User model and require login.
- Application status changes are made by admins by adding a row in the
  "Application status history" section of the application page.
