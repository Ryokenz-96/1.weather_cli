import sys, json, requests,csv,os
from time_forcli import get_local_time
def get_weather_response(lat,long,api_key):
    try:
        response=requests.get("https://api.openweathermap.org/data/2.5/weather?lat="+lat+"&lon="+long+"&appid="+api_key,timeout=20)
        #print(json.dumps(response.json(),indent=2))
        '''Just prints all in a readable JSON structure'''
        #print(response.json())
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise ValueError(f"Weather API request failed: {e}.")
    except requests.exceptions.ConnectionError:
        raise ConnectionError(f"Could Not Connect To The Weather Service.")
    except requests.exceptions.Timeout:
        raise TimeoutError(f"Weather Server Took Too Long To Respond.")
    return response.json()
def extract_weather_info(json_format):
    try:
        desc_store=[]
        for i in json_format['weather']:
            desc_store.append(i['description'])
        refined_dict={"temp":(json_format['main']['temp']-273.15),"feels_like":(json_format['main']['feels_like']-273.15),"humidity":(json_format['main']['humidity']),"wind_speed":json_format['wind']['speed'],"wind_deg":json_format['wind']['deg'],"wind_gust":json_format['wind'].get('gust'),"country":json_format['sys']['country'],"name":json_format['name'],"date":json_format['dt'],"sunrise":json_format['sys']['sunrise'],"sunset":json_format['sys']['sunset'],"timezone":json_format['timezone']}
        #print(refined_dict['timezone'])
        refined_dict['description']=",".join(desc_store)
        #print(refined_dict)
    except KeyError as e:
        raise KeyError(f"Missing Key: {e}.")
    except TypeError as e:
        raise TypeError(f"Invalid Data: {e}.")
    return refined_dict
def display_weather(data):
    print(f"\nDescription: {data['description']}")
    print(f"Temp is: {data['temp']:.02f}C, while it feels-like:{data['feels_like']:.02f}C")
    print(f"Humidity is at {data['humidity']}%.")
    print(f"Wind speed and Wind degree are {data['wind_speed']}m/s and {data['wind_deg']}° respectively while wind gust is {data['wind_gust']}m/s,")
    print(f"Country:{data['country']}")
    print(f"City:{data['name']}")
    cur_time=get_local_time(data['date'],data['timezone'])
    #print(cur_time)
    sunrise=get_local_time(data['sunrise'],data['timezone'])
    sunset=get_local_time(data['sunset'],data['timezone'])
    print(f"Local Time in {data['country']}|{data['name']}: {cur_time.strftime('%Y-%m-%d %I:%M:%S %p')}")
    print(f"Sunrise: {sunrise.strftime('%I:%M:%S %p')}\nSunset:{sunset.strftime('%I:%M:%S %p ')}\n")
    #print(data)
def store_weather_data(refined_data,filename="weather.csv"):
    file_is_new = (not os.path.exists(filename)) or (os.path.getsize(filename) == 0)
    try:
        with open(filename,"a+",newline="",encoding="utf-8") as file:
            file.seek(0)
            reader=csv.DictReader(file)
            count=0
            Is_duplicate=False
            for row in reader:
                count+=1
                if (row['name']==refined_data['name'] and row['raw_epoch']==str(refined_data['date'])):
                    Is_duplicate=True
                    break
            writer=csv.DictWriter(file,fieldnames=["count","country","name","temp","humidity","cur_time","raw_epoch"])
            '''if  file.tell()==0 :
                writer.writeheader()'''#shitty way, reading, then doing ts, like  asking "in what page are you, after reading some pages"
            if file_is_new:
                writer.writeheader()
            if Is_duplicate:
                count+=0
            else:
                count+=1
                writer.writerow({'count':count,'country':refined_data['country'],'name':refined_data['name'],'temp':f"{refined_data['temp']:.02f}",'humidity':refined_data['humidity'],"raw_epoch":refined_data['date'],"cur_time":get_local_time(refined_data['date'],refined_data['timezone']).strftime('%Y-%m-%d %I:%M:%S %p ')})
    except PermissionError: #subcategory of OSError, only catches if file is open, which is very common.
        print(f"Couldn't Save Data, '{filename}' may be open.")
    except OSError as e:
        print(f"Couldn't Save Weather Data: {e}.")
def main():
    try:
        if len(sys.argv)!=4:
            sys.exit(f"Usage Instructions: {sys.argv[0]} <arg1> <arg2> <arg3>")
        lat,long,api_key=sys.argv[1],sys.argv[2],sys.argv[3]
        raw_data=get_weather_response(lat,long,api_key)
        refined_data=extract_weather_info(raw_data)
        display_weather(refined_data)
        store_weather_data(refined_data)
    except (ValueError,TypeError,ConnectionError,TimeoutError,KeyError) as e:
        print(f"Error: {e}")
if __name__=="__main__":
    main()