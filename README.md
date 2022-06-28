# Postreceiver

## What is this?

This is a simple script that listens for POST-requests on a specific URL-slug. When it receives the POST-payload, it executes shell-commands locally. 

## How does this work?

It uses a Flask application that ideally should run inside a python virtual environment. The POST-payload is proxied through NGINX to the application that runs on "localhost:5000". While it runs, it listens on the specified port for JSON POST-payloads. Currently, it reacts merely on the fact that the request is of type POST.

## Dependencies

 - Python >= 3.8
 - Flask >= 2.1.1

## How do i run it locally?

1. ```git clone git@github.com:Cengelsen/postreceiver.git```
2. ```. venv/bin/activate```
3. install python3, dependent on your OS
4. ```pip install flask```
5. ```python3 receiver.py ```
6. profit

## How to run it as a system service

Since this program occupies the terminal and the localhost terminates when quitting, it is quite beneficial to run the server in the background. This is what works for me; Run it as a system service which starts on boot.

Here is an example for a system file:

```sh
[Unit]
Description= <Name of service>
After=network.target

[Service]
User=root
WorkingDirectory= <Directory where the script is located>
ExecStart=/bin/sh -c '. venv/bin/activate && python3 receiver.py'
Restart=always

[Install]
WantedBy=multi-user.target
```

Save this in a file located in the service-folder, with a ```.service```-extension. For an ubuntu 20.04 server, the folder would be ```etc/systemd/system/```. 

After the file is saved, remember to run ```sudo systemctl daemon-reload```, before starting the service. 

## The Nginx config

This is what was required to enable NGINX to proxy the POST-payload to the localhost.

```sh
location /webhook {
	include proxy_params;
        proxy_pass http://127.0.0.1:5000;
}
```

## Payload verification

This script also contains a verification function. This limits the serverlocal commands to only be executed when the head of the POST-payload contains a special signature. This way, only the owner of the repo (and others who know the secret token) can trigger the serverlocal commands. 

I followed [this guide](https://docs.github.com/en/developers/webhooks-and-events/webhooks/securing-your-webhooks#validating-payloads-from-github)

You can use Ruby to create the token. I then gave this secret token to the webhook in github, and github generated a hexadecimal SHA256-signature and placed it in the header of the POST-request.

In order to verify the request serverside, you need to compare the received signature with a locally generated signature.

NB: it's important to include the entire payload when generating the local key, otherwise the request-signature will be longer the the local key. 

NBB: The HMAC-function requires the key and msg parameters to both be a bytes, or bytearray, object. 

## Feel free to create issues for this repo if you see room for improvements :)
