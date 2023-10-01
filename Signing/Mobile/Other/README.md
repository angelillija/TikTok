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
