import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sqlalchemy import create_engine, Table, Column, String, Float, MetaData
from sqlalchemy.sql import select


class WeatherProvider:
    def __init__(self, key):
        self.key = key

    def get_data(self, location, start_date, end_date):
        url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history'
        params = {
            'aggregateHours': 24,
            'startDateTime': f'{start_date}T00:0:00',
            'endDateTime': f'{end_date}T23:59:59',
            'unitGroup': 'metric',
            'location': location,
            'key': self.key,
            'contentType': 'json',
        }
        data = requests.get(url, params).json()
        return [
            {
                'date': row['datetimeStr'][:10],
                'mint': row['mint'],
                'maxt': row['maxt'],
                'location': 'Berlin,Germany',
                'humidity': row['humidity'],
            }
            for row in data['locations'][location]['values']
        ]


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

provider = WeatherProvider('RLSTBNJPQLM5SPLDFWR7KJ0KK')

c.execute(weather.insert(), provider.get_data('Moscow,Russia', '2021-01-01', '2021-01-31'))

for row in c.execute('SELECT * FROM weather'):
    print(row)

#Create weather plots
fig, ax = plt.subplots()
ax.set(title='Plot of maximum temperature in Moscow in january')

ax.grid(which='minor',
        color = 'm')

maxt_y = []
maxt_x = []

#Select days from database
for row in c.execute('SELECT date FROM weather'):
    maxt_x.append(row)

#распаковываем список
maxt_x = [i for i, in maxt_x]

#Select minimal temperature from database
for row in c.execute('SELECT maxt FROM weather'):
    maxt_y.append(row)

#распаковываем список
maxt_y = [j for j, in maxt_y]


#plot limits
plt.xlim(0, len(maxt_y))
plt.ylim(min(maxt_y), max(maxt_y))

#plot building
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())

#set plot design
plt.plot(maxt_x, maxt_y, color='y', linewidth=2,
         linestyle='--')

plt.gcf().autofmt_xdate()
plt.show()