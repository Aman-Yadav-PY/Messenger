import socket
import sys

class client:
	HEADERSIZE = 10

	def __init__(self, IP, PORT, label):
		self.IP = IP
		self.PORT = PORT
		self.label = label

	def connector(self, username):
		self.myusername = username#input('Username : ')
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client_socket.connect((self.IP, self.PORT))
		self.client_socket.setblocking(True)
		user = bytes(f"{len(self.myusername):<{self.HEADERSIZE}}"+self.myusername, 'utf-8')

		self.client_socket.send(user)

	def reciever(self):
		header = self.client_socket.recv(self.HEADERSIZE)

		if header == False:
			return 'Connect to the server'
	
		user_length = int(header.decode('utf-8').strip())
		self.username = self.client_socket.recv(user_length).decode('utf-8')

		msgheader = self.client_socket.recv(self.HEADERSIZE)
		msglength = int(msgheader.decode('utf-8').strip())
		msg_recv = self.client_socket.recv(msglength).decode('utf-8')

		return msg_recv


	def info_exchanger(self, message):
		while True:
			content = message#input(f"{self.myusername} : ")

			if content:
				msg = bytes(f"{len(content):<{self.HEADERSIZE}}"+content, 'utf-8')
				self.client_socket.send(msg)

			elif len(content) == 0:
				content == False

			while True:
				header = self.client_socket.recv(self.HEADERSIZE)

				if header == False:
					self.label.config(text = 'Connection Closed')# print("[Connection Closed]")
					sys.exit()

			
				user_length = int(header.decode('utf-8').strip())
				self.username = self.client_socket.recv(user_length).decode('utf-8')

				msgheader = self.client_socket.recv(self.HEADERSIZE)
				msglength = int(msgheader.decode('utf-8').strip())
				msg_recv = self.client_socket.recv(msglength).decode('utf-8')

				return msg_recv
				print(f"[{self.username}] : {msg_recv}")
				break

if __name__ == '__main__':
	activator = client('127.0.0.1', 5050)
	activator.connector()
	activator.info_exchanger()
