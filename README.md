# FCE-Bot 

Began as a personal learning project to get familiar with AWS EC2 and Linux. It gradually evolved to a WeRobot server that implements auto-reply feature for a Wechat public account. This feature enables querying of CMU FCE (Faculty Couse Evaluation) information, which comes rather handy during course registration periods. 

## Dependencies 

- Python 3.x 
- Werobot 1.13.1
- Postgres 14 with a user named `ec2-user` 

Or simply execute `$ pip install -r requirements.txt` to install Python dependencies. 

## Setup 

- Execute `$ psql -U "ec2-user" -d postgres -f database/initialize.sql` to initialize database. 
- Execute `$ bash launch.sh` to start the service as a background process. 
- Execute `$ python FCE_bot.py` to run as foreground for debugging. 
