import serial
import pynmea2

def read_gps_data():
    try:
        # Configure the serial port
        ser = serial.Serial("/dev/ttyS0", 9600, timeout=1)
        
        while True:
            try:
                # Read a line from the serial port
                line = ser.readline().decode('utf-8').strip()
                
                # Check if the line is a valid NMEA sentence
                if line.startswith("$GPGGA") or line.startswith("$GNRMC"):
                    msg = pynmea2.parse(line)
                    
                    # Print the parsed data
                    print("Timestamp: %s" % msg.timestamp)
                    print("Latitude: %s %s" % (msg.latitude, msg.latitude_direction))
                    print("Longitude: %s %s" % (msg.longitude, msg.longitude_direction))
                    print("---")
                    
            except pynmea2.ParseError as e:
                print(f"Parse error: {e}")
            except UnicodeDecodeError as e:
                print(f"Decode error: {e}")
    except serial.SerialException as e:
        print(f"Serial port error: {e}")

if __name__ == "__main__":
    read_gps_data()
