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
        x = self.data.decode('ascii')
        print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("HTTP/1.1 200 OK\n\n" + open("./www/index.html", 'r').read(),'utf-8'))
        
        # Return a status code of “405 Method Not Allowed” for any method you cannot handle (POST/PUT/DELETE)
        if x.split(' ')[0] != 'GET':
           self.request.sendall('HTTP/1.1 405 Method Not Allowed\n\n'.encode('utf-8'))
           return

        auth_path = x.split(' ')[1]
        req_path = Path('www/' + auth_path)

        # The webserver can server 404 errors for paths not found
        if req_path.is_file():
            self.request.sendall(bytearray('HTTP/1.1 200 OK\n\n' + req_path.read_text(), 'utf-8'))

        elif req_path.is_dir(): 

           
            if (req_path/'index.html').is_file():
                self.request.sendall(bytearray('HTTP/1.1 200 OK\n\n' + (req_path/'index.html').read_text() , 'utf-8'))
            else:
                self.request.sendall('HTTP/1.1 404 File Not Found\n\n'.encode('utf-8'))       
        else:
            self.request.sendall('HTTP/1.1 404 File Not Found\n\n'.encode('utf-8'))       

        # req_path.suffix
         




if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()