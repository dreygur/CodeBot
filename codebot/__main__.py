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

import sys
import threading

# Stop Writing Bytecodes
sys.dont_write_bytecode = True

# In-App Modules
from codebot.app import app
from codebot.app import awaker

if __name__ == "__main__":
	try:
		# Run the MAIN FUNCTION
		# main = threading.Thread(target=app)
		# awake = threading.Thread(target=awaker)

		# Start Thread
		# main.start()
		# awake.start()

		# Join Threads with OS Processes
		# main.join()
		# awake.join()
		app()
	except Exception as e:
		print(e)
