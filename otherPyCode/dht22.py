import urllib2 
myAPI = "280089" 
def getSensorData(): 
   RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 23) 
   return (str(RH), str(T)) 
def main(): 
   print 'starting...' 
   baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 
   while True: 
       try: 
           RH, T = getSensorData() 
           f = urllib2.urlopen(baseURL + 
                               "&field1=%s&field2=%s" % (RH, T)) 
           print f.read() 
           f.close() 
           sleep(300) #uploads DHT22 sensor values every 5 minutes 
       except: 
           print 'exiting.' 
           break 
# call main 
if __name__ == '__main__': 
   main()  
