from random import randint
from time import time
from struct import unpack
from base64 import b64encode
from hashlib import md5
from urllib.parse import parse_qs
from Crypto.Cipher.AES import new, MODE_CBC, block_size
from Crypto.Util.Padding import pad
from utils.signer.lib.Sm3 import SM3
from utils.signer.lib.Simon import simon_enc
from utils.signer.lib.protobuf import ProtoBuf

from Crypto.Cipher.AES import new, MODE_CBC, block_size


class Argus:
    def encrypt_enc_pb(data, l):
        data = list(data)
        xor_array = data[:8]

        for i in range(8, l):
            data[i] ^= xor_array[i % 8]

        return bytes(data[::-1])

    @staticmethod
    def get_bodyhash(stub: str or None = None) -> bytes:
        return (
            SM3().sm3_hash(bytes(16))[0:6]
            if stub == None or len(stub) == 0
            else SM3().sm3_hash(bytes.fromhex(stub))[0:6]
        )

    @staticmethod
    def get_queryhash(query: str) -> bytes:
        return (
            SM3().sm3_hash(bytes(16))[0:6]
            if query == None or len(query) == 0
            else SM3().sm3_hash(query.encode())[0:6]
        )

    @staticmethod
    def encrypt(xargus_bean: dict):
        protobuf = pad(bytes.fromhex(ProtoBuf(xargus_bean).toBuf().hex()), block_size)
        new_len = len(protobuf)
        sign_key = b"\xac\x1a\xda\xae\x95\xa7\xaf\x94\xa5\x11J\xb3\xb3\xa9}\xd8\x00P\xaa\n91L@R\x8c\xae\xc9RV\xc2\x8c"
        sm3_output = b"\xfcx\xe0\xa9ez\x0ct\x8c\xe5\x15Y\x90<\xcf\x03Q\x0eQ\xd3\xcf\xf22\xd7\x13C\xe8\x8a2\x1cS\x04"  # sm3_hash(sign_key + b'\xf2\x81ao' + sign_key)

        key = sm3_output[:32]
        key_list = []
        enc_pb = bytearray(new_len)

        for _ in range(2):
            key_list = key_list + list(unpack("<QQ", key[_ * 16 : _ * 16 + 16]))

        for _ in range(int(new_len / 16)):
            pt = list(unpack("<QQ", protobuf[_ * 16 : _ * 16 + 16]))
            ct = simon_enc(pt, key_list)
            enc_pb[_ * 16 : _ * 16 + 8] = ct[0].to_bytes(8, byteorder="little")
            enc_pb[_ * 16 + 8 : _ * 16 + 16] = ct[1].to_bytes(8, byteorder="little")

        b_buffer = Argus.encrypt_enc_pb(
            (b"\xf2\xf7\xfc\xff\xf2\xf7\xfc\xff" + enc_pb), new_len + 8
        )
        b_buffer = b"\xa6n\xad\x9fw\x01\xd0\x0c\x18" + b_buffer + b"ao"

        cipher = new(md5(sign_key[:16]).digest(), MODE_CBC, md5(sign_key[16:]).digest())

        return b64encode(
            b"\xf2\x81" + cipher.encrypt(pad(b_buffer, block_size))
        ).decode()

    @staticmethod
    def get_sign(
        queryhash: None or str = None,
        data: None or str = None,
        timestamp: int = int(time()),
        aid: int = 1233,
        license_id: int = 1611921764,
        platform: int = 0,
        sec_device_id: str = "",
        sdk_version: str = "v04.04.05-ov-android",
        sdk_version_int: int = 134744640,
    ) -> dict:
        params_dict = parse_qs(queryhash)

        return Argus.encrypt(
            {
                1: 0x20200929 << 1,  # magic
                2: 2,  # version
                3: randint(0, 0x7FFFFFFF),  # rand
                4: str(aid),  # msAppID
                5: params_dict["device_id"][0],  # deviceID
                6: str(license_id),  # licenseID
                7: params_dict["version_name"][0],  # appVersion
                8: sdk_version,  # sdkVersionStr
                9: sdk_version_int,  # sdkVersion
                10: bytes(8),  # envcode -> jailbreak Detection
                11: platform,  # platform (ios = 1)
                12: timestamp << 1,  # createTime
                13: Argus.get_bodyhash(data),  # bodyHash
                14: Argus.get_queryhash(queryhash),  # queryHash
                15: {
                    1: 1,  # signCount
                    2: 1,  # reportCount
                    3: 1,  # settingCount
                    7: 3348294860,
                },
                16: sec_device_id,  # secDeviceToken
                # 17: timestamp,                     # isAppLicense
                20: "none",  # pskVersion
                21: 738,  # callType
                23: {1: "NX551J", 2: 8196, 4: 2162219008},
                25: 2,
            }
        )
