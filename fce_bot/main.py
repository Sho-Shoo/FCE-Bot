import json
import werobot
import sys
import pathlib

# reading authentication and configurations
project_root = pathlib.Path(__file__).parent.parent.resolve()
auth_file = open(project_root / "auth.json")
auth_info = json.load(auth_file)
TOKEN = auth_info["TOKEN"]
TEST_APP_ID = auth_info["TEST_APP_ID"]
TEST_APP_SECRET = auth_info["TEST_APP_SECRET"]
ACTUAL_APP_ID = auth_info["ACTUAL_APP_ID"]
ACTUAL_APP_SECRET = auth_info["ACTUAL_APP_SECRET"]

config_file = open(project_root / "config.json")
config = json.load(config_file)


################################################################################
# Server setup
################################################################################
robot = werobot.WeRoBot(token=TOKEN)
robot.config['HOST'] = config["host"]
robot.config['PORT'] = config["port"]
robot.config['APP_ID'] = ACTUAL_APP_ID
robot.config['APP_SECRET'] = ACTUAL_APP_SECRET
################################################################################

@robot.text
def fce_by_text(message):
    return "Hello world!"


@robot.subscribe
def get_subscribe_msg():
    return "Welcome here!"


server = robot.wsgi

