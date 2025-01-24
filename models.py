from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Companhia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    modelos = db.relationship('ModeloAeronave', backref='companhia', lazy=True)

class ModeloAeronave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)
    companhia_id = db.Column(db.Integer, db.ForeignKey('companhia.id'), nullable=False)

class Voo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_voo = db.Column(db.String(20), unique=True, nullable=False)
    companhia_id = db.Column(db.Integer, db.ForeignKey('companhia.id'), nullable=False)
    modelo_aeronave_id = db.Column(db.Integer, db.ForeignKey('modelo_aeronave.id'), nullable=False)
    tipo_voo = db.Column(db.String(20), nullable=False)  # Regular ou Charter
    tipo_aeronave = db.Column(db.String(10), nullable=False)  # PC, MC, LC
    qtd_voos = db.Column(db.Integer, nullable=False)
    horario_voo = db.Column(db.String(10), nullable=False)  # EAM, AM, AN, PM, ALL
    qtd_passageiros = db.Column(db.Integer, nullable=False)
    nota_obj = db.Column(db.Integer)  # Salvar como número
    nota_pontualidade = db.Column(db.Integer)
    nota_servicos = db.Column(db.Integer)
    nota_patio = db.Column(db.Integer)
    data_insercao = db.Column(db.DateTime, default=datetime.utcnow)  # Data automática
    
    #relacionamentos
    companhia = db.relationship('Companhia', backref='voos')
    modelo_aeronave = db.relationship('ModeloAeronave', backref='voos')