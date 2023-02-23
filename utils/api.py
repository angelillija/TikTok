import os
import uuid
import time
import json
import pytz
import random
import base64
import string
import hashlib
import requests
import binascii
import datetime
import threading
import urllib.parse
from utils.xgorgon import Xgorgon
from utils.ttencrypt import TTEncrypt
from utils.eazyui import *

class Output:
    def error(txt: str) -> None:
        Console.printError(txt, PrintType.CLEAN)

    def debug(txt: str) -> None:
        Console.printInfo(txt, PrintType.CLEAN)

    def good(txt: str) -> None:
        Console.printSuccess(txt, PrintType.CLEAN)

    def other(txt: str) -> None:
        Console.printOther(txt, PrintType.CLEAN)

application = {
    "aid"                   : 1233,
    "app_name"              : "musical_ly",
    "version_code"          : "100110",
    "version_name"          : "10.1.10",
    "ab_version"            : "10.1.10",
    "build_number"          : "10.1.10",
    "update_version_code"   : 2019030429,
    "manifest_version_code" : 2019030429,
    "app_version"           : "10.1.10",
    "version_code"          : 100110,
    "git_hash"              : "27690874",
    "release_build"         : "bd04df5_20190304",
    "sig_hash"              : "194326e82c84a639a52e5c023116f12a",
    "sdk"                   : "2",
    "sdk_version"           : "400",
}

class Utils:
    @staticmethod
    def xor(string):
        return "".join([hex(ord(c) ^ 5)[2:] for c in string])

class Email:
    def create_email(self):
        return "{}@{}".format(
            "".join(random.choices(string.ascii_lowercase, k = 13)), 
            random.choice(["lasagna.pro", "rblx.rocks", "linustechtips.email"])
        )

    def get_mail(self, email):
        with requests.Session() as session:
            base_mail = session.get(f"https://lasagna.pro/api/inbox/{email}")

            if base_mail.json()["emails"] == []:
                    return None
            else:
                return base_mail.json()["emails"]

class Device:
    locales = [
        {"by": "be-BY"},
        {"bg": "bg-BG"},
        {"es": "ca-ES"},
        {"cz": "cs-CZ"},
        {"dk": "da-DK"},
        {"de": "de-DE"},
        {"gr": "el-GR"},
        {"au": "en-AU"},
        {"us": "en-US"},
        {"fr": "fr-FR"},
        {"hr": "hr-HR"},
        {"it": "it-IT"},
        {"lt": "lt-LT"},
        {"pl": "pl-PL"},
        {"pt": "pt-BR"},
        {"ro": "ro-RO"},
        {"ru": "ru-RU"},
        {"sk": "sk-SK"},
        {"se": "sv-SE"},
        {"il": "iw-IL"},
        {"in": "hi-IN"},
    ]

    devices = [
        {
            "brand"     : "samsung",
            "model"     : ["SM-A127F"],
            "resolution": "1467x720",
            "dpi"       : 300,
            "build"     : ["RP1A.200720.012"],
            "rom"       : ["A127FXXU3AUJ5"],
            "board": [
                "universal7884B",
                "mt6768",
                "mt6768",
                "atoll",
                "universal9825",
                "universal7904",
                "universal7904",
                "universal9611",
                "mt6765",
                "msm8953",
                "universal7870",
                "universal9610",
                "universal9610",
                "universal9611",
                "msm8937",
                "universal7870",
                "universal7870",
                "msm8953",
                "universal7570",
                "msm8953",
                "mt6765",
                "mt6739",
                "sm6150",
                "universal9810",
                "msm8998",
                "universal7904",
                "sdm660",
                "universal7885",
                "msm8953",
                "universal7885",
                "msm8937",
                "universal7884B",
                "atoll",
                "universal9820",
                "universal3830",
                "mt6739",
                "sdm845",
                "universal9611",
                "universal3830",
                "universal9820",
                "universal3830",
                "mt6768",
                "sm6150",
                "mt6768",
                "universal9810",
                "universal9611",
                "universal9610",
                "universal7904",
                "kona",
                "msm8937",
                "msm8953",
                "mt6765",
                "msm8937",
                "mt6765",
                "msm8937",
                "bengal",
                "universal9810",
                "msmnile",
                "universal7904",
                "universal2100_r",
            ],
            "core": [
                "exynos7884B",
                "k69v1_64_titan_marmot",
                "k68v1_64_titan",
                "atoll",
                "exynos9825",
                "exynos7904",
                "exynos7904",
                "exynos9611",
                "S96116RA1",
                "msm8953",
                "exynos7870",
                "exynos9610",
                "exynos9610",
                "exynos9611",
                "msm8937",
                "exynos7870",
                "exynos7870",
                "msm8953",
                "exynos7570",
                "QC_Reference_Phone",
                "k65v1_64_bsp_titan_rat",
                "k39tv1_bsp_1g_titan",
                "sm6150",
                "exynos9810",
                "msm8998",
                "exynos7904",
                "sdm660",
                "exynos7885",
                "QC_Reference_Phone",
                "exynos7885",
                "QC_Reference_Phone",
                "exynos7884B",
                "atoll",
                "exynos9820",
                "exynos850",
                "k39tv1_bsp_titan_hamster",
                "sdm845",
                "exynos9611",
                "exynos850",
                "exynos9820",
                "exynos850",
                "k68v1_64_titan",
                "sm6150",
                "k69v1_64_titan_buffalo",
                "exynos9810",
                "exynos9611",
                "exynos9610",
                "exynos7904",
                "kona",
                "QC_Reference_Phone",
                "QC_Reference_Phone",
                "hs03s",
                "QC_Reference_Phone",
                "ot8",
                "QC_Reference_Phone",
                "bengal",
                "exynos9810",
                "msmnile",
                "exynos7904",
                "exynos2100",
            ],
            "device": [
                {"device": "a10", "product": "a10ser"},
                {"device": "a32", "product": "a32ser"},
                {"device": "a31", "product": "a31ser"},
                {"device": "a72q", "product": "a72qnsxx"},
                {"device": "d1", "product": "d1eea"},
                {"device": "a30", "product": "a30ser"},
                {"device": "a30s", "product": "a30sser"},
                {"device": "a51", "product": "a51nsser"},
                {"device": "a10s", "product": "a10sxx"},
                {"device": "a6plte", "product": "a6plteser"},
                {"device": "j6lte", "product": "j6lteser"},
                {"device": "a50", "product": "a50xser"},
                {"device": "a50", "product": "a50ser"},
                {"device": "m31", "product": "m31nsser"},
                {"device": "j6primelte", "product": "j6primelteser"},
                {"device": "j6lte", "product": "j6ltexx"},
                {"device": "a6lte", "product": "a6lteser"},
                {"device": "a20s", "product": "a20sxx"},
                {"device": "j4lte", "product": "j4lteser"},
                {"device": "a02q", "product": "a02qnnser"},
                {"device": "a12", "product": "a12nsser"},
                {"device": "a01core", "product": "a01coreser"},
                {"device": "a71", "product": "a71naxx"},
                {"device": "star2lte", "product": "star2lteser"},
                {"device": "gts4llte", "product": "gts4llteser"},
                {"device": "a40", "product": "a40ser"},
                {"device": "a9y18qlte", "product": "a9y18qlteser"},
                {"device": "a7y18lte", "product": "a7y18ltejt"},
                {"device": "m11q", "product": "m11qnsser"},
                {"device": "a7y18lte", "product": "a7y18lteser"},
                {"device": "gto", "product": "gtoser"},
                {"device": "a20", "product": "a20ser"},
                {"device": "a52q", "product": "a52qnsser"},
                {"device": "beyond0", "product": "beyond0lteser"},
                {"device": "a12s", "product": "a12snsser"},
                {"device": "a02", "product": "a02cisser"},
                {"device": "star2qltesq", "product": "star2qltesq"},
                {"device": "m21", "product": "m21nsser"},
                {"device": "m12", "product": "m12nsser"},
                {"device": "beyond2", "product": "beyond2ltexx"},
                {"device": "a21s", "product": "a21snsser"},
                {"device": "a41", "product": "a41ser"},
                {"device": "a60q", "product": "a60qzh"},
                {"device": "a22", "product": "a22nsser"},
                {"device": "starlte", "product": "starlteser"},
                {"device": "m31s", "product": "m31snsser"},
                {"device": "a50", "product": "a50dd"},
                {"device": "a30", "product": "a30dd"},
                {"device": "x1q", "product": "x1quex"},
                {"device": "a01q", "product": "a01qser"},
                {"device": "a11q", "product": "a11qnsser"},
                {"device": "a03s", "product": "a03snnser"},
                {"device": "gtowifi", "product": "gtowifiser"},
                {"device": "gta7litewifi", "product": "gta7litewifiser"},
                {"device": "m01q", "product": "m01qser"},
                {"device": "gta4l", "product": "gta4lxx"},
                {"device": "crownlte", "product": "crownlteser"},
                {"device": "r5q", "product": "r5qnaxx"},
                {"device": "gta3xl", "product": "gta3xlxx"},
                {"device": "o1s", "product": "o1sxser"},
            ],
            "display_density": "mdpi",
            "os"             : 10,
        }
    ]


    @staticmethod
    def openudid() -> str:
        return binascii.hexlify(random.randbytes(8)).decode()
    
    @staticmethod
    def uuid() -> str:
        return str(uuid.uuid4())
    
    @staticmethod
    def install_time() -> int:
        return int(round(time.time() * 1000)) - random.randint(13999, 15555)
    
    @staticmethod
    def ut() -> str:

        return random.randint(100, 500)
    
    @staticmethod
    def uid() -> int:
        return random.randrange(10000, 10550, 50)

    @staticmethod
    def ts() -> int:
        return round(random.uniform(1.2, 1.6) * 100000000) * -1

    @staticmethod
    def cba() -> str:
        return f"0x{random.randbytes(4).hex()}"
    
    @staticmethod
    def hc() -> str:
        return f"0016777{random.randint(260, 500)}"
    
    @staticmethod
    def dp() -> str:
        return f"{random.randint(700000000, 900000000)},0,0"
    
    @staticmethod
    def rom() -> int:
        return str(random.randint(700000000, 799999999))

    @staticmethod
    def setup_timezone(country_code: str) -> dict:
        timezone_name = random.choice(pytz.country_timezones[country_code])
        timezone      = round(int(datetime.now(pytz.timezone(timezone_name)).utcoffset().seconds/ 3600))
        offset        = round(datetime.now(pytz.timezone(timezone_name)).utcoffset().total_seconds())
        return {
            "timezone_name" : timezone_name,
            "timezone"      : timezone,
            "offset"        : offset,
        }

    @staticmethod
    def setup_locale(country_code: str) -> str:
        try:
            search_country = [
                country for country in Device().locales if country_code in country.keys()
            ]
            return search_country[0][country_code]
        except Exception as e:
            raise ValueError(e)

    @staticmethod
    def set_gmt(timezone: int) -> str:
        if 0 < timezone < 10:
            result = "GMT+0{}:00".format(str(timezone))
        if 0 > timezone > -10:
            result = "GMT-0{}:00".format(str(timezone))
        if 0 < timezone and timezone >= 10:
            result = "GMT+{}:00".format(str(timezone))
        if timezone < 0 and timezone <= -10:
            result = "GMT+{}:00".format(str(timezone))
        return result

    @staticmethod
    def detect_api_level(os_version: float) -> int:
        if os_version == 7.0:
            return 24
        if os_version == 8.0:
            return 26
        if os_version == 9.0:
            return 28
        if os_version == 10.0:
            return 29
        if os_version == 11.0:
            return 30

    @staticmethod
    def security_path() -> str:
        paths = []
        for i in range(2):
            random_bytes = os.urandom(16)
            encoded_path = base64.urlsafe_b64encode(random_bytes).decode()
            paths.append(encoded_path)
        return f"/data/app/~~{paths[0]}/com.zhiliaoapp.musically-{paths[1]}/base.apk"

    def create_device(self, country_code: str = "us"):
        simple_device   = random.choice(Device().devices)

        timezone_params = self.setup_timezone(country_code)
        locales_params  = self.setup_locale(country_code)
        gmt             = self.set_gmt(timezone_params["timezone"])

        build           = random.choice(simple_device["build"])
        rom             = random.choice(simple_device["rom"])
        core            = random.choice(simple_device["core"])
        model           = random.choice(simple_device["model"])
        product_info    = random.choice(simple_device["device"])
        board           = random.choice(simple_device["board"])

        device_i = product_info["device"]
        product  = product_info["product"]

        device = {
            "device_brand"    : simple_device["brand"],
            "device_model"    : model,
            "google_aid"      : self.uuid(),
            "cdid"            : self.uuid(),
            "clientudid"      : self.uuid(),
            "req_id"          : self.uuid(),
            "build"           : build,
            "rom"             : rom,
            "rom_version"     : build + "." + rom,
            "resolution"      : simple_device["resolution"],
            "timezone_name"   : timezone_params["timezone_name"],
            "timezone"        : timezone_params["timezone"],
            "offset"          : timezone_params["offset"],
            "locale"          : locales_params,
            "os"              : simple_device["os"],
            "os_api"          : self.detect_api_level(simple_device["os"]),
            "openudid"        : self.openudid(),
            "display_density" : simple_device["display_density"],
            "dpi"             : simple_device["dpi"],
            "device"          : device_i,
            "product"         : product,
            "install_time"    : int(round(time.time() * 1000)) - random.randint(5000, 30000),
            "region"          : country_code.upper(),
            "language"        : "en" if country_code == "us" else country_code,
            "app_language"    : "en" if country_code == "us" else country_code,
            "op_region"       : country_code.upper(),
            "sys_region"      : country_code.upper(),
            "core"            : core,
            "board"           : board,
            "gmt"             : gmt,
            "ut"              : random.randint(100, 500),
            "cba"             : hex(random.randint(1000000000, 5900000000)),
            "ts"              : random.randint(-1414524480, -1014524480),
            "uid"             : random.randrange(10000, 10550, 50),
            "dp"              : random.randint(100000000, 999999999),
            "hc"              : f"0016{random.randint(500000, 999999)}",
            "bas"             : random.randint(10, 100),
            "bat"             : random.randrange(3500, 4900, 500),
            "path"            : self.security_path(),
            "dbg"             : random.randint(-100, 0),
            "token_cache"     : base64.urlsafe_b64encode(os.urandom(108)).decode().replace("=", "_"),
        }
        return device


class Applog:
    def __init__(self, device: dict):
        self.device = device
        self.host = "log-va.tiktokv.com"

    def headers(self, params: str, payload: (str or bool) = None) -> dict:
        sig = Xgorgon().calculate(params, payload, None)

        headers = {
            "x-ss-stub"            : str(hashlib.md5(str(payload).encode()).hexdigest()).upper(),
            "accept-encoding"      : "gzip",
            "passport-sdk-version" : "10",
            "sdk-version"          : "2",
            "x-ss-req-ticket"      : str(int(time.time())) + "000",
            "x-tt-dm-status"       : "login=0;ct=0",
            "host"                 : self.host,
            "connection"           : "Keep-Alive",
            "content-type"         : "application/octet-stream",
            "user-agent"           : f"com.zhiliaoapp.musically/{application['version_code']} (Linux; U; Android {self.device['os']}; pt_BR; {self.device['device_model']}; Build/{self.device['build']}; Cronet/TTNetVersion:5f9640e3 2021-04-21 QuicVersion:47946d2a 2020-10-14)",
            "X-Gorgon"             : sig["X-Gorgon"],
            "X-Khronos"            : str(sig["X-Khronos"]),
        }

        return headers

    def params(self) -> str:
        base_params = {
            "ac"                    : "wifi",
            "channel"               : "googleplay",
            "aid"                   : application["aid"],
            "app_name"              : "musical_ly",
            "version_code"          : application["version_code"],
            "version_name"          : application["version_name"],
            "device_platform"       : "android",
            "ab_version"            : application["ab_version"],
            "ssmix"                 : "a",
            "device_type"           : self.device["device_model"],
            "device_brand"          : self.device["device_brand"],
            "language"              : self.device["language"],
            "os_api"                : self.device["os_api"],
            "os_version"            : self.device["os"],
            "openudid"              : self.device["openudid"],
            "manifest_version_code" : application["manifest_version_code"],
            "resolution"            : str(self.device["resolution"]).split("x")[1] + "*" + str(self.device["resolution"]).split("x")[0],
            "dpi"                   : self.device["dpi"],
            "update_version_code"   : application["update_version_code"],
            "_rticket"              : round(time.time() * 1000),
            "app_type"              : "normal", 
            "sys_region"            : self.device["sys_region"],
            "timezone_name"         : self.device["timezone_name"],
            "app_language"          : self.device["app_language"],
            "ac2"                   : "wifi",
            "uoo"                   : "0",
            "op_region"             : self.device["op_region"],
            "timezone_offset"       : self.device["offset"],
            "build_number"          : application["build_number"],
            "locale"                : self.device["locale"],
            "region"                : self.device["region"],
            "ts"                    : int(time.time()),
            "cdid"                  : self.device["cdid"],
            "cpu_support64"         : "true",
            "host_abi"              : "armeabi-v7a",
        }

        return urllib.parse.urlencode(base_params)

    def payload(self):

        payload = {
            "magic_tag": "ss_app_log",
            "header": {
                "display_name"          : "TikTok",
                "update_version_code"   : application["update_version_code"],
                "manifest_version_code" : application["manifest_version_code"],
                "app_version_minor"     : "",
                "aid"                   : application["aid"],
                "channel"               : "googleplay",
                "package"               : "com.zhiliaoapp.musically",
                "app_version"           : application["app_version"],
                "version_code"          : application["version_code"],
                "sdk_version"           : "2.12.1-rc.17",
                "sdk_target_version"    : 29,
                "git_hash"              : application["git_hash"],
                "os"                    : "Android",
                "os_version"            : str(self.device["os"]),
                "os_api"                : self.device["os_api"],
                "device_model"          : self.device["device_model"],
                "device_brand"          : self.device["device_brand"],
                "device_manufacturer"   : self.device["device_brand"],
                "cpu_abi"               : "armeabi-v7a",
                "release_build"         : application["release_build"],
                "density_dpi"           : self.device["dpi"],
                "display_density"       : self.device["display_density"],
                "resolution"            : self.device["resolution"],
                "language"              : self.device["language"],
                "timezone"              : self.device["timezone"],
                "access"                : "wifi",
                "not_request_sender"    : 0,
                "rom"                   : self.device["rom"],
                "rom_version"           : self.device["rom_version"],
                "cdid"                  : self.device["cdid"],
                "sig_hash"              : application["sig_hash"],
                "gaid_limited"          : 0,
                "google_aid"            : self.device["google_aid"],
                "openudid"              : self.device["openudid"],
                "clientudid"            : self.device["clientudid"],
                "region"                : self.device["region"],
                "tz_name"               : f"{self.device['timezone_name'].split('/')[0]}\/{self.device['timezone_name'].split('/')[1]}",
                "tz_offset"             : self.device["offset"],
                "req_id"                : self.device["req_id"],
                "custom": {
                    "is_kids_mode" : 0,
                    "filter_warn"  : 0,
                    "web_ua"       : f"Dalvik\/2.1.0 (Linux; U; Android {self.device['os']}; {self.device['device_model']} Build\/{self.device['build']})",
                    "user_period"  : 0,
                    "user_mode"    : -1,
                },
                "apk_first_install_time" : self.device["install_time"],
                "is_system_app"          : 0,
                "sdk_flavor"             : "global",
            },
            "_gen_time": round(time.time() * 1000),
        }
        return payload

    @staticmethod
    def tt_encryption(data: dict) -> str:
        ttencrypt = TTEncrypt()
        data_formated = json.dumps(data).replace(" ", "")
        return ttencrypt.encrypt(data_formated)

    def register_device(self, proxy):
        params = self.params()

        try:
            r = requests.post(
                url     = f"https://{self.host}/service/2/device_register/?",
                params  = params,
                headers = self.headers(params),
                data    = bytes.fromhex(self.tt_encryption(self.payload())),
                proxies = {
                    "http"  : proxy,
                    "https" : proxy
                }
            )
            
            if r.json()["device_id"] == 0 or r.json()["device_id"] == "0":
                self.register_device(proxy)
            return r.json()["device_id"], r.json()["install_id"]
        except requests.exceptions.ProxyError:
            Output.error("Invalid Proxy, retrying")
            return self.register_device(proxy)
        except requests.exceptions.SSLError:
            Output.error("Invalid Proxy, retrying")
            return self.register_device(proxy)



class Xlog:
    def __init__(self, device_id):
        self.device_id = device_id

    def bypass(self, proxy):
        params = urllib.parse.urlencode(
            {
                "os": "0",
                "ver": "0.6.11.29.19-MT",
                "m": "2",
                "app_ver": "10.1.10",
                "region": "en_US",
                "aid": "1233",
                "did": self.device_id,
            }
        )
        sig = Xgorgon().calculate(params, None, None)

        try:
            requests.get(
                url = "https://xlog-va.tiktokv.com/v2/s/?", 
                params = params,
                headers = {
                    "accept-encoding": "gzip",
                    "cookie": "sessionid=",
                    "x-ss-req-ticket": str("".join(str(time.time()).split(".")))[:13],
                    "x-tt-dm-status": "login=0;ct=0",
                    "X-Gorgon": sig["X-Gorgon"],
                    "X-Khronos": str(sig["X-Khronos"]),
                    "host": "xlog-va.tiktokv.com",
                    "connection": "Keep-Alive",
                    "user-agent": "okhttp/3.10.0.1",
                },
                proxies = {
                    "http": proxy,
                    "https": proxy
                }
            )
        except requests.exceptions.ProxyError:
            Output.error("Invalid Proxy, retrying")
            self.bypass(proxy)
        except requests.exceptions.SSLError:
            Output.error("Invalid Proxy, retrying")
            self.bypass(proxy)
