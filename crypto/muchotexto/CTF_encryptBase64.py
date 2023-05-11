import base64

string="ETSIIT_CTF{33__times__Base64_COM0__33?_EL_NANO?}"

for i in range(33):
    encoded_bytes = string.encode("utf-8")
    encoded_bytes = base64.b64encode(encoded_bytes)
    string = encoded_bytes.decode("utf-8")

print(string)
