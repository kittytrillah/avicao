class DataParser:
    def getairportdata(self, icao_i):
        result_date = 'N/A'; result_dp = 0; result_pressure = 0; result_relhum = 0; result_temp = 0; result_tempo = 0;
        result_visibility = 0; result_windspd = 0; result_place = ''; result_overallconditions = 0; result_critwind = 0;
        result_crithumid = 0; result_crittemp = 0; result_coordinatex = 0; result_coordinatey = 0;
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
                else:
                    try:
                        result_place_temp = result_place + ':'
                        result_coordinates = result_place_temp[
                                             (result_place_temp.index(' (' + icao_i + ') ') + len(
                                                 ' (' + icao_i + ') ')):result_place_temp.index(
                                                 ':')]

                        result_split = re.split('[SN]+\s+', result_coordinates)
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
        return(icao_i, result_date, result_pressure, result_windspd, result_relhum,
               result_tempo, result_place, result_overallconditions, result_critwind, result_crithumid,
               result_crittemp, result_coordinatex, result_coordinatey)


import os
import sys
sys.path.insert(0, os.getcwd()+"/")
import sqlite3

conn = sqlite3.connect("icao_db.db")
dataparser = DataParser()
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


def recordtext(icao, info):
    f = open("static/" + icao + ".txt", "w+")
    f.write("" + info)
    f.close()
    return 'Done'
