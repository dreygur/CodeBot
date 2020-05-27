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

def app() -> None:
	"""
	The MAIN function

	Args:
		None

	Returns:
		None
	"""
	try:
		# Facebook User Details
		user = "01647561445"
		password = "798193274622"
		agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"

		# Use Old Cookie
		cookies: dict = {}
		try:
			with open("cookies.json", "r") as cookie:
				cookies = json.load(cookie)
		except: pass

		# fbchat Instance
		fb = CodeBot(user, password,
					user_agent=agent,
					session_cookies=cookies,
					logging_level=20)
		# fbchat Session
		with open("cookies.json", "w") as cookie:
			json.dump(fb.getSession(), cookie)

		fb.listen()
		# res = runCode("print('Hello')", "python3", "")
		# print(res)
	except rq.exceptions.ConnectionError:
		print("[*] Check network connection...")

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