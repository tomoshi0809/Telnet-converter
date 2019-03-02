#!/usr/bin/python
#coding: utf-8

import sys
import socketserver

ENCODE_TYPE = "UTF-8"


class TerminalHandler(socketserver.BaseRequestHandler):
    prompt = "$ "

    def execute(self, command):
        if command == "ls":
            self.send_all("bin     etc     proc    usr     dev     home\r\n")
        elif command == "ls -l":
            self.send_all("drwxrwxrwx+ 1 taro staff 0 2 5 12:35 bin\r\n")
            self.send_all("drwxrwxrwx+ 1 taro staff 0 2 5 12:35 etc\r\n")
            self.send_all("drwxrwxrwx+ 1 taro staff 0 2 5 12:35 proc\r\n")

        elif command == "date":
            self.send_all("2019/01/23 15:21:16.48\n")

        else:
            self.send_all("Could not find such a command\n")

    def send_all(self, str):
        self.request.send_all(bytes(str, "UTF-8"))

    def handle(self):
        buff = []
        while True:
            recv_bytes = self.request.recv(1024)

            try:
                recv_str = recv_bytes.decode(ENCODE_TYPE)
                if "\n" in recv_str:
                    last_arg = recv_str.rstrip("\n")
                    cmd = "".join(buff) + last_arg
                    del buff[:]
                    self.execute(cmd)
                else:
                    buff.append(recv_str)

            except UnicodeDecodeError:
                print("UnicodeDecode Error")
                print(recv_bytes)

if __name__ == "__main__":
    HOST, PORT = "localhost", 23
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer((HOST, PORT), TerminalHandler)
    server.serve_forever()
