import sys, json, requests, csv, os
from time_forcli import get_local_time


class WeatherReport:
    def __init__(self, lat, long, api_key):
        self.lat = lat
        self.long = long
        self.api_key = api_key
        self.raw_data = {}
        self.data = {}

    def fetch(self):
        try:
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather?lat="
                + self.lat + "&lon=" + self.long + "&appid=" + self.api_key,
                timeout=20
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ValueError(f"Weather API request failed: {e}.")
        except requests.exceptions.ConnectionError:
            raise ConnectionError(f"Could Not Connect To The Weather Service.")
        except requests.exceptions.Timeout:
            raise TimeoutError(f"Weather Server Took Too Long To Respond.")

        self.raw_data = response.json()
        return self.raw_data

    def parse(self):
        try:
            desc_store = []
            for i in self.raw_data['weather']:
                desc_store.append(i['description'])

            refined_dict = {
                "temp": (self.raw_data['main']['temp'] - 273.15),
                "feels_like": (self.raw_data['main']['feels_like'] - 273.15),
                "humidity": (self.raw_data['main']['humidity']),
                "wind_speed": self.raw_data['wind']['speed'],
                "wind_deg": self.raw_data['wind']['deg'],
                "wind_gust": self.raw_data['wind'].get('gust'),
                "country": self.raw_data['sys']['country'],
                "name": self.raw_data['name'],
                "date": self.raw_data['dt'],
                "sunrise": self.raw_data['sys']['sunrise'],
                "sunset": self.raw_data['sys']['sunset'],
                "timezone": self.raw_data['timezone'],
            }
            refined_dict['description'] = ",".join(desc_store)
        except KeyError as e:
            raise KeyError(f"Missing Key: {e}.")
        except TypeError as e:
            raise TypeError(f"Invalid Data: {e}.")

        self.data = refined_dict
        return self.data

    def display(self):

        print(f"\nDescription: {self.data['description']}")
        print(f"Temp is: {self.data['temp']:.02f}C, while it feels-like:{self.data['feels_like']:.02f}C")
        print(f"Humidity is at {self.data['humidity']}%.")
        print(f"Wind speed and Wind degree are {self.data['wind_speed']}m/s and {self.data['wind_deg']}° respectively while wind gust is {self.data['wind_gust']}m/s,")
        print(f"Country:{self.data['country']}")
        print(f"City:{self.data['name']}")

        cur_time = get_local_time(self.data['date'], self.data['timezone'])
        sunrise = get_local_time(self.data['sunrise'], self.data['timezone'])
        sunset = get_local_time(self.data['sunset'], self.data['timezone'])

        print(f"Local Time in {self.data['country']}|{self.data['name']}: {cur_time.strftime('%Y-%m-%d %I:%M:%S %p')}")
        print(f"Sunrise: {sunrise.strftime('%I:%M:%S %p')}\nSunset:{sunset.strftime('%I:%M:%S %p ')}\n")

    def save(self, filename="weather.csv"):
        file_is_new = (not os.path.exists(filename)) or (os.path.getsize(filename) == 0)

        try:
            with open(filename, "a+", newline="", encoding="utf-8") as file:
                file.seek(0)
                reader = csv.DictReader(file)
                count = 0
                Is_duplicate = False
                for row in reader:
                    count += 1
                    if (row['name'] == self.data['name'] and row['raw_epoch'] == str(self.data['date'])):
                        Is_duplicate = True
                        break

                writer = csv.DictWriter(file, fieldnames=["count", "country", "name", "temp", "humidity", "cur_time", "raw_epoch"])

                if file_is_new:
                    writer.writeheader()

                if Is_duplicate:
                    count += 0
                else:
                    count += 1
                    writer.writerow({
                    'count': count,
                    'country': self.data['country'],
                    'name': self.data['name'],
                    'temp': f"{self.data['temp']:.02f}",
                    'humidity': self.data['humidity'],
                    "raw_epoch": self.data['date'],
                    "cur_time": get_local_time(self.data['date'], self.data['timezone']).strftime('%Y-%m-%d %I:%M:%S %p ')
                })
        except PermissionError:
            print(f"Couldn't Save Data, '{filename}' may be open.")
        except OSError as e:
            print(f"Couldn't Save Weather Data: {e}.")


def main():
    try:
        if len(sys.argv) != 4:
            sys.exit(f"Usage Instructions: {sys.argv[0]} <arg1> <arg2> <arg3>")

        lat, long, api_key = sys.argv[1], sys.argv[2], sys.argv[3]

        report = WeatherReport(lat, long, api_key)
        report.fetch()
        report.parse()
        report.display()
        report.save()
    except (ValueError, TypeError, ConnectionError, TimeoutError, KeyError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()