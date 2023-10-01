# TikTok X-SS-STUB

When intercepting TikTok's mobile API, you will notice a header called `X-SS-STUB`, this is added whenever there is a post request. 


![image](https://github.com/angelillija/priv/assets/105955582/0c21dbfe-672c-4663-af13-5b70e1cfde2f)

At first glance, you can clearly tell this is just MD5 hashed, in uppercase. We can verify this by going to [Hashes.com](https://hashes.com/en/tools/hash_identifier) & checking which hash this is.

![image](https://github.com/angelillija/priv/assets/105955582/60faf354-0fa1-4325-9759-c89d09db8061)

The encrypted data is the urlencoded form of the request body.

Here is the code that can generate this:

- `body=null` is encoded into bytes using the UTF-8 encoding because hashlib.md5() requires bytes as input.
- `hashlib.md5().hexdigest()` computes the MD5 hash of the input bytes.
- The `.upper()` method is used to convert the MD5 hash to uppercase.
```py
import hashlib

data = "body=null"

print(hashlib.md5(data.encode()).hexdigest().upper())
```
Just like shown in the first image, the generated output of the exact same request body is `46C03B52742B3F2615A3ABDF1636B754`

# Tiktok XOR Encryption

When intercepting TikTok's mobile API & looking at requests such as login, register, etc, you'll see that the email/username and password is encrypted.

![image](https://github.com/angelillija/priv/assets/105955582/0443758c-2622-4cb4-a505-6370bb523a07)

We can check what this is by going to [Hashes.com](https://hashes.com/en/tools/hash_identifier) & can see it's hex encoded.

![image](https://github.com/angelillija/priv/assets/105955582/8975b309-59a4-4044-a4fb-117e92e3176c)

```Dkb`iJkQju``` is a bytes literal in Python, representing a sequence of bytes. Each character in the string is represented as its ASCII byte value.


Here is code to decode it:

- ```for byte in b"Dkb`iJkQju"``` is a loop that iterates over each byte (ASCII value of a character) in the bytes literal.
- `byte ^ 5`: For each byte (ASCII value), the XOR (^) operation is performed with the constant value 5.
- The `bytes([...])` method constructs a new bytes object from the resulting list of XORed values.
- `.decode('utf-8')` decodes the bytes into a string using UTF-8 encoding.

```py
print(bytes([byte ^ 5 for byte in b"Dkb`iJkQju"]).decode('utf-8'))
```

The output is `AngelOnTop` which is correct but this is only decrypting it, we need a way to encrypt it.

- For each character, it performs an XOR operation between the ASCII value of the character and 5.
- It converts the XOR result to its hexadecimal representation using `hex(ord(c) ^ 5)`.
- It takes the hexadecimal representation (excluding the "0x" prefix) of each XOR result and concatenates them to form the encrypted string.

```py
def encrypt(string):
    return "".join([hex(ord(c) ^ 5)[2:] for c in string])

print(encrypt("AngelOnTop"))
```
Output: `446b6260694a6b516a75` As shown in the image in the request body, this is completely valid.
