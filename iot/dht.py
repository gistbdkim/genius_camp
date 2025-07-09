# dht_simple.py

import time
import board
import adafruit_dht

dht_sensor = adafruit_dht.DHT11(board.D4)

print("Starting temperature and humidity measurement. (Press Ctrl+C to exit)")

try:
    while True:
        try:
            temperature_c = dht_sensor.temperature
            humidity = dht_sensor.humidity

            print(f"Temperature: {temperature_c:.1f}°C, Humidity: {humidity:.1f}%")

        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dht_sensor.exit()
            raise error

        time.sleep(2.0)

except KeyboardInterrupt:
    print("\nExiting program.")
    dht_sensor.exit()
