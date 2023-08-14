from flask import Flask
from flask import send_file, abort
from flask import Response
import json
import os
from .variables import *
from .auth import apikey_required
import logging

def api_app():
    app = Flask(__name__, instance_relative_config=True)
    
    logging.basicConfig(format="[%(asctime)s] %(process)s %(levelname)s %(message)s", level=logging.DEBUG)
    # get waitress logger
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.DEBUG)
    
    # Get client by id
    @app.get('/client/<client_id>')
    @apikey_required
    def get_client(client_id):
        client_file = f'{CLIENTS_PATH}/{client_id}/{client_id}.ovpn'
        logger.info(f"Request for client id {client_id} received.")
        if os.path.isfile(client_file):
            logger.info(f"Sending file client id {client_id} received.")
            return send_file(client_file)
        else:
            logger.error(f"Config file for client id {client_id} was not found.")
            logger.debug(f"Client file name {client_file} not found.")
            return Response(json.dumps({"message":f"Config file for client id {client_id} was not found."}), status=404, mimetype='application/json')

    # Create new client
    @app.post('/client')
    @apikey_required
    def create_client():
        logger.info("Request to create client received.")
        try:
            client_id = os.popen(GENSCRIPT).read().strip()
            logger.info(f"Client with id {client_id} created.")
            data = {'message':'New client successfully created.','client_id':client_id}
            return Response(json.dumps(data), status=201, mimetype='application/json') 
        except:
            return Response(json.dumps({'massage':'Internal Error occured.','client_id':0}), status=500, mimetype='application/json') 

    @app.delete('/client/<client_id>')
    @apikey_required
    def revoke_client(client_id):
        client_file = f'{CLIENTS_PATH}/{client_id}/{client_id}.ovpn'
        logger.info(f"Request to remove client id {client_id} received.")
        if os.path.isfile(client_file):
            logger.debug(f"Calling rmscript {RMSCRIPT}")
            os.system(f"{RMSCRIPT} {client_id}")
        else:
            logger.error(f"Client id {client_id} not found.")
            return Response(json.dumps({"message":f"Client with id {client_id} was not found."}), status=404, mimetype='application/json')
        return Response(status=200)
    return app