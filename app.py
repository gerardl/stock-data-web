from flask import Flask, render_template, request, url_for, flash, redirect, abort
from stock_loader import StockLoader
from av_service import AlphaVantageService
from chart_service import ChartService

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
    if request.method == 'POST':
        symbol = request.form['symbol']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        chart_type = int(request.form['chart_type'])
        try:
            av_service = AlphaVantageService('demo')
            time_series = av_service.get_time_series_daily(symbol, start_date, end_date)
            chart_service = ChartService()
            chart_service.create_chart(chart_type, time_series)
        except Exception as e:
            flash(str(e))
            return redirect(url_for('index'))
    return render_template('index.html', stocks=app.stocks)

app.run(host="0.0.0.0", port=PORT)