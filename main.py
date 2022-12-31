from utils.api import *

class Account:
    def __init__(self) -> None:
        self.registered = 0
        self.errors     = 0
        self.total      = 0


        self.proxies = open("./data/proxies.txt", "r").read().splitlines()

        self.session = requests.Session()
        self.proxy   = "http://" + random.choice(self.proxies)
        self.session.proxies.update({"http": self.proxy, "https": self.proxy})

        print("Fully made by ai | https://aithe.dev\n")

        self.accounts_to_register = int(input("Number of accounts to register: "))
        self.threads              = int(input("Threads: "))

    def base_params(self) -> dict:
        return urllib.parse.urlencode(
            {
                "account_sdk_version"   : 355,
                "app_language"          : "en", 
                "manifest_version_code" : 2019030429, 
                "_rticket"              : int(time.time() * 1000), 
                "iid"                   : self.device[1], 
                "channel"               : "googleplay", 
                "language"              : "en", 
                "device_type"           : "CPH2235", 
                "resolution"            : "1080*2153", 
                "openudid"              : binascii.hexlify(os.urandom(8)).decode(), 
                "update_version_code"   : 2019030429, 
                "sys_region"            : "EG", 
                "os_api"                : 31, 
                "is_my_cn"              : 0, 
                "timezone_name"         : "Africa/Cairo", 
                "dpi"                   : 480, 
                "carrier_region"        : "EG", 
                "ac"                    : "wifi", 
                "device_id"             : self.device[0], 
                "pass-route"            : 1, 
                "mcc_mnc"               : 60203, 
                "timezone_offset"       : 7200, 
                "os_version"            : 12, 
                "version_code"          : 100110, 
                "carrier_region_v2"     : 602, 
                "app_name"              : "musical_ly", 
                "ab_version"            : "10.1.10", 
                "version_name"          : "10.1.10", 
                "device_brand"          : "OPPO", 
                "ssmix"                 : "a", 
                "pass-region"           : 1, 
                "build_number"          : "10.1.10", 
                "device_platform"       : "android", 
                "region"                : "US", 
                "aid"                   : 1233, 
                "ts"                    : int(time.time()), 
                "as"                    : "a1qwert123", 
                "cp"                    : "cbfhckdckkde1", 
                "mas"                   : "01232325227f9453bfd5d49d706e97a1952c2c4c2ca66c0c2ccca6"
            }
        )
    

    def base_data(self, update: dict = {}) -> dict:
        base_data = {
            "app_language"          : "en",
            "manifest_version_code" : 2019030429,
            "_rticket"              : int(time.time() * 1000),
            "iid"                   : self.device[1],
            "channel"               : "googleplay",
            "language"              : "en", 
            "device_type"           : "CPH2235", 
            "type"                  : "34", 
            "resolution"            : "1080*2153", 
            "openudid"              : binascii.hexlify(os.urandom(8)).decode(), 
            "update_version_code"   : 2019030429, 
            "sys_region"            : "EG", 
            "os_api"                : 31, 
            "is_my_cn"              : 0, 
            "timezone_name"         : "Africa/Cairo", 
            "dpi"                   : 480, 
            "retry_type"            : "no_retry", 
            "carrier_region"        : "EG", 
            "ac"                    : "wifi", 
            "device_id"             : self.device[0], 
            "pass-route"            : 1, 
            "mcc_mnc"               : 60202, 
            "mix_mode"              : 1, 
            "timezone_offset"       : 7200, 
            "os_version"            : 12, 
            "version_code"          : 100110, 
            "carrier_region_v2"     : 602, 
            "app_name"              : "musical_ly", 
            "ab_version"            : "10.1.10", 
            "account_sdk_source"    : "app", 
            "version_name"          : "10.1.10", 
            "device_brand"          : "OPPO", 
            "ssmix"                 : "a", 
            "pass-region"           : 1, 
            "build_number"          : "10.1.10", 
            "device_platform"       : "android", 
            "region"                : "US", 
            "aid"                   : 1233
        }

        base_data.update(update)
        return urllib.parse.urlencode(base_data)

    def base_headers(self) -> dict:
        return {
            "Host"            : "api2.musical.ly",
            "Connection"      : "close",
            "Accept-Encoding" : "gzip, deflate",
            "sdk-version"     : "1",
            "Content-Length"  : str(len(self.base_data())),
            "Content-Type"    : "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent"      : "com.zhiliaoapp.musically/2019030429 (Linux; U; Android 12; en_EG; CPH2235; Build/SKQ1.210216.001; Cronet/58.0.2991.0)"
        }

    def generate_device(self) -> None:
        device: dict          = Device().create_device()
        device_id, install_id = Applog(device).register_device(self.proxy)
        Xlog(device_id).bypass(self.proxy)

        return device_id, install_id

    def send_code(
        self,
        email: str    = None,
        password: str = None
    ) -> None:
    
        response = self.session.post(
            url     = "https://api2.musical.ly/passport/email/send_code/",
            params  = self.base_params(),
            data    = self.base_data({"password": Utils().xor(password), "email": Utils().xor(email)}), 
            headers = self.base_headers()
        
        )
        if not response.json()["message"] == "success":
            print(response.json())

    def verify_code(
        self,
        code: int     = None,
        email: str    = None,
        password: str = None
    ) -> None:

        response = self.session.post(
            url     = "https://api2.musical.ly/passport/email/register_verify_login/",
            params  = self.base_params(), 
            data    = self.base_data({"password": Utils().xor(password), "email": Utils().xor(email), "code": code}), 
            headers = self.base_headers()
        )
        if response.text.__contains__("session_key"):
            self.registered += 1

            session_id = response.json()["data"]["session_key"]
            
            open("./output/accounts.txt", "a").write(f"{self.device[0]}:{self.device[1]}:{email}:{password}:{self.session_id}\n")
            print(f"[ {self.registered} ] Registered Account | [Email: {email} Password: {password} Session ID: {session_id}]")
        else:
            print(response.json())


    def register(self) -> None:
        for _ in range(self.accounts_to_register):
            self.device = self.generate_device()
            email       = Email().create_email()
            password    = "".join(random.choices(string.ascii_lowercase, k = 9)) + "".join(random.choices(string.digits, k = 4))
            self.send_code(email, password)
            
            while True:
                messages = Email().get_mail(email)
                if messages:
                    break

            code = messages[0]["Subject"][:6]
            self.verify_code(code, email, password)        
            self.edit_profile()

    def start(self) -> None:
        for _ in range(self.threads):
            threading.Thread(target = self.register).start()


if __name__ == "__main__":
    Account().start()