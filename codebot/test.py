#!/usr/bin/env python3

import threading
import requests as rq
from time import sleep

def a():
	for i in range(200, 300):
		print(f"[*] {i}")
		sleep(2)

def b():
	for i in range(1, 100):
		print(f"[*] {i}")
		sleep(2)

def runCode(
	code: str,
	lang: str,
	inp: str,
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
	reply = "Report: \n________\n\n"
	print("Got it!")
	if res["status"] == "SUCCESS":
		sleep(10)
		nres = rq.post(uri + "submissionResult.php",
						data = {
							'sid': res['sid'],
							'requestType': 'fetchResults'
						}).json()
		if nres["compResult"] == "S":
			reply += "Compile: Success!\n"
			print(res)
			print(nres)
			if nres.get("rntError"):
				reply += 'Run: Error!\nReason: ' + nres ['rntError'][:-1] + '!'
			else:
				reply += 'Run: Success!'
		elif nres.get("cmpError") is not None:
			reply += 'Compile: Failed!\nReason: ' + nres['cmpError']
		if nres.get("time") is not None and nres.get('memory') is not None:
			reply += '\n\nTime: ' + nres['time'] + '\nMemory: ' + nres['memory']
		
		output = nres['output']

		print(res)
		print(nres)

if __name__ == "__main__":
	p1 = threading.Thread(target=a)
	p2 = threading.Thread(target=b)

	# p1.start()
	# p2.start()

	runCode("print('Hello')", "Python3", "")

	# p1.join()
	# p2.join()