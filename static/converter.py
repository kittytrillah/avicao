import os
import sys
sys.path.insert(0, os.getcwd()+"/")
import sqlite3
import json
import requests
import re


def truncate(f, n):
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


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