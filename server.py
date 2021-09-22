#  coding: utf-8 
import socketserver
import os.path
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        decode_data = self.data.decode('utf-8')
        # print ("Got a request of: %s\n" % self.data)
        # self.request.sendall(bytearray("OK",'utf-8'))

        is_get_method = 'GET' in decode_data.split()[0] # True iff is GET methord
        path = './www' + self.data.split()[1]  # file path

        send_301 = False
        if (not path.endswith('.css')) and (not path.endswith('.html')):
            if path.endswith('/'):
                path += 'index.html'
            else:
                send_301 = True
                path += '/index.html'
        path_exist = os.path.exists(path) # True iff path file exist
        #print('Methor is GET: ' + str(is_get_methord) + ' , path is: ' + path + ', file exist status: ' + str(path_exist))

        # begin here
        if is_get_method:
            if send_301:
                self.request.sendall(bytearray('HTTP/1.1 301 Move Permanently\r\n' + path + '\r\n', 'utf-8'))
            if path_exist:
                self.request.sendall(bytearray('HTTP/1.1 200 OK\r\n', 'utf-8'))
                f = open(path, 'r')
                read = f.read()
                self.request.sendall(bytearray(read, 'utf-8'))
            else:
                self.request.sendall(bytearray('HTTP/1.1 404 Not Found\r\n', 'utf-8'))

        else:
            self.request.sendall(bytearray('HTTP/1.1 405 Method Not Allowed\r\n', 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

