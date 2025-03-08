from Model import Measurement, Station, session

from sqlalchemy import select, func
import datetime

import matplotlib.pyplot as plt
import pandas as pd



def main():
  q = select(Measurement.date).order_by(Measurement.date.desc())
  most_recent_date = session.scalars(q).first()
  print(f'most_recent_date = {most_recent_date}')

  most_recent_date = datetime.datetime.strptime(most_recent_date, '%Y-%m-%d')
  one_year_ago = most_recent_date - datetime.timedelta(days=365)

  data = session.execute(select(Measurement.date, Measurement.prcp).where(Measurement.date >= one_year_ago)).all()
  # print(f'data = {data}')

  df = pd.DataFrame(data, columns=['date', 'prcp'])
  df = df.set_index('date').sort_values('date').dropna()

  # print(df)

  df.plot(y='prcp', use_index=True, label='Precipitation', color='teal', rot=90)

  plt.xlabel('Date')
  plt.ylabel('Inches')
  plt.title('Precipitation in Hawaii from 2016-08-23 to 2017-08-23')
  plt.legend()
  plt.tight_layout()

  plt.savefig('images/hawaii_prec.png')

  plt.show()

  # Summary statistics
  print(df.describe())

  q = select(Station.station)
  total_stations = session.scalars(q).all()
  print(f'total_stations = {len(total_stations)}')

  q = select(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc())
  most_active_stations = session.execute(q).all()
  print(f'most_active_stations = {most_active_stations}')

  most_active_station = most_active_stations[0]
  print(f'most_active_station = {most_active_station}')

  least_active_station = most_active_stations[-1]
  print(f'least_active_station = {least_active_station}')

  most_active_station = most_active_station[0]
  print(f'most_active_station = {most_active_station}')

  q = select(Measurement.date, Measurement.tobs).where(Measurement.station == most_active_station)
  most_active_station_data = session.execute(q).all()
  # print(f'most_active_station_data = {most_active_station_data}')

  
  df = pd.DataFrame(most_active_station_data, columns=['date', 'tobs'])
  df = df.set_index('date').sort_values('date').dropna()

  # print(df)

  df.plot.hist(bins=12, color='teal')

  plt.xlabel('Temperature')
  plt.ylabel('Frequency')
  plt.title(f'Temperature Frequency at Station {most_active_station}')
  plt.legend()
  plt.tight_layout()

  plt.savefig('images/hawaii_temp.png')

  plt.show()

  # Summary statistics
  print(df.describe())

if __name__ == '__main__':
  main()

