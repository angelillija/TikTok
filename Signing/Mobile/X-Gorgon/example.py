from signature import Signature

signer = signature(params="", data="", cookies="").get_value()

print(f"X-Gorgon: {signer['X-Gorgon']} X-Khronos: {signer['X-Khronos']}")
