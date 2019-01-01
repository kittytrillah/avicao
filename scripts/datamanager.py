import os
import sqlite3

conn = sqlite3.connect("icao_db.db")
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


def getdata():
    for icao_i in icao:
        temp_array = dataparser.getairportdata(icao_i)
        print('/////////TEMP ARRAY//////////')
        print(temp_array)
        print('////////*************////////')
        setdb(temp_array[0],temp_array[1],temp_array[2],temp_array[3],temp_array[4],temp_array[5],temp_array[6],
              temp_array[7],temp_array[8],temp_array[9],temp_array[10],temp_array[11],temp_array[12])
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
