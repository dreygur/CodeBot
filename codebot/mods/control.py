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
from fbchat.models import *

from codebot.mods.creds import setBotState

def ctrl(obj, inComingText, message_object, thread_id, thread_type):
	"""
	Controls the bot's awaking time

	Args:
		obj
		inComingText
	"""

	command = inComingText.split(" ")[1]
	reply = f"Bot Turned {command}!"

	if command == "off":
		setBotState(False)
		obj.send(Message(reply, reply_to_id=message_object.uid), thread_id=thread_id, thread_type=thread_type)
	elif command == "on":
		setBotState(True)
		obj.send(Message(reply, reply_to_id=message_object.uid), thread_id=thread_id, thread_type=thread_type)