# TikTok Captcha Solver

TikTok's puzzle captcha is a mechanism to distinguish humans from bots using a sliding puzzle. This code solves it programmatically, automating the process while maintaining user authenticity.

TikTok binds the captcha to the user's `device_id` & `install_id`.

### Processing Images
This function is responsible for preprocessing the puzzle and piece images. 
It begins by decoding the base64 strings into image data, then converting it to grayscale. 
A Gaussian blur is applied to the grayscale image to reduce noise, and Sobel operators are employed to compute horizontal and vertical gradients. 
These gradients are combined using a weighted average to enhance edges and features in the image.

```py
@staticmethod
def process_image(buffer: BufferedReader):
    nparr = frombuffer(buffer, uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    blurred = cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (3, 3), 0)
    return cv2.addWeighted(
        cv2.convertScaleAbs(cv2.Sobel(blurred, cv2.CV_16S, 1, 0, ksize=3)),
        0.5,
        cv2.convertScaleAbs(cv2.Sobel(blurred, cv2.CV_16S, 0, 1, ksize=3)),
        0.5,
        0,
    )
```

### Solving Captcha
This function initiates by sending a request to `https://rc-verification-i18n.tiktokv.com/captcha/get` to retrieve captcha data, including the URLs for puzzle and piece images. 
These images are then processed through the `process_image` function, which involves decoding the base64 string, converting it into a grayscale image, and applying a weighted gradient to enhance relevant features. 
After preprocessing, a random sliding length is generated for the puzzle solver. Template matching is performed on the puzzle and piece images, identifying the best match and its position. 
Using this position and the sliding length, a response payload is crafted, simulating the sliding action required for the captcha challenge. 
Finally, a POST request is made to `https://rc-verification-i18n.tiktokv.com/captcha/verify` with the generated payload, aiming to verify the captcha challenge. The response from this request is then returned.

```py
def solve_captcha(self) -> dict:
    captcha = self.session.get(
        url=f"{self.base_url}/captcha/get", 
        params=self.params
    ).json()
    puzzle, piece = [
        self.process_image(
            self.session.get(captcha["data"]["question"][f"url{url}"]).content
        )
        for url in [1, 2]
    ]

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
                    "relative_time": (i * randlength),
                    "x": round(max_loc / (randlength / i)),
                    "y": captcha["data"]["question"]["tip_y"],
                }
                for i in range(1, randlength)
            ],
        },
    ).json()
```

## Example Usage

```py
from solver import TikTokCaptchaSolver

# Replace with an actual device_id and install_id
print(TikTokCaptchaSolver(device_id=1234567891012345678, install_id=1234567891012345678).solve_captcha())

# Expected Output:
# {'code': 200, 'data': None, 'message': 'Verification complete', 'msg_code': '200', 'msg_sub_code': 'success'}
```