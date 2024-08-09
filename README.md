# Questomati-Automatic-Question-Generatorquestomatic

Questomatic - Automated Question Generator
Questomatic is a Flask-based web application that allows users to upload text files and generate questions based on the content. The application supports both English and Marathi languages for question generation. It also includes user authentication and allows downloading the generated questions in PDF format with a custom header and footer.


Features


User Authentication: Secure login and registration using Flask-Login and Flask-Bcrypt.
Question Generation: Automatically generate questions from uploaded text files in both English and Marathi.
File Upload: Supports PDF and TXT file uploads for generating questions.
PDF Download: Download the generated questions in a PDF format with a custom header and footer containing the username and input file name.
Technologies Used
Flask: Web framework used for building the application.
MySQL: Database backend used to store user information.
SQLAlchemy: ORM used for database operations.
Flask-Login: Used for user session management.
Flask-Bcrypt: Used for password hashing.
FPDF: Used to create PDFs for the generated questions.
Stanza: NLP library used for generating questions.


Setup and Installation

Python 3.x
MySQL
pip (Python package installer)


Installation Steps
Clone the Repository

bash

git clone https://github.com/yourusername/questomatic.git

cd questomatic
Create a Virtual Environment

bash

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install Dependencies

bash

pip install -r requirements.txt
Configure the Database

Ensure MySQL is installed and running.
Create a new database named questomatic_db.
Update the SQLALCHEMY_DATABASE_URI in app.py with your MySQL username and password.
Run Database Migrations

bash

python -c "from app import db; db.create_all()"
Run the Application

bash

python app.py



# Usage


Register an Account

Visit the /register route.
Create a new account with a username and password.
Login

Visit the /login route.
Log in with your credentials.
Upload a File and Generate Questions

After logging in, you will be redirected to the home page.
Choose a text file (PDF or TXT) and select the language (English or Marathi).
Specify the number of questions to generate and submit the form.
The generated questions will be displayed on the page.
Download Generated Questions

After generating the questions, click on the "Download PDF" button to download the questions in PDF format.
The PDF will include a header "Generated Questions" and a footer with your username and the name of the uploaded file.



Project Structure 


├── app.py                  # Main Flask application file
├── question_generation_english.py  # English question generation logic
├── question_generation_marathi.py  # Marathi question generation logic
├── templates/
│   ├── index.html          # Main page template
│   ├── login.html          # Login page template
│   └── register.html       # Registration page template
├── static/
│   ├── css/                # CSS files
│   └── js/                 # JavaScript files
├── uploads/                # Directory for uploaded files and generated PDFs
└── README.md               # Project README file
