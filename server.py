import os
from flask import Flask, request,session, url_for, render_template
from twilio.util import TwilioCapability
from twilio.rest import TwilioRestClient
import twilio.twiml

# Account Sid and Auth Token can be found in your account dashboard
ACCOUNT_SID = 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
AUTH_TOKEN = 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

# TwiML app outgoing connections will use
APP_SID = 'APb7372771a18a38669a83e5f115dabeb8'

CALLER_ID = '+19189472310'
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
  
  
  
  #We are adding a call queue in Python to see if it works.
# Accept a POST request from Twilio, and provide TwiML to put caller
# in a queue.
@app.route('/caller', methods=['GET', 'POST'])
def caller():
    response = twilio.twiml.Response()
   # Use Enqueue verb to place caller in a Queue
    response.enqueue("Queue One",waitUrl="/music")
  
    return str(response)
    
#We are adding the second part of our code right here for agent to connect with caller
# Accept a POST request from Twilio, and provide TwiML to connect agent
# with first caller in the Queue.
@app.route('/agent', methods=['GET', 'POST'])
def agent():
    response = twilio.twiml.Response()
    # Dial into the Queue we placed the caller into to connect agent to
    # first person in the Queue.
    with response.dial() as dial:
        dial.queue("Queue One")
    return str(response)
    
    
        # Deliver hold music when in Queue. 
@app.route('/music', methods=['POST', 'GET'])
def music():
    response = twilio.twiml.Response()
    response.pause(length="2")
    response.say("Hello thanks for calling blah blah blah! Please stay on the line and we will be with you shortly.")
    response.play("https://s3.amazonaws.com/hotcoffeydesign/Uptown+Funk+Feat+Bruno+Mars+Mark+Ronson+-+1420814645+Part+1+of+5.mp3")
    #TODO: sms notifacation when someone calls
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    call = client.calls.create(url="http://mobile-quickstart4.herokuapp.com/caller",to="+19189924892",from_="+19189472310") 
    print call.sid
    #with response.gather(numDigits=1, action="/digit", method="POST") as g:
        #g.say("To continue the call, press 1. To leave a message, press 2.")
    return str(response)
    
    

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
  
   #we are moving secret key out of if block
  app.secret_key='super duper blooper pooper mgruder key'
@app.route('/', methods=['GET', 'POST'])
def welcome():
  resp = twilio.twiml.Response()
  resp.say("Welcome to Twilio")
  return str(resp)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
