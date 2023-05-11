import base64

encoded_string = input(" ")
decoded_string = ""

while not decoded_string.startswith("ETSIIT_CTF"):
    decoded_bytes = base64.b64decode(encoded_string)
    decoded_string = decoded_bytes.decode("utf-8")
    encoded_string = decoded_string

print("Flag:", decoded_string)