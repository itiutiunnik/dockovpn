import os

CONFIG_DIR=os.environ['APP_PERSIST_DIR']
CLIENT_FILE_NAME=f'{client_id}.ovpn'
CLIENT_FILE_PATH=f'{CONFIG_DIR}/clients/{client_id}/{CLIENT_FILE_NAME}'
SCRIPTS_DIR=os.environ['APP_INSTALL_PATH']
GENSCRIPT=f"{SCRIPTS_DIR}/genclient.sh"
RMSCRIPT=f"{SCRIPTS_DIR}/rmclient.sh"
