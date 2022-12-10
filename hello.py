import werobot

token = 'token'
APP_ID = 'wx279feebefe92554b'
APP_SECRET = '7d66328e707024e8e538f1726ec3d573'

robot = werobot.WeRoBot(token=token)
# 让服务器监听在 0.0.0.0:80
robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.config['APP_ID'] = APP_ID 
robot.config['APP_SECRET'] = APP_SECRET


@robot.handler
def hello(message):
    return 'Hello World!'


robot.run()