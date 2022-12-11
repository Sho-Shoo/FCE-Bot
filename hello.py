import werobot

token = 'token'
TEST_APP_ID = 'wx279feebefe92554b'
TEST_APP_SECRET = 'a926374c46290d02d7ed37771bae8f64'

ACTUAL_APP_SECRET = '713cd7f2002ffcd9c84e7fcd7635448f'
ACTUAL_APP_ID = 'wx96478d0e33536a7a'

robot = werobot.WeRoBot(token=token)
robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = '8080'
robot.config['APP_ID'] = TEST_APP_ID 
robot.config['APP_SECRET'] = TEST_APP_SECRET

@robot.text
def hello(message):
    return 'Hello World!'


robot.run()
