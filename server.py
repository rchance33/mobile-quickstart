import os
from flask import Flask, request
from twilio.util import TwilioCapability
import twilio.twiml
##
# Account Sid and Auth Token can be found in your account dashboard
ACCOUNT_SID = 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
AUTH_TOKEN = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'

# TwiML app outgoing connections will use
APP_SID = 'APb7372771a18a38669a83e5f115dabeb8'

CALLER_ID = '+19189924892'
CLIENT = 'mobile-quickstart4'

app = Flask(__name__)

@app.route('/token')
def token():
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  auth_token = os.environ.get("AUTH_TOKEN", AUTH_TOKEN)
  app_sid = os.environ.get("APP_SID", APP_SID)

  capability = TwilioCapability(account_sid, auth_token)

  # This allows outgoing connections to TwiML application
  if request.values.get('allowOutgoing') != 'false':
     capability.allow_client_outgoing(app_sid)

  # This allows incoming connections to client (if specified)
  client = request.values.get('client')
  if client != None:
    capability.allow_client_incoming("mobile-quickstart4")

  # This returns a token to use with Twilio based on the account and capabilities defined above
  return capability.generate()

@app.route('/call', methods=['GET', 'POST'])
def call():
  """ This method routes calls from/to client                  """
  """ Rules: 1. From can be either client:name or PSTN number  """
  """        2. To value specifies target. When call is coming """
  """           from PSTN, To value is ignored and call is     """
  """           routed to client named CLIENT                  """
  resp = twilio.twiml.Response()
  from_value = request.values.get('From')
  to = request.values.get('To')
  if not (from_value and to):
    return str(resp.say("Invalid request"))
  from_client = from_value.startswith('client')
  caller_id = os.environ.get("CALLER_ID", CALLER_ID)
  if not from_client:
    # PSTN -> client
    resp.dial(callerId=from_value).client(CLIENT)
  elif to.startswith("client:"):
    # client -> client
    resp.dial(callerId=from_value).client(to[7:])
  else:
    # client -> PSTN
    resp.dial(to, callerId=caller_id)
  return str(resp)

 # Delivers music after mute  
@app.route('/mutesic', methods=['POST', 'GET'])
def mute_music():
  response = twilio.twiml.Response()
  response.pause(length="2")
  response.say("Thank you for calling Hot Coffey Design. Please hold")
  response.play("https://s3.amazonaws.com/hotcoffeydesign/Uptown+Funk+Feat+Bruno+Mars+Mark+Ronson+-+1420814645+Part+1+of+5.mp3")
  return str(response)

#Launches mute. This is the one your in-app button should trigger
@app.route('/mute', methods=['POST', 'GET'])
def mute():
  #We are testing code that makes our mute button redirect so we can hear on hold music for our customer
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  auth_token = os.environ.get("AUTH_TOKEN", AUTH_TOKEN)
  client = TwilioRestClient(account_sid, auth_token)
  call = client.calls.update(app_sid, url="http://demo.twilio.com/docs/voice.xml", method="POST")
  ##We are going to x this out and try and see if code will initiate with out the print.to function
  #print call.to
@app.route('/', methods=['GET', 'POST'])
def welcome():
  resp = twilio.twiml.Response()
  resp.say("Welcome to Twilio")
  return str(resp)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
