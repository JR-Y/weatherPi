# ThingSpeak Update Using MQTT
# Copyright 2016, MathWorks, Inc

# This is an example of publishing to multiple fields simultaneously.
# Connections over standard TCP, websocket or SSL are possible by setting
# the parameters below.
#
# CPU and RAM usage is collected every 20 seconds and published to a
# ThingSpeak channel using an MQTT Publish
#
# This example requires the Paho MQTT client package which
# is available at: http://eclipse.org/paho/clients/python

from __future__ import print_function
import paho.mqtt.publish as publish

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

while(True):
    
 
    temperature = "temp"
    humidity = "hum"
    print (" Temp: =",temperature,"   Hum =",humidity)

    tPayload = "field1=" + str(humidity) + "&field2=" + str(temperature)

    try:
        publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)

    except (KeyboardInterrupt):
        break

    except:
        print ("There was an error while publishing the data.")