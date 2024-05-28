import serial
import os
from gpiozero import LED
from time import sleep

led=LED(23)
led.on()
sleep(0.5)
led.off()
sleep(0.5)

firstFixFlag = False # this will go true after the first GPS fix.
firstFixDate = ""

# Set up serial:
ser = serial.Serial(
    port='/dev/ttyS0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=1)

# Helper function to take HHMM.SS, Hemisphere and make it decimal:
def degrees_to_decimal(data, hemisphere):
    try:
        decimalPointPosition = data.index('.')
        degrees = float(data[:decimalPointPosition-2])
        minutes = float(data[decimalPointPosition-2:])/60
        output = degrees + minutes
        if hemisphere is 'N' or hemisphere is 'E':
            return output
        if hemisphere is 'S' or hemisphere is 'W':
            return -output
    except:
        return ""

# Helper function to take a $GPRMC sentence, and turn it into a Python dictionary.
# This also calls degrees_to_decimal and stores the decimal values as well.
def parse_GPGGA(dat):
    dat = dat.split(',')
    dicta = {
            'Afix_time': dat[1],
            'Avalidity': dat[2],
            'Alatitude': dat[2],
            'Alatitude_hemisphere' : dat[3],
            'Alongitude' : dat[4],
            'Alongitude_hemisphere' : dat[5],
            'Aspeed': dat[7],
            'Atrue_course': dat[8],
            'Altitude': dat[9],
            'Avariation': dat[10],
            'Avariation_e_w' : dat[11],
            'Achecksum' : dat[12]
    }
    dicta['decimal_latitude'] = degrees_to_decimal(dicta['Alatitude'], dicta['Alatitude_hemisphere'])
    dicta['decimal_longitude'] = degrees_to_decimal(dicta['Alongitude'], dicta['Alongitude_hemisphere'])
    return dicta

def parse_GPRMC(data):
    data = data.split(',')
    dict = {
            'fix_time': data[1],
            'validity': data[2],
            'latitude': data[3],
            'latitude_hemisphere' : data[4],
            'longitude' : data[5],
            'longitude_hemisphere' : data[6],
            'speed': data[7],
            'true_course': data[8],
            'fix_date': data[9],
            'variation': data[10],
            'variation_e_w' : data[11],
            'checksum' : data[12]
    }
    dict['decimal_latitude'] = degrees_to_decimal(dict['latitude'], dict['latitude_hemisphere'])
    dict['decimal_longitude'] = degrees_to_decimal(dict['longitude'], dict['longitude_hemisphere'])
    return dict

led.off()

# Main program loop:
while True:
    line = ser.readline()
    print (line)
    if "$GPRMC" in line: # This will exclude other NMEA sentences the GPS unit provides.
        gpsData = parse_GPRMC(line) # Turn a GPRMC sentence into a Python dictionary called gpsData
        if gpsData['validity'] == "A": # If the sentence shows that there's a fix, then we can log the line
            print ("Validity OK")
	    led.on()
	    sleep(1)
	    if firstFixFlag is False: # If we haven't found a fix before, then set the filename prefix with GPS date & time.
                firstFixDate = gpsData['fix_date'] + "-" + gpsData['fix_time']
                firstFixFlag = True
		with open("/home/pi/gps_experimentation/" + firstFixDate +"-simple-log.txt", "a") as myfile:
                    myfile.write('Date,GMT_Time,Latitude, Longitude, Speed' +"\n")
		with open("/home/pi/gps_experimentation/" + firstFixDate +"-simple-log_gpgga.txt", "a") as myfile:
                    myfile.write('GMT_Time, Latitude, Hemisphere, Longitude, Meridien, Altitude' +"\n")
		led.off()

            else: # write the data to a simple log file and then the raw data as well:
#		print (line)
		#print (gpsData['fix_time'])
		led.on()
                with open("/home/pi/gps_experimentation/" + firstFixDate +"-simple-log.txt", "a") as myfile:
                    myfile.write(gpsData['fix_date'] + "," + gpsData['fix_time'] + "," + str(gpsData['decimal_latitude']) + "," + str(gpsData['decimal_longitude'])+","+gpsData['speed'] +"\n")
                with open("/home/pi/gps_experimentation/" + firstFixDate +"-gprmc-raw-log.txt", "a") as myfile:
                    myfile.write(line)
#		led.off()

    if "$GPGGA" in line :
	led.on()
	print (line)
	gpsData = parse_GPGGA(line)
#	print (gpsData['Afix_time'])
#	print ("altitude" , gpsData['Altitude'])
#	print ("latitude", gpsData['Alatitude'], gpsData['Alatitude_hemisphere'])
#       print ("longitude", gpsData['Alongitude'],gpsData['Alongitude_hemisphere'])

#	with open("/home/pi/gps_experimentation/" + firstFixDate +"-simple-log_gpgga.txt", "a") as myfile:
#		myfile.write(gpsData['Afix_time'] + "," + str(gpsData['Alatitude'])+ ","+ str(gpsData['Alatitude_hemisphere']) + "," + str(gpsData['Alongitude'])+","+str(gpsData['Alongitude_hemisphere'])+str(gpsData['Altitude'] +"\n")

	with open("/home/pi/gps_experimentation/" + firstFixDate +"-gpgga-raw-log.txt", "a") as myfile:
         	myfile.write(line)

        with open("/home/pi/gps_experimentation/" + firstFixDate +"-simple-log_gpgga.txt", "a") as myfile:
           	myfile.write(gpsData['Afix_time'] + "," + gpsData['Alatitude']+ ","+ str(gpsData['Alatitude_hemisphere']) + "," + gpsData['Alongitude']+","+str(gpsData['Alongitude_hemisphere'])+","+gpsData['Altitude']+"\n")


	led.off()


