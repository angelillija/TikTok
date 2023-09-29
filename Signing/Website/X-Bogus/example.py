from bogus import Signer

url = ""
user_agent = ""

x_bogus = sign(url.split("?")[1], user_agent)

print(f"{url.split("?")[0]}?{x_bogus}")