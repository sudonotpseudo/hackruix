import os
import boto3
from boto3.dynamodb.conditions import Key
import decimal
import pyglet
import datetime

from keys import secretKey, publicKey

os.environ["AWS_ACCESS_KEY_ID"] = publicKey

os.environ["AWS_SECRET_ACCESS_KEY"] = secretKey

AWS_REGION = 'us-east-1'

db = boto3.resource('dynamodb',
                    region_name = AWS_REGION)

GDP_YoY = {"Argentina" : "ARGQPYOX Index",
            "Australia" : "AUNAGDPY Index",
            "Brazil" : "BZGDYOY% Index",
            "Canada" : "CAGDPYOY Index",
            "France" : "FRGEGDPY Index",
            "Germany" : "GRGDPPGY Index",
            "India" : "IGDRYOY Index",
            "Italy" : "ITPIRLYS Index",
            "Japan" : "JGDFDEFY Index",
            "South Korea" : "KOGDPYOY Index",
            "South Africa" : "SAGDPYOY Index",
            "Turkey" : "TUGPCOYW Index",
            "United Kingdom" : "UKGRABIY Index"}

GDP_QoQ = {"Argentina" : "ARADTOTQ Index",
            "Australia" : "AUNAGDPC Index",
            "Brazil" : "BZGDQOQ% Index",
            "Canada" : "CAGDPMOM Index",
            "France" : "FRGEGDPQ Index",
            "Germany" : "GRGDPPGQ Index",
            "India" : "IGQREGDY Index",
            "Italy" : "ITPIRLQS Index",
            "Japan" : "JGDPQGDP Index",
            "South Korea" : "KOGDPQOQ Index",
            "South Africa" : "SAGDPANN Index",
            "Turkey" : "TUGPCOQS Index",
            "United Kingdom" : "UKGRABIQ Index"}

pathToTrump = []

def countryToDataList(country):
    years = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013']
    valueList = []
    for year in years:
        table = db.Table(year)
        data = table.query(KeyConditionExpression = Key('Ticker').eq(GDP_YoY[country]))['Items']
        for item in data:
            val = int(abs(item['Value']) *1000)
            print "*"
            valueList.append(val)
        data = table.query(KeyConditionExpression = Key('Ticker').eq(GDP_QoQ[country]))['Items']
        for item in data:
            val = int(abs(item['Value']) *1000)
            valueList.append(val)
            print "*"
    return valueList

def toAudio(valueList, audioPath):
    string = 'ffmpeg -i \"concat:'
    path = ''
    for number in valueList:
        if path != '':
            path += '|'        
        path +=   pathToTrump[number%len(pathToTrump)]
    string += path + '\" ' + audioPath
    os.system(string)


if __name__ == '__main__':
    for root, dirs, files in os.walk(r'./sounds'):
        for file in files:
            if file.endswith('.mp3'):
                pathToTrump.append('./sounds/'+file)
    newString = './speeches/trump' + datetime.datetime.now().strftime("%I%M%p-%B-%d-%Y") + ".mp3"
    os.system('touch ' + newString)
    print "Please Select one of the following countries: (They are case sensative)"
    country = raw_input("Argentina, Austrailia, Brazil, Canada, France, Germany, India,\nItaly, Japan, South Korea, South Africa, Turkey, United Kingdom\n")
    toAudio(countryToDataList(country), newString)
    print "Done"
