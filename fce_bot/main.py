import json
import logging
import sys
import pymongo.errors
import werobot
import pathlib
from pymongo import MongoClient
import os
from fce_bot.text_reply.text_message_replier import TextMessageReplier
from werobot.session.mongodbstorage import MongoDBStorage

################################################################################
# Reading authentication and configurations
################################################################################
project_root = pathlib.Path(__file__).parent.parent.resolve()
try:
    auth_file = open(project_root / "auth.json")
except FileNotFoundError:
    auth_file = open(project_root / "test_auth.json")  # fake auth info for CI usage
auth_info = json.load(auth_file)
TOKEN = auth_info["TOKEN"]
TEST_APP_ID = auth_info["TEST_APP_ID"]
TEST_APP_SECRET = auth_info["TEST_APP_SECRET"]
ACTUAL_APP_ID = auth_info["ACTUAL_APP_ID"]
ACTUAL_APP_SECRET = auth_info["ACTUAL_APP_SECRET"]
################################################################################


################################################################################
# Server setup
################################################################################
robot = werobot.WeRoBot(token=TOKEN)
robot.config['APP_ID'] = ACTUAL_APP_ID
robot.config['APP_SECRET'] = ACTUAL_APP_SECRET
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
# use mongo db to do session storage
session_collection = db["session"]
session_storage = MongoDBStorage(session_collection)
robot.config['SESSION_STORAGE'] = session_storage
################################################################################

text_replier = TextMessageReplier(db, logger)

robot.text(lambda message, session: text_replier.reply(message, session))


@robot.subscribe
def get_subscribe_msg():
    return "你好，欢迎使用CMU生活服务号CMU Bot！我们现在支持以下功能：\n\n" \
           "1. 使用课程号码进行FCE信息查询；您可以尝试发送'15213'给机器人"


server = robot.wsgi
