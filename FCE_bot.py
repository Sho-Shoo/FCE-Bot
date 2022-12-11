import werobot
import FCE_services as FCE

################################################################################
# Server setup
################################################################################
token = 'token'
TEST_APP_ID = 'wx279feebefe92554b'
TEST_APP_SECRET = 'a926374c46290d02d7ed37771bae8f64'

ACTUAL_APP_SECRET = '713cd7f2002ffcd9c84e7fcd7635448f'
ACTUAL_APP_ID = 'wx96478d0e33536a7a'

robot = werobot.WeRoBot(token=token)
robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = '8080'
robot.config['APP_ID'] = ACTUAL_APP_ID 
robot.config['APP_SECRET'] = ACTUAL_APP_SECRET
################################################################################

################################################################################
# Other
################################################################################

# formulate subscribe message 
with open("logo.txt", "r") as txt: 
     logo = txt.read() 
     logo = logo.replace(" ", "  ") # double spacing to fit wechat chatbox display

subscribe_txt = "Welcome to ShoShoBot, it provides CMU FCE querying services. Type course number to continue."
subscribe_msg = logo + "\n" + subscribe_txt

################################################################################
# Handler definitions 
################################################################################
@robot.text
def fce_by_course_num(message):
    return FCE.get_fce_info(message.content)

@robot.subscribe 
def get_subscribe_msg(): 
    return subscribe_msg

robot.run()
