# X-Gorgon 0404 & X-Khronos

Two of the four current TikTok's security headers in their mobile android API are X-Gorgon & X-Khronos. These two are used by TikTok to authenticate and secure API requests.

X-Gorgon is created by hashing key components and combining them with a version and timestamp, ensuring the validity and integrity of requests to TikTok's servers.

X-Khronos is just a hexadecimal timestamp.

### Hashed String Example: 
- Params Hash -> 9336ebf25087d91c818ee6e9ec29f8c1 
- No Data -> 00000000000000000000000000000  
- No Cookies -> 00000000000000000000000000000000000

### Encrypted String example:
- Version -> 0404
- Static hash -> b0d30000
- Encrypted hash string -> 3f2892cbeb57387ccee15dbc3694a6f7df5311c6

TikTok decrypts the X-Gorgon header to validate the request. If the decryption is successful, the request is considered valid and access to the API is granted; otherwise, an empty response or an error status code may be returned.



### Base String Generation:

- The base string is generated by concatenating MD5 hashes of URL parameters, post data, and cookies, along with a hexadecimal timestamp.
- The hash values are generated using MD5 (message-digest algorithm) for the respective parameters (URL Params, Post Data, Cookies).
- If any parameter (data or cookies) is not provided, 32 zeros are used in place of their hashes.

```py
    def calc_gorgon(self) -> str:
        gorgon = self.hash(self.params)
        if self.data:
            gorgon += self.hash(self.data)
        else:
            gorgon += str("0"*32)
        if self.cookies:
            gorgon += self.hash(self.cookies)
        else:
            gorgon += str("0"*32)
        gorgon += str("0"*32)
        return gorgon
```
  
### Encryption Key Generation:

- The base string is converted to a hex list.
- This hex list is used as an encryption key.

```py
def get_value(self):
    return self.encrypt(self.calc_gorgon())
```
  
### Base String Encryption:

- The base string is encrypted using bitwise operations and XOR with a predefined encryption key.

```py
    def encrypt(self, data: str):
        unix = int(time.time())
        len = 0x14
        key = [
            0xDF,
            0x77,
            0xB9,
            0x40,
            0xB9,
            0x9B,
            0x84,
            0x83,
            0xD1,
            0xB9,
            0xCB,
            0xD1,
            0xF7,
            0xC2,
            0xB9,
            0x85,
            0xC3,
            0xD0,
            0xFB,
            0xC3,
        ]

        param_list = []

        for i in range(0, 12, 4):
            temp = data[8 * i : 8 * (i + 1)]
            for j in range(4):
                H = int(temp[j * 2 : (j + 1) * 2], 16)
                param_list.append(H)

        param_list.extend([0x0, 0x6, 0xB, 0x1C])

        H = int(hex(unix), 16)

        param_list.append((H & 0xFF000000) >> 24)
        param_list.append((H & 0x00FF0000) >> 16)
        param_list.append((H & 0x0000FF00) >> 8)
        param_list.append((H & 0x000000FF) >> 0)

        eor_result_list = []

        for A, B in zip(param_list, key):
            eor_result_list.append(A ^ B)

        for i in range(len):

            C = self.reverse(eor_result_list[i])
            D = eor_result_list[(i + 1) % len]
            E = C ^ D

            F = self.rbit(E)
            H = ((F ^ 0xFFFFFFFF) ^ len) & 0xFF
            eor_result_list[i] = H

        result = ""
        for param in eor_result_list:
            result += self.hex_string(param)

        return {"X-Gorgon": ("0404b0d30000" + result), "X-Khronos": str(unix)}
```
  
### Header Construction:

- The X-Gorgon header is constructed using the version (0404), a static hash (b0d30000), and the encrypted hash string.

```py
return {"X-Gorgon": ("0404b0d30000" + result), "X-Khronos": str(unix)} # can be found in the encrypt function
```

## Example Usage:

```py
from signature import signature

signer = signature(params="example_params", data="example_data", cookies="example_cookies").get_value()

print(f"X-Gorgon: {signer['X-Gorgon']} X-Khronos: {signer['X-Khronos']}")
```