#!/bin/bash
# conda activate ShoShoBot !!! for some reason, this operaition is not supported
rm nohup.out # remove log from previous session 
rm werobot_session.sqlite3 # remove session sqlite file 
nohup python FCE_bot.py & 
