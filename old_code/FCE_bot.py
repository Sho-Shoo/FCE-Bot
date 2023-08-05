import werobot
import FCE_services
import psycopg2
import sys


def get_auth(auth_file): 
    """
    Returns authorization information from a file as a tuple
    """
    tup = tuple()
    with open(auth_file, 'r') as auth: 
        infos = auth.readlines() 
        for info in infos: 
            info = info.replace('\n', '')
            tup += (info,)

    return tup


################################################################################
# Server setup
################################################################################
TOKEN, TEST_APP_ID, TEST_APP_SECRET, \
ACTUAL_APP_SECRET, ACTUAL_APP_ID = get_auth("wechat_auth.txt")

robot = werobot.WeRoBot(token=TOKEN)
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
with open("../logo.txt", "r") as txt:
     logo = txt.read() 
     logo = logo.replace(" ", "  ") # double spacing to fit wechat chatbox display

subscribe_txt = "Welcome to FCE-Bot, which provides CMU FCE querying services. Type course number to continue."
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
