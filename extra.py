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

	Args:
		code 	The source-code to be run
		lang 	Target Language of Source-Code
		inp 	Input for the executed instance

	Returns:
		status 	Status for the runtime

	Raises:
		None
	"""

	uri = "https://ide.geeksforgeeks.org/"
	data = {'lang':lang, 'code': code, 'input': inp, 'save': 'false'}
	res = rq.post(uri + "main.php", data=data).json()
	reply = "Report: \n+-+-+-+\n\n"

	if res["status"] == "SUCCESS":
		# Wait 10 Seconds to get the Output
		sleep(10)
		# Response from Compilation Instance
		nres = rq.post(uri + "submissionResult.php",
						data = {
							'sid': res['sid'],
							'requestType': 'fetchResults'
						}).json()

		# Result Success
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
		
		output = nres.get("output")
		obj.send(Message(reply, reply_to_id=uid),
					thread_id=thread_id,
					thread_type=thread_type)

		if output is None:
			return

		if len(output) < 1001:
			if len(output) > 601:
				n = len(output) // 2
				outputs = [output[i:i+n] for i in range(0, len(output), n)]
				for output in outputs:
					uid = obj.send(Message(output,
									reply_to_id=uid),
									thread_id=thread_id,
									thread_type=thread_type)
					sleep(randint(1,3))
			else:
				obj.send(Message(output, reply_to_id=uid),
						thread_id=thread_id,
						thread_type=thread_type)
		else:
			n = str(randint(0, 1000))
			while os.path.isfile(n):
				n = str(randint(0, 1000)) 
				print(n)
			n += '.txt'
			with open(n, 'w') as f:
				f.write(output)
			obj.sendLocalFiles([n],
								Message('Output:', reply_to_id=uid),
								thread_id=thread_id,
								thread_type=thread_type)
			os.remove(n)
	# return status
