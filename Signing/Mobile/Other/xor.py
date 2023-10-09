def encrypt(string):
    return "".join([hex(ord(c) ^ 5)[2:] for c in string])


# Add string to encrypt
print(encrypt(""))
