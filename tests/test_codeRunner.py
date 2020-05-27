#!/usr/bin/env python3

# Test
from codebot.mods.codebot import CodeBot
from codebot.mods.coderunner import runCode

def test_runCode():
	bot = CodeBot(email, password)
	assert runCode("print('Hello from Python')", "python3", "", obj, thread_id, thread_type, uid)