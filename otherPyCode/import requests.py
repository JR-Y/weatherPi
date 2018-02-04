import requests
r = requests.post("https://api.thingspeak.com/update", {'field2': dht[i].latest_temperature, 'field1': dht[i].latest_humidity})






conn = httplib.HTTPConnection("api.thingspeak.com:80")                
                        try:
                                conn.request("POST", "/update", params, headers)
                                response = conn.getresponse()
                                print temp
                                print response.status, response.reason
                                data = response.read()
                                conn.close()
                        except:
                                print "connection failed"