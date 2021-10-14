from twilio.rest import Client
from twilio.twiml.voice_response import Record, VoiceResponse, Say, Gather
import os, sys

#Find these values at https://twilio.com/user/account
account_sid = "ACc68e021c8ad138449a2a4fd840448a88"
auth_token = "e585fadbdb2247b35b510b20414b6cfe"

client = Client(account_sid, auth_token)

call = client.calls.create(
    to="+14038056689",
    from_="+16046701815",
   url='http://tawfi.hopto.org/test.xml',
   status_callback= 'https://auto-phone-8526.twil.io/status-callback',
   status_callback_method = 'POST',
   status_callback_event = ['initiated', 'ringing', 'answered', 'completed'])

callID = call.sid
callInfo = client.calls(callID).fetch()
while(callInfo.status != 'completed'):
    callInfo = client.calls(callID).fetch()
    print(callInfo.status)
'''
try:
    while True:
        call = client.calls('CA7182f8b446718489fc1364f7edd2188c').
except Exception as e:
    print(e)

response = VoiceResponse()
gather = Gather(input='speech')
gather.say('Welcome, please tell us why you are calling')
response.append(gather)
call = client.calls('CA6c6b947e7c160d7b99d752e49d4e2b00').update(twiml=response)
'''