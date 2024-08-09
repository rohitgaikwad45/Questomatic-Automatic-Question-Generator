import os
import fitz
from flask import Flask, render_template, request, current_app, send_file, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from fpdf import FPDF
from question_generation_english import generate_questions_english
from question_generation_marathi import generate_questions_marathi

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'Pass@123'

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://questomatic_user:root@localhost/questomatic_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app) 

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_pdf(file_path):
    text = ''
    with fitz.open(file_path) as doc:
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()
    return text

def read_file(file_path):
    if file_path.lower().endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    elif file_path.lower().endswith('.pdf'):
        return read_pdf(file_path)
    else:
        raise ValueError('Unsupported file format')

def create_pdf(questions, username, filename, file_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Header
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 10, 'Generated Questions', 0, 1, 'C')
     # Add some space after the header
    
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 10, 'by', 0, 1, 'C')
   
    # Footer
    
    pdf.set_font("Arial", 'B', 15)
    pdf.cell(0, 10, '(Questomatic)', 0, 1, 'C')
    pdf.ln(10)  # Add some space after the header
    
    # Add some space after the header

    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, f'Questions Generated for: {username}', 0, 1, 'L')
    pdf.cell(0, 10, f'Input File_Name: {filename}', 0, 1, 'L')
    pdf.ln(10)  # Add some space after the footer

    # Content
    pdf.set_font("Arial", size=12)
    for i, question in enumerate(questions):
        pdf.cell(200, 10, txt=f"{i + 1}. {question}", ln=True, align='L')
    pdf.output(file_path)

    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))  
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error='No selected file')
        if 'num_questions' not in request.form:
            return render_template('index.html', error='Number of questions not provided')
        if 'language' not in request.form:
            return render_template('index.html', error='Language not provided')
        
        num_questions = int(request.form['num_questions'])
        language = request.form['language']

        if file and allowed_file(file.filename):
            try:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                text_from_file = read_file(file_path)
                if language == 'english':
                    generated_questions = generate_questions_english(text_from_file, num_questions)
                elif language == 'marathi':
                    generated_questions = generate_questions_marathi(text_from_file, num_questions)
                else:
                    return render_template('index.html', error='Unsupported language')
                
                os.remove(file_path)
                
                # Create PDF and provide download link
                pdf_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'generated_questions.pdf')
                create_pdf(generated_questions, current_user.username, file.filename, pdf_file_path)

                return render_template('index.html', questions=generated_questions)
            
            except Exception as e:
                print("An error occurred:", str(e))  # Debugging
                return render_template('index.html', error='Error processing the file')
    
    return render_template('index.html')

@app.route('/download_pdf')
@login_required
def download_pdf():
    pdf_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'generated_questions.pdf')
    if os.path.exists(pdf_file_path):
        return send_file(pdf_file_path, as_attachment=True)
    else:
        return render_template('index.html', error='PDF file not found')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
