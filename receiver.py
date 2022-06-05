from flask import Flask, request
import json, logging, subprocess

app = Flask(__name__)

@app.route('/webhook',methods=['POST'])

# Converts json payload to dictionary
data = json.loads(request.data)

# The function that handles the POST-request
def deployWebsite():
   logmsg = "New commit by: {}".format(data['commits'][0]['author']['name'])

   # Verifies the payload, executes the commands and logs the event
   if request.method == 'POST':
       verify_signature(data)
       subprocess.call(['sh', '../build_site.sh'])
       logEvents(logmsg)
       return 'OK', 200
   else:
       abort(400)

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
def verify_signature(data)
  signature = 'sha256=' + OpenSSL::HMAC.hexdigest(OpenSSL::Digest.new('sha256'), ENV['SECRET_TOKEN'], payload_body)
  return halt 500, "Signatures didn't match!" unless Rack::Utils.secure_compare(signature, request.env['HTTP_X_HUB_SIGNATURE_256'])

if __name__ == '__main__':
   app.run(debug=True)
