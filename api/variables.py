import os

CONFIG_DIR=os.environ['APP_PERSIST_DIR']
CLIENTS_PATH=f'{CONFIG_DIR}/clients'
SCRIPTS_DIR=os.environ['APP_INSTALL_PATH']
GENSCRIPT=f"{SCRIPTS_DIR}/genclient.sh"
RMSCRIPT=f"{SCRIPTS_DIR}/rmclient.sh"
APIKEY_HEADER='API-Key'
