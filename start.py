import os

username = raw_input('Username:      ')
password = raw_input('Password:      ')

os.environ['IMPERSONATE'] =  '0'
os.environ['TTR_PLAYCOOKIE'] =  username
os.environ['TTR_PASSWORD'] =  password

import toontown.toonbase.ToontownStart
