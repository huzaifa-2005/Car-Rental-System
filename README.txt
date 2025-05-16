================================
Car Rental System - OOP Project
===============================

Overview:
---------
This is a Django-based Online Car Rental System developed as a complex engineering project (CEP) for the Object-Oriented Programming (OOP) course. The system implements Python's OOP principles such as inheritance, composition, method overriding, exception handling, and abstract classes.

The system allows users to:
- Sign up, log in, and rent available cars.
- Return rented cars early with no compensation.
- View rental and transaction histories.
- Admins can add/remove cars and generate PDF reports.

Technologies Used:
------------------
- Python 3
- Django 5.2
- HTML/CSS
- SQLite (default database)
- xhtml2pdf (for PDF report generation)

Project Structure:
------------------
Car_Rental_System/
│
├── main_app/                    ( Django app containing models, views, templates)
├── Car_Rental_System/     ( Django project settings and URLs )
├── media/                          
                ├── car_images/  ( where car images added by the admin on website will be saved)
├── static/                          
                ├── styles/         ("style.css" Parent CSS script)
                ├── images/        (from here, admin can browse car images which will be manually saved here firstly by the admin. )

├── templates/                    ( Parent HTML template )
├── .gitignore                      ( Git ignore rules. )
├── db.sqlite3                      ( SQLite3 database file )
├── manage.py                      ( Django's CLI utility script )
├── requirements.txt            ( Project dependencies )
└── README.txt                  ( Project overview (this file) )



=================================
INTIAL SETUP (First-Time Run)
=================================

Prerequisites:
--------------
- Python 3.6+ installed.
- Terminal (Command Prompt for Windows / Terminal for macOS/Linux) or IDE terminal (e.g., VS Code).

FOLLOW THESE STEPS IN ORDER AFTER UNZIPPING THE PROJECT:
=====================================================================

1. Open a Terminal:
-------------------
- For Windows: Press `Win + R`, type `cmd`, and hit Enter (or use IDE terminal).
- For macOS/Linux: Open "Terminal" (or use IDE terminal).
- Run this command in the opened terminal to navigate to the project folder (where `manage.py` is located):
cd "your_path/to/unzipped_project_folder"


2. Create a Virtual Environment:
--------------------------------
- Run this command in the opened terminal:
- For Windows:
  
  python -m venv venv
  
- For macOS/Linux:
  
  python3 -m venv venv
  
(This creates a `venv` folder in your project's folder where you navigated in the first step above.)

3. Activate the Virtual Environment:
-----------------------------------

Run this command in the opened terminal :
- For Windows:
venv\Scripts\activate
-For macOS/Linux:
source venv/bin/activate

Now, you’ll see `(venv)` in the terminal prompt once activated.

4. Install Dependencies:
-----------------------
- Run this in the "activated venv terminal":
pip install -r requirements.txt
(This installs Django and other packages listed in `requirements.txt`.)

5. Set Up the Database:
----------------------
- Run these commands **in order** in the same opened terminal (where venv is now activated):
python manage.py makemigrations
python manage.py migrate

(This creates the database tables.)

6. Creating superuser :
-------------------------------------
- To access the admin interface, firstly, you'll need to create a superuser by running this command in the same opened terminal:
python manage.py createsuperuser
Then, follow the prompts to set a username/email/password for the admin.

7. Run the Development Server:
-----------------------------
- Start the server with:
python manage.py runserver
Output will show:
Starting development server at http://127.0.0.1:8000/


8. Access the Project:
---------------------
- Holding the "Ctrl" key, click on `http://127.0.0.1:8000/` in the terminal 
OR
-Open a browser and go to `http://127.0.0.1:8000/`
The web interface will get opened where initially you'll be an unauthenticated user.
On the opened web interface, you can login as admin by giving your admin's credentials as well as sign in as a normal user. 


9. Stop the Server:
------------------
- Press `Ctrl + C` in the terminal where the server is running.

10. Deactivate Virtual Environment (When Done):
---------------------------------------------
- Type this in the terminal:
deactivate
(The `(venv)` prefix will disappear.)

Troubleshooting:
----------------
- If `pip` fails, ensure the terminal is in the project folder and `venv` is activated.
- If migrations fail, delete `db.sqlite3` (if any) and re-run `makemigrations` + `migrate`.


===========================================================================
STEPS FOR RE-RUNNING THE PROJECT AFTER CLOSING THE TERMINAL :
===========================================================================

Once the project is set up (virtual environment created, dependencies installed, etc.), follow these steps to restart it:

1.Open a terminal and navigate to the project folder.
2.In the same opened terminal, activate the virtual environment created while setting up the project.
3.Start the server by running this command:
python manage.py runserver
Access the app at http://127.0.0.1:8000/.

You don’t need to re-run pip install or migrations unless you’ve made changes to the project.
To stop the server, press Ctrl + C. To exit the virtual environment, type deactivate.



NOTE ON FILE NAMING:
=========================

- The `venv/` folder and `.git/` folder were intentionally removed before submission to reduce file size and follow best practices.
- The Python files inside this Django project (e.g., `views.py`, `models.py`, `urls.py`) follow Django's standard naming conventions and have not been renamed according to the naming conventions shared in the Google classroom. 
-This is intentional since renaming Django’s default script names will disrupt the framework's internal linking and break project functionality.
-Hence, we have followed Django’s professional standards while maintaining functionality and clarity.


Submitted by :  HUZAIFA AHMED (CS-24091) AND WASI MUZAMMIL (CS-24093) FROM G-3 GROUP.
Course: Object-Oriented Programming  
Batch: 2024
Semester: Spring 2025
