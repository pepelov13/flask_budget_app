from flask import Flask, render_template, request, redirect, url_for
from models import db, Expense
from config import Config
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract

app = Flask(__name__)
app.config.from_object(Config)

# Uploads folder + allowed file types
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db.init_app(app)

# Create tables once
with app.app_context():
    db.create_all()

# Helper to check file type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    expenses = Expense.query.all()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        category = request.form['category']
        amount = float(request.form['amount'])
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        description = request.form.get('description')

        new_expense = Expense(category=category, amount=amount, date=date, description=description)
        db.session.add(new_expense)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_expense.html')

# ===== New Route: Upload & Scan Receipt =====
@app.route('/upload_receipt', methods=['GET', 'POST'])
def upload_receipt():
    if request.method == 'POST':
        if 'receipt' not in request.files:
            return "No file uploaded"
        
        receipt = request.files['receipt']
        if receipt.filename == '':
            return "No file selected"

        if receipt and allowed_file(receipt.filename):
            filename = secure_filename(receipt.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            receipt.save(filepath)

            # Run OCR
            img = Image.open(filepath)
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            text = pytesseract.image_to_string(img)

            return render_template("scan_result.html", text=text)

    return render_template("upload_receipt.html")


if __name__ == "__main__":
    app.run(debug=True)
