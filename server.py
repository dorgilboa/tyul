import threading, socket, app

IP = '127.0.0.1'
PORT = 5050
clients_threads = []



class Server(threading.Thread):
    def __init__(self):
        self.serversock = socket.socket()
        self.serversock.bind((IP,PORT))
        self.serversock.listen()
        print("listening for clients on Port: " + str(PORT) + " IP: " + IP)

    def get_client(self):
        global clients_threads
        while True:
            try:
                self.clientsock, self.clientadd = self.serversock.accept()
                print("client connected")
                map_load_thrd = MapLoadThread(self.clientsock, self.randnum)
                map_load_thrd.start()
                clients_threads.append([self.clientsock, map_load_thrd, ""])
            except:
                pass

class MapLoadThread():
    def __init__(self, client, randnum):
      self.client = client
      threading.Thread.__init__(self)

    def run(self):
        global clients_threads
        lock = threading.Condition()
        login = True

        while True:
            try:
                if login:
                    # code communication with client and db
                    login = False
                else:
                    data_request = self.client.recv(1024).decode() #GET request from client
                    lock.acquire()
                    tracks = [app.get_tracks()]
                    self.client.send(tracks)
                    ### client data recv and send ###
                    lock.notify()
                    lock.release()
            except ConnectionResetError:
                print(f'{self.client.getpeername()} disconnected.\n')
                for i in range(len(clients_threads)):
                    if self.client == clients_threads[i - 1][0]:
                        del clients_threads[i - 1]
                self.client.close()
                break


def main():
    s = Server()
    s.get_client()


if __name__ == '__main__':
    main()

# import socketio

# server_sock = socketio.Server()
# app = socketio.WSGIApp(server_sock)

# @server_sock.event
# def connect(sid, environ): gets session-id for every connection and environment.
#   print(sid, ' connected')

# @server_sock.event
# def disconnect(sid):
#   print(sid, ' disconnected')


# from aiohttp import web
# import socketio

# serverSock = socketio.AsyncServer()
# app = web.Application()
# serverSock.attach(app)

# async def index(request):
#   return web.Response(text= "hello world", content_type= "text/html")

# @serverSock.on('message')
# async def print_message(sid, message):
#     ## When we receive a new event of type
#     ## 'message' through a socket.io connection
#     ## we print the socket ID and the message
#     print("Socket ID: " , sid)
#     print(message)


# app.router.add_get('/', index)

# if __name__ == '__main__':
#   web.run_app(app)
