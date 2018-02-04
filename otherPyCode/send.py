try:
    sendThing(latest_value_datetime,"0",dht[0].latest_temperature,"0",dht[0].latest_humidity)
except:
    print ("There was an error while publishing the data.")  
    
def sendThing(timestamp,tempIn,tempOut,humIn,humOut):
  channelID = "280089"

  apiKey = "9QDFQOBPVXVGCDVX"

  useSSLWebsockets = True

  mqttHost = "mqtt.thingspeak.com"

  if useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
    tPort = 443

  topic = "channels/" + channelID + "/publish/" + apiKey
    
  temperature = tempOut
  humidity = humOut
  print (" Temp: =",temperature,"   Hum =",humidity)
  tPayload = "field1=" + str(humidity) + "&field2=" + str(temperature)

  try:
    publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)

  except:
    print ("There was an error while publishing the data.")