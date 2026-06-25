# Weather CLI

## A Personal Project involving Python to fetch weather data using api, print and save it on a .csv file


This is the first project I have built, while continuing the Youtube series of CS50P, it is a weather api project which takes the lat, and long of a location, along with an API Key(for reference, this project uses data from OpenWeatherMap ), and prints out that location's weather, with some twists, also creates a CSV file which stores that data.

## How It Works:
 * Sends an HTTP request to the API of OpenWeatherMap(using requests.get() ).
 * Gets data of that location in JSON format.
 * Converts the JSON format to Python Object to tinker with.(using <variable>.json())
 * Displays Certain Data from the JSON string, on the terminal window.
 * Saves the data in a csv file, without duplication of data.

 ## What Makes It Interesting
 * It converts the raw-epoch value and the offset time(in seconds) to a human readable Time, based on the timezone.(using datetime library)
 * Has Unit tests of all the functions( except main() and get_weather_response())
 * Has Exception Handling in required functions.
 * Has Clean code, properly put in specific functions to avoid confusion, and increase readability(SoC, so as to speak).
 * Creates a CSV file to store unduplicated data.(using csv, and os libraries)
 * Exits the program run when the no. of inputted items is not equal to 4.(using sys library)

 ## How to Use This Project
 * Get a valid API key,(from OpenWeather, or if you want to do in other servers, get the key, and change the url in get_weather_response to what the docs say in their site)
 * Input the lat, and long of a location along with the api key to get weather data.
 * Input only these 3 things, more or less of it, would end the program and you have to start again.
 * Done!, the data will be shown in the terminal window, and it will be stored in a csv file named as weather.csv

Testing:-
* All tests are written with pytest library. A few specific habits worth recording:
* Tests were written alongside each function as it was built, not bolted on afterward. Retrofitting tests onto code you've already moved past is slower and finds fewer real bugs.
* pytest silently ignores any test function that doesn't start with "test_....." . 
* Test cases are grouped by what they're asserting i.e " returning a value" vs. " raising an exception" which  decides where a @pytest.mark.parametrize boundary goes.
* Probably the most important thing in this project(gives a deeper insight of the topics.)
* Unit Testing is very important, in my opinion, as it takes you to the edge and makes you question everything that could go wrong(It also takes much space in your mind, and may gnaw at you, at some points of time)

## Known Issues
This Project is the first one I've ever made, and I' noted down some of the things which may cause an issue at some of time.
* Change get gust print statement when there would be no gust.
* Reduce the size for extract_weather testcases using **kwargs
* Make Separate files for the unit testing of separate functions.
* Make Test Cases for main() and get_weather_response().

## Created Using
* Python
* Libraries Used:- requests(for API call), csv(For storing data), os(For checking that header is applied only once), sys(To check the no. of arguements passed by user = 4), json(converting JSON data into Python Object), pytest( for unit testing(capsys->checking stdout, tmp_path-> creating temp file, parametrize->to pass values having similar outputs, to a single test function, pytest.raises-> to check for errors))
* OpenWeatherMap API
* CS50P
* Claude
* Google