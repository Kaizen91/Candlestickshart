from pandas_datareader import data
import datetime
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.resources import CDN

start = datetime.datetime(2020,1,1)
end = datetime.datetime(2020,6,10)
df  = data.DataReader(name="AAPL",data_source="yahoo",start=start,end=end)


def increase_decrease(close, opn):
    if close > opn:
        value = "Increase"
    elif close < opn:
        value = "Decrease"
    else:
        value = "Equal"
    return value

df["Status"] = [increase_decrease(close, opn) for close, opn in zip(df.Close,df.Open)]
df["Middle"] = (df.Open + df.Close)/2
df["Height"] = abs(df.Close - df.Open)


p = figure(x_axis_type='datetime',width=1000,height=300,sizing_mode="scale_width")
p.title.text="Candlestick Chart"
p.grid.grid_line_alpha=0.2

hours_12 = 12 * 60 * 60 * 1000

p.segment(df.index, df.High, df.index, df.Low, color = "black")

p.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"], hours_12,
       df.Height[df.Status == "Increase"], fill_color="#CCFFFF", line_color="black")

p.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"], hours_12,
       df.Height[df.Status == "Decrease"], fill_color="#FF3333", line_color="black")


script1, div1 = components(p)
cdn_js = CDN.js_files[0]

output_file("CandleStick.html")
show(p)