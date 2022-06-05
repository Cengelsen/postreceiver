from flask import Flask, request
import json, logging, subprocess, os

app = Flask(__name__)

# Converts json payload to dictionary
data = json.loads(request.data)

@app.route('/webhook',methods=['POST'])

# The function that handles the POST-request
def deployWebsite():
   logmsg = "New commit by: {}".format(data['commits'][0]['author']['name'])

   # Verifies the payload, executes the commands and logs the event
   if request.method == 'POST':
       if verify_signature(data):
           subprocess.call(['sh', '../build_site.sh'])
           logEvents(logmsg)
           return 'Success', 200
       return 'Signatures did not match!', 500
   return 'Not allowed', 405

# function that defines how events are logged
def logEvents(event):

    # This defines the format of the locally stored log-event. 
    logging.basicConfig(filename=r"/var/www/postreceiver/logs/POST.log", 
            format='%(asctime)s %(levelname)s %(message)s', filemode='a')

    # creates the log-object
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.debug(event)

# Githubs recommended function to verify JSON POST payloads
def verify_signature(data):

    received_sign = req.headers.get('X-Hub-Signature-256').split('sha256=')[-1].strip()
    secret = os.environ(['SECRET_KEY']).encode()
    expected_sign = HMAC(key=secret, msg=data.data, digestmod=sha256).hexdigest()
    return compare_digest(received_sign, expected_sign)

if __name__ == '__main__':
   app.run(debug=True)
