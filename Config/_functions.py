import numpy as np
import random, string
from Config._const import ALPHABET

# grammar_list : Simple function to properly list many strings
def grammar_list(listed):
	if len(listed) > 2:
		first_list = ", ".join(listed[:-1])
		listed = first_list + ", and " + str(listed[-1])
	elif len(listed) == 2:
		listed = " and ".join(listed)
	elif len(listed) == 1:
		listed = "".join(listed)
	else:
		listed = "none"
	return listed

# word_count : Returns a response's word count
def word_count(response):
	words = 0
	for piece in response.split(" "):
		for character in piece:
			if character.isalnum():
				words += 1
				break
	return words

# elim_prize : Returns how many contestants should prize and be eliminated (based on Dark's formulas)
def elim_prize(count, elim_rate=0.2):
	numbers = []

	if count == 2:
		numbers.append(1)
	else:
		numbers.append(round(count * elim_rate))
	
	numbers.append(np.floor(np.sqrt(count) * np.log(count) / 3.75))
	return numbers

# formatting_fix : Fixes weirdly formatted lines that might cause formatting problems
def formatting_fix(line):
	format_types = ["||", "~~", "__", "***", "**", "*", "_"]

	for r in format_types:
		if line.count(r) % 2 == 1:
			line = line.replace(r, "")
	
	return line

# is_whole : Detects integers
def is_whole(s):
	try:
		es = int(s)
		es2 = float(s)
		if es == es2:
			return True
		else:
			return False
	except:
		return False

# is_float : Detect numbers that have decimal components
def is_float(s):
	try:
		es = int(s)
		es2 = float(s)
		if es2 - es != 0:
			return True
		else:
			return False
	except:
		return False

# key_generator : Generates a random alphanumeric string with variable length
def key_generator(n):
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(n))

# number_key : Generates a random numeric string with variable length
def number_key(n):
	return ''.join(random.SystemRandom().choice(string.digits) for _ in range(n))

# strip_alpha : Strip a string to only alphabet characters
def strip_alpha(string, spaces=False):
	if spaces:
		return ''.join([x for x in list(string) if x.upper() in ALPHABET[:26] or x == " "])
	return ''.join([x for x in list(string) if x.upper() in ALPHABET[:26]])