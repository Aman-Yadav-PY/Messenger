import socket
import select
import json
import os

class server:

	HEADERSIZE = 10

	def __init__(self, IP, PORT):
		self.IP = IP
		self.PORT = PORT

	def connector(self):
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_socket.bind((self.IP, self.PORT))
		self.server_socket.listen()

		self.all_servers = [self.server_socket]
		self.clients = {}

	def reciever(self, client_server):
		header = client_server.recv(self.HEADERSIZE)
		if header:
			msglength = int(header.decode('utf-8').strip())
			return{'header':header, 'message': client_server.recv(msglength)}

		else:
			return False

	def exchanger(self):
		while True:
			rlist, _, xlist = select.select(self.all_servers, self.all_servers, self.all_servers)

		
			for notified_sockets in rlist:
				if notified_sockets == self.server_socket:
					self.connected_socket, self.address = notified_sockets.accept()

					self.username = self.reciever(self.connected_socket)
					
					if self.username == False:
						continue

					self.all_servers.append(self.connected_socket)
					self.clients[self.connected_socket] = self.username

					print(f"{self.username['message'].decode('utf-8')} : Active")

				else:
					msg_recv = self.reciever(notified_sockets)

					if msg_recv != False:
						print(f"{[self.username['message'].decode('utf-8')]} : {msg_recv['message'].decode('utf-8')}")

					else:
						print('No message recieved!')


					for connected_socket in self.clients:
						if connected_socket != notified_sockets:
							if msg_recv != False:
								message = self.username['header']+self.username['message']+msg_recv['header']+msg_recv['message']
								connected_socket.send(message)

							else:
								print(f"{self.username} : Closed")
								break

if __name__ == '__main__':
	activator = server('127.0.0.1', 5050)
	activator.connector()
	activator.exchanger()