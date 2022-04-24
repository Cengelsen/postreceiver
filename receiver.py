"""
Fremgang så langt:
    Flask-instansen mottar POST gjennom NGINX

    Målet er nå å kjøre sciptet i bakgrunnen
    Siden den okkuperer terminalen med logg
        - nohup fungerer ikke
        - å flytte kommandoene inn i shell-script fungerer ikke
        - nohup på shell-criptet fungerer ikke

    Det siste jeg prøvde var å legge kommandoene inn i en system-tjeneste.
    Det funket om man kjørte kommandoene i systemd-filen med shell-environment!

    Det som gjenstår:

    Det som er gjort:
    - Scriptet må logge commits til en lokalt lagret logg-fil
    - Scriptet må kjøre shell-kommandoer i de riktige mappene
    
    Forbedringspunkter:
    - Endre /webhook til å være en "hashet" kode
    - Legge inn tester for å forsikre meg om at POST som scriptet
      skal reagere på, er fra min commit.
    - Opprette en cron-jobb som sletter loggfilen hver måned
    - Spesialtilpasse loggingen
"""


from flask import Flask, request
import json
import os
import logging

app = Flask(__name__)

@app.route('/webhook',methods=['POST'])
def deployWebsite():
   data = json.loads(request.data)
   logmsg = "New commit by: {}".format(data['commits'][0]['author']['name'])

   if request.method == 'POST':
       os.system('cd /var/www/cengelsen.no && git pull && hugo && echo "Update has been deployed"')
       logEvents(logmsg)
       return 'OK', 200
   else:
       abort(400)

def logEvents(event):
    logging.basicConfig(filename=r"/var/www/webhook/logs/POST.log", 
            format='%(asctime)s %(levelname)s %(message)s', filemode='a')

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.debug(event)

if __name__ == '__main__':
   app.run(debug=True)
