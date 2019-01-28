import datetime as dt
import numpy as np
import pandas as pd
from bokeh import events
from bokeh.core import properties
from bokeh.plotting import figure, save, output_file, show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, Band, Axis
from bokeh.models.tools import HoverTool

def reindex_by_df(reindex_df, by_df, timeframe):
    prev_index = 0
    for j in range(reindex_df.shape[0]):
        for i in range(prev_index, by_df.shape[0]):
            prev_index = i
            if reindex_df.at[j,'date'] == by_df.at[i,'date']:
                reindex_df.at[j,'index'] = by_df.at[i,'index']
                break
            elif reindex_df.at[j,'date'] > by_df.at[i,'date'] and reindex_df.at[j,'date'] < by_df.at[i,'date'] + dt.timedelta(minutes=timeframe):
                reindex_df.at[j,'index'] = ((reindex_df.at[j,'date'] - by_df.at[i,'date']) / dt.timedelta(minutes=timeframe)) + by_df.at[i,'index']
                break
    return reindex_df

def plot_cs_prof(alg, instr, filename):
    def update_triangle(source):
        return CustomJS(
            args=dict(source=source, xr=p.x_range),
            code="""
        var data = source.data;
        var x = data["size"]
        var range = data["range"]
        var cond = range[0] / (xr.end - xr.start)
        if (Math.abs(cond - 1) > 0.001)
            for (var i = 0; i < x.length; i++) {
                x[i] = x[i] * cond;
                range[i] = xr.end - xr.start
            }
        source.change.emit();
        """)

    timeframe = instr.timeframe
    close_df = pd.DataFrame(columns=[
        'time', 'close_price', 'open_price_oncl', 'close_side', 'last_indic',
        'profit'
    ])
    open_df = pd.DataFrame(columns=[
        'time', 'open_price', 'close_price_onop', 'open_side', 'first_indic',
        'profit'
    ])

    for pos in alg.positions:
        pos_trades = pos.trades
        for j in range(len(pos_trades)):
            if pos.closed:
                if j < len(pos_trades) - 1:
                    close_df = close_df.append(
                        pd.DataFrame(
                            [[
                                pos_trades[j].close_time,
                                pos_trades[j].close_price,
                                pos_trades[j].open_price, pos_trades[j].side,
                                0, 0
                            ]],
                            columns=[
                                'time', 'close_price', 'open_price_oncl',
                                'close_side', 'last_indic', 'profit'
                            ]))
                elif pos_trades[j].close_time > 0:
                    close_df = close_df.append(
                        pd.DataFrame(
                            [[
                                pos_trades[j].close_time,
                                pos_trades[j].close_price,
                                pos_trades[j].open_price, pos_trades[j].side,
                                1, pos.profit
                            ]],
                            columns=[
                                'time', 'close_price', 'open_price_oncl',
                                'close_side', 'last_indic', 'profit'
                            ]))
            if j > 0:
                open_df = open_df.append(
                    pd.DataFrame(
                        [[
                            pos_trades[j].open_time, pos_trades[j].open_price,
                            pos_trades[j].close_price, pos_trades[j].side, 0,
                            pos.profit
                        ]],
                        columns=[
                            'time', 'open_price', 'close_price_onop',
                            'open_side', 'first_indic', 'profit'
                        ]))
            else:
                open_df = open_df.append(
                    pd.DataFrame(
                        [[
                            pos_trades[j].open_time, pos_trades[j].open_price,
                            pos_trades[j].close_price, pos_trades[j].side, 1,
                            pos.profit
                        ]],
                        columns=[
                            'time', 'open_price', 'close_price_onop',
                            'open_side', 'first_indic', 'profit'
                        ]),
                    ignore_index=True)
        
    df = pd.DataFrame(instr.candles)
    
    opendf_len = len(open_df)
    closedf_len = len(close_df)

    df['size'] = 12.0
    close_df['size'] = 12.0
    open_df['size'] = 12.0
    df["date"] = pd.to_datetime(
        df["time"].astype(str), format='%Y%m%d%H%M%S%f')
    timedelta = df['date'][len(df) - 1] - df['date'][len(df) - 1].floor(
        str(timeframe) + 'T')

    df = df.drop(['time'], axis=1)

    close_df["date"] = pd.to_datetime(
        close_df["time"].astype(str), format='%Y%m%d%H%M%S%f')
    close_df = close_df.drop(['time'], axis=1)
    open_df["date"] = pd.to_datetime(
        open_df["time"].astype(str), format='%Y%m%d%H%M%S%f')
    open_df = open_df.drop(['time'], axis=1)
    df = df.sort_values(by=['date'])
    close_df = close_df.sort_values(by=['date'])
    open_df = open_df.sort_values(by=['date'])

    df = df.reset_index()
    df['index'] = df.index
    close_df = close_df.reset_index()
    open_df = open_df.reset_index()
    df['index'] = df['index'].astype(np.float64)
    close_df['index'] = df['index'].astype(np.float64)
    open_df['index'] = df['index'].astype(np.float64)

    close_df = reindex_by_df(close_df, df, timeframe)
    open_df = reindex_by_df(open_df, df, timeframe)
    w = (0.5)

    output_file(filename, title="Graphs")
    TOOLS = "pan,wheel_zoom,reset,save"

    inc = df['close'] > df['open']
    dec = ~inc

    ind_close = close_df["last_indic"] == 1
    ind_close_subseq = close_df["last_indic"] == 0
    ind_close_pos = close_df['close_side'] == -1

    ind_open_subseq = open_df["first_indic"] == 0
    ind_open = open_df["first_indic"] == 1
    ind_open_pos = open_df['open_side'] == -1

    max_range = (df['high'] - df['low']).max()

    range_constant = 31 if len(df) - 31 > 0 else len(df)
    min_low_range = df['low'][:range_constant].min()

    max_high_range = df['high'][:range_constant].max()
    p = figure(
        title="Candlestick chart with timeframe = " + str(timeframe) +
        " munutes",
        x_axis_type="linear",
        tools=TOOLS,
        plot_width=1000,
        toolbar_location="left",
        x_range=(-1.5,30),
        y_range=(min_low_range - max_range / 2,
                 max_high_range + max_range / 2))

    df['range'] = p.x_range.end - p.x_range.start
    close_df['range'] = p.x_range.end - p.x_range.start
    open_df['range'] = p.x_range.end - p.x_range.start
    p.segment(df['index'], df['high'], df['index'], df['low'], color="black")
    min_diff = np.fabs(df['close'] - df['open'])
    min_diff = min_diff[min_diff > 0].min()
    prec = "0"
    for i in range(0, 16):
        if min_diff * 10**i >= 1:
            prec = prec * i
            break

    df['close_eq'] = df['close'] + min_diff
    df.loc[df['close'] + min_diff > df['high'],
           'close_eq'] = df['close'] - min_diff
    ind_eq = df['close'] == df['open']
    df['index'] = df.index
    mysource1 = ColumnDataSource(df[inc])
    mysource2 = ColumnDataSource(df[dec])
    mysource3 = ColumnDataSource(df[ind_eq])
    bars_1 = p.vbar(
        source=mysource1,
        x="index",
        width=w,
        bottom="open",
        top="close",
        fill_color="honeydew",
        line_color="black",
        line_width=1)
    bars_2 = p.vbar(
        source=mysource2,
        x="index",
        width=w,
        bottom="close",
        top="open",
        fill_color="deepskyblue",
        line_color="black",
        line_width=1)
    bars_3 = p.vbar(
        source=mysource3,
        x="index",
        width=w,
        bottom="close_eq",
        top="open",
        fill_color="white",
        line_color="black",
        line_width=1,
        fill_alpha=0.0)
    hover = HoverTool(
        renderers=[bars_1, bars_2, bars_3],
        tooltips=[('high', '@high{0.' + str(prec) + '}'),
                  ('low', '@low{0.' + str(prec) + '}'),
                  ('open', '@open{0.' + str(prec) + '}'),
                  ('close', '@close{0.' + str(prec) + '}'),
                  ('volume', '@vol{0.0}'),
                    ('date', "@date{%Y-%m-%d %H:%M:%S}")],
            formatters={"date": "datetime"})
    p.add_tools(hover)
    p.xaxis.major_label_overrides = {
        i: date.strftime('%Y-%m-%d %H:%M:%S') for i, date in enumerate(df["date"])
    }
    if (opendf_len > 0):
        open_df['time'] = open_df['date'].dt.floor(str(timeframe) +
                                                   'T') + timedelta
        source1 = ColumnDataSource(
            open_df[ind_open & (open_df['open_side'] == 1)])
        source2 = ColumnDataSource(
            open_df[ind_open & (open_df['open_side'] == -1)])
        source5 = ColumnDataSource(
            open_df[ind_open_subseq & (open_df['open_side'] == 1)])
        source6 = ColumnDataSource(
            open_df[ind_open_subseq & (open_df['open_side'] == -1)])
        tr_1 = p.triangle(
            x="index",
            y="open_price",
            size="size",
            fill_alpha=0.7,
            source=source1,
            fill_color="green")
        inv_tr_1 = p.inverted_triangle(
            x="index",
            y="open_price",
            size="size",
            fill_alpha=0.7,
            source=source2,
            fill_color="green")
        tr_3 = p.triangle(
            x="index",
            y="open_price",
            size="size",
            fill_alpha=0.7,
            source=source5,
            fill_color="purple")
        inv_tr_3 = p.inverted_triangle(
            x="index",
            y="open_price",
            size="size",
            fill_alpha=0.7,
            source=source6,
            fill_color="purple")

        p.x_range.js_on_change('start', update_triangle(source1))
        p.x_range.js_on_change('start', update_triangle(source2))
        p.x_range.js_on_change('start', update_triangle(source5))
        p.x_range.js_on_change('start', update_triangle(source6))

        hover1 = HoverTool(
            renderers=[tr_1, inv_tr_1, tr_3, inv_tr_3],
            tooltips=[('open_price', '@open_price{0.' + str(prec) + '}'),
                      ('close_price_onop',
                       '@close_price_onop{0.' + str(prec) + '}'),
                       ('date', "@date{%Y-%m-%d %H:%M:%S}")],
            formatters={"date": "datetime"})
        p.add_tools(hover1)

    if (closedf_len > 0):
        close_df['time'] = close_df['date'].dt.floor(str(timeframe) +
                                                     'T') + timedelta

        source3 = ColumnDataSource(
            close_df[ind_close & (close_df['close_side'] == 1)])
        source4 = ColumnDataSource(
            close_df[ind_close & (close_df['close_side'] == -1)])
        source7 = ColumnDataSource(
            close_df[ind_close_subseq & (close_df['close_side'] == 1)])
        source8 = ColumnDataSource(
            close_df[ind_close_subseq & (close_df['close_side'] == -1)])

        tr_2 = p.inverted_triangle(
            x="index",
            y="close_price",
            size="size",
            fill_alpha=0.7,
            source=source3,
            fill_color="yellow")
        inv_tr_2 = p.triangle(
            x="index",
            y="close_price",
            size="size",
            fill_alpha=0.7,
            source=source4,
            fill_color="yellow")
        tr_4 = p.inverted_triangle(
            x="index",
            y="close_price",
            size="size",
            fill_alpha=0.7,
            source=source7,
            fill_color="brown")
        inv_tr_4 = p.triangle(
            x="index",
            y="close_price",
            size="size",
            fill_alpha=0.7,
            source=source8,
            fill_color="brown")

        p.x_range.js_on_change('start', update_triangle(source3))
        p.x_range.js_on_change('start', update_triangle(source4))
        p.x_range.js_on_change('start', update_triangle(source7))
        p.x_range.js_on_change('start', update_triangle(source8))

        hover2 = HoverTool(
            renderers=[tr_2, inv_tr_2, tr_4, inv_tr_4],
            tooltips=[('close_price', '@close_price{0.' + str(prec) + '}'),
                      ('open_price_oncl',
                       '@open_price_oncl{0.' + str(prec) + '}'),
                       ('date', "@date{%Y-%m-%d %H:%M:%S}")],
            formatters={"date": "datetime"})
        p.add_tools(hover2)

    p.yaxis.axis_label = 'Price'
    p.xaxis.major_label_orientation = 3.14 / 4
    p.grid.grid_line_alpha = 0.5
    point_attributes = ['x', 'y', 'sx', 'sy']
    wheel_attributes = point_attributes + ['delta']

    close_df = close_df[close_df['last_indic'] == 1]
    close_df.loc[np.isnan(close_df['profit']), 'profit'] = 0.0
    prof = close_df['profit'].iloc[-1]
    if (open_df['date'].iloc[-1] > close_df['date'].iloc[-1]):
        prof = open_df['profit'].iloc[-1]

    first_el = df.iloc[0]
    first_el = first_el.to_frame().T
    first_el['profit'] = 0.0
    last_el = df.iloc[-1]
    last_el = last_el.to_frame().T
    last_el['profit'] = prof
    last_el['date'] = last_el['date'] + dt.timedelta(minutes=timeframe)

    close_df = close_df.append(first_el, sort=True)
    close_df = close_df.append(last_el, sort=True)

    close_df = close_df.sort_values(by=['date'])
    close_df = close_df.reset_index()
    close_df['cumsum'] = close_df['profit'].cumsum(skipna=True)
    close_df['pos'] = 0.0

    close_df['pos'] = close_df.loc[close_df['cumsum'] > 0, 'cumsum']
    close_df.loc[np.isnan(close_df['pos']), 'pos'] = 0
    close_df['neg'] = 0.0
    close_df['neg'] = close_df.loc[close_df['cumsum'] < 0, 'cumsum']
    close_df.loc[np.isnan(close_df['neg']), 'neg'] = 0.0
    close_df['zeros'] = 0.0
    plot_prof = figure(
        title="Profit plot",
        x_axis_type="datetime",
        tools=TOOLS,
        plot_width=1000,
        toolbar_location="left",
        x_range=(df["date"].min(), close_df["date"].max()),
        y_range=(close_df['cumsum'].min() -
                 (close_df['cumsum'].max() - close_df['cumsum'].min()) * 0.1,
                 close_df['cumsum'].max() +
                 (close_df['cumsum'].max() - close_df['cumsum'].min()) * 0.1))

    date_mid = pd.DataFrame()
    close_df['date'] = (pd.DatetimeIndex(close_df['date']).astype(np.int64))

    curloc = np.sign(
        close_df['cumsum'].shift().fillna(0) * close_df['cumsum']) < 0

    date_mid['date'] = close_df['date'].shift(
    )[curloc] + close_df['cumsum'].shift()[curloc] * (
        close_df['date'][curloc] - close_df['date'].shift())[curloc] / (
            close_df['cumsum'].shift()[curloc] - close_df['cumsum'])[curloc]
    date_mid = date_mid[np.isfinite(date_mid['date'])]
    date_mid['date'] = pd.to_datetime(date_mid['date'])
    close_df['date'] = pd.to_datetime(close_df['date'])

    date_mid['cumsum'] = 0.0
    date_mid['pos'] = 0.0
    date_mid['neg'] = 0.0
    date_mid['zeros'] = 0.0

    close_df = close_df.drop(['level_0','index'],axis=1)
    close_d_no_mids = close_df
    close_df = pd.concat([close_df, date_mid], sort=True)
    close_df = close_df.sort_values(by=['date'])
    close_df = close_df.reset_index()
    close_d_no_mids = close_d_no_mids.sort_values(by=['date'])
    close_d_no_mids = close_d_no_mids.reset_index()
    close_d_no_mids = close_d_no_mids.drop(['index'],axis=1)
    close_df = close_df.drop(['index'],axis=1)

    source_no_mids = ColumnDataSource(close_d_no_mids)
    source = ColumnDataSource(close_df)

    band = Band(
        base='date',
        lower='zeros',
        upper='pos',
        source=source,
        fill_alpha=0.75,
        fill_color="green")
    plot_prof.add_layout(band)
    plot_prof.yaxis.axis_label = 'Profit'
    band = Band(
        base='date',
        lower='zeros',
        upper='neg',
        source=source,
        fill_alpha=0.75,
        fill_color="red")
    plot_prof.add_layout(band)
    profit_line = plot_prof.line(
        x='date', y='cumsum', source=source_no_mids, line_width=2)
    hover3 = HoverTool(
        renderers=[profit_line],
        tooltips=[('date', '@date{%Y-%m-%d %H:%M:%S}'),
                  ('profit', '@cumsum{0.' + str(prec) + '}')],
        formatters={"date": "datetime"})
    plot_prof.add_tools(hover3)

    candlestick_y_axis = p.select(dict(type=Axis, layout="left"))[0]
    candlestick_y_axis.formatter.use_scientific = False
    prof_y_axis = plot_prof.select(dict(type=Axis, layout="left"))[0]
    prof_y_axis.formatter.use_scientific = False
    save(column(p,plot_prof), filename)
