import requests
import datetime


#data = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=30.3514766&lon=-97.8648535&appid=0983053a78a9e5a4582893655da68947&units=imperial').json()

def time_converter(unix):
    time = datetime.datetime.fromtimestamp(unix)
    return time.strftime('%Y-%m-%d %H:%M:%S')

def degToCompass(num):
    val=int((num/22.5)+.5)
    arr=["North","North-Northeast","Northeast","East-Northeast","East","East-Southeast", "Southeast", "South-Southeast","South","South-Southwest","Southwest","West-Southwest","West","West-Northwest","Northwest","North-Northwest"]
    return arr[(val % 16)]


def get_current_weather():
    data = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=30.3514766&lon=-97.8648535&appid=0983053a78a9e5a4582893655da68947&units=imperial').json()
    current = data['current']
    current_temp = current['temp']
    current_description = current['weather'][0]['description']
    current_weather = f'Currently, it is {current_temp} degrees fahrenheit with {current_description}.'
    current_wind = current['wind_speed']

    if current_wind:
        current_wind_deg = current['wind_deg']

        current_weather += f' There is a {current_wind} mile per hour wind from the {degToCompass(current_wind_deg)}.'
    
    return current_weather


def get_future_weather(ind, time):
    data = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=30.3514766&lon=-97.8648535&appid=0983053a78a9e5a4582893655da68947&units=imperial').json()
    
    conversion = {'eve': ' evening',
                  'morn': ' morning',
                  'day': ' afternoon',
                  'night': ' night',
                   'max': ''}

    min_ = None

    daily = data['daily'][ind]
    temp = daily['temp'][time]
    if time == 'max':
        min_ = daily['temp']['min']
    description = daily['weather'][0]['description']
    wind_s = daily['wind_speed']
    wind_dir = degToCompass(daily['wind_deg'])

    if ind == 0:
        if time == 'night':
            time_str = 'tonight'
        else:
            time_str = 'this' + conversion[time]
    else:
        time_str = 'tomorrow' + conversion[time]

    start_1 = f'It will be {temp} degrees fahrenheit {time_str}'
    start_2 = f'There is a high of {temp} degrees fahrenheit and a low of {min_} degrees fahrenheit {time_str}'

    weather_forecast = f'{start_1 if min_ is None else start_2} with {description}.'

    if wind_s:
        weather_forecast += f' There will be a {wind_s} mile per hour wind from the {wind_dir}.'



    return weather_forecast



def getLakeAustinTemp():
    headersget={
        'referer': 'https://www.google.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        }

    url='https://www.google.com/search?q=what+is+the+current+water+temperature+of+lake+austin&sourceid=chrome&ie=UTF-8'
    with requests.Session() as session:
        r=session.get(url,headers=headersget)
        a=r.text
        index=a.find("data-tts-text")
        temperature=""
        while True:
            temperature+=a[index]
            index+=1
            if a[index]=='°':
                break
        for char in temperature:
            if char not in ['1','2','3','4','5','6','7','8','9','0']:
                temperature=temperature.replace(char,'')
        return temperature

def get_weather(statement):
    if 'right now' in statement.lower():
        return get_current_weather() + ". The water is currently" + getLakeAustinTemp() + " degrees Farenheight in Lake Austin."
    
    new = set(statement.lower().split())

    if 'today' in new:
        ind = 0
        time = 'max'
    elif 'tonight' in new:
        ind = 0
        time = 'night'
    elif 'this' in new:
        ind = 0
        if 'morning' in new:
            time = 'morn'
        elif 'afternoon' in new:
            time = 'day'
        elif 'evening' in new:
            time = 'eve'
        elif 'night' in new:
            time = 'night'
        else:
            raise Exception('Not supported yet')

    elif 'tomorrow' in new:
        ind = 1
        time = 'max'
        if 'morning' in new:
            time = 'morn'
        elif 'afternoon' in new:
            time = 'day'
        elif 'evening' in new:
            time = 'eve'
        elif 'night' in new:
            time = 'night'
    else:
        return get_current_weather() + ". The water is currently" + getLakeAustinTemp() + " degrees Farenheight in Lake Austin."

    return get_future_weather(ind, time)


    