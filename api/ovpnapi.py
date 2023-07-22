from flask import Flask
from flask import send_file, abort
from flask import Response
import json
import os
from variables import *
import logging

app = Flask
logger = logging.basicConfig(format="[%(asctime)s] %(levelname)s %(message)s")
logger.setLevel(logging.DEBUG)

# Get client by id
@app.get('/client/<client_id>')
def get_client(client_id):
    client_file = f'{CLIENTS_PATH}/{client_id}/{client_id}.ovpn'
    logger.info(f"Request for client id {client_id} received.")
    if os.path.isfile(client_file):
        logger.info(f"Sending file client id {client_id} received.")
        send_file(client_file)
    else:
        logger.error(f"Config file for client id {client_id} was not found.")
        logger.debug(f"Client file name {client_file} not found.")
        abort(404)

# Create new client
@app.post('/client')
def create_client():
    logger.info("Request to create client received.")
    client_id = os.popen(GENSCRIPT).read().strip()
    logger.info(f"Client with id {client_id} created.")
    data = {'client_id':client_id}
    return Response(json.dumps(data), status=201, mimetype='application/json') 

@app.delete('/client/<client_id>')
def revoke_client(client_id):
    client_file = f'{CLIENTS_PATH}/{client_id}/{client_id}.ovpn'
    logger.info(f"Request to remove client id {client_id} received.")
    if os.path.isfile(client_file):
        logger.debug(f"Calling rmscript {RMSCRIPT}")
        os.system(f"{RMSCRIPT} {client_id}")
    else:
        logger.error(f"Client id {client_id} not found.")
        abort(404)
    return Response(status=200)