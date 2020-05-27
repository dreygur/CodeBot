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
from codebot.mods.coderunner import runCode

def run(
	obj,
	author_id,
	message_object,
	inComingText,
	thread_id,
	thread_type
):
	"""
	This function is responsible for sending code output
	and results if the bot gets message as `/run`

	Args:
		obj 			Class instance from parent class
		author_id 		Author ID
		message_object 	Message Object
		thread_id 		Thread ID
		thread_type 	Thread Type

	Returns:
		None

	Raises:
		None
		
	"""
	replyText = message_object.replied_to

	if replyText is not None:
		# SOURCE-CODE of URI
		codeUri = replyText.text

		if codeUri is None:
			reply = "Please reply to the message containg code..."
		else:
			if codeUri[:7] == "http://" or codeUri[:8] == "https://":
				site = codeUri.split("/")[2]
			else: site = ""

			if site == "pastebin.com":
				code = rq.get(codeUri[:21] + "raw/" + codeUri[21:]).text
			elif site == "paste.ubuntu.com":
				codeUri = codeUri if codeUri[-1] == '/' else codeUri + '/'
				code = rq.get(codeUri + 'plain',
					cookies={"sessionid": ubuntuPastebin}).text
				print(code)
			else: code = codeUri

			args = inComingText.split(" ")
			reply = 'Please Wait while I Complete Execution :)'
			error = False
			language = {'C':'C', 'C++':'Cpp', 'Cpp':'Cpp', 'Java':'Java', 'Python':'Python3','Python3':'Python3','Py':'Python3', 'C#':'Csharp', 'Csharp':'Csharp'}

			if len(args) == 1:
				reply += '\n\nBy the way ;) , the standard format is /run language input(s)'
				codeArgs = (code, 'C', '', obj, thread_id, thread_type, message_object.uid)
			elif len(args) == 2:
				lang = args[1].title()
				if lang in language.keys():
					codeArgs = (code, language[lang], '', obj, thread_id, thread_type, message_object.uid)
					reply += '\n\nBy the way, I\'ll consider that this program has no input ;)'
				else:
					error = True
					reply = 'Lanuguae Not Supported! Supported Languages are: C / Cpp / Java / Python / C#'
			else:
				lang = args[1].title()
				if lang in language.keys():
					codeArgs = (code, language[lang], ' '.join(args[2:]), obj, thread_id, thread_type, message_object.uid)
					reply += '\n\nBy the way, Best of Luck!'
				else:
					error = True
					reply = 'Lanuguae Not Supported! Supported Languages are: C / C++(Cpp) / Java / Python / C#(Csharp)'
			if not error:
				threading.Thread(target=runCode, args=codeArgs).start()

			obj.send(Message(reply), thread_id=thread_id, thread_type=thread_type)
