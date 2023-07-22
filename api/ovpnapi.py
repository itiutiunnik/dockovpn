from flask import Flask
from flask import send_file, abort
from flask import Response
import json
import os
from variables import *
import logging

app = Flask
logger = logging.basicConfig(format="[%(asctime)s] %(process)s %(level)s %(message)s")
# Get client by id
@app.get('/client/<client_id>')
def get_client(client_id):
    logger.info("Request for client id %(client_id)s received.")
    if os.path.isfile(CLIENT_FILE_PATH):
        logger.info("Sending file client id %(client_id)s received.")
        send_file(CLIENT_FILE_PATH)
    else:
        logger.error("Config file for client id %(client_id)s was not found.")
        logger.debug("Client file name %(CLIENT_FILE_PATH)s not found.")
        abort(404)

# Create new client
@app.post('/client')
def create_client():
    logger.info("Request to create client received.")
    client_id = os.popen(GENSCRIPT).read().strip()
    logger.info("Client with id %(client_id)s created.")
    data = {'client_id':client_id}
    return Response(json.dumps(data), status=201, mimetype='application/json') 

@app.delete('/client/<client_id>')
def revoke_client(client_id):
    if os.path.isfile(CLIENT_FILE_PATH):
        os.system("%(RMSCRIPT)s %(client_id)s")
    else:
        abort(404)
    return Response(status=200)