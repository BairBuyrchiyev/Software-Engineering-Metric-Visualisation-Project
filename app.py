import requests
import json
from math import pi
import pandas as pd
from bokeh.plotting import figure
from bokeh.palettes import Category20
from bokeh.models import ColumnDataSource, Slider, TextInput, FixedTicker, RadioButtonGroup
from bokeh.transform import cumsum
from bokeh.models.annotations import Title
from bokeh.layouts import column, row
from bokeh.io import curdoc

numRep = 0
username = "BairBuyrchiyev"
token = open("token.txt", "r").read()
response = requests.get("https://api.github.com/users/" + username + "/repos", auth = (username, token))
biggestNumRep = 0
numRepList = []
repoNames = []
usernameList = ["BairBuyrchiyev"]

def update_user(attrname, old, new):
    global response, usernameList
    response = requests.get("https://api.github.com/users/" + text.value + "/repos", auth = (username, token))
    if response.status_code != 404:
        usernameList.append(text.value)
    update_repos()
    update_graph()

def update_repos():
    global numRep, numRepList, biggestNumRep
    numRep = 0
    if response.status_code != 404:
        for entry in json.loads(response.text):
            numRep += 1
        numRepList.append(numRep)
        if numRep > biggestNumRep:
            biggestNumRep = numRep

def update_graph():
    global numRep, repoNames
    p = figure(plot_width=400, plot_height=400, title=text.value, x_range=usernameList, y_range=[0, biggestNumRep + 1], toolbar_location=None, tools="")
    if response.status_code == 404:
        t = Title()
        t.text = "USER NOT FOUND"
        p.title = t
    p.vbar(x=usernameList, width=0.8, bottom=0, top=numRepList, color="firebrick")
    p.yaxis.ticker = FixedTicker(ticks=list(range(0, biggestNumRep + 2)))
    p.yaxis.axis_label = "No. of repositories"

    if response.status_code != 404:
        repoDict = json.loads(response.text)
        repoNames = []
        for entry in repoDict:
            repoNames.append(entry["name"])
        radio = RadioButtonGroup(labels=repoNames, active=0)
        #radio.on_click(specific_repo)
        specific_repo(0)
        print("shitsfucjdifjsoidfd")
    else:
        radio = RadioButtonGroup(labels=[])

    newGraph = column(text, radio, row(p, pie), width=1000)
    graphs.children = newGraph.children

def specific_repo(attrname):
    global graphs, repoNames, pie
    print(repoNames)
    response = requests.get("https://api.github.com/repos/" + usernameList[-1] + "/" + repoNames[radio.active] + "/languages", auth = (username, token))
    languages = json.loads(response.text)

    print(usernameList[-1])
    print(radio.active)
    print(repoNames[radio.active])
    print(languages)

    data = pd.Series(languages).reset_index(name='value').rename(columns={'index':'lang'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi

    if len(languages) < 2:
        data['color'] = ["#1f77b4"]
    elif len(languages) < 3:
        data['color'] = ["#1f77b4", "#aec7e8"]
    else:
        print(len(languages))
        data['color'] = Category20[len(languages)]

    pie = figure(plot_height=400, title=repoNames[radio.active], toolbar_location=None, tools="hover", tooltips="@lang: @value", x_range=(-0.5, 1.0))
    pie.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'), line_color="white", fill_color='color', legend_field='lang', source=data)

    pie.axis.axis_label=None
    pie.axis.visible=False
    pie.grid.grid_line_color = None

    newGraph = column(text, radio, row(p, pie), width=1000)
    graphs.children = newGraph.children

# INITIALISING PRESET USER 
update_repos()

text = TextInput(title="Please enter a user:", value='BairBuyrchiyev')

p = figure(plot_width=400, plot_height=400, title="BairBuyrchiyev", x_range=usernameList, y_range=[0, biggestNumRep + 1], toolbar_location=None, tools="")
p.vbar(x=usernameList, width=0.8, bottom=0, top=numRepList, color="firebrick")
p.yaxis.ticker = FixedTicker(ticks=list(range(0, biggestNumRep + 2)))
p.yaxis.axis_label = "No. of repositories"

repoDict = json.loads(response.text)
for entry in repoDict:
   repoNames.append(entry["name"])
radio = RadioButtonGroup(labels=repoNames, active=0)

response = requests.get("https://api.github.com/repos/" + usernameList[-1] + "/" + repoNames[radio.active] + "/languages", auth = (username, token))
languages = json.loads(response.text)
data = pd.Series(languages).reset_index(name='value').rename(columns={'index':'lang'})
data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = ["#1f77b4"]
pie = figure(plot_height=400, title=repoNames[0], toolbar_location=None, tools="hover", tooltips="@lang: @value", x_range=(-0.5, 1.0))
pie.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'), line_color="white", fill_color='color', legend_field='lang', source=data)
pie.axis.axis_label=None
pie.axis.visible=False
pie.grid.grid_line_color = None

# UPDATE USER

text.on_change('value', update_user)
radio.on_click(specific_repo)

graphs = column(text, radio, row(p, pie), width=1000)
curdoc().add_root(graphs)
curdoc().title = "BIG WORKY"