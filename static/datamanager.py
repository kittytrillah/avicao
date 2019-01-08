import os
import sys
sys.path.insert(0, os.getcwd()+"/")
import converter
import sqlite3
import json
import requests
import re


class DataParser:
    def getairportdata(self, icao_i):
        print('Airport data is getting')
        result_date = 'N/A'; result_dp = 0; result_pressure = 0; result_relhum = 0; result_temp = 0; result_tempo = 0;
        result_visibility = 0; result_windspd = 0; result_place = ''; result_overallconditions = 0; result_critwind = 0;
        result_crithumid = 0; result_crittemp = 0; result_coordinatex = 0; result_coordinatey = 0;
        result_hour = 25; result_minute = 61; result_date = ''
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
                            result_coordinatex = converter.parse_dms(whole_part_sn)
                            result_coordinatey = converter.parse_dms(whole_part_we)
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
            if f.text.partition(' / ')[-1].rpartition(' UTC\n'):
                res = f.text.partition(' / ')[-1].rpartition(' UTC\n')[0]
                respure = res.split()
                result_date = respure[0]
                restime = respure[1]
                result_hour = restime[0] + restime[1]
                if len(result_hour) > 1:
                    if result_hour[0] == '0':
                        result_hour = '' + result_hour[1]
                result_minute = restime[2] + restime[3]
                if len(result_minute) > 1:
                    if result_minute[0] == '0':
                        result_minute = '' + result_minute[1]
        except Exception as err:
            print(err)
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
        print(result_date)
        print(result_hour)
        print(result_minute)
        print("///-------------------------------///")
        recordtext(icao_i, result_info)
        return(icao_i, result_date, result_pressure, result_windspd, result_relhum,
               result_tempo, result_place, result_overallconditions, result_critwind, result_crithumid,
               result_crittemp, result_coordinatex, result_coordinatey, result_date, result_hour, result_minute)

conn = sqlite3.connect("icao_db.db")
dataparser = DataParser()
wind_crit = 17.3 #20 MPH
humid_crit = 90
temp_crit = 19.4 #-7C
icao = ['CWDT', 'CWIX', 'CWEE', 'CWKD', 'KC62', 'VOPB', 'FMCV', 'SADO', 'DNIB', 'SANU', 'HTGW', 'SACE', 'KSYM', 'SMZP', 'FVCZ', 'FVKB', 'FVMV', 'EDAH', 'MGTU', 'SAOU', 'SARM', 'SANL', 'SPAY', 'KM63', 'DTHL', 'CYKQ', 'KOQU', 'MSLU', 'CWHL', 'SAAP', 'SANC', 'NZFX', 'CWEP', 'SAAV', 'RJTK', 'RJFY', 'RJOE', 'RJOZ', 'SARS', 'VEDG', 'NFNR', 'FQQL', 'BIHU', 'OITK', 'NVSC', 'OERY', 'LIMV', 'DNGO', 'HESN', 'LKKU', 'SAWB', 'SPHZ', 'BIGR', 'GMMP', 'CYCA', 'GQNI', 'SATR', 'SBTD', 'SBPG', 'MMMV', 'KDLZ', 'KH78', 'VOMY', 'BGNS', 'PACZ', 'LESU', 'CYGH', 'SFAL', 'LIPK', 'LPAR', 'SLPO', 'FAGM', 'KPEZ', 'SADP', 'SBJE', 'SLOR', 'GQPA', 'GQPZ', 'KMGG', 'SGCO', 'SGSJ', 'SBCX', 'CXWB', 'BIHN', 'SVMG', 'SPHY', 'MHYR', 'MHNO', 'SBBG', 'SUCA', 'KTBX', 'KGDJ', 'SVBM', 'SBPC', 'SBNM', 'SBLP', 'SBGM', 'SBOI', 'SCIR', 'SCAS', 'SCCC', 'SCHR', 'SCFM', 'MTCH', 'SUSO', 'SLVM', 'CYAW', 'SBMS', 'SBTC', 'SBUF', 'SBAA', 'SBCC', 'SBCI', 'SBLB', 'SBUA', 'SBBW', 'KBKD', 'SPJE', 'SBPK', 'MMCT', 'SPJI', 'SPLO', 'SETU', 'SERB', 'SCGE', 'SCJO', 'SCMK', 'SBPP', 'SUDU', 'SEAM', 'CYFT', 'CYNC', 'TVSM', 'DNAA', 'SYLT', 'SYMB', 'SBPF', 'SBPR', 'SBAT', 'SBEK', 'SBHT', 'SBIC', 'SBIH', 'SBMY', 'SBTU', 'SGME', 'SGLV', 'SGPJ', 'SGPC', 'SGSP', 'SGGR', 'SGVR', 'SGPI', 'SAMR', 'SBCJ', 'MRLM', 'SBPB', 'KQZF', 'PANV', 'MDAB', 'SPGM', 'SPYL', 'SUAA', 'MHTE', 'PFYU', 'TDCF', 'SKMZ', 'SLRY', 'SLRQ', 'SLJO', 'SLCP', 'SLJE', 'CYSP', 'CYGT', 'CYXN', 'CYLU', 'CYTQ', 'CYKO', 'CYAS', 'CYIK', 'CYKG', 'CYLA', 'CYMU', 'CYZG', 'CYBV', 'TRPG', 'SETN', 'SBAX', 'SBGW', 'MBGT', 'K1V6', 'SBTF', 'TJIG', 'KPOC', 'MDBH', 'MDJB', 'MDCY', 'SBTT', 'MSAC', 'MHAM', 'PKMJ', 'TQPF', 'KBYH', 'SECA', 'SENL', 'SECO', 'SESM', 'SEMC', 'SPHO', 'SPMS', 'SPTU', 'SCGZ', 'SLMG', 'SLSA', 'SLCO', 'SLSI', 'SLRB', 'SLPS', 'SLCA', 'SLYA', 'MNPC', 'MNRS', 'MNJG', 'MNJU', 'MNCH', 'MNBL', 'SKPV', 'SKRH', 'SKEJ', 'SKMD', 'SKVV', 'SKPS', 'SKIP', 'SEJD', 'CYDA', 'CZFA', 'CYCS', 'CYJF', 'CYXP', 'CYXQ', 'CYAB', 'CYPG', 'CYFR', 'KAPG', 'CYHA', 'SBJR', 'SBVH', 'KOMN', 'MMBT', 'MRPV', 'SEST', 'SEGS', 'TKPN', 'TLPC', 'TDPD', 'SCRD', 'SCTB', 'CYOA', 'MGPB', 'MGSJ', 'MGRT', 'MGQZ', 'MGCB', 'MGZA', 'MGES', 'MGMT', 'SKPC', 'MHTR', 'MHPL', 'MHSR', 'MHGS', 'MHLE', 'MHCH', 'CYPC', 'KDPG', 'MWCB', 'MYGF', 'CYCP', 'CYGE', 'CYCQ', 'CYFO', 'CYXZ', 'CYKD', 'CYSY', 'CYWJ', 'CYLJ', 'CZFM', 'CZFN', 'CWSW', 'SESA', 'CPIR', 'NVVA', 'SBBI', 'CYMJ', 'KBVI', 'TJBQ', 'KIFP', 'PADG', 'HAAB', 'MSSA', 'MSSM', 'RJSH', 'MMPN', 'MMCE', 'MMPQ', 'MMCV', 'MMPG', 'MMCB', 'MMPA', 'TKPK', 'SCNT', 'MZBZ', 'MPBO', 'CWAE', 'CYBD', 'CYCG', 'CYZW', 'CYHI', 'CYLK', 'CYRA', 'CYSK', 'CYAZ', 'CYDC', 'CZST', 'SYEC', 'RJOF', 'KTIX', 'TUPJ', 'PTSA', 'KEKM', 'PAEC', 'PALJ', 'MMCN', 'MMGM', 'MMLT', 'MMMA', 'MMNL', 'MMRX', 'MMOX', 'MMPB', 'MMZO', 'SLAL', 'SERO', 'SKUC', 'SKUI', 'TVSA', 'CYND', 'CYRJ', 'CYLD', 'CYPL', 'CYSN', 'CYOC', 'CZMT', 'MMMT', 'VABV', 'VIBR', 'VEGK', 'VIKO', 'VILH', 'VIGG', 'VEBD', 'VIAG', 'VICG', 'VIGR', 'VIJU', 'VIAR', 'KHSA', 'VIDN', 'KBAK', 'VIDP', 'KRYN', 'MWCR', 'KEVB', 'KASG', 'VISR', 'VIDD', 'MBPV', 'KGEU', 'MPSM', 'MPPA', 'MPDA', 'MDLR', 'PARC', 'MMVA', 'MMEP', 'MMIA', 'MMDO', 'MMZH', 'KSCH', 'SPJL', 'SPME', 'SKVP', 'SKLC', 'SKAR', 'SKIB', 'SKNV', 'CYPW', 'CYGR', 'CYRL', 'MPMG', 'PAKU', 'KWHP', 'KEMT', 'KCGF', 'KGYR', 'KVCV', 'KCPC', 'KBCT', 'KTOA', 'KCHD', 'KJQF', 'PHJH', 'KUNV', 'SKBG', 'MMCS', 'MMCU', 'MMTC', 'MMPS', 'MMLM', 'KFTK', 'SKMR', 'CYVT', 'CYGK', 'LIBQ', 'SBCA', 'RJSU', 'YPMQ', 'SKCC', 'KCNW', 'PALP', 'KPAO', 'VEPY', 'PTPN', 'FHAW', 'MRLB', 'KGXF', 'MMCL', 'MMSL', 'MMTG', 'MMTM', 'MMVR', 'SPST', 'CYWH', 'CYCD', 'CYBL', 'CYZU', 'SKSM', 'DNEN', 'NVVW', 'HESC', 'VERP', 'SBCZ', 'SAOR', 'MHRO', 'MHLC', 'KCAV', 'PPIZ', 'SKPE', 'MMLP', 'MMSD', 'MMAS', 'MMLO', 'MMAN', 'MSSS', 'KRHV', 'LTBZ', 'FAIR', 'NFTL', 'VTSK', 'CYBB', 'CYUB', 'CWND', 'FMMS', 'LIVC', 'LIVF', 'GAKD', 'GAMB', 'GANR', 'DXSK', 'LIRT', 'RJTE', 'SBLE', 'GOOK', 'GOOD', 'FVJN', 'FVRG', 'KOWA', 'NFKD', 'HEAR', 'VEKO', 'FTTD', 'RJNY', 'FAEO', 'ENHV', 'ENMH', 'FADY', 'KMHR', 'MMCM', 'MMCP', 'PABR', 'LIPU', 'VAPR', 'RJAF', 'RJEB', 'RJTF', 'RJTI', 'RJTO', 'FYWH', 'WIEE', 'WAHQ', 'WAPP', 'RJSO', 'GOSP', 'DNMN', 'DNJO', 'FXMM', 'SBIL', 'SBDN', 'SBMK', 'CWUX', 'PTTP', 'SBML', 'SBMG', 'FNKU', 'VAAU', 'VOCP', 'VAID', 'MMIO', 'MPTO', 'ENVR', 'KFOE', 'NFTV', 'KMWN', 'RJCA', 'MUGM', 'KPKV', 'PAWS', 'PFKT', 'MTPP', 'NCRG', 'NCAT', 'NCMG', 'NCMK', 'NCMR', 'NCMH', 'NCPY', 'NCRK', 'LGTG', 'BGTL', 'PAED', 'FASB', 'MMZC', 'SAZM', 'YSNW', 'VEMR', 'FMNN', 'FMNM', 'FMSD', 'VGEG', 'DTMB', 'EGOW', 'LTAH', 'FQVL', 'OAJL', 'FABM', 'EGWC', 'FAEL', 'FAPN', 'LIRU', 'LICD', 'FQLC', 'FQTT', 'FMCH', 'KGTB', 'OIBV', 'OIFS', 'VOBM', 'OIAG', 'FMNA', 'LPOV', 'LPMR', 'LPMT', 'LPST', 'CYUT', 'KLXL', 'CTRA', 'CZHY', 'CWWE', 'CWNH', 'CWOY', 'CWHQ', 'CWHV', 'CWJH', 'CWVP', 'CWVQ', 'CWWA', 'CXBO', 'CWNE', 'CWOE', 'CWPE', 'CWAJ', 'CWPC', 'CWNZ', 'CWXI', 'CWEZ', 'CWGD', 'CWSD', 'CWSK', 'CWSL', 'CWSR', 'CWXL', 'CWYY', 'CXHM', 'CXKE', 'CWJI', 'CWJR', 'CWMQ', 'CXTO', 'CXZV', 'CZKD', 'CZZJ', 'OIMT', 'WMAU', 'WMBA', 'WMKA', 'WMKB', 'WMKC', 'WMKD', 'WMKI', 'WMKL', 'WMKM', 'WMKN', 'ULWC', 'UWLW', 'LIPA', 'LIBA', 'LIBN', 'LICZ', 'LIEB', 'LIEC', 'KRCA', 'OICM', 'GGOV', 'GOGS', 'GOTK', 'GOTT', 'GOGG', 'GUCY', 'NIUE', 'OOSH', 'LKVO', 'AYPY', 'AYNZ', 'AYMH', 'FYKT', 'FYOA', 'FYRN', 'FYWB', 'FYWW', 'FQNP', 'KBAB', 'LOAN', 'LOAV', 'WIMM', 'WABB', 'WIHH', 'VAUD', 'DNCA', 'DNMM', 'DNKN', 'DRRM', 'DRRN', 'DRRT', 'DRZA', 'DRZR', 'DGAA', 'DGSI', 'OEAB', 'OEAH', 'OEAR', 'OEBA', 'OEBH', 'OEDM', 'OEGN', 'OEGS', 'OEGT', 'OEHL', 'OEJB', 'OEKJ', 'OEDR', 'OEKM', 'OENG', 'OEPA', 'OERF', 'OERR', 'OESH', 'OESK', 'OETB', 'OETF', 'OETR', 'OEWD', 'OEWJ', 'OEYN', 'DNIL', 'DNKT', 'DNYO', 'DXXX', 'DXNG', 'DBBB', 'FTTJ', 'FTTY', 'FTTA', 'DFOO', 'DFFD', 'OTHH', 'GOOG', 'GOSM', 'WAQQ', 'WAOO', 'FCBB', 'FCPP', 'FKKD', 'FKYS', 'FKKR', 'FKKN', 'FKKL', 'FEFF', 'HCMF', 'HCMH', 'HCMM', 'HKKI', 'GOSS', 'UTFF', 'FGSL', 'FGBT', 'FPST', 'WMKE', 'LIBH', 'LIBV', 'LIBY', 'OIAI', 'OICJ', 'OIFK', 'OIGK', 'OIKO', 'OINB', 'OINK', 'OISA', 'OITU', 'CWDO', 'CWWS', 'CWRM', 'CWZS', 'CAHR', 'CXNP', 'CXMY', 'CXOX', 'CWNC', 'CWVU', 'CWGY', 'CWNQ', 'CWPR', 'CXDK', 'CXSE', 'CZRP', 'KNJM', 'SESG', 'YAYT', 'AZUH', 'FNCT', 'FNBG', 'FNSU', 'HKWJ', 'FDPP', 'FDST', 'FNGI', 'FNUB', 'HSPN', 'HSOB', 'HSNN', 'FTTC', 'YCDU', 'YCNM', 'YCOM', 'YDBY', 'YEML', 'YESP', 'YBHI', 'YBMK', 'YBNA', 'YBOK', 'YBPN', 'YGFN', 'YGTE', 'YGTH', 'YHUG', 'YKRY', 'YLEC', 'YLIS', 'YNBR', 'YNTN', 'YNWN', 'YOLD', 'YPBO', 'YRMD', 'FEFT', 'MUCL', 'SBAN', 'SBPJ', 'SBJU', 'SBKG', 'SBQV', 'SBCH', 'SBCO', 'SBJV', 'SBSM', 'SBIZ', 'SBSY', 'SBAF', 'SBAU', 'SBBH', 'SBBQ', 'SBBU', 'SBES', 'SBLS', 'SBME', 'SBMT', 'SBSC', 'SBSR', 'SBTA', 'SBUL', 'SBUR', 'KLAL', 'KS33', 'K40B', 'FNSA', 'FNMA', 'NFNA', 'FNSO', 'GOGK', 'HKNW', 'HRYR', 'CWDZ', 'CWEK', 'CZDB', 'CWXC', 'CWDM', 'CXLL', 'CXTN', 'CXYH', 'RKSM', 'GOOY', 'KCDD', 'FNHU', 'FNCA', 'FNUG', 'OIIS', 'VCBI', 'VRMM', 'VCRI', 'FNUE', 'FNMO', 'FNDU', 'VOPC', 'HDAM', 'CWJO', 'CWHP', 'CWWX', 'CWZL', 'CWZV', 'CXAF', 'CXDP', 'CXTV', 'CWME', 'CWQS', 'CWRU', 'CWWL', 'EGNX', 'ESIB', 'ESIA', 'OEAO', 'ENRM', 'ENBL', 'HTAR', 'HTBU', 'HTDA', 'HTDO', 'HTIR', 'HTKA', 'HTKJ', 'HTMG', 'HTMT', 'HTMU', 'HTMW', 'HTSO', 'HTSU', 'HTTB', 'HTZA', 'HKMO', 'HETR', 'HEIS', 'ETHN', 'ETSI', 'ETSL', 'ETGG', 'ETHF', 'ETNS', 'ETNT', 'ETSH', 'DIYO', 'DIBK', 'HEMM', 'HEAX', 'HELX', 'HEGN', 'HEPS', 'HESH', 'HEAT', 'HEBA', 'HEBL', 'HESG', 'HEMA', 'ETNN', 'CXAK', 'CXDB', 'CXWM', 'HKJK', 'DNPO', 'FAOR', 'LTAZ', 'FWKI', 'OTBD', 'CXMO', 'CXOL', 'CXVM', 'CZOL', 'CZPS', 'CXAG', 'VOND', 'LRSB', 'HKML', 'KOQN', 'DAAT', 'SBIP', 'SBST', 'SBYS', 'VYMD', 'ETHL', 'KMKT', 'CXAJ', 'KAMN', 'KOEO', 'VEBN', 'UNAA', 'UNBB', 'UNEE', 'UNKL', 'UNNT', 'UNOO', 'UNTT', 'USTR', 'USHH', 'K3D2', 'PAEM', 'GOBD', 'GABS', 'GQNO', 'YPLM', 'YPTN', 'YPCC', 'YCFS', 'YPAD', 'YPDN', 'YPPH', 'YSSY', 'UTNN', 'UTNU', 'UTSA', 'UTSB', 'UTSK', 'UTSS', 'UTST', 'UTTT', 'YPKU', 'WAAA', 'WIDD', 'WARR', 'WADD', 'YLHI', 'VEBI', 'YPWR', 'YPJT', 'YHID', 'YGEL', 'YGLA', 'WATT', 'WAHS', 'WIBB', 'WIPP', 'WALL', 'HKEL', 'EISG', 'CWCI', 'CXAT', 'CWNL', 'CWPS', 'CZMU', 'CWMZ', 'CWEF', 'UTFN', 'LATI', 'ESNX', 'SBBV', 'KRUQ', 'FACV', 'ESNL', 'MNMG', 'ETNG', 'KFPK', 'EGEO', 'KCQT', 'KBRY', 'KLUX', 'KOIN', 'KRYY', 'KJDN', 'EKVG', 'EVRA', 'MYNN', 'EYKA', 'MHLM', 'MHTG', 'PTRO', 'KANK', 'KBNL', 'KD57', 'KGAF', 'PGRO', 'SBPS', 'SBEG', 'EYSA', 'EYPA', 'EETN', 'EYVI', 'ENAL', 'ENCN', 'ENHD', 'ENRO', 'ENRY', 'ENSB', 'ENTC', 'ENTO', 'ENAN', 'ENBR', 'ENBO', 'ENDU', 'ENGM', 'ENOL', 'ENVA', 'ENZV', 'KMVE', 'EFHK', 'EFTP', 'EFTU', 'EFVA', 'EFOU', 'EFRO', 'EFMA', 'EFIV', 'MSLP', 'VNKT', 'SBSL', 'EGNO', 'SBAR', 'ESUT', 'ETNH', 'SBSP', 'EKSP', 'EKKA', 'SBRF', 'SBBE', 'EVVA', 'EVLA', 'LSGC', 'LSGS', 'LSZG', 'LSZR', 'LSZS', 'LSZC', 'LSZL', 'LSZH', 'LSGG', 'LSZB', 'LSZA', 'EEEI', 'FJDG', 'OAMS', 'OJAM', 'ORBD', 'LHPA', 'KBML', 'KDAG', 'KDYA', 'KEOE', 'KGYH', 'KOCF', 'KOXC', 'KRCX', 'KSLK', 'KSPF', 'KTPL', 'PAMD', 'SBSV', 'ETMN', 'SBMO', 'KSNT', 'KBVE', 'PKMR', 'KP58', 'KATT', 'SBFN', 'LMML', 'EKRN', 'EKCH', 'EKEB', 'EKRK', 'EKAH', 'EKYT', 'EKBI', 'SBSJ', 'EKSN', 'EKSB', 'EKVD', 'EKOD', 'EKVJ', 'SBSG', 'KEWR', 'KGGE', 'KHDO', 'KHSE', 'KHTS', 'KIGM', 'KILG', 'KJCT', 'KJFK', 'KLCI', 'KLGA', 'KLGU', 'KMCJ', 'KMCX', 'KMNI', 'KMYL', 'KORD', 'KORF', 'KOXR', 'KPCZ', 'KPHX', 'KPIT', 'KPVD', 'KROW', 'KS32', 'KSAD', 'KSAN', 'KSAT', 'KSEM', 'KSJT', 'KSMO', 'KSMX', 'KSTL', 'KVCT', 'KVNW', 'KYNG', 'K74V', 'K96D', 'KABE', 'KACT', 'KAHN', 'KALB', 'KAQP', 'KAQW', 'KAVX', 'KBDL', 'KBGD', 'KBHK', 'KBKW', 'KCAK', 'KCCA', 'KCFV', 'KCLE', 'KCMH', 'KCON', 'KCRP', 'KCSG', 'KEKN', 'KELP', 'KERI', 'KEST', 'LSMA', 'LSMD', 'LSMP', 'LSMS', 'ESGG', 'ESGJ', 'ESGT', 'ESMK', 'ESMQ', 'ESMS', 'ESMT', 'ESMX', 'ESTA', 'ESTL', 'SBMN', 'EDDF', 'EDDH', 'EDDK', 'EDDL', 'EDDM', 'EDDN', 'EDDS', 'EDDT', 'EDDV', 'BGSF', 'BGBW', 'BGGH', 'BGJN', 'BGKK', 'EDDB', 'EDDC', 'EDDE', 'EDDG', 'EDDP', 'EDDR', 'EDDW', 'PABA', 'EGUB', 'LHSN', 'OPMT', 'EFJY', 'EFKU', 'EFHA', 'EFKK', 'EFPO', 'EFJO', 'EFMI', 'EFSA', 'EFSI', 'EFUT', 'EFET', 'EFKE', 'EFKI', 'EFKS', 'EFKT', 'EFLP', 'KP69', 'KCZZ', 'KREO', 'MDST', 'MDPC', 'MDSD', 'KNFW', 'KCDJ', 'KNRB', 'KBAN', 'KN60', 'KP59', 'LLBG', 'EGGD', 'EGGP', 'EGHI', 'EGNT', 'EGNV', 'EGHH', 'EGKA', 'EGKB', 'EGLF', 'EGMC', 'EGMD', 'EGTC', 'EGAA', 'EGAC', 'EGFF', 'EGGW', 'EGLC', 'EGNM', 'EGPD', 'EGBJ', 'EGCK', 'EGCN', 'EGSC', 'EGHC', 'EGHE', 'EGHQ', 'EGJA', 'EGJB', 'EGJJ', 'EGTE', 'EGBB', 'EGKK', 'EGPF', 'EGPH', 'EGPK', 'EGSS', 'EGAE', 'EGNH', 'EGNJ', 'EGNR', 'EGPE', 'EGPN', 'EGPI', 'ESNG', 'ESNK', 'ESNO', 'ESNQ', 'ESNS', 'ESNU', 'ESNZ', 'ESGR', 'ESKM', 'ESNV', 'ESST', 'ESUP', 'ESND', 'ESKN', 'ESOE', 'ESOK', 'ESOW', 'ESSA', 'ESSB', 'ESSD', 'ESSP', 'ESSV', 'LWSK', 'EGPU', 'EGPA', 'EGPC', 'EGPL', 'EGPO', 'EGNS', 'LEMO', 'ESCF', 'ESDF', 'ESPA', 'ESPE', 'ESSL', 'ESCM', 'UBEE', 'EGEC', 'EGTK', 'WIOO', 'OSDI', 'OSLK', 'OSKL', 'KHIE', 'KHLC', 'KHUT', 'KHXD', 'KIAD', 'KIEN', 'KIJD', 'KISN', 'KLKV', 'KLND', 'KLNL', 'KLRY', 'KLUM', 'KLWC', 'KMBG', 'KMCW', 'KMEB', 'KMFD', 'KMHK', 'KMKE', 'KMLF', 'KMLI', 'KMPO', 'KMWH', 'KOKB', 'KOKC', 'KOLF', 'KOMA', 'KORE', 'KOTM', 'KPNC', 'KPPF', 'KPWK', 'KPYM', 'KRAP', 'KRUG', 'KSGF', 'KSPI', 'KSPS', 'KSUX', 'KTAN', 'KTOL', 'KTRM', 'KTVY', 'KVTI', 'KVTN', 'KXVG', 'PGWT', 'K1P1', 'K2J9', 'KABI', 'KABQ', 'KALS', 'KARR', 'KATL', 'KBDR', 'KBIS', 'KBLF', 'KBLH', 'KBLU', 'KCID', 'KCKI', 'KCKV', 'KCLS', 'KCNU', 'KCNY', 'KCVG', 'KDCA', 'KDDC', 'KDPA', 'KDVN', 'KEOK', 'KFLD', 'KGGW', 'KGLS', 'LCRA', 'KQWX', 'KEFD', 'PASD', 'PATA', 'SBBR', 'EGPB', 'BKPR', 'LEJR', 'KNUI', 'KNIP', 'KOQT', 'KSDB', 'OKBK', 'TJNR', 'KNQX', 'KCQC', 'NSTU', 'KMWT', 'LLET', 'LLHA', 'LLIB', 'LLOV', 'LLSD', 'SBCB', 'EBAW', 'EBBR', 'EBCI', 'EBLG', 'EBOS', 'ELLX', 'LOWW', 'LOWL', 'LOWS', 'LOWI', 'LOWG', 'LOWK', 'LOXZ', 'ENAT', 'ENEV', 'ENFL', 'ENKB', 'ENKR', 'ENML', 'ENNA', 'LGAL', 'LGKV', 'LGMT', 'LGPZ', 'LGRX', 'LGSK', 'LGSR', 'LGZA', 'LGAD', 'LGKL', 'LGKO', 'LGLM', 'LGSA', 'LGSM', 'LGTS', 'ENNE', 'ENQR', 'ENSE', 'ENQC', 'ENQA', 'ENHM', 'ENLA', 'ENUG', 'ENWV', 'ENMS', 'ENRS', 'ENSK', 'ENSO', 'ENST', 'ENVD', 'EEKA', 'EEKE', 'EETU', 'EEPU', 'LGBL', 'LGKC', 'LGKF', 'LGKP', 'LGKZ', 'LGMK', 'LGNX', 'LGPA', 'LGSO', 'LIBD', 'LIBR', 'LICC', 'LICJ', 'LIPB', 'LIPE', 'LIPH', 'LIPQ', 'LIPR', 'LIPX', 'LIPZ', 'SBNT', 'ENOV', 'ENSD', 'ENSG', 'ENSR', 'ENSS', 'BIIS', 'ENLE', 'ENGC', 'ENHE', 'ENOA', 'ENSL', 'ENFB', 'ENSF', 'ENUN', 'ENBS', 'ENHK', 'ENNM', 'ENNO', 'ENBN', 'ENBV', 'ENHF', 'ENRA', 'ENSH', 'LIEA', 'LIEE', 'LIEO', 'LIMC', 'LIME', 'LIMF', 'LIMJ', 'LIML', 'LIRA', 'LIRF', 'LIRN', 'LIRP', 'LIRQ', 'ETWM', 'EGYD', 'KQVF', 'LRBO', 'LRCT', 'LRTZ', 'PAOM', 'PAOR', 'PAOT', 'PAPB', 'PASN', 'PASO', 'PATK', 'PATO', 'PAVL', 'PAWI', 'PHJR', 'PHNL', 'K2V5', 'KABR', 'KABY', 'KACK', 'KACV', 'KADG', 'KAEX', 'KAFW', 'KAGC', 'KAGS', 'KAIA', 'KAIK', 'KAKO', 'KALW', 'KAMA', 'KAMW', 'KANB', 'KAOH', 'KAOO', 'KAPA', 'KAPF', 'KARA', 'KASD', 'KASE', 'KASX', 'KATY', 'KBPI', 'KBPK', 'KBPT', 'KBRD', 'KBRL', 'KBRO', 'KBTL', 'KBTM', 'KBTR', 'KBUR', 'KBVO', 'KBVY', 'KBWG', 'KBYG', 'KBYI', 'KC35', 'KCAG', 'KCCR', 'KCCY', 'KCDC', 'KCDR', 'KCDS', 'KCDW', 'KCEW', 'KCEZ', 'KCHA', 'KCHO', 'KCKB', 'GVAC', 'ZMUB', 'PAAQ', 'PABE', 'PABI', 'PABT', 'PACD', 'PACV', 'PADE', 'PADQ', 'PAEG', 'PAEN', 'PAFA', 'PAGK', 'PAGY', 'PAHO', 'PAIL', 'PAKP', 'PAKT', 'PAKV', 'PAKW', 'PALH', 'PAMC', 'PAMR', 'PANC', 'PANN', 'PHTO', 'PHKO', 'PHLI', 'KAWM', 'KAXN', 'KAZO', 'KBAF', 'KBBW', 'KBCE', 'KBDE', 'KBEH', 'KBFD', 'KBFF', 'KBFI', 'KBGM', 'KBGR', 'KBHM', 'KBIL', 'KBIV', 'KBKE', 'KBKL', 'KBLI', 'KBMG', 'KBMQ', 'KBNA', 'KBNO', 'KBOI', 'KCLM', 'KCMI', 'KCMX', 'KCNM', 'KCNO', 'KCPR', 'KCQX', 'KCRE', 'KCRG', 'KCRQ', 'KCRS', 'KCSM', 'KCSV', 'KCUB', 'KCUT', 'KCYS', 'KDAB', 'KDAL', 'KDAN', 'KDBQ', 'KDCU', 'KDEN', 'KDEQ', 'KDET', 'KDEW', 'KDFI', 'EGQM', 'EGVN', 'EGXW', 'EGXZ', 'EGWU', 'EGXT', 'EGOM', 'EGOS', 'MDPP', 'OJAQ', 'SBPV', 'EDFH', 'EDFM', 'EDLV', 'EDVK', 'EDHI', 'EDHK', 'EDJA', 'EDMO', 'EDTL', 'EDTY', 'EDVE', 'EDXW', 'EDOP', 'EDAC', 'EDGS', 'EDHL', 'EDLN', 'EDLP', 'EDLW', 'EDMA', 'EDNY', 'EDQM', 'EDSB', 'KDFW', 'KDGW', 'KDHN', 'KDHT', 'KDKK', 'KDLN', 'KDLS', 'KDMN', 'KDMO', 'KDNL', 'KDRO', 'KDRT', 'KDTN', 'KDTO', 'KDTS', 'KDUJ', 'KDVT', 'KDWH', 'KDXR', 'KDYB', 'KECP', 'KEEO', 'KEET', 'KELD', 'KELM', 'KELN', 'KELY', 'KEMP', 'KFTY', 'KFUL', 'KFVE', 'KFWN', 'KFXE', 'KFYV', 'KGAG', 'KGCC', 'KGEG', 'KGEY', 'KGEZ', 'KGFK', 'KGFL', 'KGGG', 'KGIF', 'KGJT', 'KGKJ', 'KGKY', 'KGLD', 'KGLH', 'KGLR', 'KGMU', 'KGNV', 'KGOK', 'KGRB', 'KGRI', 'KGRR', 'KGSH', 'KHTL', 'KHUF', 'KHUL', 'KHVN', 'KHVR', 'KHWO', 'KHYR', 'KHZY', 'KIAG', 'KIAH', 'KICR', 'KICT', 'KIDA', 'KILM', 'KIML', 'KINF', 'KINK', 'KIPL', 'KITR', 'KIXD', 'KJBR', 'KJEF', 'KJER', 'KJKL', 'KJLN', 'KJSO', 'KLAA', 'KLAN', 'KLAR', 'KLWV', 'KLXT', 'KLXV', 'KM25', 'KMAE', 'KMAF', 'KMAI', 'KMAW', 'KMBS', 'KMCB', 'KMCE', 'KMCI', 'KMCK', 'KMCN', 'KMCO', 'KMDW', 'KMFR', 'KMGM', 'KMGW', 'KMGY', 'KMHT', 'KMIA', 'KMIC', 'KMIW', 'KMKL', 'KMKO', 'KMLB', 'KMLC', 'KOGD', 'KOGS', 'KOJC', 'KOMK', 'KONO', 'KONT', 'KOPF', 'KORL', 'KOSH', 'KOWD', 'KPAE', 'KPAH', 'KPBF', 'KPBG', 'KPBI', 'KPDK', 'KPDT', 'KPDX', 'KPEA', 'KPEO', 'KPGA', 'KPGD', 'KPIE', 'KRHI', 'KRIL', 'KRIW', 'KRKP', 'KRKS', 'KRME', 'KRMG', 'KRNM', 'KRNT', 'KRQE', 'KRSL', 'KRSW', 'KRTN', 'KRUE', 'KRVS', 'KRWF', 'KRWI', 'KRWL', 'KRXE', 'KSAC', 'KSAF', 'KSBA', 'KSBM', 'KSDL', 'KSDM', 'KSEA', 'KSEG', 'TISX', 'TIST', 'KTIW', 'KTKI', 'KTLH', 'KTMB', 'KTOP', 'KTOR', 'KTPA', 'KTRI', 'KTRL', 'KTTD', 'KTTN', 'KTUL', 'KTUP', 'KTUS', 'KTVC', 'KTVL', 'KTVR', 'KTWF', 'KTXK', 'KTYR', 'KTYS', 'KUAO', 'KUIL', 'KUNO', 'KVCB', 'KVEL', 'KVGT', 'KENW', 'KEPH', 'KEQY', 'KESF', 'KEVW', 'KEWB', 'KEYW', 'KFAR', 'KFAT', 'KFAY', 'KFCM', 'KFDR', 'KFDY', 'KFFC', 'KFFT', 'KFHR', 'KFLL', 'KFLO', 'KFMN', 'KFMY', 'KFNB', 'KFNT', 'KFOK', 'KFPR', 'KFRG', 'KFSM', 'KFST', 'KFTW', 'KLAW', 'KLAX', 'KLBB', 'KLBF', 'KLBO', 'KLBX', 'KLCH', 'KLFK', 'KLFT', 'KLGB', 'KLHQ', 'KLHX', 'KLIT', 'KLKR', 'KLLQ', 'KLMT', 'KLNS', 'KLOL', 'KLOU', 'KLOZ', 'KLPR', 'KLSE', 'KLVJ', 'KLVK', 'KLVM', 'KLVS', 'KLWD', 'KGSP', 'KGTF', 'KGUP', 'KGUY', 'KGVL', 'KGWO', 'KGZH', 'KHAO', 'KHBG', 'KHBR', 'KHEI', 'KHFD', 'KHGR', 'KHHR', 'KHIB', 'KHIO', 'KHJO', 'KHKA', 'KHKS', 'KHKY', 'KHLG', 'KHLN', 'KHOT', 'KHOU', 'KHQM', 'KHRI', 'KHRO', 'KHSI', 'KHSV', 'KMLS', 'KMLT', 'KMLU', 'KMMK', 'KMMV', 'KMNN', 'KMOD', 'KMOT', 'KMPZ', 'KMRB', 'KMSL', 'KMSN', 'KMSO', 'KMSP', 'KMSS', 'KMSY', 'KMTH', 'KMTJ', 'KMTO', 'KMVY', 'KMWL', 'KMYF', 'KMYV', 'KNEW', 'KOAK', 'KODO', 'KODX', 'KOGB', 'KSFB', 'KSFF', 'KSGR', 'KSHN', 'KSHR', 'KSIY', 'KSJC', 'KSLN', 'KSMF', 'KSMQ', 'KSNA', 'KSNS', 'KSNY', 'KSPB', 'KSPG', 'KSPW', 'KSSF', 'KSTC', 'KSTJ', 'KSTP', 'KSTS', 'KSVC', 'KSWO', 'KTCC', 'KTCL', 'KTCS', 'KTHV', 'KPIH', 'KPIR', 'KPKB', 'KPKD', 'KPLN', 'KPMD', 'KPMP', 'KPNS', 'KPOF', 'KPOU', 'KPQL', 'KPRB', 'KPRC', 'KPRO', 'KPSC', 'KPSF', 'KPSO', 'KPSP', 'KPSX', 'KPTK', 'KPTS', 'KPUB', 'KPUC', 'KPUW', 'KPWA', 'KRAC', 'KRAL', 'KRBD', 'KRBG', 'KVIH', 'KVLD', 'KVPC', 'KVRB', 'KVUO', 'KWRL', 'KWVI', 'KXNA', 'KY51', 'KYIP', 'KYKM', 'KZZV', 'NZSP', 'NGFU', 'PLCH', 'LGKR', 'LGRP', 'PTKK', 'K12N', 'KMTP', 'SBCY', 'KDMH', 'KBKB', 'KQFR', 'EGCC', 'EGLL', 'EGSH', 'EGPM', 'PGUM', 'KNKT', 'NFTF', 'NZCM', 'K04V', 'K06D', 'K08D', 'K0CO', 'K0S9', 'K20U', 'K20V', 'K22N', 'K24J', 'K2D5', 'K2P2', 'K2V6', 'K33V', 'K42J', 'K46D', 'K4A6', 'K4BM', 'K4M9', 'K57C', 'K5H4', 'K6B9', 'K6L4', 'K6S2', 'K7BM', 'K7L2', 'K82C', 'K9D7', 'K9MN', 'KAAO', 'KACB', 'KACY', 'KADU', 'KAEJ', 'KUOX', 'KUZA', 'KVAY', 'KVQQ', 'KVTA', 'KWAL', 'KWLD', 'KWWD', 'KWYS', 'KX07', 'KX60', 'KY19', 'KZPH', 'PAKN', 'KHEG', 'KHEQ', 'KHNR', 'KHOB', 'KHWD', 'KHZE', 'KICL', 'KIDI', 'KIIB', 'KIKV', 'KILN', 'KIMT', 'KIND', 'KINT', 'KIPT', 'KISW', 'KJAN', 'KJFX', 'KJMR', 'KJST', 'KJVL', 'KJVW', 'KJVY', 'KKY8', 'KL08', 'KL52', 'KLAF', 'KOLM', 'KOLS', 'KOLV', 'KORC', 'KORH', 'KORS', 'KOXV', 'KPAN', 'KPDC', 'KPHF', 'KPHL', 'KPIA', 'KPLR', 'KPNE', 'KPTW', 'KRBL', 'KRBW', 'KRCE', 'KRDG', 'KRDK', 'KRFD', 'KRFI', 'KRIC', 'KRID', 'KRMY', 'KRNH', 'KROA', 'KBWI', 'KBWW', 'KC07', 'KC99', 'KCAR', 'KCBF', 'KCCU', 'KCEU', 'KCFJ', 'KCIN', 'KCLK', 'KCMR', 'KCOS', 'KCOU', 'KCPT', 'KCPW', 'KCQW', 'KCRW', 'KCSQ', 'KCXP', 'KD50', 'KD55', 'KD60', 'KD95', 'KDDH', 'KDEC', 'KDEH', 'KDLL', 'KDNA', 'KDNS', 'KDSM', 'KDSV', 'KDUH', 'KDYL', 'KDYT', 'KECG', 'KEIK', 'KETH', 'KEUG', 'KEVV', 'KEWN', 'KFFL', 'KFFX', 'KFFZ', 'KFMH', 'KFMM', 'KFOZ', 'KFTG', 'KFWA', 'KFZY', 'KGCK', 'KGCN', 'KGED', 'KGLY', 'KGNB', 'KGNT', 'KGPC', 'KGSO', 'KGWR', 'KAIB', 'KAIO', 'KAJZ', 'KAKH', 'KAKQ', 'KAKR', 'KALO', 'KANQ', 'KAPC', 'KAPN', 'KAQX', 'KATS', 'KAUW', 'KAVL', 'KAVP', 'KAWG', 'KAXA', 'KBAC', 'KBDN', 'KBDU', 'KBFL', 'KBJC', 'KBKN', 'KBNW', 'KBOS', 'KBOW', 'KBRG', 'KBTV', 'KBUF', 'KBUU', 'KBUY', 'KBVU', 'KROC', 'KRST', 'KRVL', 'KRYV', 'KRZT', 'KS25', 'KSBN', 'KSBY', 'KSDA', 'KSET', 'KSHL', 'KSJN', 'KSLB', 'KSLC', 'KSMS', 'KSNC', 'KSOW', 'KSTF', 'KSTK', 'KSUS', 'KSWF', 'KSYR', 'KTAD', 'KTKX', 'KTNU', 'KTPF', 'KTQE', 'KTSP', 'KUIN', 'KLBE', 'KLBT', 'KLDJ', 'KLEX', 'KLLJ', 'KLNK', 'KLRJ', 'KLRO', 'KLWM', 'KLWT', 'KLYH', 'KM40', 'KMAN', 'KMBO', 'KMEM', 'KMFI', 'KMGJ', 'KMHE', 'KMIV', 'KMKC', 'KMNH', 'KMQJ', 'KMRY', 'KMUT', 'KMWC', 'KMXO', 'KMYP', 'KO22', 'KOFP', 'EGDX', 'EGOP', 'EGOV', 'EGQL', 'EGQS', 'EGXE', 'EGXU', 'UBBL', 'SBCF', 'LGIO', 'LIMW', 'PATL', 'FQNC', 'FDSK', 'FQBR', 'FNLU', 'LXGB', 'LGIR', 'PAHN', 'PHMK', 'PHOG', 'PGSN', 'GVBA', 'WADL', 'GVNP', 'HSSS', 'SCVM', 'OPST', 'SBSN', 'NFFN', 'PHNY', 'PMDY', 'TXKF', 'KQBL', 'KBYS', 'KNJK', 'FAVV', 'FAJB', 'PTYA', 'EHDL', 'EHLW', 'LGEL', 'EHAM', 'EHBK', 'EHGG', 'EHRD', 'KANJ', 'KAPY', 'KARG', 'KARM', 'KARV', 'KASH', 'KASN', 'KAST', 'KASW', 'KAUM', 'KAUO', 'KAVC', 'KAWO', 'KAXH', 'KAXS', 'KAXX', 'KAZC', 'KAZE', 'KBAM', 'KBAX', 'KBBG', 'KBCK', 'KBDH', 'KBEA', 'KBEC', 'KBHB', 'KBID', 'KBKS', 'KBKX', 'KBLM', 'KBMI', 'KCWC', 'KCXU', 'KCZL', 'KDIJ', 'KDLH', 'KDLO', 'KDNN', 'KDRI', 'KDRM', 'KDUX', 'KDVL', 'KDWU', 'KDYR', 'KDZB', 'KEAT', 'KECS', 'KECU', 'KEDC', 'KEDN', 'KEEN', 'KEFT', 'KEGE', 'KEHR', 'KEKQ', 'KEKY', 'KENV', 'KERV', 'KESC', 'KEUL', 'KLBL', 'KLEW', 'KLGD', 'KLHM', 'KLIC', 'KLNA', 'KLNC', 'KLNP', 'KLRD', 'KLUD', 'KLWA', 'KLXY', 'KLYV', 'KLZU', 'KM21', 'KMBL', 'KMDZ', 'KMGC', 'KMHL', 'KMKG', 'KMKN', 'KMKS', 'KMKY', 'KMLJ', 'KMMH', 'KMML', 'KGTR', 'KGTU', 'KGUC', 'KGWB', 'KGXY', 'KGYB', 'KGYL', 'KGYY', 'KGZL', 'KHAI', 'KHCR', 'KHDN', 'KHEF', 'KHEZ', 'KHFJ', 'KHFY', 'KHHF', 'KHNB', 'KHND', 'KHON', 'KHPT', 'KHQZ', 'KHRX', 'KHSB', 'KHUM', 'KHVE', 'KHVS', 'KHYI', 'KHYS', 'KHZL', 'KPHP', 'KPIM', 'KPNM', 'KPOV', 'KPQI', 'KPRS', 'KPRX', 'KPTB', 'KPTV', 'KPUJ', 'KPVC', 'KPVG', 'KPVU', 'KPWG', 'KPWT', 'KRCV', 'KRGA', 'KRGK', 'KRKD', 'KRKR', 'KRNO', 'KRNP', 'KROS', 'KROX', 'KRRT', 'KRSN', 'KRSV', 'KTMA', 'KTME', 'KTOB', 'KTQH', 'KTTF', 'KTVF', 'KTYQ', 'KU68', 'KUCP', 'KUDG', 'KUGN', 'KULS', 'KUNI', 'KUVA', 'KVBT', 'KVBW', 'KVIS', 'KVJI', 'KVVV', 'KW31', 'KW63', 'KW75', 'KW96', 'KW99', 'KWVL', 'KWWR', 'KXSA', 'KY23', 'KY31', 'KY50', 'K0E0', 'K0F2', 'K0V4', 'K14Y', 'K1A9', 'K1K1', 'K1M4', 'K2C8', 'K3LF', 'K3R7', 'K4I3', 'K4R5', 'K4S1', 'K4V0', 'K54J', 'K5R8', 'K5SM', 'K6A2', 'K7N0', 'K7W4', 'K82V', 'KAAS', 'KAAT', 'KACQ', 'KADC', 'KADF', 'KAEL', 'KAFJ', 'KAIT', 'KAIZ', 'KAJG', 'KAJO', 'KAJR', 'KALM', 'KANE', 'KEVM', 'KEWK', 'KF05', 'KF46', 'KFAM', 'KFCI', 'KFDW', 'KFFM', 'KFGX', 'KFIN', 'KFKL', 'KFKR', 'KFKS', 'KFLP', 'KFNL', 'KFOD', 'KFRH', 'KFRM', 'KFSO', 'KFSW', 'KFWZ', 'KGAD', 'KGAI', 'KGAO', 'KGBD', 'KGDV', 'KGLW', 'KGMJ', 'KGPI', 'KGPM', 'KGPZ', 'KI35', 'KIER', 'KIGQ', 'KIKG', 'KIKW', 'KILE', 'KINJ', 'KINL', 'KIRK', 'KIRS', 'KISM', 'KISQ', 'KITH', 'KIWD', 'KIZA', 'KJAC', 'KJHW', 'KJKJ', 'KJMS', 'KJRB', 'KJSV', 'KJWY', 'KJYG', 'KJYL', 'KJYM', 'KJYR', 'KJZI', 'KK88', 'KKLS', 'KL18', 'KBOK', 'KBPC', 'KBPG', 'KBQK', 'KBTP', 'KBVX', 'KBWD', 'KBXA', 'KBYL', 'KBYY', 'KCAO', 'KCBG', 'KCBK', 'KCDA', 'KCDH', 'KCDN', 'KCGC', 'KCGZ', 'KCIC', 'KCIU', 'KCLW', 'KCMA', 'KCMD', 'KCNC', 'KCNK', 'KCOD', 'KCOE', 'KCVN', 'KCVO', 'KCVX', 'KCWA', 'KRUT', 'KRYW', 'KSAA', 'KSAR', 'KSCD', 'KSCK', 'KSDY', 'KSEP', 'KSEZ', 'KSFM', 'KSFZ', 'KSGH', 'KSGJ', 'KSGS', 'KSGT', 'KSGU', 'KSJX', 'KSKX', 'KSLG', 'KSLH', 'KSLO', 'KSLR', 'KSMN', 'KSOP', 'KSRC', 'KSUA', 'KSUE', 'KSUZ', 'KSYF', 'KTKC', 'KMNE', 'KMNM', 'KMQB', 'KMQY', 'KMRF', 'KMSV', 'KMTW', 'KMVN', 'KMWM', 'KMYR', 'KOAJ', 'KOBE', 'KOCH', 'KOJA', 'KOKK', 'KOLG', 'KOLU', 'KOMH', 'KONA', 'KONP', 'KOOA', 'KOTG', 'KOTH', 'KOWB', 'KOWP', 'KOZW', 'KPCM', 'KPHN', 'KNFG', 'SUMU', 'KY63', 'KY70', 'KYKN', 'PAAK', 'PABV', 'PADK', 'PAFE', 'PAFM', 'PAGL', 'PAHP', 'PAII', 'PANA', 'PANI', 'PAOH', 'PAPN', 'PAQH', 'PASL', 'PAUT', 'PAZK', 'PFCL', 'PFEL', 'PFKW', 'PFNO', 'PFWS', 'PPIT', 'PABL', 'PADL', 'PADU', 'PAGA', 'PAGM', 'PAGS', 'PAHL', 'PAHY', 'PAIG', 'PAIK', 'PAIN', 'PAJZ', 'PASA', 'PASH', 'PASK', 'PASX', 'PATG', 'PAUN', 'PAVA', 'PAVC', 'PAVD', 'PAWG', 'PAWM', 'PAWN', 'PAKH', 'PAKI', 'PALG', 'PAMB', 'PAMH', 'PAMK', 'PAMM', 'PANW', 'PAOO', 'PAPG', 'PAPH', 'PAPM', 'PAPO', 'PARS', 'PARY', 'ETEB', 'ETEK', 'ETIC', 'ETIH', 'ETIK', 'EGUL', 'EHWO', 'LGLR', 'LGSY', 'OBBI', 'KQAZ', 'KQHY', 'KP28', 'EGDY', 'EGUW', 'EGVP', 'EGXC', 'ETAD', 'KCOF', 'KFSI', 'KPAM', 'KPOB', 'KRND', 'MHCA', 'OAHR', 'RODN', 'KNYG', 'KNMM', 'KAQV', 'EHEH', 'KNCA', 'K79J', 'KNOG', 'KD07', 'KOFK', 'KOKM', 'KOLE', 'KONZ', 'KORB', 'KOSC', 'KOVL', 'KOWI', 'KP08', 'KPCD', 'KPCW', 'KPEQ', 'KPHT', 'KPMH', 'KPOY', 'KPPQ', 'KPQN', 'KPTD', 'KPVB', 'KPVE', 'KPWC', 'KPYX', 'KPZQ', 'KRAS', 'KRAW', 'KRCM', 'KRDM', 'KRKW', 'KRLD', 'KRMN', 'KRNC', 'KRPH', 'KRQB', 'KRTS', 'KHWV', 'KHYA', 'KHYX', 'KHZD', 'KHZX', 'KI67', 'KI69', 'KI75', 'KIBM', 'KIKT', 'KIMM', 'KINW', 'KISP', 'KJAQ', 'KJAU', 'KJFZ', 'KJSL', 'KJTC', 'KJWN', 'KJXI', 'KLAS', 'KLDM', 'KLHB', 'KLJF', 'KLMO', 'KLRU', 'KLUA', 'KLUG', 'KLUV', 'KLWS', 'KLXN', 'KLYO', 'K05U', 'K0A9', 'K0R0', 'K13K', 'K18H', 'K1M5', 'K28J', 'K2A0', 'K2G9', 'K2LS', 'K2M2', 'K33N', 'K3L4', 'K3S8', 'K3T5', 'K46U', 'K4S2', 'K54A', 'K5T9', 'K65S', 'K6I2', 'K6S0', 'K8A3', 'K8W2', 'KA39', 'KADM', 'KADS', 'KAEG', 'KAIG', 'KAND', 'KARW', 'KATP', 'KAVK', 'KAVQ', 'KAXV', 'KAYS', 'KBBF', 'KSPD', 'KBBP', 'KBED', 'KBGF', 'KBIE', 'KBIH', 'KBIJ', 'KBJJ', 'KBKT', 'KBQX', 'KBTA', 'KBVN', 'KBZN', 'KC29', 'KC83', 'KCAD', 'KCCB', 'KCEC', 'KCFS', 'KCIR', 'KCKC', 'KCKN', 'KCKP', 'KCKZ', 'KCMY', 'KCNI', 'KCOQ', 'KCPK', 'KCQF', 'KCQM', 'KCRX', 'KCTB', 'KLZZ', 'KM02', 'KM04', 'KM08', 'KM54', 'KM75', 'KM91', 'KMBT', 'KMCC', 'KMCD', 'KMDJ', 'KMDT', 'KMEV', 'KMGN', 'KMHV', 'KMIS', 'KMJQ', 'KMMI', 'KMNV', 'KMOB', 'KMOP', 'KMOR', 'KMRC', 'KMRT', 'KMVH', 'KMZH', 'KN03', 'KN38', 'KNQA', 'KNUQ', 'KO69', 'KO86', 'KOEB', 'KP53', 'PHBK', 'KNFE', 'KNGP', 'KUKI', 'KULM', 'KUYF', 'KVAF', 'KVBS', 'KVDF', 'KVKS', 'KVKY', 'KVLL', 'KVOA', 'KVQT', 'KW13', 'KW81', 'KWBF', 'KWDG', 'KWJF', 'KWMC', 'KXBP', 'KXER', 'KXIH', 'KXNX', 'KXPY', 'PAJC', 'PPNU', 'KCVB', 'KCVW', 'KCWI', 'KCXW', 'KCXY', 'KD25', 'KDAY', 'KDIK', 'KDKX', 'KDNV', 'KDSF', 'KDUG', 'KDXX', 'KDZJ', 'KE16', 'KEAR', 'KEAU', 'KEBA', 'KEDJ', 'KEDU', 'KEED', 'KEIR', 'KEKO', 'KEKS', 'KELO', 'KELZ', 'KEMK', 'KERY', 'KETB', 'KETN', 'KEVU', 'KF00', 'KF44', 'KFCH', 'KALK', 'KFHB', 'KFOT', 'KFSD', 'KFSE', 'KFTN', 'KFWB', 'KFXY', 'KFYE', 'KFYM', 'KGBK', 'KGCD', 'KGCM', 'KGCY', 'KGHB', 'KGHW', 'KGIC', 'KGKT', 'KGON', 'KGOO', 'KGRD', 'KGRY', 'KGUL', 'KGYI', 'KGZN', 'KGZS', 'KHAE', 'KHCO', 'KHDC', 'KHHV', 'KHLB', 'KHMZ', 'KHPN', 'KHQI', 'KHQU', 'KHSD', 'KHTH', 'KRZR', 'KS39', 'KS52', 'KSAZ', 'KSBP', 'KSCF', 'KSCX', 'KSDC', 'KSFO', 'KSHV', 'KSIK', 'KSLE', 'KSNH', 'KSQI', 'KSRB', 'KSRE', 'KSUN', 'KSXU', 'KSYI', 'KSZT', 'KSZY', 'KTCY', 'KTEW', 'KTHA', 'KTKV', 'KTNB', 'KTPH', 'KTVI', 'KTWM', 'KTYL', 'KTZR', 'KU42', 'KUBE', 'KUCY', 'KUES', 'KNBC', 'KNTU', 'ORSU', 'K8D3', 'KNQI', 'SCEL', 'KGNR', 'KABH', 'SMJP', 'SMZO', 'KGNA', 'KMEH', 'KNID', 'K2WX', 'LSME', 'LSMM', 'EGDM', 'EGXP', 'EGXV', 'FQPB', 'GVSV', 'VABO', 'LWOH', 'KMQE', 'KNUW', 'KNXP', 'SPJC', 'ESNN', 'MGGT', 'KCAE', 'KCHS', 'KJAX', 'TJSJ', 'UBBY', 'ETAR', 'K2DP', 'KFBG', 'KGSB', 'KHFF', 'KHST', 'KMGE', 'KMXF', 'KQGE', 'KSSC', 'KXMR', 'KCEF', 'KRDR', 'KTBN', 'KTTS', 'OTBH', 'PHSF', 'KGUS', 'KOFF', 'K1FN', 'K1IN', 'K1JN', 'KRYM', 'KVOK', 'EGUN', 'EGVA', 'KDLF', 'KDYS', 'KHOP', 'KLFI', 'KLSF', 'KLTS', 'KMCF', 'KMMT', 'KVAD', 'KTIK', 'KXNO', 'KCBM', 'KEND', 'KFRI', 'KIAB', 'KLRF', 'OKAS', 'K1BN', 'K1MN', 'KADW', 'KMTC', 'KMUI', 'ETHS', 'ETND', 'OJAI', 'PAEI', 'PGUA', 'PAEH', 'PALU', 'PASV', 'PATC', 'RJTY', 'SBMQ', 'SBCG', 'KNTD', 'K6R6', 'KNAK', 'K1V4', 'KNSI', 'KNYL', 'PHNG', 'EHAK', 'EHDV', 'EHFD', 'EHFZ', 'EHHW', 'EHJA', 'EHJR', 'EHKV', 'EHMA', 'EHMG', 'EHPG', 'EHQE', 'EHSA', 'EHSC', 'LGHI', 'SBCT', 'SKBQ', 'KNSE', 'K04W', 'K2I0', 'KAHQ', 'KANW', 'KAUH', 'KAUN', 'KBFW', 'KBJI', 'KBQP', 'KBVS', 'KBXK', 'KC65', 'KCEY', 'KCHK', 'KCNB', 'KCTY', 'KDED', 'KDTL', 'KDVO', 'KEFK', 'KEZZ', 'KFET', 'KFGN', 'KFLG', 'KORG', 'KOSA', 'KOWX', 'KOZS', 'KPBX', 'KPEX', 'KPLU', 'KPMU', 'KPPA', 'KPSN', 'KRDU', 'KRNV', 'KROG', 'KRWV', 'KRZL', 'KSBS', 'KSEE', 'KSOA', 'KSRR', 'KSTE', 'KSVE', 'PAAD', 'KFLY', 'KFOA', 'KFWS', 'KGDB', 'KGHG', 'KGOP', 'KHCD', 'KHDE', 'KHJH', 'KHYW', 'KI23', 'KIKK', 'KIMS', 'KIOB', 'KIWA', 'KJGG', 'KL35', 'KLAM', 'KLNN', 'KLNQ', 'KMDQ', 'KMEZ', 'KMNZ', 'KMQS', 'KMWO', 'KOCQ', 'KOKV', 'KQBF', 'KQD3', 'KQDG', 'KQN3', 'KQND', 'KQRH', 'KSMP', 'KP60', 'SKCL', 'SKCG', 'SKRG', 'SKSP', 'SBFI', 'SBPA', 'NZWD', 'SBFZ', 'K1EM', 'K1OM', 'K4MR', 'K9L2', 'KCWN', 'KFCS', 'KFEW', 'KSUU', 'KVBG', 'K1BW', 'K1GW', 'KAFF', 'KBAD', 'KDMA', 'KHIF', 'KHMN', 'KMUO', 'K1AM', 'K1YT', 'KGFA', 'KINS', 'K1FM', 'K1GM', 'K1HM', 'K1JM', 'KBIF', 'KCVS', 'KFHU', 'KGRF', 'KLGF', 'KRIV', 'KSKA', 'KSLI', 'KTCM', 'KSZL', 'RKJK', 'MHSC', 'ROTM', 'MMHO', 'MMML', 'MMMZ', 'MMTJ', 'KNRS', 'K1CM', 'K1LM', 'SBGR', 'K0J4', 'KEUF', 'MMMY', 'MMAA', 'MMMX', 'MMQT', 'MMTO', 'ENGK', 'BIBD', 'UBBQ', 'LGAV', 'MMGL', 'MMMM', 'MMPR', 'MMSP', 'MMCZ', 'MMMD', 'MMTP', 'MMUN', 'MGMM', 'MGHT', 'ORBI', 'ORMM', 'ORNI', 'ORER', 'SBKP', 'SVMI', 'SARI', 'SBMA', 'LTAC', 'LTAF', 'LTAI', 'LTAJ', 'LTBA', 'LTBJ', 'LTBR', 'LTBS', 'LTCG', 'LTCS', 'LTFC', 'LTFE', 'LTFJ', 'LTFM', 'LTAG', 'LTAN', 'LTAP', 'LTAT', 'LTAU', 'LTBF', 'LTBU', 'LTCC', 'LTCE', 'LTCJ', 'LTAR', 'LTAY', 'LTBY', 'LTCA', 'LTCD', 'LTCF', 'LTCI', 'LTDA', 'LTFH', 'LTAL', 'LTAS', 'LTAW', 'LTBD', 'LTBH', 'LTBO', 'LTCB', 'LTCK', 'LTCL', 'LTCM', 'LTCN', 'LTCO', 'LTCP', 'LTCR', 'LTCT', 'LTCU', 'LTCV', 'LTCW', 'LTFD', 'LTFG', 'LTFK', 'LCEN', 'OEDF', 'OEJN', 'OEMA', 'OERK', 'KP68', 'SCIP', 'SCPQ', 'SCTN', 'SCCH', 'SCRM', 'SCIC', 'SCCY', 'SACO', 'SBVT', 'SEQM', 'SEMT', 'SELT', 'SECU', 'HECA', 'SAWH', 'SPCL', 'SPJR', 'ENLK', 'KEBG', 'KEHA', 'KELA', 'KELK', 'KENL', 'KEQA', 'KEZF', 'KEZM', 'KF70', 'KFEP', 'KFKA', 'KFKN', 'KFVX', 'KFYG', 'KFZG', 'KGBG', 'KGGP', 'KGLE', 'KGNC', 'KGRN', 'KHHG', 'KHHW', 'KHLX', 'KHQG', 'KHSG', 'KHSP', 'KHTO', 'KHWY', 'KI19', 'KI63', 'KIJX', 'KJAS', 'KJCA', 'KJDD', 'KONM', 'KOPL', 'KOPN', 'KOZA', 'KPMV', 'KPNT', 'KPRG', 'KPVF', 'KPVW', 'KPXE', 'KRCR', 'KREG', 'KRPJ', 'KRZN', 'KSAW', 'KSJS', 'KSNK', 'KSNL', 'KSWW', 'KSYN', 'KT20', 'KT35', 'KTAZ', 'KTBR', 'KTEX', 'KTFP', 'KTIF', 'KTIP', 'KTMK', 'KTOC', 'KTXW', 'KUTA', 'KUXL', 'KVDI', 'KVNY', 'K06C', 'K0R4', 'K19S', 'K1A6', 'K1F0', 'K1H2', 'K2J3', 'K2J5', 'K3F3', 'K3N8', 'K40J', 'K48A', 'K49A', 'K4A9', 'K4O4', 'K5A6', 'K5C1', 'K66R', 'K6B0', 'K6P9', 'K8A0', 'K9A5', 'K9V9', 'KA08', 'KAAA', 'KADH', 'KAFK', 'KAFO', 'KJKA', 'KJOT', 'KJWG', 'KJYO', 'KJZP', 'KLCG', 'KLCK', 'KLGC', 'KLKU', 'KLOM', 'KLPC', 'KLVL', 'KM30', 'KMDD', 'KMEI', 'KMER', 'KMGR', 'KMKJ', 'KMLE', 'KMMU', 'KMPV', 'KMRH', 'KMTV', 'KMWA', 'KMYZ', 'KOGA', 'KOLY', 'KONL', 'KVWU', 'KVYS', 'KW22', 'KWDR', 'KXLL', 'KALN', 'KALX', 'KAPS', 'KAQR', 'KASL', 'KATW', 'KAUG', 'KBBD', 'KBCB', 'KBDG', 'KBMT', 'KC09', 'KCDI', 'KCFD', 'KCFE', 'KCKF', 'KCOM', 'KCQB', 'KCTJ', 'KCUH', 'KCVC', 'KCXE', 'KD39', 'KDBN', 'KDKB', 'KDKR', 'KDQH', 'KDTA', 'KDUA', 'KDUB', 'KDUC', 'KDVK', 'KDVP', 'KE11', 'KE38', 'KDOV', 'EGVO', 'EGYM', 'ETNW', 'VAJB', 'FYGF', 'VEIM', 'VASU', 'VILK', 'SBJP', 'SBRJ', 'UBBB', 'NGTA', 'VGHS', 'LUKK', 'SBLO', 'DIAP', 'SCFA', 'SCAR', 'SCBA', 'SCCF', 'SCIE', 'SCAT', 'SCDA', 'SCSE', 'SCQP', 'SCTE', 'SCVD', 'SCCI', 'SBPL', 'SCSN', 'SCON', 'SCFT', 'SCAP', 'KSXT', 'K1AN', 'K1DN', 'K1EN', 'K1GN', 'KBLV', 'KGOV', 'KPSM', 'KWRI', 'KXIF', 'SBFL', 'SAZS', 'MUHA', 'MUVR', 'MUSC', 'MUCC', 'MUCM', 'MUHG', 'MUCU', 'MUCF', 'SPHI', 'SPQT', 'SPQU', 'SPRU', 'SPSO', 'SPTN', 'SPZO', 'FSIA', 'ETSB', 'VOCB', 'TAPA', 'KNDZ', 'SLLP', 'SLVR', 'SLCB', 'SLTJ', 'OPPS', 'SBCP', 'SBNF', 'SBCR', 'SKBO', 'KEOD', 'KHEY', 'KQRD', 'KSXS', 'SAWG', 'SANT', 'UBBN', 'SBGO', 'UBBG', 'K1AW', 'K1KM', 'KBKF', 'KEDW', 'KSKF', 'KT70', 'KPOE', 'NSFA', 'OAIX', 'PAFR', 'KNOZ', 'KNZY', 'YBRK', 'TFFF', 'OPSK', 'SBTE', 'SBGL', 'LZIB', 'LZKZ', 'LZTT', 'FMMI', 'SKLT', 'YMTG', 'YTEF', 'YBTL', 'YBUD', 'YBWP', 'YBWX', 'YCAR', 'YCAS', 'YCBA', 'YCBB', 'YCBP', 'YCCY', 'NWWW', 'OOMS', 'OOSA', 'OODQ', 'OMAA', 'OMAD', 'OMAL', 'OMDB', 'OMDW', 'OMFJ', 'OMRK', 'OMSJ', 'WAMM', 'LHBP', 'LBSF', 'LBWN', 'LBBG', 'LBPD', 'LBGO', 'LBPG', 'LBIA', 'LBPL', 'LBWB', 'RPLC', 'RPVD', 'RPVP', 'RPMR', 'LDDU', 'LDOS', 'LDPL', 'LDRI', 'LDSP', 'LDZA', 'LDZD', 'TFFR', 'VOML', 'SOCA', 'KNY0', 'KO54', 'KOUN', 'KOXD', 'KOXI', 'KOYM', 'KPSK', 'KPTT', 'KSBD', 'KSBO', 'KSDF', 'KSFQ', 'KSFY', 'KSHD', 'KSME', 'KSQL', 'KT82', 'KTRK', 'KUKT', 'KVER', 'KW43', 'KW78', 'KY49', 'K11R', 'K17J', 'K21D', 'K3AU', 'K3J7', 'K3K3', 'K5M9', 'KACP', 'KAUS', 'KBMC', 'KC75', 'KCCO', 'KCKM', 'KCLL', 'KCVH', 'KCWF', 'KCWV', 'KD73', 'KDWX', 'KEAN', 'KEHY', 'KEMV', 'KFRR', 'KFWC', 'KGVT', 'KHAF', 'KHII', 'KHZR', 'KIDP', 'KJES', 'KJHN', 'KLWB', 'KM19', 'KMFV', 'KMZZ', 'WSSS', 'FLKK', 'SULS', 'SABE', 'SARC', 'SBRP', 'FMMT', 'VHHH', 'KGRK', 'KHLR', 'KHUA', 'PAFB', 'RKSG', 'KNGU', 'KNLC', 'KNHK', 'WSSL', 'UKBB', 'UKHH', 'UKOO', 'UKDE', 'UKDD', 'UKLL', 'UKDR', 'SBUG', 'MROC', 'KNBG', 'SAEZ', 'KNKX', 'SGAS', 'SGEN', 'PKWA', 'KDRA', 'YLRE', 'YMAV', 'YMAY', 'YMDG', 'YMEK', 'YMEN', 'YMER', 'YMIA', 'YMML', 'YMOR', 'LTBQ', 'KNEL', 'NTAA', 'GMAD', 'GMFF', 'GMME', 'GMMN', 'GMMX', 'GMTT', 'GMAG', 'GMAT', 'GMFK', 'GMFM', 'GMFO', 'GMMB', 'GMMC', 'GMMD', 'GMMH', 'GMMI', 'GMML', 'GMMW', 'GMMZ', 'GMTA', 'GMTN', 'KSRQ', 'KSUW', 'KTGI', 'KTVK', 'KVES', 'KVPZ', 'KACJ', 'KAQO', 'KARB', 'KBGE', 'KBHC', 'KBKV', 'KBWP', 'KCGI', 'KCJR', 'KCPU', 'KCUL', 'KCXO', 'KDCY', 'KDTW', 'KEMM', 'KFBR', 'KFYJ', 'KGVE', 'KHBV', 'KI16', 'KIWI', 'KIYA', 'KLCQ', 'KLOT', 'KMRJ', 'KMVL', 'KMYJ', 'KNOW', 'KOVS', 'KOXB', 'KPNA', 'KPPO', 'KRQO', 'KSEF', 'FMCZ', 'VEGT', 'VARK', 'VORY', 'VEJS', 'TNCB', 'TNCE', 'EHFS', 'LHBC', 'LHDC', 'LHPP', 'LHPR', 'LHSM', 'LHUD', 'EPGD', 'EPKK', 'EPLL', 'EPPO', 'EPRZ', 'EPWA', 'EPBY', 'EPKT', 'EPLB', 'EPMO', 'EPRA', 'EPSC', 'EPSY', 'EPWR', 'EPZG', 'MKJS', 'KQEL', 'KQER', 'KQEV', 'KQEW', 'KQEY', 'KQFB', 'KQFT', 'KQFV', 'KQFX', 'EQYG', 'PAFS', 'WAJJ', 'WSAP', 'FIMR', 'FIMP', 'VOBL', 'TGPY', 'SADF', 'GBYD', 'YABA', 'YAMB', 'YARG', 'YAYE', 'YBAS', 'YBBN', 'YBCG', 'YBCS', 'YBCV', 'YBDV', 'EBBE', 'EBCV', 'EBDT', 'EBFN', 'EBFS', 'EBLB', 'EGYE', 'LOXT', 'EHGR', 'EHVK', 'ETNL', 'KFAF', 'LHKE', 'RJNG', 'PAIM', 'RKSO', 'KLSV', 'CWWU', 'SAZN', 'SARE', 'YBHM', 'KMDS', 'SAME', 'OPKC', 'OPIS', 'OPLA', 'OPNH', 'OPRN', 'LZPP', 'LZSL', 'LZZI', 'LKKV', 'LKMT', 'LKPR', 'LKTB', 'SASA', 'SBRB', 'CYPQ', 'CYER', 'LTAB', 'LTAD', 'LTAE', 'LTAV', 'LTBG', 'LTBL', 'LTFA', 'KVPS', 'KWRB', 'KDAA', 'KMIB', 'TNCA', 'YBMA', 'YBRM', 'YCIN', 'YFRT', 'YMHB', 'YMLT', 'YPEA', 'YPGV', 'YPKG', 'YPPD', 'YSCB', 'YSDU', 'YSNF', 'YSRI', 'YWLM', 'CYEK', 'BIAR', 'BIEG', 'BIKF', 'BIRK', 'LYBE', 'LYBT', 'LYKV', 'LYNI', 'LYPG', 'LYTV', 'LYUZ', 'LYVR', 'LQBK', 'LQMO', 'LQSA', 'LQTZ', 'SARP', 'EGYH', 'VQPR', 'EIDW', 'EINN', 'EICK', 'EIKN', 'PADM', 'PAMO', 'PASM', 'KAMG', 'KCPS', 'KEYE', 'KIOW', 'KJXN', 'KMDH', 'KPWM', 'KSSI', 'EGYP', 'DTKA', 'DTNH', 'DTTA', 'DTTF', 'DTTG', 'DTTJ', 'DTTX', 'DTTZ', 'SYCJ', 'CYVO', 'FOOL', 'LCLK', 'LCPH', 'TNCM', 'OIBB', 'OIBP', 'OICS', 'OITL', 'OIBL', 'OIBQ', 'OIIK', 'OIMC', 'OIMD', 'OIMQ', 'OINE', 'OITM', 'OIBA', 'OIIP', 'OIMB', 'OIMN', 'OIZJ', 'OIAW', 'OIFM', 'OIII', 'OIKB', 'OIKK', 'OIMM', 'OISS', 'OITT', 'OIZH', 'OIAA', 'OIBK', 'OICC', 'OIGG', 'OIIE', 'OINZ', 'OITR', 'OIYY', 'OIBJ', 'OIBS', 'OIHR', 'OING', 'OIZB', 'OIZI', 'OIAM', 'OICI', 'OIKQ', 'OINN', 'OINR', 'OISL', 'OISY', 'OITZ', 'OIAH', 'OISF', 'OISR', 'OITP', 'TBPB', 'CXBW', 'CZEL', 'SAAR', 'SARF', 'SAWE', 'LFBD', 'LFBH', 'LFLL', 'LFMN', 'LFPG', 'LFPO', 'LFQQ', 'LFRB', 'LFRS', 'LFOA', 'LFPV', 'LFCR', 'LFJL', 'LFKC', 'LFKF', 'LFKJ', 'LFLC', 'LFLS', 'LFMP', 'LFMV', 'LFSL', 'LFOC', 'LFOE', 'LFOJ', 'LFRJ', 'LFRL', 'LFSI', 'LFSO', 'LFSX', 'LFYR', 'LFBI', 'LFBL', 'LFBO', 'LFBP', 'LFBT', 'LFBZ', 'LFKB', 'LFLB', 'LFML', 'LFBE', 'LFGJ', 'LFMD', 'LFMH', 'LFOT', 'LFRG', 'LFST', 'LFTH', 'LFTW', 'PAQT', 'PAWD', 'PANT', 'FQCH', 'VECC', 'DTTB', 'DTTD', 'DTTK', 'DTTL', 'DTTN', 'VEGY', 'DTTR', 'FWCL', 'FDMS', 'VOTP', 'LFCK', 'LFLP', 'LFLU', 'LFLX', 'LFOH', 'LFOP', 'LFQA', 'LFQB', 'LFSN', 'LFBA', 'LFMI', 'LFOV', 'LFRI', 'LFRM', 'LFRO', 'LFRV', 'LFRZ', 'LFSG', 'LFLY', 'LFMK', 'LFMT', 'LFMU', 'LFOB', 'LFOK', 'LFPB', 'LFRD', 'LFRN', 'LFSB', 'LFBC', 'LFBG', 'LFBM', 'LFKS', 'LFMC', 'LFMO', 'LFMY', 'LFLN', 'LFPM', 'LFPT', 'LFRH', 'LFRQ', 'LFRT', 'LFSD', 'LFAQ', 'LFAT', 'LFBU', 'LFGA', 'LFJR', 'LFPN', 'LFRC', 'LFRK', 'LFRU', 'LJLJ', 'LJMB', 'LJPZ', 'LJCE', 'GCGM', 'GCHI', 'GCFV', 'GCLA', 'GCLP', 'GCRR', 'GCTS', 'GCXO', 'LEAM', 'LEAS', 'LEBB', 'LECO', 'LEGE', 'LEGR', 'LEMH', 'LERS', 'LESO', 'LEAL', 'LEBL', 'LEIB', 'LEMD', 'LEMG', 'LEPA', 'LEVC', 'LEVX', 'LEZL', 'LRBS', 'LRCK', 'LROP', 'LRTR', 'LESA', 'LEVD', 'LEDA', 'LEST', 'LEVT', 'LEZG', 'LRAR', 'LRBM', 'LRCL', 'LROD', 'LRSM', 'LRTM', 'LEAG', 'LEBG', 'LECH', 'LETL', 'LRBC', 'LRCV', 'LRIA', 'LRSV', 'LRTC', 'LEPP', 'LEXJ', 'LELN', 'GEML', 'LEMI', 'KEBS', 'KFME', 'KGGI', 'KLNR', 'KMBY', 'KMIE', 'KMWK', 'KOSU', 'KOVE', 'KWST', 'VELP', 'VOTR', 'VOTK', 'VANP', 'VEPT', 'VOMM', 'VOBZ', 'VOHS', 'VOMD', 'KQEN', 'KQES', 'KQFW', 'LPFR', 'LPMA', 'LPPR', 'LPPS', 'LPPT', 'LPLA', 'LPHR', 'LPFL', 'LPAZ', 'LPPD', 'LPBJ', 'LPCS', 'PAKF', 'PAOU', 'UMBB', 'UMGG', 'UMII', 'UMMG', 'UMMS', 'UMOO', 'VOCL', 'VELR', 'VEJH', 'VAJJ', 'VOCI', 'VEMN', 'VAAH', 'VABB', 'ETSN', 'VEBS', 'VEAT', 'KNFL', 'SLTR', 'SAVC', 'KNPA', 'YSTW', 'YSWG', 'YTNK', 'YTRE', 'YWGT', 'YWHA', 'SGES', 'KEGI', 'KLHW', 'KOZR', 'LFBY', 'KSVN', 'OAKN', 'OLBA', 'UKLR', 'UKLI', 'UKON', 'UKLU', 'UKKK', 'UKKM', 'UKLN', 'UKOH', 'UKWW', 'RKSI', 'RKSS', 'RKPC', 'RKPK', 'RKTU', 'RKTN', 'RKJB', 'RKNY', 'SLRI', 'SLET', 'LEAB', 'LEBZ', 'MKJP', 'LKCV', 'LKKB', 'LKLN', 'LKNA', 'LKPD', 'GLRB', 'TLPL', 'LELC', 'ZBAA', 'ZBSJ', 'ZBTJ', 'ZBYN', 'ZGGG', 'ZSHC', 'ZSPD', 'ZSSS', 'ZWSH', 'ZWWW', 'ZYTL', 'ZYTX', 'LIQN', 'LEBA', 'LEHC', 'LEBT', 'LELO', 'LEBR', 'LETU', 'LEVS', 'LELL', 'LESB', 'LIBC', 'LIBF', 'LIBG', 'LIBP', 'LIRI', 'LIRZ', 'LIMA', 'LIMG', 'LIMP', 'LIMS', 'LIMZ', 'LICA', 'LICB', 'LICG', 'LICR', 'LICT', 'LEAO', 'LEGA', 'LEGT', 'LERI', 'LERT', 'LETO', 'LECV', 'LEEC', 'FACT', 'FAGG', 'FAHS', 'FAKM', 'FAKN', 'FALE', 'FAPE', 'FAUP', 'FAWK', 'FBFT', 'FBKE', 'FBMN', 'FBSK', 'UGTB', 'UGKO', 'UGSB', 'LIPF', 'LIPO', 'LIPY', 'FALA', 'FAMM', 'FAPP', 'FAUT', 'LIQW', 'LIRG', 'LIRH', 'LIRL', 'LIRM', 'LIRS', 'LIRV', 'KART', 'KDAW', 'KFIT', 'KGPT', 'KGVQ', 'KHRL', 'KLEB', 'KLVN', 'KPTN', 'KSAV', 'KTDZ', 'KTEB', 'KUTS', 'KUUU', 'KVSF', 'GQPP', 'ZGKL', 'ZGNN', 'ZGOW', 'ZGSZ', 'ZLXY', 'ZPPP', 'ZSAM', 'ZSFZ', 'ZSNB', 'ZSQD', 'ZUGY', 'ZUUU', 'FQIN', 'FQMA', 'FYWE', 'WIII', 'UCFM', 'UCFO', 'UCFL', 'UDYZ', 'UDSG', 'UAAA', 'UAAH', 'UAAT', 'UADD', 'UACC', 'UACK', 'UACP', 'UAII', 'UAKK', 'UAOO', 'UASK', 'UASP', 'UASS', 'UARR', 'UATE', 'UATG', 'UATT', 'UAUU', 'UTDD', 'UTDK', 'UTDT', 'UTDL', 'UTAA', 'UTAK', 'UTAV', 'UTAM', 'UTAT', 'SASJ', 'DAAG', 'DABB', 'DABC', 'DAOO', 'DAUH', 'AGGH', 'PHHI', 'RJAA', 'RJOI', 'KPRN', 'EGDR', 'DAAS', 'DABS', 'DAUA', 'DAUB', 'DAUG', 'DAOI', 'KFFO', 'DAAE', 'DAAJ', 'DAAV', 'DABT', 'DAUZ', 'CYYL', 'DAAD', 'DAAP', 'DAAY', 'DAFH', 'DAOV', 'DAOF', 'DAOL', 'DAOR', 'DAON', 'LFVP', 'SEGU', 'DAOB', 'K1S5', 'KAAF', 'KALI', 'KCLT', 'KEGV', 'KEZS', 'KGPH', 'KLUK', 'KMAO', 'KMJX', 'KMLP', 'KPHD', 'KRPD', 'KRRL', 'KUNU', 'PAGN', 'BIVM', 'DAOY', 'DATM', 'DAUE', 'DAUK', 'DAUO', 'DAUT', 'DAUL', 'DAUU', 'DAUI', 'KMHS', 'VABP', 'VOHB', 'VOSM', 'VERC', 'VOVZ', 'UAKD', 'FMEE', 'FMEP', 'VOBG', 'RCTP', 'RCKH', 'RCSS', 'RCMQ', 'RCNN', 'RCFN', 'VMMC', 'RPLL', 'RPVM', 'RPMD', 'RPLB', 'RPLI', 'RPMZ', 'LIPC', 'EIDL', 'EIKY', 'EIME', 'EIWF', 'FOOG', 'FOOB', 'FOGR', 'FOGM', 'FOOT', 'FOOR', 'FOOK', 'FOON', 'PASI', 'PAYA', 'VOTV', 'VTSB', 'VTSC', 'VTSE', 'VTSF', 'VTSM', 'VTSR', 'VTST', 'OAKB', 'ZBHH', 'ZGHA', 'ZHCC', 'ZHHH', 'ZJHK', 'ZJSY', 'ZLLL', 'ZSNJ', 'ZSOF', 'ZUCK', 'ZYCC', 'ZYHB', 'VTBO', 'VTCH', 'VTCL', 'VTCN', 'VTCP', 'VTPB', 'VTPH', 'VTPM', 'VTPO', 'VTPP', 'TNCC', 'LFHP', 'LFLW', 'LFQG', 'KLUF', 'RJAW', 'CYLH', 'CYQB', 'RJBB', 'RJTT', 'RJOO', 'ROAH', 'RJGG', 'RJCH', 'RJSS', 'RJFO', 'RJNT', 'RJFF', 'RJCC', 'RJFK', 'RJSN', 'RJFT', 'RJFU', 'RJNK', 'RJOA', 'RJOB', 'RJOT', 'OICK', 'OIHH', 'OIHM', 'KHME', 'RJNS', 'RJSA', 'RJSF', 'RJOM', 'RJOK', 'RJFM', 'RJEC', 'RJFR', 'RJSK', 'RJAH', 'TTPP', 'TTCP', 'RJCK', 'RJCM', 'RJCB', 'RJOC', 'RJOH', 'ROIG', 'RJFS', 'ETHA', 'CYBK', 'CYBQ', 'CYBR', 'CYBU', 'CYDN', 'CYEN', 'CYET', 'CYGX', 'CYKJ', 'CYLL', 'CYMM', 'CYNE', 'CYOJ', 'CYPA', 'CYPY', 'CYQF', 'CYQL', 'CYQR', 'CYQW', 'CYVC', 'CYYN', 'CYZH', 'CZVL', 'CYQI', 'CYCB', 'CYCO', 'CYFS', 'CYHK', 'CYHY', 'CYRT', 'CYTE', 'CYWE', 'CYZS', 'CYAY', 'CYCX', 'CYDF', 'CYDP', 'CYGW', 'CYSJ', 'CYYG', 'CYDB', 'CYDQ', 'CYEV', 'CYHE', 'CYIV', 'CYKY', 'CYPR', 'CYQD', 'CYQZ', 'CYRV', 'CYVL', 'CYXC', 'CYXE', 'CYXS', 'CYZP', 'CYZT', 'CYAT', 'CYBC', 'CYBN', 'CYGQ', 'CYHM', 'CYKF', 'CYKL', 'CYKP', 'CYOO', 'CYPO', 'CYQA', 'CYQK', 'CYRB', 'CYRQ', 'CYSB', 'CYSC', 'CYVQ', 'CYXL', 'CYXU', 'CYYB', 'CYYH', 'CYYU', 'CYYW', 'CZMD', 'CZSJ', 'CWRF', 'CYBW', 'CYED', 'CYIO', 'CYLT', 'CYOD', 'CYPE', 'CYQV', 'CYSF', 'CYSM', 'CYTH', 'CYUX', 'CYXH', 'CYAM', 'CYGP', 'CYHU', 'CYMO', 'CYNA', 'CYQT', 'CYTL', 'CYTS', 'CYTZ', 'CYVP', 'CYVV', 'CYWA', 'CYYY', 'CYZE', 'CYZR', 'CYBG', 'CYEG', 'CYFB', 'CYFC', 'CYGL', 'CYHZ', 'CYMX', 'CYOW', 'CYQG', 'CYQM', 'CYQQ', 'CYQX', 'CYQY', 'CYTR', 'CYUL', 'CYVR', 'CYWG', 'CYXX', 'CYYC', 'CYYJ', 'CYYQ', 'CYYR', 'CYYT', 'CYYZ', 'CYZF', 'CYZV', 'CYZX', 'CBBC', 'CYDL', 'CYIN', 'CYKA', 'CYLW', 'CYMA', 'CYQH', 'CYQU', 'CYWL', 'CYXJ', 'CYXT', 'CYXY', 'CYYD', 'CYYE', 'CYYF', 'CYZY', 'SARL', 'CWIL', 'CWLI', 'CWPX', 'CWRX', 'CWUW', 'CWZZ', 'CZBF', 'CZCP', 'CYAH', 'CYBX', 'CYGV', 'CYMH', 'CYMT', 'CYNM', 'CYOY', 'CYPH', 'CYPX', 'CYUY', 'CYWK', 'NZAA', 'NZWN', 'NZCH', 'CWEU', 'CWFD', 'CWSA', 'CYPD', 'CZPC', 'CZUM', 'KNUC', 'LTBI', 'LTBT', 'K1A5', 'K24A', 'KASJ', 'KBAZ', 'KBFM', 'KCLI', 'KEDE', 'KEHO', 'KEKX', 'KETC', 'KFQD', 'KGWW', 'KIFA', 'KIPJ', 'KISO', 'KLHZ', 'KLUL', 'KMFE', 'KOCW', 'KPBH', 'KPGV', 'KPIL', 'KRCZ', 'KRDD', 'KRHP', 'KSCR', 'KSIF', 'KSVH', 'KTDF', 'KTOI', 'KTTA', 'KUKF', 'KVUJ', 'CYJT', 'PASC', 'VLLB', 'VLLN', 'VLPS', 'VLSK', 'VTUD', 'VTUI', 'VTUK', 'VTUL', 'VTUO', 'VTUQ', 'VTUU', 'VTUV', 'VTUW', 'VTBD', 'VTBS', 'VTBU', 'VTCC', 'VTCT', 'VTSG', 'VTSP', 'VTSS', 'CYXR', 'CWLY', 'CYCK', 'CYVM', 'KNYC', 'CPBT', 'CPEH', 'CPFI', 'CPRO', 'CPRY', 'CPST', 'CPSV', 'CPXL', 'CXFM', 'CXHD', 'CXHP', 'CXMG', 'CXPL', 'CXSC', 'CXSL', 'CXSP', 'CXTH', 'CXVW', 'CWMT', 'CZEV', 'CZFS', 'CZSM', 'CWYJ', 'CWZA', 'CWZO', 'CWZQ', 'CXKA', 'CTNK', 'CWKK', 'CXBI', 'CXZC', 'CWQH', 'CWQK', 'CWQO', 'CWQP', 'CWQR', 'CWQV', 'CWRJ', 'CWRK', 'CWRT', 'CWRY', 'CWRZ', 'CWSG', 'CWSP', 'CWST', 'CXBA', 'CXBR', 'CXCD', 'CXCP', 'CXCS', 'CXFR', 'CXHR', 'CXKI', 'CXKM', 'CXLB', 'CXOY', 'CXPA', 'CXPC', 'CXRB', 'CXRL', 'CXTD', 'CXVN', 'CZMJ', 'CZTB', 'CWEB', 'CWEL', 'CWEW', 'CWFF', 'CWFJ', 'CWFQ', 'CWGB', 'CWGL', 'CWGM', 'CWAF', 'CWAQ', 'CWAV', 'CWBA', 'CWBO', 'CWBS', 'CWBT', 'CWBZ', 'CWCF', 'CWCJ', 'CWCO', 'CWDJ', 'CWDK', 'CXBK', 'CXKT', 'CXCA', 'CXCK', 'CXDE', 'CXDI', 'CXDW', 'CXEA', 'CXEC', 'CXEG', 'CXET', 'CXGH', 'CXHA', 'CXHF', 'CXIB', 'CXMD', 'CXMI', 'CXMM', 'CXNM', 'CXRH', 'CXSH', 'CXTP', 'CXWN', 'CWJT', 'CWJV', 'CWJW', 'CWJX', 'CWKG', 'CWKH', 'CWKX', 'CWLC', 'CWLE', 'CWLM', 'CWMJ', 'CWMM', 'CWTA', 'CWTG', 'CWTN', 'CWTT', 'CWTY', 'CWUS', 'CWVF', 'CWVI', 'CWVN', 'CWWF', 'CWWK', 'CWXA', 'CERM', 'CZCR', 'CMFM', 'CMGB', 'CWGR', 'CWGT', 'CWGW', 'CWGX', 'CWHI', 'CWHT', 'CWID', 'CWIG', 'CWII', 'CWIJ', 'CWIP', 'CWIS', 'CWIT', 'CWIW', 'CWIZ', 'CWJB', 'CWJC', 'CWNK', 'CWNM', 'CWNP', 'CWOC', 'CWOD', 'CWPD', 'CWPF', 'CWPZ', 'CTCK', 'CWBE', 'CWLS', 'CWPO', 'CWWZ', 'CWDQ', 'CWDV', 'CWWB', 'CWCT', 'CWLB', 'CWDC', 'CWEH', 'CWKO', 'CWEQ', 'CWJD', 'CWLP', 'CWRO', 'CWZG', 'CWVT', 'CWZW', 'CWPK', 'CWBY', 'CWBV', 'CWRN', 'CWSS', 'CWRA', 'CWSF', 'CWER', 'CWBU', 'CWIK', 'WBGG', 'WBKK', 'WMKJ', 'WMKK', 'WMKP', 'WMSA', 'WBGB', 'WBGR', 'WBGS', 'WBGY', 'WBKL', 'WBKS', 'WBKT', 'WBKW', 'WBSB', 'SAOC', 'CYCY', 'EGQK', 'EGXS', 'VVCI', 'VVCR', 'VVCT', 'VVNB', 'VVPB', 'VVPQ', 'VVTS', 'VVDN', 'FABL', 'FALW', 'FAOB', 'K2G4', 'K2W6', 'K7W6', 'KAFN', 'KAFP', 'KAID', 'KCBE', 'KCGE', 'KCGS', 'KCTZ', 'KDCM', 'KDMW', 'KDPL', 'KESN', 'KEXX', 'KEYF', 'KFDK', 'KFFA', 'KFIG', 'KGEV', 'KHNZ', 'KHRJ', 'KIXA', 'KIZG', 'KJNX', 'KLEE', 'KLQK', 'KMQI', 'KMRN', 'KMTN', 'KONX', 'KPIB', 'KPLD', 'KSPA', 'KSUT', 'KVNC', 'KW29', 'PACM', 'VDPP', 'VDSR', 'VDSV', 'VLVT', 'VYYY', 'VYNT', 'ULAA', 'ULMM', 'ULOO', 'ULPB', 'UMKK', 'UUOO', 'UUYY', 'VIJP', 'URKA', 'URKK', 'URMG', 'URML', 'URMM', 'URMN', 'URMO', 'URMT', 'URRP', 'URSS', 'URWA', 'URWI', 'URWW', 'ULLI', 'UUBW', 'UUDD', 'UUDL', 'UUEE', 'UUWW', 'UUMO', 'UUOL', 'VTSH', 'VOKN', 'UIAA', 'UIBB', 'UIII', 'UIUU', 'RJOR', 'RJOS', 'RJOW', 'RJOY', 'RJSC', 'RJSI', 'RJSM', 'RJSR', 'RJSY', 'ROMY', 'RORS', 'RORY', 'ROYN', 'USPP', 'UWKD', 'UWKE', 'UWKS', 'UWOR', 'UWOO', 'UWSS', 'UWWW', 'UWUU', 'USCC', 'USNN', 'USRR', 'USSS', 'RJBD', 'RJBE', 'RJBT', 'RJCN', 'RJCO', 'RJCW', 'RJDC', 'RJDT', 'RJFE', 'RJFG', 'RJKA', 'RJNW', 'UUBC', 'UUBP', 'UUOB', 'UUOK', 'UWGG', 'UHBB', 'UHHH', 'UHPP', 'UHWW', 'UHMA', 'UHMM', 'UHSS', 'USCM', 'UEEE', 'UOOO', 'EBBL', 'EHKD', 'EHVL', 'ETHB', 'ETHC', 'ETOU', 'KBIX', 'KLOR', 'PASY', 'KHRT', 'VOHY', 'PAJN', 'LIMH', 'LIMK', 'LIMN', 'LIPL', 'LIVM', 'CYHD', 'VOGO', 'VASD', 'FAWB', 'LICF', 'LICL', 'LIED', 'LIQC', 'LIRE', 'LIRK', 'LIRX', 'LIMU', 'LIMY', 'LIPI', 'LIPS', 'LIQO', 'LIVD', 'LIVE', 'LIVO', 'LIVP', 'LIVR', 'LIVT']
link = 'http://tgftp.nws.noaa.gov/data/observations/metar/decoded/{}.TXT'
add_link = 'https://weather.gladstonefamily.net/site/{}' #use this link to get additional data & history


def getdata():
    for icao_i in icao:
        print('current ucai_i = ' + icao_i)
        temp_array = dataparser.getairportdata(icao_i)
        print('/////////TEMP ARRAY//////////')
        print(temp_array)
        print('////////*************////////')
        try:
            setdb(temp_array[0],temp_array[1],temp_array[2],temp_array[3],temp_array[4],temp_array[5],temp_array[6],
              temp_array[7],temp_array[8],temp_array[9],temp_array[10],temp_array[11],temp_array[12])
        except Exception as error:
            print(error)
    return 'Test'


def setdb(place, rdate, pressure, wind, humidity, temperature, name, crit_sum, crit_w, crit_h, crit_t, result_coordinatex, result_coordinatey, result_data, result_hour, result_minute):
    conn = sqlite3.connect("static/icao_db.db")
    c = conn.cursor()
    c.execute("Create TABLE if not exists %s (rdate TEXT,pressure FLOAT,wind FLOAT,humidity FLOAT, temperature FLOAT, name TEXT, crit_overall FLOAT, crit_wind FLOAT, crit_humidity FLOAT, crit_temperature FLOAT, r_data TEXT, r_hour FLOAT, r_minute FLOAT)"
              % place)
    try:
        c.execute("INSERT INTO %s VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)" % place, (rdate, pressure, wind, humidity, temperature, name, crit_sum, crit_w, crit_h, crit_t, result_data, result_hour, result_minute))
        conn.commit()
    except Exception as err:
        print(err)
        pass
    setuniquedb(place, rdate, pressure, wind, humidity, temperature, name, crit_sum, crit_w, crit_h, crit_t, result_coordinatex, result_coordinatey, result_data, result_hour, result_minute)
    return 'Print'


def setuniquedb(place, rdate, pressure, wind, humidity, temperature, name, crit_sum, crit_w, crit_h, crit_t,
                result_coordinatex, result_coordinatey, result_data, result_hour, result_minute):
    conn = sqlite3.connect("static/icao_db.db")
    c = conn.cursor()
    try:
        c.execute("Create TABLE if not exists currentvalues (place TEXT,rdate TEXT,pressure FLOAT,wind FLOAT, humidity FLOAT, temperature FLOAT, aname TEXT, crit_overall FLOAT, crit_wind FLOAT, crit_humidity FLOAT, crit_temperature FLOAT, result_coordinatex FLOAT, result_coordinatey FLOAT, r_data TEXT, r_hour FLOAT, r_minute FLOAT)")
    except Exception as err:
        print(err)
        pass
    try:
        c.execute("DELETE FROM currentvalues WHERE place=?", (place,))
        conn.commit()
        c.execute("INSERT INTO currentvalues VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(place, rdate, pressure, wind, humidity, temperature, name, crit_sum, crit_w, crit_h, crit_t, result_coordinatex, result_coordinatey, result_data, result_hour, result_minute))
        conn.commit()
    except Exception as err:
        print(err)
        pass
    createjson(place, rdate, pressure, wind, humidity, temperature, name, crit_sum, crit_w, crit_h, crit_t,
               result_coordinatex, result_coordinatey, result_data, result_hour, result_minute)
    return 'Print'


def clearjson():
    print('JSON got cleared')
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


def createjson(place, rdate, pressure, wind, humidity, temperature, name, crit_sum, crit_w, crit_h, crit_t,
               result_coordinatex, result_coordinatey, result_data, result_hour, result_minute):

    print("JSON created")
    crit_w_json = ''
    crit_h_json = ''
    crit_t_json = ''
    fincoordx = converter.truncate(result_coordinatex, 4)
    fincoordy = converter.truncate(result_coordinatey, 4)
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
            "crit_sum_val": crit_sum,
            "date": result_data,
            "hour": result_hour,
            "minute": result_minute
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


def recordtext(icao, info):
    f = open("static/" + icao + ".txt", "w+")
    f.write("" + info)
    f.close()
    return 'Done'