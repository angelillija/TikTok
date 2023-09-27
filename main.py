from utils.signer import Argus, Ladon, Gorgon, md5
from utils.solver import Solver
from urllib.parse import urlencode
import requests, json, string
import time, random, threading, re, secrets


class TikTokAccountCreator:
    def __init__(self) -> None:
        self.registered = 0

        self.proxies = open("./proxies.txt", "r").read().splitlines() 
        self.devices = open("./utils/devices.txt", "r").read().splitlines()
        self.threads = int(input("Threads: "))

    def xor(self, string: str) -> str:
        return "".join([hex(ord(_) ^ 5)[2:] for _ in string])

    def sign(self, params, payload: str = None, sec_device_id: str = "", cookie: str or None = None, aid: int = 1233, license_id: int = 1611921764, sdk_version_str: str = "v04.04.05-ov-android", sdk_version: int = 134744640, platform: int = 0, unix: int = None):
        x_ss_stub = md5(payload.encode('utf-8')).hexdigest() if payload != None else None
        if not unix: unix = int(time.time())
    
        return Gorgon(params, unix, payload, cookie).get_value() | { 
            "x-ladon"   : Ladon.encrypt(unix, license_id, aid),
            "x-argus"   : Argus.get_sign(params, x_ss_stub, unix,
                platform        = platform,
                aid             = aid,
                license_id      = license_id,
                sec_device_id   = sec_device_id,
                sdk_version     = sdk_version_str, 
                sdk_version_int = sdk_version
            )
        }

    def base_params(self) -> str:
        return {
            "passport-sdk-version": "19",
            "iid": self.device["install_id"],
            "device_id": self.device["device_id"],
            "ac": "wifi",
            "channel": "googleplay",
            "aid": "1233",
            "app_name": "musical_ly",
            "version_code": "300904",
            "version_name": "30.9.4",
            "device_platform": "android",
            "os": "android",
            "ab_version": "30.9.4",
            "ssmix": "a",
            "device_type": "ASUS_Z01QD",
            "device_brand": "Asus",
            "language": "en",
            "os_api": "28",
            "os_version": "9",
            "openudid": "704713c0da01388a",
            "manifest_version_code": "2023009040",
            "resolution": "1600*900",
            "dpi": "300",
            "update_version_code": "2023009040",
            "_rticket": "1692845349183",
            "is_pad": "0",
            "current_region": "BE",
            "app_type": "normal",
            "sys_region": "US",
            "mcc_mnc": "20610",
            "timezone_name": "Asia/Shanghai",
            "residence": "BE",
            "app_language": "en",
            "carrier_region": "BE",
            "ac2": "wifi",
            "uoo": "0",
            "op_region": "BE",
            "timezone_offset": "28800",
            "build_number": "30.9.4",
            "host_abi": "arm64-v8a",
            "locale": "en",
            "region": "US",
            "ts": "1692845349",
            "cdid": "60c2140f-c112-491a-8c93-183fd1ea8acf",
            "support_webview": "1",
            "okhttp_version": "4.1.120.34-tiktok",
            "use_store_region_cookie": "1"
        }       
        

    def send_code(
        self,
        email: str    = None,
        password: str = None
    ) -> None:

        data = urlencode({
            "password": self.xor(password),
            "account_sdk_source": "app",
            "rule_strategies": 2,
            "mix_mode": 1,
            "multi_login": 1,
            "type": 34,
            "email": self.xor(email)
        })
        headers = {
            "sdk-version": "2",
            "user-agent": "com.zhiliaoapp.musically/2023009040 (Linux; U; Android 9; en; ASUS_Z01QD; Build/PI;tt-ok/3.12.13.1)",
            "host": "api16-normal-c-useast2a.tiktokv.com",
        }
        headers.update(self.sign(urlencode(self.base_params()), data))
        response = requests.post(
            url = "https://api16-normal-c-useast2a.tiktokv.com/passport/email/send_code/",
            params = self.base_params(),
            data = data,
            headers = headers,
            proxies = {
                "http": f"http://{random.choice(self.proxies)}",
                "https": f"http://{random.choice(self.proxies)}"
            }
        )

        if not response.text.__contains__("success"):
            print(response.content)

    def verify_code(
        self,
        code: int     = None,
        email: str    = None,
        password: str = None
    ) -> None:
        data = f"birthday={random.randint(1980, 2000)}-0{random.randint(1, 9)}-{random.randint(10, 25)}&code={code}&account_sdk_source=app&mix_mode=1&multi_login=1&type=34&email={self.xor(email)}"
        headers = {
            "accept-encoding": "gzip",
            "sdk-version": "2",
            "x-bd-kmsv": "0",
            "multi_login": "1",
            "passport-sdk-version": "19",
            "x-tt-dm-status": "login=1;ct=1;rt=8",
            "x-tt-bypass-dp": "1",
            "x-vc-bdturing-sdk-version": "2.3.2.i18n",
            "user-agent": "com.zhiliaoapp.musically/2023009040 (Linux; U; Android 9; en; ASUS_Z01QD; Build/PI;tt-ok/3.12.13.1)",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "host": "api16-normal-c-useast2a.tiktokv.com",
            "connection": "Keep-Alive"
        }
        headers.update(self.sign(urlencode(self.base_params()), data))
        response = requests.post(
            url = "https://api16-normal-c-useast2a.tiktokv.com/passport/email/register_verify_login/", 
            params = self.base_params(),
            data = data, 
            headers = headers, 
            proxies = {
                "http": f"http://{random.choice(self.proxies)}",
                "https": f"http://{random.choice(self.proxies)}"
            }
        )

        if response.text.__contains__("session_key"):
            session_id = response.json()["data"]["session_key"]
            
            open("./output/accounts.txt", "a+").write(f"{email}:{password}:{session_id}\n")
            print(f"Registered Account | [Email: {email} - Password: {password} - Session ID: {session_id}]")
        else:
            print(response.content)


    def register(self) -> None:
        while True:
            self.device = eval(random.choice(self.devices))
            Solver(self.device["device_id"], self.device["install_id"]).solve_captcha()
            email    = f"{''.join(random.choices(string.ascii_letters.lower() + string.digits, k=10))}@vjuum.com"
            password = ''.join(random.choices(string.ascii_letters + string.ascii_uppercase, k=11)) + "1!"
            self.send_code(email, password)

            while True:
                messages = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={email.split('@')[0]}&domain={email.split('@')[1]}").json()
                if messages:
                    break

            code = ''.join(re.findall(r'\b\d+\b', messages[0]["subject"]))
            self.verify_code(code, email, password)

    def start(self) -> None:
        for _ in range(self.threads):
            threading.Thread(target = self.register).start()


if __name__ == "__main__":
    TikTokAccountCreator().start()