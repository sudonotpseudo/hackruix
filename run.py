from flask import Flask
from OpenSSL import SSL
from flask import request
from twilio.rest import TwilioRestClient
from random import randint
import pickle

app = Flask(__name__)

def call(number):
    
    
    all_numbers = pickle.load( open( "phones.p", "rb" ) )

    all_numbers[number]=number

    pickle.dump( all_numbers, open( "phones.p", "wb" ) )

    # Download the Python helper library from twilio.com/docs/python/install
    
 
    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = "AC9bf8fa13be19f052621d4e304db63182"
    auth_token  = "99503bbf9c4e89924dc8a247f5304a68"
    client = TwilioRestClient(account_sid, auth_token)
 
    
    #phones = [7322725973,7322665998,5164136757,7329666086,7327032645,2018952456,2019935587,2017053156]

    num = randint(0,12)
         
    call = client.calls.create(
                to=number, 
        	from_="+19292519397", 
        	url="http://wilson.renan.cool/~dincert/"+str(num)+".mp3",  
        	method="GET",  
        	fallback_method="GET",  
        	status_callback_method="GET",    
        	record="false") 

    print call.sid 
@app.route("/message", methods=['GET', 'POST'])
def hello():
    body = request.form["Body"]
    recipient = str(body)
    if(len(body)!= 10):
 
         return "<Response><Sms>YOU DID NOT ENTER A VALID 10 DIGIT PHONE NUMBER, STOP TRYING TO RUIN AMERICA!</Sms></Response>"
    else:
         call(recipient)
         return "<Response><Sms>THANKS FOR MAKING AMERICA GREAT AGAIN!!</Sms></Response>"
 
if __name__ == "__main__":
    app.run(debug = True,host='li1255-234.members.linode.com',port=5000,ssl_context=("/TRUMP/server.crt","/TRUMP/server.key"))
