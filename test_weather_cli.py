import pytest,csv
from weathercli import extract_weather_info, display_weather, store_weather_data
def make_weather_data(**kwargs):
    base={
  "coord": {
    "lon": 10.99,
    "lat": 44.34
  },
  "weather": [
    {
      "id": 501,
      "main": "Rain",
      "description": "moderate rain",
      "icon": "10d"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 298.48,
    "feels_like": 298.74,
    "temp_min": 297.56,
    "temp_max": 300.05,
    "pressure": 1015,
    "humidity": 64,
    "sea_level": 1015,
    "grnd_level": 933
  },
  "visibility": 10000,
  "wind": {
    "speed": 0.62,
    "deg": 349,
    "gust": 1.18
  },
  "rain": {
    "1h": 3.16
  },
  "clouds": {
    "all": 100
  },
  "dt": 1661870592,
  "sys": {
    "type": 2,
    "id": 2075663,
    "country": "IT",
    "sunrise": 1661834187,
    "sunset": 1661882248
  },
  "timezone": 7200,
  "id": 3163858,
  "name": "Zocca",
  "cod": 200
}
    base.update(kwargs)
    return base

def test_normal_extract_testcase():
    result=extract_weather_info(make_weather_data())
    expected={"temp":25.33,"feels_like":25.59,"humidity":64,"wind_speed":0.62,"wind_deg":349,"wind_gust":1.18,"country":"IT","name":"Zocca","date":1661870592,"sunrise":1661834187,"sunset":1661882248,"timezone":7200,"description":"moderate rain"}
    assert pytest.approx(result)==(expected)
def test_extradata_extract_testcase():
    result=extract_weather_info(make_weather_data(dt_txt="2022-09-04 12:00:00",rainy=0.49))
    expected={"temp":25.33,"feels_like":25.59,"humidity":64,"wind_speed":0.62,"wind_deg":349,"wind_gust":1.18,"country":"IT","name":"Zocca","date":1661870592,"sunrise":1661834187,"sunset":1661882248,"timezone":7200,"description":"moderate rain"}
    assert pytest.approx(result)==(expected)
def test_list_multiple_elements_extract_testcase():
    result=extract_weather_info(make_weather_data(weather=[
    {
      "id": 501,
      "main": "Rain",
      "description": "moderate rain",
      "icon": "10d"
    },
    {
      "id": 510,
      "main": "Sunny",
      "description": "overcast clouds",
      "icon": "10b"
    }
]))
    expected={"temp":25.33,"feels_like":25.59,"humidity":64,"wind_speed":0.62,"wind_deg":349,"wind_gust":1.18,"country":"IT","name":"Zocca","date":1661870592,"sunrise":1661834187,"sunset":1661882248,"timezone":7200,"description":"moderate rain,overcast clouds"}
    assert pytest.approx(result)==(expected)
def test_nogust_extract_testcase():
    result=extract_weather_info(make_weather_data(wind={"speed": 0.62, "deg": 349, "gust": None}))
    expected={"temp":25.33,"feels_like":25.59,"humidity":64,"wind_speed":0.62,"wind_deg":349,"wind_gust":None,"country":"IT","name":"Zocca","date":1661870592,"sunrise":1661834187,"sunset":1661882248,"timezone":7200,"description":"moderate rain"}
    assert pytest.approx(result)==expected



def test_missing_data_extract_testcase():
    raw_data=make_weather_data()
    del raw_data['weather'],raw_data['wind']
    with pytest.raises(KeyError):
      result=extract_weather_info(raw_data)
def test_error_no_dict_case():
    with pytest.raises(KeyError):
        extract_weather_info({})
def test_error_none_case():
    with pytest.raises(TypeError):
        extract_weather_info()