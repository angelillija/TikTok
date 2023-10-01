# github.com/angelillija

import requests
import random
import base64
import numpy
import time
import cv2

class TikTokCaptchaSolver:
    def __init__(self, device_id: int, install_id: int):
        self.session = requests.Session()
        self.base_url = "https://rc-verification-i18n.tiktokv.com"
        self.params = {
            "aid": "1233",
            "os_type": "0",
            "type": "verify",
            "subtype": "slide",
            "did": device_id,
            "iid": install_id,
        }

    @staticmethod
    def process_image(string):
        nparr = numpy.frombuffer(base64.b64decode(string), numpy.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        blurred = cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (3, 3), 0)
        return cv2.addWeighted(cv2.convertScaleAbs(cv2.Sobel(blurred, cv2.CV_16S, 1, 0, ksize=3)), 0.5, cv2.convertScaleAbs(cv2.Sobel(blurred, cv2.CV_16S, 0, 1, ksize=3)), 0.5, 0)

    def solve_captcha(self) -> dict:
        captcha = self.session.get(f"{self.base_url}/captcha/get", params=self.params).json()
        puzzle, piece = [self.process_image(base64.b64encode(self.session.get(captcha["data"]["question"][f"url{url}"]).content)) for url in [1, 2]]

        time.sleep(1)

        randlength = round(random.uniform(50, 100))
        max_loc = cv2.minMaxLoc(cv2.matchTemplate(puzzle, piece, cv2.TM_CCOEFF_NORMED))[3][0]

        return self.session.post(
            url=f"{self.base_url}/captcha/verify",
            params=self.params,
            json={
                "modified_img_width": 552,
                "id": captcha["data"]["id"],
                "mode": "slide",
                "reply": [
                    {
                        "relative_time": i * randlength,
                        "x": round(max_loc / (randlength / (i + 1))),
                        "y": captcha["data"]["question"]["tip_y"],
                    }
                    for i in range(randlength)
                ]
            }   
        ).json()