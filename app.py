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
	):

		"""
		Overriding onMessage method
		"""

		# Functionwide Variables
		replyText: str = ""
		codeUri: str = ""
		code: str = ""

		# Text Message from User
		inComingText = message_object.text.lower()

		# Start execution if found command "/run"
		if inComingText.startswith("/run"):
			replyText = message_object.replied_to

			if replyText is not None:
				# SOURCE-CODE of URI
				codeUri = replyText.text

				if codeUri is None:
					reply = "Please reply to the message containg code..."
				else:
					if codeUri[:7] == "http://" or codeUri[:8] == "https://":
						site = codeUri.split("//")[1]
					else: site = ""

					if site == "pastebin.com/":
						code = rq.get(codeUri[:21] + "raw/" + codeUri[21:]).text
					elif site == "paste.ubuntu.com/p/":
						codeUri = codeUri if codeUri[-1] == '/' else codeUri + '/'
						code = rq.get(codeUri + 'plain',
							cookies={'sessionid': 'v0qhur8831ac0n7rhvf6xq8h9x7wwypn'}).text
					else: code = codeUri

					args = inComingText.split(" ")
					reply = 'Please Wait while I Complete Execution :)'
					error = False
					language = {'C':'C', 'C++':'Cpp', 'Cpp':'Cpp', 'Java':'Java', 'Python':'Python3','Python3':'Python3','Py':'Python3', 'C#':'Csharp', 'Csharp':'Csharp'}

					if len(args) == 1:
						reply += '\n\nBy the way ;) , the standard format is /run language input(s)'
						codeArgs = (code, 'C', '', self, thread_id, thread_type, message_object.uid)
					elif len(args) == 2:
						lang = args[1].title()
						if lang in language.keys():
							codeArgs = (code, language[lang], '', self, thread_id, thread_type, message_object.uid)
							reply += '\n\nBy the way, I\'ll consider that this program has no input ;)'
						else:
							error = True
							reply = 'Lanuguae Not Supported! Supported Languages are: C / Cpp / Java / Python / C#'
					else:
						lang = args[1].title()
						if lang in language.keys():
							codeArgs = (code, language[lang], ' '.join(args[2:]), self, thread_id, thread_type, message_object.uid)
							reply += '\n\nBy the way, Best of Luck!'
						else:
							error = True
							reply = 'Lanuguae Not Supported! Supported Languages are: C / C++(Cpp) / Java / Python / C#(Csharp)'
					if not error:
						threading.Thread(target=runCode, args=codeArgs).start()
						# rCode = threading.Thread(target=runCode, args=args)
						# rCode.start()
						# rCode.join()
					self.send(Message(reply), thread_id=thread_id, thread_type=thread_type)

		# self.send(Message('Please reply to the messsage that contains code you want to run and say "/run language input(s)" '), thread_id=thread_id, thread_type=thread_type)


def runCode(
	code: str,
	lang: str,
	inp: str,
	obj,
	thread_id,
	thread_type,
	uid
) -> str:
	"""
	RUNNER function for given code

	This simply passes the code to https://geekforgeeks.com
	and returns the formatted result to user.

	Arguments:
		code 	The source-code to be run
		lang 	Target Language of Source-Code
		inp 	Input for the executed instance

	Returns:
		status 	Status for the runtime
	"""

	uri = "https://ide.geeksforgeeks.org/"
	data = {'lang':lang, 'code': code, 'input': inp, 'save': 'false'}
	res = rq.post(uri + "main.php", data=data).json()
	reply = "Report: \n+-+-+-+-+-+\n\n"

	if res["status"] == "SUCCESS":
		sleep(10)
		nres = rq.post(uri + "submissionResult.php",
						data = {
							'sid': res['sid'],
							'requestType': 'fetchResults'
						}).json()
		if nres.get("compResult") == "S":
			reply += "Compile: Success!\n"
			if nres.get("rntError"):
				reply += 'Run: Error!\nReason: ' + nres ['rntError'][:-1] + '!'
			else:
				reply += 'Run: Success!'
		elif nres.get("cmpError") is not None:
			reply += 'Compile: Failed!\nReason: ' + nres['cmpError']
		if nres.get("time") is not None and nres.get("memory") is not None:
			reply += '\n\nTime: ' + nres['time'] + '\nMemory: ' + nres['memory']
		
		output = nres['output']
		obj.send(Message(reply, reply_to_id=uid), thread_id=thread_id, thread_type=thread_type)

		if output is None:
			return

		if len(output) < 1001:
			if len(output) > 601:
				n = len(output) // 2
				outputs = [output[i:i+n] for i in range(0, len(output), n)]
				for output in outputs:
					uid = obj.send(Message(output, reply_to_id=uid), thread_id=thread_id, thread_type=thread_type)
					sleep(randint(1,3))
			else:
				obj.send(Message(output, reply_to_id=uid), thread_id=thread_id, thread_type=thread_type)
		else:
			n = str(randint(0, 1000))
			while os.path.isfile(n):
				n = str(randint(0, 1000)) 
				print(n)
			n += '.txt'
			with open(n, 'w') as f:
				f.write(output)
			obj.sendLocalFiles([n], Message('Output:', reply_to_id=uid), thread_id=thread_id, thread_type=thread_type)
			os.remove(n)
	# return status

def app() -> None:
	"""
	The MAIN function

	Arguents:
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
		fb = CodeBot(user, password, user_agent=agent, session_cookies=cookies, logging_level=20)
		# fbchat Session
		with open("cookies.json", "w") as cookie:
			json.dump(fb.getSession(), cookie)

		fb.listen()
		# res = runCode("print('Hello')", "python3", "")
		# print(res)
	except rq.exceptions.ConnectionError:
		print("[*] Check network connection...")

def awaker():
	while True:
		print('[*] Awaking App!')
		rq.get('https://codebot-ttl.herokuapp.com/')
		sleep(300)

if __name__ == "__main__":
	try:
		# Run the MAIN FUNCTION
		app()
		# main = threading.Thread(target=app)

		# # Start Thread
		# main.start()

		# # Join Threads with OS Processes
		# main.join()
	except Exception as e:
		print(e)
