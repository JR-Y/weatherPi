# Written by David Neuy
# Version 0.1.0 @ 03.12.2014
# This script was first published at: http://www.home-automation-community.com/
# You may republish it as is or publish a modified version only when you 
# provide a link to 'http://www.home-automation-community.com/'. 

#install dependency with 'sudo easy_install apscheduler' NOT with 'sudo pip install apscheduler'
import os, sys, Adafruit_DHT, time, requests
from datetime import datetime, date
from config_logger import *
from apscheduler.schedulers.background import BackgroundScheduler
#from __future__ import print_function
import paho.mqtt.publish as publish

sensor_values_folder         = "public/sensor-values/"

sensor                       = Adafruit_DHT.AM2302 #DHT11/DHT22/AM2302
csv_header_temperature       = "timestamp,temperature_in_celsius\n"
csv_header_humidity          = "timestamp,relative_humidity\n"
csv_entry_format             = "{:%Y-%m-%d %H:%M:%S},{:0.1f}\n"
sec_between_log_entries      = 1800
latest_value_datetime        = None

class Sensors:
  def __init__(self, gpio, sensor_name):
      self.gpio                         = gpio
      self.sensor_name                  = sensor_name
      self.hist_temperature_file_path   = sensor_values_folder + "temperature_" + sensor_name + "_log_" + str(date.today().year) + ".csv"
      self.latest_temperature_file_path = sensor_values_folder + "temperature_" + sensor_name + "_latest_value.csv"
      self.hist_humidity_file_path      = sensor_values_folder + "humidity_" + sensor_name + "_log_" + str(date.today().year) + ".csv"
      self.latest_humidity_file_path    = sensor_values_folder + "humidity_" + sensor_name + "_latest_value.csv"
      self.latest_humidity              = 0.0
      self.latest_temperature           = 0.0

dht                          = [Sensors(4,'outside'),Sensors(17,'inside')] #define sensors (gpiopin on raspberry,name of sensor)

def write_header(file_handle, csv_header):
  file_handle.write(csv_header)

def write_value(file_handle, datetime, value):
  line = csv_entry_format.format(datetime, value)
  file_handle.write(line)
  file_handle.flush()

def open_file_ensure_header(file_path, mode, csv_header):
  f = open(file_path, mode, os.O_NONBLOCK)
  if os.path.getsize(file_path) <= 0:
    write_header(f, csv_header)
  return f

def write_hist_value_callback():
  print ("Writing historyvalues")
  try:
  	sendThing(dht[0].latest_temperature,dht[0].latest_humidity,dht[1].latest_temperature,dht[1].latest_humidity)
  except:
    print ("There was an error while publishing the data.")  
  print ("Thinspark values sent") 
  try:
    for i in range(len(dht)):
      print("writing historyvalues")    
      write_value(open_file_ensure_header(dht[i].hist_temperature_file_path, 'a', csv_header_temperature), latest_value_datetime, dht[i].latest_temperature)
      print ("History callback written from sensor: ",dht[i]," Timestamp: ",latest_value_datetime," Temp: ", dht[i].latest_temperature)
      write_value(open_file_ensure_header(dht[i].hist_humidity_file_path, 'a', csv_header_humidity), latest_value_datetime, dht[i].latest_humidity)
      print ("History callback written from sensor: ", dht[i], " Timestamp: ", latest_value_datetime, " Temp: ", dht[i].latest_humidity)
    print("historyvalues written") 
  except:
    print("failed to save historyvalues")
print ("History files written")
 
def write_latest_value(latest_temperature_file_path, latest_humidity_file_path,latest_temperature,latest_humidity):
  with open_file_ensure_header(latest_temperature_file_path, 'w', csv_header_temperature) as f_latest_value:  #open and truncate
    write_value(f_latest_value, latest_value_datetime, latest_temperature)
  with open_file_ensure_header(latest_humidity_file_path, 'w', csv_header_humidity) as f_latest_value:  #open and truncate
    write_value(f_latest_value, latest_value_datetime, latest_humidity)
print ("Ignoring first 2 sensor values to improve quality...")

def sendThing(tempOut,humOut,tempIn,humIn):
  #channelID = "your thingspeak channelid key here"
  #apiKey = "your thingspeak api key here"
  useSSLWebsockets = True
  mqttHost = "mqtt.thingspeak.com"
  topic = "channels/" + channelID + "/publish/" + apiKey

  if useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
    tPort = 443  

  tPayload = "field1=" + str(humOut) + "&field2=" + str(tempOut) + "&field3=" + str(humIn) + "&field4=" + str(tempIn)

  try:
    publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)

  except:
    print ("There was an error while publishing the data.")

for i in range(len(dht)):
  for x in range(2):
    Adafruit_DHT.read_retry(sensor, dht[i].gpio)

print ("Creating interval timer. This step takes almost 2 minutes on the Raspberry Pi...")
#create timer that is called every n seconds, without accumulating delays as when using sleep
scheduler = BackgroundScheduler()
scheduler.add_job(write_hist_value_callback, 'interval', seconds=sec_between_log_entries)
scheduler.start()

print ("Started interval timer which will be called the first time in {0} seconds.".format(sec_between_log_entries))

try:
  while True:
    for i in range(len(dht)):
      while True:
        hum, temp = Adafruit_DHT.read_retry(sensor, dht[i].gpio)
        if hum is not None and temp is not None:
          if hum < 100 and hum > 0 and temp < 60 and temp > -35:
            dht[i].latest_humidity, dht[i].latest_temperature = hum, temp
            latest_value_datetime = datetime.today()
            write_latest_value(dht[i].latest_temperature_file_path,dht[i].latest_humidity_file_path,temp,hum)
            print (dht[i].latest_temperature_file_path, temp, dht[i].latest_humidity_file_path, hum)
            break
      time.sleep(20)
except (KeyboardInterrupt, SystemExit):
  scheduler.shutdown()


