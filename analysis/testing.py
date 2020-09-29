import requests
import pprint


# Date formate should be (%Y-%m-%d)=(2020-5-12)

def twitter_api(keyword, since_date, until_date, count=10, lat=30, lng=70, radius=450):
    count = str(count)
    lat = str(lat)
    lng = str(lng)
    radius = str(radius)
    url = 'http://127.0.0.1:8000/employees/?keyword=' + keyword + '&latitude=' + lat + '&longitude=' + lng + '&radius=' + radius + '&count=' + count + ''
    print(url)
    response = requests.get(url)
    data = response.json()
    return data


data = twitter_api('siddiq', '', '')
pprint.pprint(data)
