#!/usr/bin/python
import sys
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import Adafruit_DHT as dht
import smtplib
import sqlite3
import os
import time
import glob



dbname='/var/www/templog.db'

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
send_email_ps=0
send_email_h=0
send_email_t=0
RR=0
RH=0
RT=0
recipient = [" test@email.com "]

def log_temperature(temp):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("INSERT INTO temps values(datetime('now'), (?))", (temp,))

    conn.commit()

    conn.close()


def log_humidity(humi):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("INSERT  INTO humis values(datetime('now'), (?))", (humi,))

    conn.commit()

    conn.close()



def display_temp_data():

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    for row in curs.execute("SELECT * FROM temps"):
        print str(row[0])+"	"+str(row[1])

    conn.close()

def display_humi_data():

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    for row in curs.execute("SELECT * FROM humis"):
        print str(row[0])+"     "+str(row[1])

    conn.close()



while True:

    value = mcp.read_adc(7)
    h,t = dht.read_retry(dht.DHT22, 4)
    op = open ('/home/pi/temp-data.txt', 'w')
    op.write ('{0:0.0f}\n'.format (t))
    op.close ()
    op = open ('/home/pi/humi-data.txt', 'w')
    op.write ('{0:0.0f}\n'.format (h))
    op.close ()
    log_temperature(t)
    log_humidity(h)
 #   display_temp_data()
 #   display_humi_data()
    if ( value < 1000 ):
        if (send_email_ps != 1):
               msg = "Subject:Alert\nExternal Power Supply is down\n Location: DC1 at UVA".format(value)
	       server = smtplib.SMTP('localhost')
               server.sendmail("sensor@email.com", recipient, msg)
               send_email_ps=1
               RR=1
        else:
	       pass
    else:
        if (RR==1):
                msg = "Subject:Recovery Alert\nExternal Power Supply is back up\n Location: DC1 at UVA".format(value)
                server = smtplib.SMTP('localhost')
		server.sendmail("sensor@email.com", recipient, msg)
                send_email_ps=0
                RR=0
        else:
                send_email_ps=0
                RR=0
    if ( h > 70 or h < 10 ):

        if (send_email_h != 1 ):
              	msg = "Subject:Alert\nWarning for Humidity:: Reads at: {0:0.1f}%\nLocation: DC1 at UVA".format(h)
               	server = smtplib.SMTP('localhost')
		server.sendmail("sensor@email.com", recipient, msg)
               	send_email_h=1
               	RH=1
        else:
		pass
    else:
         if (RH==1):
                msg = "Subject:Recovery Alert\nWarning for Humidity Recovered :: Reads at: {0:0.1f}%\nLocation: DC1 at UVA".format(h)
		server = smtplib.SMTP('localhost')
                server.sendmail("sensor@email.com", recipient, msg)
                send_email_h=0
                RH=0
         else:
                send_email_h=0
                RH=0
    if ( t > 42 ):
        if (send_email_t != 1):
                msg = "Subject:Alert\nCurrent Temperature Reads at : {0:0.1f} Celcius\nLocation: DC1 at UVA".format(t)
                server = smtplib.SMTP('localhost')
		server.sendmail("sensor@email.com", recipient, msg)
                send_email_t=1
                RT=1
        else:
		pass
    else:
        if (RT==1):
                msg = "Subject:Recovery Alert\nHigh Temperature Recovered :: Reads at: {0:0.1f}%\nLocation: DC1 at UVA".format(h)
		server = smtplib.SMTP('localhost')
                server.sendmail("sensor@email.com", recipient, msg)
                send_email_t=0
                RT=0
        else:
                send_email_t=0
                RT=0
    time.sleep(4)

