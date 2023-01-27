#  coding: utf-8 
import socketserver
from pathlib import Path

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
        deco_data = self.data.decode('ascii')
        print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("HTTP/1.1 200 OK\n\n" + open("./www/index.html", 'r').read(),'utf-8'))
        
        x = deco_data.split(' ')
        method, path = x[0], x[1] 

        try:
            
            if method != 'GET':
                self.handle_code_405()
                return

            req_path = Path('www' + path)

            if path.endswith('/'):
                self.request.sendall(bytearray('HTTP/1.1 200 OK\n\n' + (req_path/'index.html').read_text(), 'utf-8'))
                return
            elif path.is_file() or path.is_dir():
                path = Path(path + '/') 
                self.handle_code_301(path)
            
            if path.endswith('.css'):
                self.request.sendall(bytearray('HTTP/1.1 200 OK\n' + 'Content-Type: text/css\n\n' + req_path.read_text(), 'utf-8'))

            if path.endswith('.html'):
                self.request.sendall(bytearray('HTTP/1.1 200 OK\n' + 'Content-Type: text/html\n\n' + req_path.read_text(), 'utf-8'))
                
            else: 
                self.request.sendall(bytearray('HTTP/1.1 200 OK\n\n' + req_path.read_text(), 'utf-8'))
                # self.handle_code_404()
        

        except FileNotFoundError:

            if req_path.is_file():
                self.request.sendall(bytearray('HTTP/1.1 200 OK\n\n' + req_path.read_text(), 'utf-8'))
            else:
                self.handle_code_404()


        except IsADirectoryError:

            if req_path.is_dir():            
                if (req_path/'index.html').is_file():
                    self.request.sendall(bytearray('HTTP/1.1 200 OK\n\n' + (req_path/'index.html').read_text(), 'utf-8'))
                else:
                    self.handle_code_404()      
               
    # req_path.suffix

    def handle_code_301(self, path):
        self.request.sendall(bytearray('HTTP/1.1 301 Moved Permenantly\n Location: ' + path + '/', 'utf-8'))
         
    def handle_code_400(self):
        self.request.sendall('HTTP/1.1 400 Bad Request\n\n'.encode('utf-8'))

    def handle_code_404(self):
        self.request.sendall('HTTP/1.1 404 File Not Found\n\n'.encode('utf-8'))

    def handle_code_405(self):
        self.request.sendall('HTTP/1.1 405 Method Not Allowed\n\n'.encode('utf-8'))
    


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
