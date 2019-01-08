import re
from datetime import date, time


def refreshtime():
    currentDT = datetime.datetime.now()
    return currentDT


def getdaydelta(year, month, day):
    d0 = date(refreshtime().year, refreshtime().month, refreshtime().day)
    d1 = date(year, month, day)
    delta = d1 - d0
    return delta.days


def gethourdelta(hour): #currently left unused
    return 'Done'


def gethour():
    val = refreshtime().hour
    return val


def getminute():
    val = refreshtime().minute
    return val


def getdate():
    val = '' + str(refreshtime().year) + '.' + str(refreshtime().month) + '.' + str(refreshtime().day)
    return val