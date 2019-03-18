import socket
import time

HOST = '127.0.0.1'
PORT = 9999

class Server():
    handlers = { "GET": {}, "POST": {} }

    def parseHTTP(self, newReception):
        return newReception.split('\r\n')
    
    def findHandlerForPath(self, requestParsed):
        method = requestParsed[0].split(' ')[0]
        path = requestParsed[0].split(' ')[1]
        if path == '/favicon.ico':
            return None
        return self.handlers[method][path]

    def get(self, path, handler_func):
        self.handlers["GET"][path] = handler_func
        return

    def post(self, path, handler_func):
        self.handlers["POST"][path] = handler_func
        return

    def make_response(self, body):
        return 'HTTP/1.1 200 OK\r\nContent-Length: {}\r\n\r\n{}'.format(len(body), body)
    
    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            prevResponse = ''
            print('here1')
            
            while True:
                conn, addr = s.accept()
                print('here2')
                                        
                with conn:
                    newReception = conn.recv(1024).decode('utf-8')
                    print('newReception:', newReception)
                    requestParsed = self.parseHTTP(newReception)
                    handler = self.findHandlerForPath(requestParsed)
                    if handler == None:
                        response = prevResponse
                    else:
                        response = handler(self, None)
                        prevResponse = response
                    conn.sendall(response.encode('utf-8'))
                print('here3')
                
def handle_bar(server, req):
    return server.make_response("My name is bar")

def handle_login(server, req):
    return server.make_response("heyo bossman you're now logged in")

server = Server()
server.get("/foo", lambda server, req: server.make_response("Hello world!"))
server.get("/bar", handle_bar)
server.post("/login", handle_login)
server.start()
