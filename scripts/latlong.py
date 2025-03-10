import gps
import time
import json

def main():
    session = gps.gps(mode=gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    while True:
        report = session.next()
        if report['class'] == 'TPV':
            lat = getattr(report, 'lat', None)
            lon = getattr(report, 'lon', None)

        if lat is not None and lon is not None:
            data = {
                'lat': lat,
                'lon': lon,
                'time': getattr(report, 'time', time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
            }

        with open('gps_data.json', 'w') as outfile:
            json.dump(data, outfile)
                    
        print(f"Updated coordinates: {data}")
        time.sleep(5)
