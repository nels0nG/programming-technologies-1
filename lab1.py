import requests
from sqlalchemy import create_engine, Table, Column, String, Float, MetaData
from sqlalchemy.sql import select

url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history'
params = {
    'aggregateHours': 24,
    'startDateTime': '2020-09-29T00:0:00',
    'endDateTime': '2020-09-29T23:59:59',
    'unitGroup': 'metric',
    'location': 'Volgograd,Russia',
    'key': 'I3D60I88UB6KPSDAVGK38HNP5',
    'contentType': 'json',
}
data = requests.get(url, params).json()

engine = create_engine('sqlite:///weather.sqlite3')
metadata = MetaData()
weather = Table(
    'weather',
    metadata,
    Column('date', String),
    Column('mint', Float),
    Column('maxt', Float),
    Column('location', String),
    Column('humidity', Float),
)
metadata.create_all(engine)

c = engine.connect()

for row in data['locations']['Volgograd,Russia']['values']:
    c.execute(
        weather.insert(),
        [
            {
                'date': row['datetimeStr'][:10],
                'mint': row['mint'],
                'maxt': row['maxt'],
                'location': 'Volgograd,Russia',
                'humidity': row['humidity'],
            }
            for row in data['locations']['Volgograd,Russia']['values']
        ],
    )

for row in c.execute(select([weather])):
    print(row)

