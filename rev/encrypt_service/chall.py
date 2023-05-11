# docker run -it --rm --name my-running-script -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:3.8 python -m compileall ./chall.py
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

def main():
	passwd = input("Introduce la contraseña: ")
	if hashlib.md5(passwd.encode()).hexdigest() != "e1568c571e684e0fb1724da85d215dc0":
		print("Wrong!")
		return

	print("Bienvenido al servicio de cifrado.")
	passwd = input("Introduce el mensaje: ")
	print(encrypt(passwd.encode()))


if __name__ == "__main__":
	main()