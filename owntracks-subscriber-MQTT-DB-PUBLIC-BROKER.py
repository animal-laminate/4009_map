""" connect to MQTT and write owntracks data to a database """

import paho.mqtt.client as mqtt                                         #necessary imports
import sqlite3 as sql
import json, os
from datetime import date, datetime
import time

""" callback function for connection """    
def on_connect(client, userdata, flags, rc):                            #client method to connect
    if rc == 0:
        client.connected_flag = True                                    #set flag
        print("connected OK")                                           #let us know we connected to the broker
        client.subscribe("owntracks/4009user/#")
        #NEW TOPIC NEEDED
    else:
        print("Bad connection. Returned code = ", rc)                      #if we can't connect

""" callback function for messages received """
def on_message( client, userdata, msg ):                                #client method to get messages from topic
    con = sql.connect('locations-with-tid.db')                                   #name of the database. You might want to change it. 
    cur = con.cursor()
    try:
        cur.execute("CREATE TABLE Location(tid VARCHAR2(4), longitude NUMBER(10,6), latitude NUMBER(10,6), date VARCHAR2(20), time VARCHAR2(20));") 
    except:
        pass                                                            #if it already exists
    data = json.loads(msg.payload.decode("utf8"))                       #decode message
    day = date.today()                                                  #time functions
    clock = datetime.now()
    time = datetime.time(clock)
    print('writing to database')
    cur.execute("INSERT INTO Location values(?,?,?,?,?);", (data["tid"], data["lon"], data["lat"], str(day), str(time)))
                                                                        #puts the latitude, longitude from the posted message as well as the date and time when it was posted into the database
    print ("TID = {0} is currently at {1}, {2},{3},{4}".format(data['tid'], data['lat'], data['lon'], str(day), str(time)))
                                                                        #print device, latitude and longitude from the message; add time data (same as db)
    print(str(data))                                                    #print the entire message just for fun
    con.commit()
    cur.close()
    con.close()                                                         #close the database


client = mqtt.Client("Client-001")                                              #bind all functions to mqtt class
client.on_connect = on_connect
client.on_message = on_message
#client.username_pw_set("4009user", "mqttBROKER")                        #associate authentication details with the client
#client.tls_set("mqtt.coventry.ac.uk.crt")                               #certificate for client. needs to be in the same directory as this script
client.connect( "broker.hivemq.com" )                             #connect to the broker on an appropriate port
client.loop_forever()                                                   #keep looping forever - allows realtime subscription
