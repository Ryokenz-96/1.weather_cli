import pytest,csv
from weathercli import extract_weather_info, display_weather, store_weather_data

@pytest.mark.parametrize(
        ("json_format","expected"),
    (
pytest.param(
    {
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
},{"temp":25.33,"feels_like":25.59,"humidity":64,"wind_speed":0.62,"wind_deg":349,"wind_gust":1.18,"country":"IT","name":"Zocca","date":1661870592,"sunrise":1661834187,"sunset":1661882248,"timezone":7200,"description":"moderate rain"},id="normal_testcase"),
pytest.param(
    {
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
  "cod": 200,
"dt_txt": "2022-09-04 12:00:00","rainy": {
        "3h": 0.49# extra garbage data, which is to be ignored by function
      }},{"temp":25.33,"feels_like":25.59,"humidity":64,"wind_speed":0.62,"wind_deg":349,"wind_gust":1.18,"country":"IT","name":"Zocca","date":1661870592,"sunrise":1661834187,"sunset":1661882248,"timezone":7200,"description":"moderate rain"},id="extradata_testcase"),
pytest.param(
    {
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
    },{
      "id": 510,
      "main": "Sunny",
      "description": "overcast clouds",
      "icon": "10b"
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
  "cod": 200,
},{"temp":25.33,"feels_like":25.59,"humidity":64,"wind_speed":0.62,"wind_deg":349,"wind_gust":1.18,"country":"IT","name":"Zocca","date":1661870592,"sunrise":1661834187,"sunset":1661882248,"timezone":7200,"description":"moderate rain,overcast clouds"},id="list_multiple_elements_testcase"),
pytest.param(
    {
  "coord": {
    "lon": 10.99,
    "lat": 44.34
  },
  "weather": [
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
  "cod": 200,
},{"temp":25.33,"feels_like":25.59,"humidity":64,"wind_speed":0.62,"wind_deg":349,"wind_gust":None,"country":"IT","name":"Zocca","date":1661870592,"sunrise":1661834187,"sunset":1661882248,"timezone":7200,"description":""},id="list_no_elements+no_gust_testcase"),
    ),
)
def test_basecases(json_format,expected):
    result=extract_weather_info(json_format)
    assert pytest.approx(result)==(expected)
@pytest.mark.parametrize("json_format",
    (
pytest.param(
    {
  "coord": {
    "lon": 10.99,
    "lat": 44.34
  },
  "weather": [{}
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
  "cod": 200,
},id="missing_elements_testcase"),
pytest.param(
    {},id="empty_dict_testcase"),                        
        ),
)
def test_errorcases(json_format):
    with pytest.raises(KeyError):
        extract_weather_info(json_format)
def test_error_none_case():
    with pytest.raises(TypeError):
        extract_weather_info()
#Extraction test done, now display test
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

#test for store_weather_data function
def test_normal_first_entry_store_testcase(tmp_path):
    tmp_file=tmp_path/"weather.csv"
    sample_data={
        "country":"MM",
        "name":"Monywa",
        "temp":31.41,
        "humidity":57,
        "timezone":23400,
        "date":1782231933
    }
    store_weather_data(sample_data,filename=tmp_file)
    assert tmp_file.exists()
    with open(tmp_file,newline="",encoding='utf-8') as file:
        rows=list(csv.DictReader(file))
        assert len(rows)==1
        assert rows[0]['count']=="1"
        assert rows[0]['name']=="Monywa"
        assert rows[0]['country']=="MM"
        assert rows[0]['raw_epoch']=="1782231933"
        assert rows[0]['cur_time']=="2026-06-23 10:55:33 PM "

'''@pytest.mark.parametrize("sample_data",
      ({"count":1,
        "country":"JP",
        "name":"Mitsushimachō-ōfunakoshi",
        "temp":19.44,
        "humidity":57,
        "timezone":32400,
        "date":1782236359},
       {"count":2,
        "country":"JP",
        "name":"Izuhara",
        "temp":20.77,
        "humidity":98,
        "timezone":32400,
        "date":1782297491}
      ) This creates separate files for the things passed into them.
)'''

'''def test_no_repeated_header_multiple_entries_store_testcase(tmp_path):
    tmp_file=tmp_path/"weather.csv"
    first_entry={
        "country":"JP",
        "name":"Mitsushimachō-ōfunakoshi",
        "temp":19.44,
        "humidity":57,
        "timezone":32400,
        "date":1782236359}
    second_entry={
        "country":"JP",
        "name":"Izuhara",
        "temp":20.77,
        "humidity":98,
        "timezone":32400,
        "date":1782297491}
    store_weather_data(first_entry,filename=tmp_file)
    store_weather_data(second_entry,filename=tmp_file)
    assert tmp_file.exists()
    with open(tmp_file,newline="",encoding='utf-8')as file:
        rows=list(csv.DictReader(file))
        print(rows)
        assert len(rows)==2
        assert rows[0]['count']=="1"
        assert rows[1]['count']=="2"
        assert rows[0]['name']=="Mitsushimachō-ōfunakoshi"
        assert rows[1]['name']=="Izuhara"
def test_duplicate_entries_store_testcase(tmp_path):
    tmp_file=tmp_path/"weather.csv"
    first_entry={
        "country":"JP",
        "name":"Mitsushimachō-ōfunakoshi",
        "temp":19.44,
        "humidity":57,
        "timezone":32400,
        "date":1782236359}
    second_entry={
        "country":"JP",
        "name":"Izuhara",
        "temp":20.77,
        "humidity":98,
        "timezone":32400,
        "date":1782297491}
    third_entry={
        "country":"JP",
        "name":"Mitsushimachō-ōfunakoshi",
        "temp":19.44,
        "humidity":57,
        "timezone":32400,
        "date":1782236359}
    store_weather_data(first_entry,filename=tmp_file)
    store_weather_data(second_entry,filename=tmp_file)
    store_weather_data(third_entry,filename=tmp_file)
    assert tmp_file.exists()
    with open(tmp_file,newline="",encoding='utf-8')as file:
        rows=list(csv.DictReader(file))
        #print(rows)
        assert len(rows)==2
        
        assert rows[0]['count']=="1"
        assert rows[1]['count']=="2"
        assert rows[0]['name']=="Mitsushimachō-ōfunakoshi"
        assert rows[1]['name']=="Izuhara"'''
first_entry={
        "country":"JP",
        "name":"Mitsushimachō-ōfunakoshi",
        "temp":19.44,
        "humidity":57,
        "timezone":32400,
        "date":1782236359}
second_entry={
        "country":"JP",
        "name":"Izuhara",
        "temp":20.77,
        "humidity":98,
        "timezone":32400,
        "date":1782297491}
@pytest.mark.parametrize(('entries','expected'),
      (
          pytest.param([first_entry,second_entry],
                       [{"count":1,"name":"Mitsushimachō-ōfunakoshi","temp":19.44,"country":"JP","humidity":57,"timezone":32400,"date":1782236359},
                        {"count":2,"country":"JP","name":"Izuhara","temp":20.77,"humidity":98,
                        "timezone":32400,"date":1782297491}],id="two_diff_entries_no_repeated_header_testcase"),
          pytest.param([first_entry,second_entry,first_entry],
                       [{"count":1,"name":"Mitsushimachō-ōfunakoshi","temp":19.44, "country":"JP","humidity":57,"timezone":32400,   "date":1782236359},
                        {"count":2,"country":"JP","name":"Izuhara","temp":20.77,"humidity":98,"timezone":32400,"date":1782297491}]
                        ,id="no_duplicate_data_testcase"),
      ),
)
def test_store_weather_data(entries, expected,tmp_path):
    tmp_file = tmp_path / "weather.csv"
    for entry in entries:
        store_weather_data(entry,filename=tmp_file)
    with open(tmp_file,newline="",encoding="utf-8") as file:
        rows=list(csv.DictReader(file))
        assert len(rows)==len(expected)
        for row, expect in zip(rows,expected):
            assert row['count']==str(expect['count'])
            assert row['name']==expect['name']
            assert row['country']==expect['country']
            assert row['temp']==str(expect['temp'])