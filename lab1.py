import requests
import sqlite3

url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history'
params = {
    'aggregateHours':24,
    'startDateTime':'2020-09-29T00:0:00',
    'endDateTime':'2020-09-29T23:59:59',
    'unitGroup':'metric',
    'location': 'Volgograd,Russia',
    'key': 'I3D60I88UB6KPSDAVGK38HNP5',
    'contentType':'json'
}
data = requests.get(url, params).json()

with sqlite3.connect('weather.sqlite3') as connection:
    c = connection.cursor()
    c.execute('create table if not exists weather (date text, mint real, maxt real, location text, humidity real)')
    for row in data['locations']['Volgograd,Russia']['values']:
        c.execute('insert into weather values (?,?,?,?,?);', (row['datetimeStr'][:10], row['mint'], row['maxt'], 'Volgograd,Russia', row['humidity']))

    for row in c.execute('select * from weather;'):
        print(row)


