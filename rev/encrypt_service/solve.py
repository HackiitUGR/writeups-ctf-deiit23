import hashlib
import os
import random
import base64
from datetime import datetime

def encrypt(msg):
	t = datetime.now().timestamp()
	random.seed(t)

	result = bytearray()
	for b in msg:
		result.append(b ^ random.randint(0, 0xFF))
	result += str(t).encode()

	return base64.b64encode(result).decode()

def decrypt(msg):
	msg = base64.b64decode(msg)
	t = float(msg[-17:].decode())
	random.seed(t)

	result = bytearray()
	for b in msg[:-17]:
		result.append(b ^ random.randint(0, 0xFF))
	return result.decode()


def main():
	with open("msg.enc") as f:
		msg_enc = f.read()
	print(decrypt(msg_enc))


if __name__ == "__main__":
	main()