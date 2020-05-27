#!/usr/bin/env python3

import random as rnd

from fbchat.models import *

def sendToGF(obj, inComingText, message_object, thread_id, thread_type):
	excuse = [
		"আমি তো অনলাইনে নাই জানু, এসে রিপ্লাই দিচ্ছি!",
		"জানপাখি, আমি তো একটু ব্যাস্ত। বট সেট করে রাখছি। এসে কল দেই?",
		"লাভ ইউ জান্টুস!\nআমি অফলাইনে\n <3",
		"ভালবাসা নিও প্রিয়ে, আমি এখন অফলাইনে\n <3"
	]

	if "আচ্ছা" in inComingText:
		obj.send(Message("আচ্ছা"), thread_id=thread_id, thread_type=thread_type)
	else:
		obj.send(Message(rnd.choice(excuse), reply_to_id=message_object.uid), thread_id=thread_id, thread_type=thread_type)