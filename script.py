#!/usr/bin/env python

from datetime          import datetime
from flask             import Flask
from flask_sqlalchemy  import SQLAlchemy

import signal
import os
import requests
import threading

DB_USERNAME = "postgres"
DB_PASSWORD = "ABMcobol729"
DB_HOST = "74.48.132.213"
DB_PORT = "5432"
DB_NAME = "exchange"

headers = {
    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Brave\";v=\"120\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "Referer": "https://www.sunat.gob.pe/",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

request_url = "https://www.sunat.gob.pe/a/txt/tipoCambio.txt"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Precio(db.Model):
    __tablename__ = 'precios'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    precio_venta = db.Column(db.Numeric(10, 3), nullable=False)
    precio_compra = db.Column(db.Numeric(10, 3), nullable=False)

    def __init__(self, fecha, precio_venta, precio_compra):
        self.fecha = fecha
        self.precio_venta = precio_venta
        self.precio_compra = precio_compra

def extract_data():
    response = requests.get(request_url, headers=headers)
    substrings = response.text.split('|')
    fecha = datetime.strptime(substrings[0], '%d/%m/%Y').date()
    p_venta = float(substrings[1])
    p_compra = float(substrings[2])

    with app.app_context():
        price_data = Precio(fecha=fecha, precio_venta=p_venta, precio_compra=p_compra)
        print(price_data.fecha)

    return price_data

def insert_data_and_stop_server(data):
    with app.app_context():
        nuevo_precio = Precio(
            fecha=data.fecha,
            precio_venta=data.precio_venta,
            precio_compra=data.precio_compra
        )
        db.session.add(nuevo_precio)
        db.session.commit()

    # Señal para detener el servidor Flask
    os.kill(os.getpid(), signal.SIGINT)

if __name__ == "__main__":
    data = extract_data()
    t = threading.Thread(target=insert_data_and_stop_server, args=(data,))
    t.start()
    app.run(debug=False)
