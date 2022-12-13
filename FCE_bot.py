import werobot
import FCE_services
import psycopg2
import sys

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
# DB connection setup
################################################################################
try:
    db, user = 'fce_db', 'ec2-user'
    if len(sys.argv) >= 2:
        db = sys.argv[1]
    if len(sys.argv) >= 3:
        user = sys.argv[2]
    conn = psycopg2.connect(database=db, user=user)
    conn.autocommit = True
    cur = conn.cursor()
    print("Successfully connected to database. ")
except psycopg2.Error as e:
    print("Unable to open connection: %s" % (e,))
    exit()
except Exception as e: 
    print(f"Other DB connection error: {e}")
    exit()

################################################################################
# Other stuff
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
FCE = FCE_services.FCE_services(cur)

@robot.text
def fce_by_text(message):
    return FCE.get_fce_info(message.content)

@robot.subscribe 
def get_subscribe_msg(): 
    return subscribe_msg

robot.run()
