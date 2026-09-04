import pytest
from datetime import datetime, timezone,timedelta
from time_forcli import get_local_time
@pytest.mark.parametrize(("utc_unixtime","offset_seconds","expected"),
    (
        pytest.param(0,0,datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc),id="test_baseline"),
        #pytest.param(1750551967,-10000,datetime(2025, 6, 22, 0, 26, 7, tzinfo=timezone.utc),id="test_+ offset") Instead of timezone.utc, we'll do timezone(timedelta(seconds=19800seconds))
        pytest.param(1750551967,19800,datetime(2025,6,22,5,56,7,tzinfo=timezone(timedelta(seconds=19800))),id="test_positive_offset"),
        pytest.param(1750551967,-9000,datetime(2025,6,21,21,56,7,tzinfo=timezone(timedelta(seconds=-9000))),id="test_negative_offset"),
        pytest.param(1659397414,3600,datetime(2022,8,2,0,43,34,tzinfo=timezone(timedelta(seconds=3600))),id="test_positive_offset,+1day"),#UK
        pytest.param(1667785414,-21600,datetime(2022,11,6,19,43,34,tzinfo=timezone(timedelta(seconds=-21600))),id="test_negative_offset,-1day"),#Chicago
        pytest.param(1667785414,-86399,datetime(2022,11,6,1,43,34,tzinfo=timezone(timedelta(seconds=-86399))),id="offset_just_below_24_hours"),#Chicago	
                         ),
)
def test_basecases(utc_unixtime,offset_seconds,expected):
    #print(type(expected))
    #assert get_local_time(utc_unixtime,offset_seconds) == expected
    #Here, LHS is not on UTC timezone, but upon doing "=="", it subtracts the offset, so it becomes UTC, now the RHS is in UTC, so it minuses 0, as it requires a universal time to compare, so the test passes, but we are not checking if the universal times of both sides are equal or not, we need the time of the specified place, so we need to check the offset, along with day, hour,minute, i dont think we need to check seconds, as seconds would be same in unixtime
    result = get_local_time(utc_unixtime, offset_seconds)
    assert result.utcoffset() == expected.utcoffset()
    assert (result.day,result.hour, result.minute) == (expected.day,expected.hour, expected.minute)
@pytest.mark.parametrize(("utc_unixtime","offset_seconds"),
        (
            pytest.param("0",0,id='string_unixtime'),
            pytest.param(None,0,id='none_unixtime'),
            pytest.param(None,None,id='none_unix&offsettime'),
            pytest.param(1667785414,"-21600",id='string_offset'),
            pytest.param("1667785414","9000",id='string_offset&unixtime'),                    
        ),
)
def test_error_cases1(utc_unixtime,offset_seconds):
    with pytest.raises(TypeError):
        get_local_time(utc_unixtime,offset_seconds)
@pytest.mark.parametrize("offset_seconds",
        (
            pytest.param(-100000,id='offset_too_less_than_24_hours'),             
            pytest.param(+86401,id='offset_larger_than_24_hours'),
            #pytest.param(+86399,id='offset_larger_than_24_hours'), jk, this one wont raise error, as it is within 24 hours.
        ),
)
def test_error_cases2(offset_seconds):
    with pytest.raises(ValueError):
        timezone(timedelta(seconds=offset_seconds))