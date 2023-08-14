import json
import logging
import sys
import pymongo.errors
import werobot
import pathlib
from pymongo import MongoClient
import os

# reading authentication and configurations
project_root = pathlib.Path(__file__).parent.parent.resolve()
auth_file = open(project_root / "auth.json")
auth_info = json.load(auth_file)
TOKEN = auth_info["TOKEN"]
TEST_APP_ID = auth_info["TEST_APP_ID"]
TEST_APP_SECRET = auth_info["TEST_APP_SECRET"]
ACTUAL_APP_ID = auth_info["ACTUAL_APP_ID"]
ACTUAL_APP_SECRET = auth_info["ACTUAL_APP_SECRET"]


################################################################################
# Server setup
################################################################################
robot = werobot.WeRoBot(token=TOKEN)
robot.config['APP_ID'] = ACTUAL_APP_ID
robot.config['APP_SECRET'] = ACTUAL_APP_SECRET
server = robot.wsgi
################################################################################

################################################################################
# Logger setup
################################################################################
log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s")
gunicorn_logger = logging.getLogger()
gunicorn_logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
gunicorn_logger.addHandler(console_handler)

robot.logger.handlers = gunicorn_logger.handlers
robot.logger.setLevel(gunicorn_logger.level)
logger = robot.logger
################################################################################

################################################################################
# Mongo connection
################################################################################
mongo_client = MongoClient(host=os.getenv("MONGODB_URL"), serverSelectionTimeoutMS=3000)
try:
    mongo_server_info = mongo_client.server_info()
    logger.info(f"Connection with MongoDB is successful! Mongo server info: {mongo_server_info}")
except pymongo.errors.ServerSelectionTimeoutError as e:
    logger.error("Connection with MongoDB fails")
    raise ConnectionError("Connection with MongoDB fails")
db = mongo_client["fce_db"]
################################################################################


@robot.subscribe
def get_subscribe_msg():
    return "Welcome here!"

