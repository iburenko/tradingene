import numpy as np
from bokeh import events
from bokeh.core import properties
import tng.algorithm_backtest.tng as tng
import pandas as pd
from bokeh.plotting import figure, show, output_file
import datetime as dt
from bokeh.models import ColumnDataSource, CustomJS, Band
from bokeh.models.tools import HoverTool

def plot_cs_prof(alg, timeframe):
    def update_triangle(source):
        return CustomJS(args=dict(source=source, xr=p.x_range), code="""
        console.log(xr.start, xr.end)
        var data = source.data;
        var x = data["size"]
        var range = data["range"]
        var cond = range[0] / (xr.end - xr.start)
        if (Math.abs(cond - 1) > 0.001)
            for (var i = 0; i < x.length; i++) {
                x[i] = x[i] * cond;
                range[i] = xr.end - xr.start
            }
        console.log(x[0])
        console.log(range[0])
        console.log(cond)
        source.change.emit();
        """)

    close_df = pd.DataFrame()   
    open_df = pd.DataFrame()

    for i in range(len(alg.positions)):
        if (alg.positions[i].closed):
            pos_trades = alg.positions[i].trades
            for j in range(len(pos_trades)):
                print([pos_trades[j].close_time, pos_trades[j].open_time, pos_trades[j].close_price[0], pos_trades[j].open_price[0], pos_trades[j].side, len(pos_trades)])
                if  j < len(pos_trades) - 1:
                    close_df = close_df.append([[pos_trades[j].close_time, pos_trades[j].close_price[0], pos_trades[j].open_price[0], pos_trades[j].side, 0, 0]])
                elif pos_trades[j].close_time > 0:
                    close_df = close_df.append([[pos_trades[j].close_time, pos_trades[j].close_price[0], pos_trades[j].open_price[0],pos_trades[j].side, 1, alg.positions[i].profit[0]]])
                if  j > 0:
                    open_df = open_df.append([[pos_trades[j].open_time, pos_trades[j].open_price[0], pos_trades[j].close_price[0], pos_trades[j].side, 0]])
                else:
                    open_df = open_df.append([[pos_trades[j].open_time, pos_trades[j].open_price[0], pos_trades[j].close_price[0], pos_trades[j].side, 1]])

    df = list(alg.instruments)[0].rates
    df = pd.DataFrame(df[1:(len(df) - 50)])

    close_df.columns = ['time', 'close_price', 'open_price_oncl', 'close_side', 'last_indic', 'profit']
    open_df.columns = ['time', 'open_price', 'close_price_onop', 'open_side', 'first_indic']

    df['size'] = 12.0
    close_df['size'] = 12.0
    df["date"] = pd.to_datetime(df["time"].astype(str), format='%Y%m%d%H%M%S%f')
    df = df.drop(['time'], axis = 1)
    close_df["date"] = pd.to_datetime(close_df["time"].astype(str), format='%Y%m%d%H%M%S%f')
    close_df = close_df.drop(['time'], axis = 1)
    open_df["date"] = pd.to_datetime(open_df["time"].astype(str), format='%Y%m%d%H%M%S%f')
    open_df = open_df.drop(['time'], axis = 1)
    close_df.index = range(len(close_df))

    df = pd.merge(df, open_df, how = 'left', on ='date')

    w = (timeframe / 2) * 60 * 1000

    output_file("candlestick.html", title="Graphs")
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    inc = df.close > df.open
    dec = df.open > df.close
    ind_close = close_df["last_indic"] == 1
    ind_close_subseq = close_df["last_indic"] == 0

    ind_open_subseq = df["first_indic"] == 0
    ind_open = df["first_indic"] == 1
    ind_close_pos = close_df['close_side'] == -1
    ind_open_pos = df['open_side'] == -1

    max_range = (df['high'] - df['low']).max()
    min_low_range = df['low'][(len(df)-31):(len(df)-1)].min()

    max_high_range = df['high'][(len(df)-31):(len(df)-1)].max()

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, toolbar_location="left",
    x_range=(df["date"].min() - dt.timedelta(minutes=timeframe), df["date"].min() + dt.timedelta(minutes=timeframe*30)),
    y_range = (min_low_range - max_range / 2, max_high_range + max_range / 2))

    df['range'] = p.x_range.end - p.x_range.start
    close_df['range'] = p.x_range.end - p.x_range.start
    mysource1 = ColumnDataSource(df[inc])
    mysource2 = ColumnDataSource(df[dec])

    source1 = ColumnDataSource(df[ind_open & (df['open_side'] == 1)])
    source2 = ColumnDataSource(df[ind_open & (df['open_side'] == -1)])
    source3  = ColumnDataSource(close_df[ind_close & (close_df['close_side'] == 1)])
    source4  = ColumnDataSource(close_df[ind_close & (close_df['close_side'] == -1)])

    source5 = ColumnDataSource(df[ind_open_subseq & (df['open_side'] == 1)])
    source6 = ColumnDataSource(df[ind_open_subseq & (df['open_side'] == -1)])
    source7  = ColumnDataSource(close_df[ind_close_subseq & (close_df['close_side'] == 1)])
    source8  = ColumnDataSource(close_df[ind_close_subseq & (close_df['close_side'] == -1)])


    p.segment(df.date, df.high, df.date, df.low, color="black")

    bars_1 = p.vbar(source = mysource1, x="date", width=w, bottom="open", top="close", fill_color="honeydew", line_color="black")
    bars_2 = p.vbar(source = mysource2, x="date", width=w, bottom="close", top="open", fill_color="deepskyblue", line_color="black")

    hover = HoverTool(renderers=[bars_1, bars_2], tooltips = [('high', '@high'),
                                  ('low', '@low'),
                                  ('open', '@open'),
                                  ('close', '@close')])
    p.add_tools(hover)
    
    tr_1 = p.triangle(x="date", y="open_price", size="size", fill_alpha=0.7, source = source1, fill_color="green")
    inv_tr_1 = p.inverted_triangle(x="date", y="open_price", size="size", fill_alpha=0.7, source = source2, fill_color="green")

    tr_2 = p.inverted_triangle(x="date", y="close_price", size="size", fill_alpha=0.7, source = source3, fill_color="yellow")
    inv_tr_2 = p.triangle(x="date", y="close_price", size="size", fill_alpha=0.7, source = source4, fill_color="yellow")

    tr_3 = p.triangle(x="date", y="open_price", size="size", fill_alpha=0.7, source = source5, fill_color="purple")
    inv_tr_3 = p.inverted_triangle(x="date", y="open_price", size="size", fill_alpha=0.7, source = source6, fill_color="purple")

    tr_4 = p.inverted_triangle(x="date", y="close_price", size="size", fill_alpha=0.7, source = source7, fill_color="brown")
    inv_tr_4 = p.triangle(x="date", y="close_price", size="size", fill_alpha=0.7, source = source8, fill_color="brown") 
     

    p.x_range.js_on_change('start', update_triangle(source1))
    p.x_range.js_on_change('start', update_triangle(source2))
    p.x_range.js_on_change('start', update_triangle(source3))
    p.x_range.js_on_change('start', update_triangle(source4))
    p.x_range.js_on_change('start', update_triangle(source5))
    p.x_range.js_on_change('start', update_triangle(source6))
    p.x_range.js_on_change('start', update_triangle(source7))
    p.x_range.js_on_change('start', update_triangle(source8))

    hover1 = HoverTool(renderers=[tr_1, inv_tr_1, tr_3, inv_tr_3],
                        tooltips = [('date', '@date'), ('open_price', '@open_price'),('close_price_onop', '@close_price_onop')])
    p.add_tools(hover1)

    hover2 = HoverTool(renderers=[tr_2, inv_tr_2, tr_4, inv_tr_4],
                        tooltips = [('date', '@date'), ('close_price', '@close_price'), ('open_price_oncl', '@open_price_oncl')])
    p.add_tools(hover2)

    p.xaxis.major_label_orientation = 3.14/4
    p.grid.grid_line_alpha = 0.5
    point_attributes = ['x','y','sx','sy']
    wheel_attributes = point_attributes+['delta']

    show(p)

    close_df = close_df[close_df['last_indic'] == 1]
    close_df['profit'][np.isnan(close_df['profit'])] = 0.0
    close_df['cumsum'] = close_df['profit'].cumsum(skipna=True)
    close_df['pos'] = 0.0

    close_df['pos'] = close_df['cumsum'][close_df['cumsum'] > 0]
    close_df['pos'][np.isnan(close_df['pos'])] = 0
    close_df['neg'] = 0.0
    close_df['neg'] = close_df['cumsum'][close_df['cumsum'] < 0]
    close_df['neg'][np.isnan(close_df['neg'])] = 0
    close_df['zeros'] = 0.0
    plot_prof = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, toolbar_location="left",
    x_range=(df["date"].min(), df["date"].max()),
    y_range =(close_df['cumsum'].min() - (close_df['cumsum'].max() - close_df['cumsum'].min()) * 0.1,
                close_df['cumsum'].max() + (close_df['cumsum'].max() - close_df['cumsum'].min()) * 0.1))


    date_mid = pd.DataFrame()
    date_mid['date'] = close_df['date'].shift() + close_df['cumsum'] * (close_df['date'] - close_df['date'].shift()) / (close_df['cumsum'] - close_df['cumsum'].shift())
    date_mid['diff'] = np.sign(close_df['cumsum'].shift() * close_df['cumsum'])
    date_mid = date_mid[1:]
    date_mid = date_mid[date_mid['diff'] < 0]

    date_mid['cumsum'] = 0.0
    date_mid['pos'] = 0.0
    date_mid['neg'] = 0.0
    date_mid['zeros'] = 0.0


    close_df = pd.concat([close_df, date_mid])
    close_df = close_df.reset_index()
    close_df = close_df.sort_values(by=['date'])
    source = ColumnDataSource(close_df)

    band = Band(base='date', lower='zeros', upper='pos', source = source, fill_alpha=0.7, fill_color="green")
    plot_prof.add_layout(band)
    band = Band(base='date', lower='zeros', upper='neg', source = source, fill_alpha=0.7, fill_color="red")
    plot_prof.add_layout(band)

    show(plot_prof)