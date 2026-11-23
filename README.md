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
4. IMPORTANT (only once): open internship_system/settings.py and put your
   Oracle XE password in the PASSWORD line of the DATABASES section.
5. In VS Code open 00_setup.ipynb and run all cells top to bottom
   (Shift+Enter). The last cell starts the website - it keeps "running",
   that is normal.
6. Open the browser:
   - Website : http://127.0.0.1:8000
   - Admin   : http://127.0.0.1:8000/admin  (login: admin / admin123)
7. Run 01_seed_data.ipynb to fill the database with demo data, then refresh
   the website.
8. Run 02_reports.ipynb for the SQL / PL/SQL reports.

## Project structure
- internship_system/  -> project settings + urls (DATABASE password is here)
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
