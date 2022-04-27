from flask import Flask, request
import json, os, logging

app = Flask(__name__)

@app.route('/webhook',methods=['POST'])

# The function that handles the POST-request
def deployWebsite():
   data = json.loads(request.data)
   logmsg = "New commit by: {}".format(data['commits'][0]['author']['name'])

   # Verifies if the method is POST, executes the commands and logs the event
   if request.method == 'POST':
       os.system('cd /var/www/cengelsen.no && git pull && hugo && echo "Update has been deployed"')
       logEvents(logmsg)
       return 'OK', 200
   else:
       abort(400)

# function that defines how events are logged
# currently, there are only one type of event; as defined by logmsg
def logEvents(event):

    # This defines the format of the log-event. 'a' means append, 
    # which means the message is appended into the file POST.log
    logging.basicConfig(filename=r"/var/www/postreceiver/logs/POST.log", 
            format='%(asctime)s %(levelname)s %(message)s', filemode='a')

    # defining the log-object that actually logs the message
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.debug(event)

if __name__ == '__main__':
   app.run(debug=True)
