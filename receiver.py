from flask import Flask, request
from hashlib import sha256
from hmac import HMAC, compare_digest
import json, logging, subprocess, os, hashlib

app = Flask(__name__)

@app.route('/webhook',methods=['POST'])

# The function that handles the POST-request
def deployWebsite():
    
    # Converts json payload to dictionary
    data = json.loads(request.data)
    head = request.headers

    logmsg = "New commit by: {}".format(data['commits'][0]['author']['name'])
   
    # Verifies the payload, executes the commands and logs the event
    if request.method == 'POST':
       if verify_signature(data, head):
           subprocess.call(['sh', '../build_site.sh'])
           logEvents(logmsg)
           return 200
       else:
           logEvents("Signatures did not match")
           return 500
    else:
        logEvents("This request is not allowed")
        return 405

# function that defines how events are logged
def logEvents(event):

    # This defines the format of the locally stored log-event. 
    logging.basicConfig(filename=r"/var/www/postreceiver/logs/POST.log", 
            format='%(asctime)s %(levelname)s %(message)s', filemode='a')

    # creates the log-object
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.debug(event)


def verify_signature(data, head):
    
    received_sign = head.get('X-Hub-Signature-256').strip()

    # Opens local json-file and converts to dictionary
    with open('.env.local.json', 'r') as token:
        secret = json.load(token)
    
    # Generates a hexadecimal based on secret token and request payload
    expected_sign = 'sha256=' + HMAC(key=bytes(secret['SECRET_TOKEN'], 'utf-8'), msg=request.get_data(), digestmod=hashlib.sha256).hexdigest()

    logmsg = "Dette er hmac: " + expected_sign
    logEvents(logmsg)
    return compare_digest(received_sign, expected_sign)

if __name__ == '__main__':
   app.run(debug=True)
