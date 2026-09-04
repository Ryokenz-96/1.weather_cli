import pytest
from weathercli import display_weather
def make_weather_data(**overrides):
    base={'temp': 31.410000000000025, 'feels_like': 34.950000000000045, 'humidity': 57, 'wind_speed': 5.09, 'wind_deg': 178, 'wind_gust': 6.23, 'country': 'MM', 'name': 'Monywa', 'date': 1782194906, 'sunrise': 1782168987, 'sunset': 1782217677, 'timezone': 23400, 'description': 'overcast clouds'}
    base.update(overrides)
    return base
def test_normal_display_testcase(capsys):
    display_weather(make_weather_data())
    stdout,stderr=capsys.readouterr()
    assert stdout==("\nDescription: overcast clouds\nTemp is: 31.41C, while it feels-like:34.95C\nHumidity is at 57%.\nWind speed and Wind degree are 5.09m/s and 178° respectively while wind gust is 6.23m/s,\nCountry:MM\nCity:Monywa\nLocal Time in MM|Monywa: 2026-06-23 12:38:26 PM\nSunrise: 05:26:27 AM\nSunset:06:57:57 PM \n\n")
def test_no_windgust_display_testcase(capsys):
    display_weather(make_weather_data(wind_gust=None))
    stdout,stderr=capsys.readouterr()
    assert stdout==("\nDescription: overcast clouds\nTemp is: 31.41C, while it feels-like:34.95C\nHumidity is at 57%.\nWind speed and Wind degree are 5.09m/s and 178° respectively while wind gust is Nonem/s,\nCountry:MM\nCity:Monywa\nLocal Time in MM|Monywa: 2026-06-23 12:38:26 PM\nSunrise: 05:26:27 AM\nSunset:06:57:57 PM \n\n")
def test_extra_data_display_testcase(capsys):
    display_weather(make_weather_data(cod=200,visbility=10000,sea_level=1003))
    stdout,stderr=capsys.readouterr()
    assert stdout==("\nDescription: overcast clouds\nTemp is: 31.41C, while it feels-like:34.95C\nHumidity is at 57%.\nWind speed and Wind degree are 5.09m/s and 178° respectively while wind gust is 6.23m/s,\nCountry:MM\nCity:Monywa\nLocal Time in MM|Monywa: 2026-06-23 12:38:26 PM\nSunrise: 05:26:27 AM\nSunset:06:57:57 PM \n\n")

def test_display_empty_dict_testcase():
    with pytest.raises(KeyError):
        display_weather({})
def test_none_display_testcase():
    #only none given for displaying
    with pytest.raises(TypeError):
        display_weather(None)
@pytest.fixture
def full_weather_data():
    return{'temp': 31.410000000000025, 'feels_like': 34.950000000000045, 'humidity': 57, 'wind_speed': 5.09, 'wind_deg': 178, 'wind_gust': 6.23, 'country': 'MM', 'name': 'Monywa', 'date': 1782194906, 'sunrise': 1782168987, 'sunset': 1782217677, 'timezone': 23400, 'description': 'overcast clouds'}
@pytest.mark.parametrize("deleted_keys",
        (
            "temp", "feels_like", "humidity", "wind_speed", "wind_deg",
            "country", "name", "date", "sunrise", "sunset", "timezone"
        ),
)
def test_missing_fields_display_testcase(full_weather_data,deleted_keys):
    #remove some fields from dict given for displaying
    del full_weather_data[deleted_keys]
    with pytest.raises(KeyError):
        display_weather(full_weather_data)