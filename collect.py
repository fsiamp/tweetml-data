import twitter
import time
import sys
import re
from random import randint

positive_list = [':‑)',':-]',':-3',':->','8-)',':-}',':o)',':c)',':^)','=]','=)',':)',':]',':3',':>','8)',':}',':D','8D','xD','XD','=D','=3','B^D',':P',':O',':‑O','D:<']
negative_list = [':‑(',':(',':‑c',':‑<',':c',':<',':[',':-||','>:[',':{',':@','>:(']
latitudeStorage = []
longitudeStorage = []
countryTemp = []

api = twitter.Api(consumer_key='<consumer_key>',
  consumer_secret='<consumer_secret>',
  access_token_key='<access_token_key>',
  access_token_secret='<access_token_secret>')

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def writeContent(id,country,text,file):
    file.write(",")
    file.write(id)
    file.write(",")
    file.write(country)
    file.write(",")
    file.write(text.replace("\n", " "))
    file.write("\n")
    
def getCoordinates(country):
    latitude = 0
    longitude = 0
    with open("countries.txt", "r") as f:
        for line in f:
            if country in line:
                latitude=line.split(',')[0]
                longitude=line.split(',')[1]
    return latitude,longitude
               

def getData(check_english,exclude_retweets,geolocation,file):
    if geolocation != '':
        for country in geolocation.split(","):
            latitude, longitude = getCoordinates(country)
            latitudeStorage.append(latitude);
            longitudeStorage.append(longitude);
            countryTemp.append(country)
            
    else:
        raise ValueError("No country name was provided")
    with open("words.txt", "r") as ins:
        for line in ins:
            for latitude, longitude,country in zip(latitudeStorage, longitudeStorage,countryTemp):
                locationInfo = '"' + str(latitude) + ',' + str(longitude) + ',100km"'
                print(line,locationInfo,country)
                search = api.GetSearch(term=line,count=100,geocode=locationInfo)
                for tweet in search:
                    if (str(tweet.text).startswith('RT') and (exclude_retweets == "true")):
                        continue
                    elif not isEnglish(str(tweet.text)) and (check_english == "true"):
                        continue
                    else:
                        if any(emoticon in tweet.text for emoticon in positive_list):
                            file.write("2")
                        elif any(emoticon in tweet.text for emoticon in negative_list):
                            file.write("0")
                        else:
                            file.write("1")
                        print(tweet.text)
                        writeContent(str(tweet.id),str(country),tweet.text,file)
                time.sleep(15)

def main(argv):

    geolocation = input("Countries: ")

    file = open("datasets/" + str(randint(11111111, 99999999)) + ".data","a")

    if len(sys.argv)>=2:
        if "--check-english" in sys.argv and "--exclude-retweets" not in sys.argv:
            getData("true","false",geolocation,file)
        elif "--check-english" in sys.argv and "--exclude-retweets" in sys.argv:
           getData("true","true",geolocation,file)
        elif "--check-english" not in sys.argv and "--exclude-retweets" in sys.argv:
           getData("false","true",geolocation,file)
        else:
           getData("false","false",geolocation,file)
    else:
       getData('false','false',geolocation,file)

    file.close()
main(sys.argv)
