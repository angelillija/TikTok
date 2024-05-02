from solver import TikTokCaptchaSolver

# Replace with an actual device_id and install_id
print(
    TikTokCaptchaSolver(
        device_id=1234567891012345678, install_id=1234567891012345678
    ).solve_captcha()
)

# Expected Output:
# {'code': 200, 'data': None, 'message': 'Verification complete', 'msg_code': '200', 'msg_sub_code': 'success'}
