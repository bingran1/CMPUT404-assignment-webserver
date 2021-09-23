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
        # receive the data
        self.data = self.request.recv(1024).strip()
        # decode the data to string 
        decode_data = self.data.decode('utf-8')
        # check if the request is empty, then return directly
        if(len(decode_data)==0):
            return
        #print ("Got a request of: %s\n" % decode_data)

        # using split method to cut the data string
        # if the first element is 'GET', then return True
        # next, form the file path by using the first elemnt in 
        # the splited data plus './www'
        is_get_method = 'GET' in decode_data.split()[0] 
        path = './www' + decode_data.split()[1]  
        # True iff path file exist
        path_exist = os.path.exists(path) 

        # set two flags for checking the status of 
        # sending 301 or 404
        send_301 = False
        send_404 = False

        # If the path exist and the path does not 
        # end with '.css' and '.html', then checking
        # if the path end with '/'. If it is, plus
        # 'index.html' at the end, if not, set 301 flag
        # to True and path plus '/index.html'
        if path_exist and (not path.endswith('.css')) and (not path.endswith('.html')):
            if path.endswith('/'):
                path += 'index.html'
            else:
                send_301 = True
                path += '/index.html'
        
        # if something like '../' in path, set 404 flag to True
        if '../' in path:
            send_404 = True

        # function for getting content type
        # if the path ends with '.html', the type 
        # should be text/html. If the path ends with
        # '.css', the type should be text/css. Else 
        # should be text/plain. Return at the end 
        def get_type(path):
            if path.endswith('.html'):
                content_type = 'Content-Type:text/html'
            elif (path.endswith('.css')):
                content_type = 'Content-Type:text/css'
            else:
                content_type = 'Content-Type:text/plain'
            return content_type
        
        # function for reading file
        def read_file(path):
            f = open(path, 'r')
            read = f.read()
            self.request.sendall(bytearray(read,'utf-8'))
            f.close()

        # if the method is 'GET'
        if is_get_method:
            # if the path exists and this situation
            # does not belong to 404 case
            if path_exist and (not send_404):
                # check 301 situation
                if send_301:
                    self.request.sendall(bytearray('HTTP/1.1 301 Move Permanently\r\n' + path + '/' + '\r\n', 'utf-8'))
                # if not 301 case, then it should send 200 status code
                self.request.sendall(bytearray('HTTP/1.1 200 OK\r\n', 'utf-8'))
                content_type = get_type(path)
                self.request.sendall(bytearray(content_type + '\r\n' + '\r\n\r\n', 'utf-8'))
                read_file(path)
            else:
                self.request.sendall(bytearray('HTTP/1.1 404 Not Found\r\n', 'utf-8'))
        # other situations should belong 405 case
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

