import pytest,csv
from weathercli import store_weather_data
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
      ) This creates separate files for the things passed into them. i.e, this is wrong
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
          pytest.param((first_entry,second_entry),
                       ({"count":1,"name":"Mitsushimachō-ōfunakoshi","temp":19.44,"country":"JP","humidity":57,"timezone":32400,"date":1782236359},
                        {"count":2,"country":"JP","name":"Izuhara","temp":20.77,"humidity":98,
                        "timezone":32400,"date":1782297491}),id="two_diff_entries_no_repeated_header_testcase"),
          pytest.param((first_entry,second_entry,first_entry),
                       ({"count":1,"name":"Mitsushimachō-ōfunakoshi","temp":19.44, "country":"JP","humidity":57,"timezone":32400,   "date":1782236359},
                        {"count":2,"country":"JP","name":"Izuhara","temp":20.77,"humidity":98,"timezone":32400,"date":1782297491})
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