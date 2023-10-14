'''
http://127.0.0.1:7008/input_sensor?temperature=30&humidity=79
'''

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from datetime import date, timedelta

# objek flask
app = Flask(__name__)

# api-key
app.secret_key = "djfljdfljfnkjsfhjfshjkfjfjfhjdhfdjhdfu"

# koneksi ke database
userpass = "mysql+pymysql://fadli:Kucinghitam123@"
basedir = "127.0.0.1"
dbname = "/iot_SPDKH"

app.config["SQLALCHEMY_DATABASE_URI"] = userpass + basedir + dbname
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# tabel komposter

class Hutan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    moisture = db.Column(db.Float, nullable=False)
    co = db.Column(db.Float, nullable=False)
    count_tip = db.Column(db.Integer, nullable=False)
    rainfall = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())

    def __init__(self, temperature, humidity, moisture, co, count_tip, rainfall, status):
        self.temperature = temperature
        self.humidity = humidity
        self.moisture = moisture
        self.co = co
        self.count_tip = count_tip
        self.rainfall = rainfall
        self.status = status
