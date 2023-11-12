from flask import Flask, render_template, request, url_for, flash, redirect, abort
from stock_loader import StockLoader
from av_service import AlphaVantageService
from chart_service import ChartService
from datetime import datetime

PORT = 5001

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'

# menu options
app.stocks = []
app.chart_types = ["Bar", "Line"]
app.time_series = ["Intraday", "Daily", "Weekly", "Monthly"]

app.api_key = 'SV7DD9W1DE9D97RZ'

@app.before_request
def load_stock_data():
    app.stocks = StockLoader('stocks.csv').stocks

def validate_inputs(symbol, chart_type, time_series, start_date, end_date) -> bool:
    valid = True

    if not symbol:
        flash('Symbol is required!')
        valid = False
    if not chart_type or chart_type not in app.chart_types:
        flash('Chart Type is required!')
        valid = False
    if not time_series or time_series not in app.time_series:
        flash('Time Series is required!')
        valid = False
    if not start_date or not end_date:
        flash('Start and End Date are required!')
        valid = False
    # # turn start_date and end_date into datetime objects and compare
    # start_date = datetime.strptime(start_date, '%Y-%m-%d')
    # end_date = datetime.strptime(end_date, '%Y-%m-%d')
    if start_date > end_date:
        flash('End Date must be greater than or equal to Start Date!')
        valid = False
    
    return valid
    

@app.route('/', methods=['GET', 'POST'])
def index():
    chart = None

    if request.method == 'POST':
        symbol = request.form['symbol']
        chart_type = request.form['chart_type']
        time_series = request.form['time_series']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        

        if validate_inputs(symbol, chart_type, time_series, start_date, end_date):
            try:
                print(f"symbol: {symbol}")
                print(f"chart_type: {chart_type}")
                print(f"time_series: {time_series}")
                print(f"start_date: {start_date}")
                print(f"end_date: {end_date}")
                av_service = AlphaVantageService(app.api_key)
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                # todo: pass type instead
                if time_series == 'Intraday':
                    time_series = av_service.get_intraday(symbol, start_date, end_date)
                elif time_series == 'Daily':
                    time_series = av_service.get_daily(symbol, start_date, end_date)
                elif time_series == 'Weekly':
                    time_series = av_service.get_weekly(symbol, start_date, end_date)
                elif time_series == 'Monthly':
                    time_series = av_service.get_monthly(symbol, start_date, end_date)
                chart_service = ChartService()
                chart = chart_service.create_chart(chart_type, time_series)
            except Exception as e:
                flash(str(e))
                return redirect(url_for('index'))

        # try:
        #     av_service = AlphaVantageService(app.api_key)
        #     time_series = av_service.get_time_series_daily(symbol, start_date, end_date)
        #     chart_service = ChartService()
        #     chart_service.create_chart(chart_type, time_series)
        # except Exception as e:
        #     flash(str(e))
        #     return redirect(url_for('index'))
    return render_template('index.html', stocks=app.stocks, chart_types=app.chart_types, time_series=app.time_series, chart=chart)

app.run(host="0.0.0.0", port=PORT)