# TikTok X-Bogus 
The X-Bogus security parameter is a critical component in TikTok's API for validating requests. When a request is made to TikTok's servers, it includes this parameter. TikTok processes the X-Bogus parameter using a proprietary decryption mechanism. If the decryption succeeds, the request is recognized as legitimate, granting access to the API. However, if the decryption fails, TikTok might respond with an empty response or an error status code, denying access.

In essence, the X-Bogus parameter acts as a validation token, allowing TikTok to ensure the authenticity and integrity of incoming API requests.

### Hashing with MD5
   
The MD5 hash function is used to process input data. The md5_2x function applies a double MD5 hash to enhance data security.
```py
def md5_2x(string):
    return md5(md5(string.encode()).digest()).hexdigest()
```

### RC4 Encryption
   
The RC4 encryption algorithm is employed to encrypt the user agent string. The resulting encrypted string is a key component of the X-Bogus header.
```py
    def rc4_encrypt(plaintext: str, key: list[int]) -> str:
        s_box = [i for i in range(256)]
        index = 0
        
        for _ in range(256):
            index = (index + s_box[_] + key[_ % len(key)]) % 256
            s_box[_], s_box[index] = s_box[index], s_box[_]
        
        _          = 0
        index      = 0
        ciphertext = ""
        
        for char in plaintext:
            _ = (_ + 1) % 256
            index = (index + s_box[_]) % 256
            s_box[_], s_box[index] = s_box[index], s_box[_]
            keystream = s_box[(s_box[_] + s_box[index]) % 256]
            ciphertext += chr(ord(char) ^ keystream)
        
        return ciphertext
```

### Base64 Encoding
Base64 encoding is used to convert binary data into a format suitable for transmission. The b64_encode function performs this encoding.

```py
    def b64_encode(
        string,
        key_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="):
        
        last_list = list()
        for i in range(0, len(string), 3):
            try:
                num_1 = ord(string[i])
                num_2 = ord(string[i + 1])
                num_3 = ord(string[i + 2])
                arr_1 = num_1 >> 2
                arr_2 = (3 & num_1) << 4 | (num_2 >> 4)
                arr_3 = ((15 & num_2) << 2) | (num_3 >> 6)
                arr_4 = 63 & num_3
                
            except IndexError:
                arr_1 = num_1 >> 2
                arr_2 = ((3 & num_1) << 4) | 0
                arr_3 = 64
                arr_4 = 64
                
            last_list.append(arr_1)
            last_list.append(arr_2)
            last_list.append(arr_3)
            last_list.append(arr_4)
            
        return "".join([key_table[value] for value in last_list])
```

### Data Scrambling
The `scramble` function takes various parameters and arranges them in a specific order, providing a scrambled representation of the input data.
```py
    def scramble(a, b, c, d, e, f, g, h, i, j, k, l, m, n,o, p, q, r, s) -> str:
        return "".join([chr(_) for _ in [
            a, k, b, l, c, m,
            d, n, e, o, f, p,
            g, q, h, r, i, s,
            j,
        ]])
        
    def checksum(salt_list: str) -> int:
        checksum = 64; _ = [checksum := checksum ^ x for x in salt_list[3:]]
```

### Checksum Calculation
The `checksum` function calculates a checksum based on a provided list of integers.
```py
    def checksum(salt_list: str) -> int:
        checksum = 64; _ = [checksum := checksum ^ x for x in salt_list[3:]]
        
        return checksum
```

### X-Bogus Generation
The `_x_bogus` function constructs the X-Bogus header by combining the processed data, user agent, and a timestamp. It applies specific operations and conversions to generate a unique X-Bogus value.

```py
    def _x_bogus(params: str, user_agent: str, timestamp: int, data: str = '') -> str:
        
        md5_data    = Signer.md5_2x(data)
        md5_params  = Signer.md5_2x(params)
        md5_ua      = md5(Signer.b64_encode(Signer.rc4_encrypt(user_agent, [0, 1, 14])).encode()).hexdigest() 
        
        salt_list   = [
            timestamp,
            536919696,
            64,
            0,
            1,
            14,
            bytes.fromhex(md5_params)[-2],
            bytes.fromhex(md5_params)[-1],
            bytes.fromhex(md5_data)[-2],
            bytes.fromhex(md5_data)[-1],
            bytes.fromhex(md5_ua)[-2],
            bytes.fromhex(md5_ua)[-1]
        ]
        
        salt_list.extend([(timestamp >> i) & 0xff for i in range(24, -1, -8)])
        salt_list.extend([(salt_list[1] >> i) & 0xff for i in range(24, -1, -8)])
        salt_list.extend([Signer.checksum(salt_list), 255])
        
        num_list     = Signer.filter(salt_list)
        rc4_num_list = Signer.rc4_encrypt(Signer.scramble( *num_list), [255])

        return Signer.b64_encode(
            f'\x02ÿ{rc4_num_list}', "Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe"
        )

```

### X-Bogus Signing
The `sign` function takes the parameters and user agent, generates the X-Bogus value using the `_x_bogu`s function, and appends it to the request parameters.
```py
def sign(params: str, ua: str) -> str:
    return params + '&X-Bogus=' + _x_bogus(params, ua, int(time()))
```

## Example Usage:
```py
from bogus import Signer

url = ""
user_agent = ""

x_bogus = sign(url.split("?")[1], user_agent)

print(f"{url.split("?")[0]}?{x_bogus}")
```