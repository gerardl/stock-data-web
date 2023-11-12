import pygal
from datetime import datetime
import lxml
from models import StockValue, TimeSeries

class ChartService:
    DEFAULT_ROTATION = 35
    DATE_FORMAT = '%Y-%m-%d'

    def create_chart(self, chart_type, time_series: TimeSeries):
        chart = pygal.Line(x_label_rotation=self.DEFAULT_ROTATION) if chart_type == 'Line' else pygal.Bar(x_label_rotation=self.DEFAULT_ROTATION)
        chart.title = f'Stock Data for {time_series.symbol}: {datetime.strftime(time_series.start_date, self.DATE_FORMAT)} to {datetime.strftime(time_series.end_date, self.DATE_FORMAT)}'
        time_series.series.reverse()
        chart.x_labels = [stock.date for stock in time_series.series]
        
        # use time_series.sersies for pygal chart
        open = [item.open for item in time_series.series]
        high = [item.high for item in time_series.series]
        low = [item.low for item in time_series.series]
        close = [item.close for item in time_series.series]
        chart.add('Open', open)
        chart.add('High', high)
        chart.add('Low', low)
        chart.add('Close', close)
        
        # show in browser with lxml
        chart.render_in_browser()





