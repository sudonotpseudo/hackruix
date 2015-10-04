import os
import boto3
from boto3.dynamodb.conditions import Key
import decimal
import pyglet

os.environ["AWS_ACCESS_KEY_ID"] = 'AKIAJRFUYM7RWTDBHQKQ'

os.environ["AWS_SECRET_ACCESS_KEY"] = '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'

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
pathToTrump = [] #128 trump clips with paths as Strings


def countryToDataList(country):
    years = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013']
    valueList = []
    for year in years:
        table = db.Table(year)
        data = table.query(KeyConditionExpression = Key('Ticker').eq(GDP_YoY[country]))['Items']
        for item in data:
            val = int(abs(item['Value']) *1000)
            print val
            valueList.append(val)
        data = table.query(KeyConditionExpression = Key('Ticker').eq(GDP_QoQ[country]))['Items']
        for item in data:
            val = int(abs(item['Value']) *1000)
            print val
            valueList.append(val)
    print str(len(valueList))+ " Length"
    return valueList

def toAudio(valueList):
    for number in valueList:
        path = "./sounds/trump.wav|" + pathToTrump[number%128]
        os.system('ffmpeg -i \"concat:%s\" ./sounds/trump.wav')


def main():
    print "Please Select one of the following countries: (They are case sensative)"
    country = raw_input("Argentina, Austrailia, Brazil, Canada, France, Germany, India,\nItaly, Japan, South Korea, South Africa, Turkey, United Kingdom\n")
    countryToDataList(country)
    #song = pyglet.media.load('./sounds/trump.wav')
    #song.play()
    #pyglet.app.run()
    exit()

main()
