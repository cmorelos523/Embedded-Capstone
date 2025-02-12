import gps

# Create a GPS session
session = gps.gps("localhost", "2947")

# Loop to get GPS data
while True:
    session.next()  # Get the next GPS data
    if session.valid:
        # If valid data is available, print the data
        print("Latitude: ", session.lat)
        print("Longitude: ", session.lon)
        print("Altitude: ", session.alt)
        print("Time: ", session.time)
    else:
        # If the data is invalid, print a message indicating no fix
        print("Waiting for GPS fix...")

