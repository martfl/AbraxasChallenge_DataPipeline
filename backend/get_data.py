import os
import requests
import redis
from datetime import datetime

url = "https://datos.cdmx.gob.mx/api/records/1.0/search/"
parameters = {"dataset": "prueba_fetchdata_metrobus", "rows": 0 }
response = requests.get(url, params=parameters)
nhits = response.json()["nhits"]
parameters["rows"] = nhits
print("{} units available. Starting data loading...".format(nhits))
response = requests.get(url, params=parameters)
data = response.json()["records"]

print(os.environ)
r = redis.Redis(host=os.environ['REDIS_MASTER_SERVICE_HOST'], port=os.environ['REDIS_MASTER_SERVICE_PORT'])
if r.ping() is True:
  print("Redis server connected!")
else:
  print("Unable to connect to redis.")

def get_alcaldia(lat,long):
  rlat = str(round(float(lat),2))
  rlong = str(round(float(long),2))
  coords = ",".join([rlat,rlong])
  cache = r.hget("cached_coords", coords)

  if cache is not None:
    print("Cached alcaldia found.")
    return cache.decode("utf-8")

  dist = "400"
  parameters = {
    "dataset": "ubicacion-acceso-gratuito-internet-wifi-c5",
    "geofilter.distance": ",".join([lat,long,dist])
  }
  response = requests.get(url, params=parameters).json()
  if "nhits" in response and response["nhits"] > 0:
    alcaldia = response["records"][0]["fields"]["alcaldia"]
    r.hmset("cached_coords",{coords:alcaldia})
    return alcaldia
  else:
    print("Location not found.")
    print({lat,long})
    return "FUERA DE RANGO"

r.delete("available_units", "available_alcaldias")
# TO DO delete each alcaldia:<NAME> key

for d in data:
  bus_id = d["fields"]["vehicle_id"]
  bus_lat, bus_long = d["fields"]["geographic_point"]
  bus_ts = int(datetime.timestamp(datetime.strptime(d["fields"]["date_updated"], "%Y-%m-%d %H:%M:%S")))
  bus_alcaldia = get_alcaldia(str(bus_lat), str(bus_long))

  record = {"coords":[bus_lat,bus_long], "alcaldia": bus_alcaldia, "date_updated": d["fields"]["date_updated"]}
  print(bus_id)
  print(record)
  r.rpush("available_units", bus_id)
  r.zadd("vehicle_id:{}".format(bus_id), {str(record):bus_ts})
  r.sadd("available_alcaldias", bus_alcaldia)
  r.hmset("alcaldia:{}".format(bus_alcaldia), {bus_id:bus_ts})

