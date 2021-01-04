import requests
import json
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Slider, TextInput, FixedTicker
from bokeh.layouts import column, row
from bokeh.io import curdoc

username = "BairBuyrchiyev"
token = open("token.txt", "r")
response = requests.get("https://api.github.com/users/" + username + "/repos", auth = (username, token))
numRep = 5

text = TextInput(title=str(numRep), value='BairBuyrchiyev')

p = figure(plot_width=400, plot_height=400, title="BairBuyrchiyev",
            x_range=[0, 5], y_range=[0, 10])
p.vbar(x=1, width=1, bottom=0,
    top=numRep, color="firebrick")

def update_user(attrname, old, new):
    global response, numRep, graphs
    response = requests.get("https://api.github.com/users/" + text.value + "/repos", auth = (username, token))
    numRep = 0
    for entry in json.loads(response.text):
        numRep += 1
    p = figure(plot_width=400, plot_height=400, title=text.value,
            x_range=[0, 5], y_range=[0, numRep + 1])
    p.vbar(x=1, width=1, bottom=0,
        top=numRep, color="firebrick")
    p.yaxis.ticker = FixedTicker(ticks=list(range(0, numRep + 1)))
    newGraph = row(text, p, width=1000)
    graphs.children = newGraph.children
    
text.on_change('value', update_user)

graphs = row(text, p, width=1000)

curdoc().add_root(graphs)
curdoc().title = "BIG WORKY"