from __future__ import division, unicode_literals
import codecs
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import matplotlib.pyplot as plt
import requests
import re
import itertools
import sqlite3
import seaborn as sns
import base64
import random
import os
from flask import Response
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
conn = sqlite3.connect("icao_db.db")

# Input values
wind_crit = 17.3 #20 MPH
humid_crit = 90
temp_crit = 19.4 #-7C
icao = ['KMSV','MYNN','KM40','KJHN','CWSL','KEGV','SBAA','KNYG','OOSH','SBIZ','SBKP','RJOT','SEMT','SBGL','NTAA','MGMM',
             'KGDV','KFNT','ESDF','KGVL','KJSL','EPMO','K1IN','KLNC','MDAB','CYQZ','K1JN','PPNU','PAMM','KVAF','LTAP','KDYS','K1JM','CXMM','KMYR','KFLY','MRLM','KDMN','CWXL','KFIT','KW75','LEMH','PAMC','KCKZ','KHOT',
             'DAAV','LRBO','YESP','KBUY','EDQM','KDFI','CYYB','KMCJ','KSZL','SLJE','K1MW','CWBU','KETN','KMYV','KLWB', 'KFIG', 'KIOB', 'MMQT', 'CYOY', 'KENL', 'SKSP', 'CWMM', 'KS52', 'KGYL', 'KSGJ', 'KEVU', 'VTCC',
          'GMFM', 'GMTN', 'KCTY', 'CYFO', 'CWID', 'PAVC', 'KSTC', 'SBGR', 'CXEC', 'YMTG', 'MTPP', 'KJVL', 'VEJH',
          'ROYN', 'SKIP', 'KTTA', 'NZFX']
link = 'http://tgftp.nws.noaa.gov/data/observations/metar/decoded/{}.TXT'
add_link = 'https://weather.gladstonefamily.net/site/{}' #use this link to get additional data & history

mapbox_access_token = 'pk.eyJ1Ijoia2l0dHl0cmlsbGFoIiwiYSI6ImNqajlzY3dydDB6aGMza3AyeDFscXppcDYifQ.aRIq9GQtJxSojfnkEf-xTg'

@app.route("/")
def hello():
    # clearjson()
    # getdata()
    #plotdraw()
    #createhtml_icaolist()
    return render_template('index.html',
        mapbox_access_token=mapbox_access_token, r_long=0, r_lat=0)

@app.route('/favicon.ico')
def fav():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico')


def getdata():
    for icao_i in icao:
        result_date = 'N/A'
        result_dp = 0
        result_pressure = 0
        result_relhum = 0
        result_temp = 0
        result_tempo = 0
        result_visibility = 0
        result_windspd = 0
        result_place = ''
        result_overallconditions = 0
        result_critwind = 0
        result_crithumid = 0
        result_crittemp = 0
        result_coordinatex = 0
        result_coordinatey = 0
        try:
            f = requests.get(link.format(icao_i))
            print(f)
        except Exception as err:
            print(err)
            return {"error": err}
        try:
            if f.text.split('\n')[0]:
                result_place = f.text.split('\n')[0]
                if 'Station name not' in result_place:
                    print('Station name not found. Proceed to alt parsing')
                    f_a = requests.get(add_link.format(icao_i))
                    print(f_a)
                    try:
                        result_place = f_a.text[
                                       (f_a.text.index('<title>METAR Information for ' + icao_i + ' in ') + len(
                                           '<title>METAR Information for ' + icao_i + ' in ')):f_a.text.index(
                                           '</title></head><body>\n<script type="text/javascript" src="https://ajax.googleapis')]
                    except Exception as err:
                        print(err)
                        pass
                    try:
                        result_place = f_a.text[
                                       (f_a.text.index('<title>NonFedAWOS Information for ' + icao_i + ' in ') + len(
                                           '<title>NonFedAWOS Information for ' + icao_i + ' in ')):f_a.text.index(
                                           '</title></head><body>\n<script type="text/javascript" src="https://ajax.googleapis')]
                    except Exception as err:
                        print(err)
                        pass
                    try:
                        substring_temp = f_a.text[
                                         (f_a.text.index('Latitude: ') + len('Latitude: ')):f_a.text.index(
                                             '(LORAN)')]
                        print(substring_temp)
                        result_coordinatex = substring_temp[
                                             (substring_temp.index('(deg min sec), ') + len(
                                                 '(deg min sec), ')):substring_temp.index(
                                                 '&deg; (decimal), ')]
                        print('///result_coordinatex')
                        print(result_coordinatex)
                    except Exception as err:
                        print(err)
                        pass
                    try:
                        substring_temp = f_a.text[
                                         (f_a.text.index('>\n<meta property="og:longitude" ') + len('>\n<meta property="og:longitude" ')):f_a.text.index(
                                             '>\n<meta property="og:type" content="landmark"')]
                        print(substring_temp)
                        result_coordinatey = substring_temp[
                                             (substring_temp.index('content="') + len(
                                                 'content="')):substring_temp.index(
                                                 '"/')]
                        print('///result_coordinatey')
                        print(result_coordinatey)
                    except Exception as err:
                        print(err)
                        pass
                else: #get coords from the name 'Tete, Mozambique (FQTE) 16-11S 033-35E 150M -> 78°55'44.29458"N ///55-07-52N
                    try:
                        result_place_temp = result_place + ':'
                        result_coordinates = result_place_temp[
                                             (result_place_temp.index(' (' + icao_i + ') ') + len(
                                                 ' (' + icao_i + ') ')):result_place_temp.index(
                                                 ':')]

                        result_split = re.split('[SN]+\s+', result_coordinates) #Sometimes it skips whitespace /// NEEDS A FIX
                        print(result_split)
                        sn_word = ""
                        we_word = ""
                        sn_part = ""
                        we_part = ""
                        whole_part_sn = ""
                        whole_part_we = ""
                        if result_coordinates.find("S") == -1:
                            sn_word = "N"
                            #"No 'S' here!"
                        else:
                            sn_word = "S"
                            #"Found 'S' in the string."
                        if result_coordinates.find("E") == -1:
                            we_word = "W"
                            #"No 'E' here!"
                        else:
                            we_word = "E"
                            #"Found 'E' in the string."
                        if len(result_split) == 2:
                            print("result split equals 2")
                            whole_part_sn = result_split[0].replace(" ", "")
                            whole_part_we = result_split[1].replace(" ", "").replace("W", "").replace("E", "")
                            list_sn_word = whole_part_sn.split("-")
                            print("list_sn_word ///")
                            if len(list_sn_word) == 2:
                                print("list_sn_word equals 2")
                                whole_part_sn = "" + list_sn_word[0] + "°" + list_sn_word[1] + "'" + '0"' + sn_word
                            else:
                                print("list_sn_word equals more")
                                whole_part_sn = "" + list_sn_word[0] + "°" + list_sn_word[1] + "'" + list_sn_word[2] + '"' + sn_word
                                print(whole_part_sn)
                            list_we_word = whole_part_we.split("-")
                            if len(list_we_word) == 2:
                                print("list_we_word equals 2")
                                whole_part_we = "" + list_we_word[0] + "°" + list_we_word[1] + "'" + '0"' + we_word
                            else:
                                print("list_we_word equals more")
                                whole_part_we = "" + list_we_word[0] + "°" + list_we_word[1] + "'" + list_we_word[2] + '"' + we_word
                                print(whole_part_we)
                            result_coordinatex = parse_dms(whole_part_sn)
                            result_coordinatey = parse_dms(whole_part_we)
                            print("Result Coordinatex DMS O DD")
                            print(result_coordinatex)
                            print("Result Coordinatey DMS O DD")
                            print(result_coordinatey)
                    except Exception as err:
                        print(err)
                        pass
                print(result_place)
        except Exception as err:
            print(err)
            return {"error": err}
        try:
            result_date = re.findall('/ (\d+.\d+.\d+) ', f.text)[0]
            print('date: ' + result_date)
        except Exception as err:
            print(err)
            return {"error": err}
        try:
            if re.findall('at (\d+) MPH', f.text):
                result_windspd = float(re.findall('at (\d+) MPH', f.text)[0])
                if result_windspd>wind_crit:
                    result_critwind = 1
            else:
                result_windspd = ""

        except Exception as err:
            print(err)
            return {"error": err}
        try:
            if re.findall('Relative Humidity: (\d+)%', f.text):
              result_relhum = float(re.findall('Relative Humidity: (\d+)%', f.text)[0])
              if result_relhum > humid_crit:
                  result_crithumid = 1
            else:
              result_relhum = ""
        except Exception as err:
            print(err)
            return {"error": err}
        try:
            if f.text.partition('Visibility: ')[-1].rpartition(':0'):
                result_visibility = f.text.partition('Visibility: ')[-1].rpartition(':0')[0]
            else:
                result_visibility = 'N/A'
        except Exception as err:
            print(err)
            return {"error": err}
        try:
            if f.text.partition('Dew Point: ')[-1].rpartition('\nRelative '):
                result_dp = f.text.partition('Dew Point: ')[-1].rpartition('\nRelative ')[0]
            else:
                result_dp = 0
        except Exception as err:
            print(err)
            return {"error": err}
        try:
            result_pressure = re.search('([0-9]{3,5})( hPa)', f.text, re.MULTILINE)
            if result_pressure is None:
                result_pressure = ""
            else:
                result_pressure = float(re.search('([0-9]{3,5})( hPa)', f.text, re.MULTILINE).group(1))
        except Exception as err:
            print(err)
            return {"error": err}
        try:
            result_temp = re.search('(Temperature: )([0-9]{0,2})', f.text, re.MULTILINE)
            if result_temp is None:
                result_tempo = ""
                print("None")
            qwe = result_temp.group(0)
            result_tempo = ""
            val = re.search(r'\d+', qwe)
            if val is None:
                print("None")
            else:
                result_tempo = float(re.search(r'\d+', qwe).group())
                if result_tempo < temp_crit:
                    result_crittemp = 1
        except Exception as err:
            print(err)
            pass
        result_overallconditions = result_crittemp + result_crithumid + result_critwind
        result_place = result_place + " ICAO: " + icao_i
        result_info = ""
        midval = 100 - result_overallconditions*33
        result_info = "" + result_place + " Weather condition: " + str(100 - result_overallconditions*33) + "%"
        print("***-------------------------------***")
        print(icao_i)
        print(result_place)
        print(result_date)
        print(result_pressure)
        print(result_windspd)
        print(result_relhum)
        print(result_tempo)
        print(result_coordinatex)
        print(result_coordinatey)
        print("///-------------------------------///")
        recordtext(icao_i, result_info)
        setdb(icao_i, result_date, result_pressure, result_windspd, result_relhum, result_tempo, result_place, result_overallconditions, result_critwind, result_crithumid, result_crittemp, result_coordinatex, result_coordinatey)
    return 'Test'


def setdb(place, rdate, pressure, wind, humidity, temperature, name, crit_sum, crit_w, crit_h, crit_t, result_coordinatex, result_coordinatey):
    conn = sqlite3.connect("icao_db.db")
    c = conn.cursor()
    c.execute("Create TABLE if not exists %s (rdate TEXT,pressure FLOAT,wind FLOAT,humidity FLOAT, temperature FLOAT, name TEXT, crit_overall FLOAT, crit_wind FLOAT, crit_humidity FLOAT, crit_temperature FLOAT)"
              % place)
    try:
        c.execute("INSERT INTO %s VALUES (?,?,?,?,?,?,?,?,?,?)" % place, (rdate, pressure, wind, humidity, temperature, name, crit_sum, crit_w, crit_h, crit_t))
        conn.commit()
    except Exception as err:
        print(err)
        pass
    setuniquedb(place, rdate, pressure, wind, humidity, temperature, name, crit_sum, crit_w, crit_h, crit_t, result_coordinatex, result_coordinatey)
    return 'Print'


def setuniquedb(place, rdate, pressure, wind, humidity, temperature, name, crit_sum, crit_w, crit_h, crit_t, result_coordinatex, result_coordinatey):
    conn = sqlite3.connect("icao_db.db")
    c = conn.cursor()
    try:
        c.execute("Create TABLE if not exists currentvalues (place TEXT,rdate TEXT,pressure FLOAT,wind FLOAT,humidity FLOAT, temperature FLOAT, aname TEXT, crit_overall FLOAT, crit_wind FLOAT, crit_humidity FLOAT, crit_temperature FLOAT, result_coordinatex FLOAT, result_coordinatey FLOAT)")
    except Exception as err:
        print(err)
        pass
        #c.execute('UPDATE currentvalues SET rdate = ' + str(rdate) + ', pressure = ' + pressure + ', wind = ' + wind + ', humidity = ' + humidity + ', temperature = ' + temperature + ', aname = ' + str(name) + ' WHERE place =?', (place[1]))
    try:
        c.execute("DELETE FROM currentvalues WHERE place=?", (place,))
        conn.commit()
        c.execute("INSERT INTO currentvalues VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",(place, rdate, pressure, wind, humidity, temperature, name, crit_sum, crit_w, crit_h, crit_t, result_coordinatex, result_coordinatey))
        conn.commit()
    except Exception as err:
        print(err)
        pass
    createjson(place, rdate, pressure, wind, humidity, temperature, name, crit_sum, crit_w, crit_h, crit_t, result_coordinatex, result_coordinatey)
    return 'Print'


def clearjson():
    data = {}
    data['features'] = []
    if os.path.exists("static/data.geojson"):
        os.remove("static/data.geojson")
    else:
        print("The file does not exist")
    with open('static/data.geojson', 'w') as outfile:
        json.dump(data, outfile)
    getdata()
    return 'Done'


def createjson(place, rdate, pressure, wind, humidity, temperature, name, crit_sum, crit_w, crit_h, crit_t, result_coordinatex, result_coordinatey):
    print("JSON created")
    crit_w_json = ''
    crit_h_json = ''
    crit_t_json = ''
    fincoordx = truncate(result_coordinatex, 4)
    fincoordy = truncate(result_coordinatey, 4)
    crit_sum_json = 'Weather condition: ' + str(4-crit_sum) + "/4"
    if crit_w == 1:
        crit_w_json = 'Critical wind value'
    else:
        crit_w_json = 'Wind value is OK'
    if crit_h == 1:
        crit_h_json = 'Critical humidity value'
    else:
        crit_h_json = 'Humidity value is OK'
    if crit_t == 1:
        crit_t_json = 'Critical temperature value'
    else:
        crit_t_json = 'Temperature value is OK'

    json_dir = open('static/data.geojson').read()
    data = json.loads(json_dir)
    data['features'].append({
        "type": "Feature",
        "properties": {
            "icon": crit_sum,
            "title": name,
            "icao": place,
            "crit_w": crit_w_json,
            "crit_h": crit_h_json,
            "crit_t": crit_t_json,
            "crit_sum": crit_sum_json,
            "crit_w_val": crit_w,
            "crit_h_val": crit_h,
            "crit_t_val": crit_t,
            "crit_sum_val": crit_sum
        },
        "geometry": {
            "type": "Point",
            "coordinates": [
                fincoordx,
                fincoordy
            ]
        }
    })

    with open('static/data.geojson', 'w') as outfile:
        json.dump(data, outfile)
    return 'Done'


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
    conn = sqlite3.connect("icao_db.db")
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
    conn = sqlite3.connect("icao_db.db")
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


def recordtext(icao, info):
    f = open("static/" + icao + ".txt", "w+")
    f.write("" + info)
    f.close()
    return 'Done'


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


def dms2dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if direction == 'W' or direction == 'S':
        dd *= -1
    return dd


def dd2dms(deg):
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]


def parse_dms(dms):
    print("parse dms")
    parts = re.split('[^\d\w]+', dms)
    print(parts)
    lat = dms2dd(parts[0], parts[1], parts[2], parts[3])

    return lat


def refreshdata():
    clearjson()
    return 'Done'


def truncate(f, n):
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


def getactiveairports():
    return 'Done'


def getuip():
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)


scheduler.add_job(func=refreshdata, trigger="interval", minutes=1440)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

app.wsgi_app = ProxyFix(app.wsgi_app)
if __name__ == '__main__':
    app.run(host='http://194.87.147.155/')
