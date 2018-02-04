Still in works...

Uses code from http://www.home-automation-community.com/temperature-and-humidity-from-am2302-dht22-sensor-displayed-as-chart/

Except that the nodejs-webserver-with-soap-services.js & temperature-and-humidity-to-csv-logger.py fiels have been altered and renamed to index.js & logger.py

On pi you need to run:
pip install paho-mqtt

For posting / pulishing to thingspeak
git clone https://github.com/eclipse/paho.mqtt.python
cd paho.mqtt.python
python setup.py install