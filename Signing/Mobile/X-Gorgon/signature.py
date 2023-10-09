# github.com/angelillija

import hashlib
import time


class Signature:
    def __init__(self, params: str, data: str, cookies: str) -> None:
        self.params = params
        self.data = data
        self.cookies = cookies

    def get_value(self) -> dict:
        gorgon = self.encrypt(
            "".join(
                hashlib.md5(value.encode()).hexdigest()
                if value
                else "00000000000000000000000000000000"
                for value in [self.params, self.data, self.cookies]
            )
        )
        return {
            "X-Gorgon": f"0404b0d30000{gorgon}", 
            "X-Khronos": str(int(time.time()))
        }

    @staticmethod
    def encrypt(data: str) -> str:
        unix = int(time.time())
        length = 0x14
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

        param_list = [
            int(data[8 * i : 8 * (i + 1)][j * 2 : (j + 1) * 2], 16)
            for i in range(3)
            for j in range(4)
        ]
        param_list.extend([0x0, 0x6, 0xB, 0x1C])

        unix_bytes = unix.to_bytes(4, byteorder="big")
        param_list.extend(unix_bytes)

        eor_result_list = [A ^ B for A, B in zip(param_list, key)]

        for i in range(length):
            eor_result_list[i] = (~eor_result_list[i] ^ length) & 0xFF

        return "".join(f"{param:02x}" for param in eor_result_list)
