from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<Expense {self.category} - {self.amount}>"
