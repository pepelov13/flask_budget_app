from flask import Flask, render_template, request, redirect, url_for
from models import db, Expense
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Create tables once
with app.app_context():
    db.create_all()

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

if __name__ == "__main__":
    app.run(debug=True)