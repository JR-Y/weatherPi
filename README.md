Still in works...

Uses code from http://www.home-automation-community.com/temperature-and-humidity-from-am2302-dht22-sensor-displayed-as-chart/

Except that the nodejs-webserver-with-soap-services.js & temperature-and-humidity-to-csv-logger.py fiels have been altered and renamed to index.js & logger.py

On pi you need to run:
pip install paho-mqtt

For posting / pulishing to thingspeak
git clone https://github.com/eclipse/paho.mqtt.python
cd paho.mqtt.python
python setup.py install


AUTOMATICALLY STARTING THE SCRIPTS ON BOOT

To run the node.js script in the background, forever will be used. 
To install it type  sudo npm -g install forever. 

Then open /etc/rc.local and add the following 3 lines before the 'exit 0' line



cd /home/pi/projects/temp-and-humidity  
/usr/bin/sudo /usr/bin/python logger.py 
&
/usr/bin/sudo /usr/local/bin/forever start index.js



With the next boot, the sensor data is recorded automatically and and the web server is started.