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
import re
import sys
import json
import threading
from time import sleep
from time import time

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
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.messages = list()
		self.actions = dict()
		self.reacts = dict()

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
				if not inComingText.lower().startswith("stop"):
					self.send(Message(reply, reply_to_id=message_object.uid), thread_id=thread_id, thread_type=thread_type)

		if author_id != self.uid and thread_type == ThreadType.USER:
			message_object.uid = mid
			self.messages.append(message_object)
			for message in self.messages:
				ts = (time() - 10 * 60) * 1000
				if message.timestamp < ts:
					self.messages = list(filter(lambda x: x is not message, self.messages))

	def onMessageUnsent(
		self,
		mid=None,
		author_id=None,
		thread_id=None,
		thread_type=None,
		ts=None,
		msg=None
	):
		for message in self.messages:
			if message.uid == mid:
				files, unsendable_files, shares = [], [], []
				for a in message.attachments:
					if isinstance(a, ImageAttachment):
						if a.is_animated: files.append(a.animated_preview_url)
						else:
							url = a.large_preview_url or a.preview_url or a.thumbnail_url
							if url: files.append(url)
					elif isinstance(a, VideoAttachment):
						files.append(a.preview_url)
					elif isinstance(a, AudioAttachment):
						fileName = a.filename[:-1] + '3'
						r = requests.get(a.url)
						with open(fileName, 'wb') as f:
							f.write(r.content)
						unsendable_files.append(fileName)
					elif isinstance(a, FileAttachment):
						r = requests.get(a.url)
						url = re.search(r"document\.location\.replace\(\"(.*)\"\);", r.text).group(1)
						url = url.replace(r'\/', '/')
						files.append(url)
					elif isinstance(a, ShareAttachment):
						shares.append([a.title, a.original_url, a.description])

				author = self.fetchUserInfo(message.author)[message.author]
				message.reply_to_id = None
				self.send(Message("{} deleted the message:".format(author.name),
								  mentions=[Mention(author.uid, length=len(author.name))]))
				if message.text or message.sticker:
					self.send(message)
				if unsendable_files:
					self.sendLocalFiles(unsendable_files)
				if files:
					self.sendRemoteFiles(files)
				if shares:
					for share in shares:
						self.send(Message('Shared a link:\n\n{}\n\nLink: {}\n\nDescription: {}'.format('Title: '+share[0] if share[0]!='' else '',share[1], share[2])))
				
				self.messages = list(filter(lambda x: x is not message, self.messages))
				for f in unsendable_files:
					os.remove(f)
				break