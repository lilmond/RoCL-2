from bs4 import BeautifulSoup as htmlparser
import requests

def check_token(token: str) -> None:
    http = requests.get("https://www.roblox.com/home", cookies={".ROBLOSECURITY": token})
    html = htmlparser(http.text, features="html.parser")

    user = html.find("meta", {"name": "user-data"})

    if not user:
        print(f"\r\nERROR: invalid token\r\n")
        return

    info = "\r\n" \
    f"Username: {user.get('data-name')}\r\n" \
    f"User ID : {user.get('data-userid')}\r\n" \
    f"Premium : {user.get('data-ispremiumuser')}\r\n" \
    f"Underage: {user.get('data-isunder13')}\r\n" \
    f"Creation: {user.get('data-created')}\r\n"

    print(info)

def main():
    try:
        while True:
            token = input("Token: ").strip()
            check_token(token)
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()
