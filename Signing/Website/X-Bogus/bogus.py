# github.com/angelillija

from hashlib import md5
from time import time

class Signer:
    def md5_2x(string):
        return md5(md5(string.encode()).digest()).hexdigest()

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

    def filter(num_list: list):
        return [num_list[x - 1] for x in [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 4, 6, 8, 10, 12, 14, 16, 18, 20]]

    def scramble(a, b, c, d, e, f, g, h, i, j, k, l, m, n,o, p, q, r, s) -> str:
        return "".join([chr(_) for _ in [
            a, k, b, l, c, m,
            d, n, e, o, f, p,
            g, q, h, r, i, s,
            j,
        ]])
        
    def checksum(salt_list: str) -> int:
        checksum = 64; _ = [checksum := checksum ^ x for x in salt_list[3:]]
        
        return checksum

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
        
    def sign(params: str, ua: str) -> str:
        return params + '&X-Bogus=' + Signer._x_bogus(params, ua, int(time()))