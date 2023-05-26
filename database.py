from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    mark = db.Column(db.String(120), nullable=False)
    fuel = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def repr(self):
        return f'<Car {self.full_name}>'

def initialize_database(app):
    with app.app_context():
        db.create_all()