import re

for session_id in open("./output/accounts.txt").read().splitlines():
    session = re.search(r"(\w{32})", session_id)
    if session:
        open("./sessions.txt", "a").write(f"{session.group(0)}\n")
        print(session.group(0))