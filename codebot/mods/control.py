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

from codebot.mods.creds import botState

def ctrl(obj, inComingText):
	"""
	Controls the bot's awaking time

	Args:
		obj
		inComingText
	"""

	command = inComingText.split(" ")[1]
	if command == "off": botState = False
	elif command == "on": botState = True