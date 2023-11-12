from flask import Flask, render_template, request, url_for, flash, redirect, abort
from stock_loader import StockLoader

PORT = 5001

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True
app.stocks = []

@app.before_request
def load_stock_data():
    app.stocks = StockLoader('stocks.csv').stocks

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', stocks=app.stocks)

app.run(host="0.0.0.0", port=PORT)