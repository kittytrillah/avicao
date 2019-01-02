from __future__ import division, unicode_literals
import codecs
from flask import Flask, render_template, request, redirect, Response
import sys, os
sys.path.insert(0, os.getcwd()+"/static")
import datamanager as dm
import matplotlib.pyplot as plt
import requests
import re
import itertools
import sqlite3
import seaborn as sns
import base64
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from werkzeug.contrib.fixers import ProxyFix
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup as Soup
import atexit
import json
try:
    from StringIO import StringIO
except ImportError:
    import io as StringIO

app = Flask(__name__)
scheduler = BackgroundScheduler()
conn = sqlite3.connect("static/icao_db.db")


mapbox_access_token = 'pk.eyJ1Ijoia2l0dHl0cmlsbGFoIiwiYSI6ImNqajlzY3dydDB6aGMza3AyeDFscXppcDYifQ.aRIq9GQtJxSojfnkEf-xTg'


@app.route("/")
def hello():
    dm.clearjson()
    return render_template('index.html',
        mapbox_access_token=mapbox_access_token, r_long=0, r_lat=0)

@app.route('/favicon.ico')
def fav():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico')


@app.route('/plot.png')
def plotdraw(): #name=None

    # img = StringIO.BytesIO()
    # sns.set_style("dark") #E.G.
    #
    # y = [1,2,3,4,5]
    # x = [0,2,1,3,4]
    #
    # plt.plot(x,y)
    # plt.savefig(img, format='png')
    # img.seek(0)
    #
    # plot_url = base64.b64encode(img.getvalue())
    # #return render_template('page.html', plot_url=plot_url)

    fig = create_figure()
    output = StringIO.BytesIO()
    FigureCanvas(fig).print_png(output)
    #plot_url = output #base64.b64encode(output.getvalue())
    #return render_template('page.html', plot_url=plot_url)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig


@app.route('/', methods=['POST'])
def searchfor():
    print("////////////Search started/////////////")
    text = request.form['ss']
    print("text ===")
    print(text)
    datatoreceive = []
    conn = sqlite3.connect("static/icao_db.db")
    c = conn.cursor()
    lat = 0
    long = 0
    try:
        if len(text) > 3:
            if len(text) == 4:
                c.execute("SELECT * FROM currentvalues WHERE place=?", (text,))
                conn.commit()
                rows = c.fetchall()
                print(rows)
                if (rows[0]):
                    datatoreceive = rows[0]
                    lat = datatoreceive[11]
                    long = datatoreceive[12]
                    if(lat == 0 or long == 0):
                        #elements(datatoreceive[0])
                        return redirect("/reports/" + datatoreceive[0], code=302)
                    print("Grabbed a row:::")
                    print(datatoreceive)
                else:
                    c.execute("SELECT * FROM currentvalues WHERE aname LIKE ?", ('%' + text + '%',))
                    conn.commit()
                    rows = c.fetchall()
                    print(rows)
                    if (rows[0]):
                        datatoreceive = rows[0]
                        lat = datatoreceive[11]
                        long = datatoreceive[12]
                        if (lat == 0 or long == 0):
                            #elements(datatoreceive[0])
                            return redirect("/reports/" + datatoreceive[0], code=302)
                        print("Grabbed a row:::")
                        print(datatoreceive)
            else:
                c.execute("SELECT * FROM currentvalues WHERE aname LIKE ?", ('%' + text + '%',))
                conn.commit()
                rows = c.fetchall()
                print(rows)
                if (rows[0]):
                    datatoreceive = rows[0]
                    lat = datatoreceive[11]
                    long = datatoreceive[12]
                    if (lat == 0 or long == 0):
                        #elements(datatoreceive[0])
                        return redirect("/reports/" + datatoreceive[0], code=302)
                    print("Grabbed a row:::")
                    print(datatoreceive)
        # for row in range(0, len(rows), 1):
        #     datatoreceive = rows[0]
        #     print("Grabbed a row")
        #     print(datatoreceive)
        #     pass
    except Exception as err:
        print(err)
        pass
    return render_template('index.html',
                           mapbox_access_token=mapbox_access_token, r_long=long, r_lat=lat)



@app.route('/reports/')
@app.route('/reports/<name>')
def elements(name=None):
    data = []
    data = getdatabyicao(name)
    print("///////////////RECEIVED DATA///////////////")
    print(data)
    result = '''<!doctype html>
    <title>''' + name + '''Weather Report</title>'''
    result += '<h2>Weather Report: ' + name + ' Date: ' + data[1] + ' </h2><h3>///' + str(data[6]) + '///</h3>'
    result += '<h3>Weather condition: ' + str((4 - data[7])*25) + '%</h3>'
    result += '<p>Pressure: ' + str(data[2]) + ' milliBars</p>'
    result += '<p>Wind: ' + str(data[3]) + ' knots</p>'
    result += '<p>Humidity: ' + str(data[4]) + '%</p>'
    result += '<p>Temperature: ' + str(data[5]) + 'F</p>'
    result += '<p>Latitude: ' + str(data[11]) + 'F</p>'
    result += '<p>Longitude: ' + str(data[12]) + 'F</p>'
    return result


def getdatabyicao(icao_get):
    datatoreceive = []
    conn = sqlite3.connect("static/icao_db.db")
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM currentvalues WHERE place=?", (icao_get,))
        conn.commit()
        rows = c.fetchall()
        for row in rows:
            datatoreceive = row
            print(row)
    except Exception as err:
        print(err)
        pass
    return datatoreceive


def createhtml_icaolist():
    f = codecs.open("templates/index.html", 'r', 'utf-8')
    document = Soup(f.read(), "html.parser").get_text()
    print(document)
    soup = Soup(document, "html.parser")
        # title = soup.find('title')
        # meta = soup.new_tag('meta')
        # meta['content'] = "text/html; charset=UTF-8"
        # meta['http-equiv'] = "Content-Type"
        # title.insert_after(meta)
    print(soup)

    return 'Done'


def refreshdata():
    dm.clearjson()
    return 'Done'


def getuip():
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)


def aircrafrparams():
    return 'Done'


scheduler.add_job(func=refreshdata, trigger="interval", minutes=60)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
    app.run(host='194.87.147.155')
