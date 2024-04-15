from database import db

# from flask_login import UserMixin    # UserMixin é uma classe que já implementa métodos de autenticação


class Snack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(50), nullable=False
    )  # nullable=False significa que o campo é obrigatório
    description = db.Column(
        db.String(200), nullable=False
    )  # nullable=False significa que o campo é obrigatório
    hours = db.Column(
        db.DateTime, nullable=False
    )  # Date Time é um tipo de dado que armazena data e hora, sua representação é 'YYYY-MM-DD HH:MM:SS'
    diet = db.Column(db.String(50), nullable=False)
