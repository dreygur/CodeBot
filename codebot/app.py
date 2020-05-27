#!/usr/bin/env python3

"""
Chatbot for Messenger Groups to Compile
and reply code-status.

The bot currently works as a facebook user

Depends on:
	- GeekForGeeks (website) - for code execution
	- fbchat (module) - to interact with facebook
	- json (module) - json data
	- threading (module) - for multithreading 
	- requests (module) - for http requests

Author: Rakibul Yeasin
	- Github: dreygur
	- Facebook: dreygur
	- Twitter: drreygur
"""

import os
import sys
import json
import threading
from time import sleep

# Third-Party Modules
import requests as rq
from fbchat import Client
from fbchat.models import *

# In-App Modules
from codebot.mods.codebot import CodeBot
from codebot.mods.creds import user, password, agent, getfbCookie,setfbCookie


def app() -> None:
	"""
	The MAIN function

	Args:
		None

	Returns:
		None
	"""
	# Cookies
	cookies = getfbCookie()

	# fbchat Instance
	fb = CodeBot(user, password,
				user_agent=agent,
				session_cookies=cookies,
				logging_level=20)

	# Save retrieved cookie
	setfbCookie(fb.getSession())

	fb.listen()

def awaker():
	"""
	Keeps the Application running 24/7
	on Heroku

	Args:
		None

	Returns:
		None

	Raises:
		None
	"""
	while True:
		print('[*] Awaking App!')
		rq.get("https://codebot-ttl.herokuapp.com/")
		sleep(300)