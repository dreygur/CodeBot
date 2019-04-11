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
from codebot.mods.run import run
from codebot.mods.control import ctrl
from codebot.mods.creds import getBotState
from codebot.mods.creds import ubuntuPastebinCookie
from codebot.mods.creds import gf
from codebot.mods.gf import sendToGF

class CodeBot(Client):
	"""
	Overriding the fbchat.Client class
	"""

	def onMessage(
		self,
		author_id,
		message_object,
		thread_id,
		thread_type,
		**kwargs
	) -> None:

		"""
		Overriding onMessage method

		Args:
			self:	Class instance
			autjor_id:	Unique ID of Messages Author
			message_object:	Text Message
			thread_id: The ID of the thread where texts are appearing
			thread_type: GROUP or Profile

		Returns:
			None

		Raises:
			None
		"""

		# Functionwide Variables
		replyText: str = ""
		codeUri: str = ""
		code: str = ""
		ubuntuPastebin: str = ubuntuPastebinCookie

		# Text Message from User
		inComingText = message_object.text.lower()

		# Start execution if found command "/run" Bot's Status is Up
		if inComingText.startswith("/run") and getBotState():
			# Run the code and send back the result to user
			run(self, author_id, message_object, inComingText, thread_id, thread_type)

			# self.send(Message('Please reply to the messsage that contains code you want to run and say "/run language input(s)" '), thread_id=thread_id, thread_type=thread_type)

		if inComingText.startswith("/ctrl"):
			# Set the bot to reply or not
			ctrl(self, inComingText, message_object, thread_id, thread_type)

		if not inComingText.startswith("/")\
			and getBotState() is False\
			and thread_type == ThreadType.USER:

			if author_id == gf:
				sendToGF(self, inComingText, message_object, thread_id, thread_type)
			elif author_id != self.uid:
				reply = """I'm offline right now. It's an automated message. To stop this message please reply with 'stop' before sending any message. I'll reply you within a short time.\n\nThanks!"""
				if inComingText.lower().startswith("stop"):
					self.send(Message(reply, reply_to_id=message_object.uid), thread_id=thread_id, thread_type=thread_type)