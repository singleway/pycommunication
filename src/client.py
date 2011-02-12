#coding=utf-8

import threading,socket,ssl,select

class client(threading.Thread):

	def __init__(self,recv_msg_callback,ssl_sock = None,server_address = ('127.0.0.1',51000)): #client will keep ssl_sock
		threading.Thread.__init__(self)
		if ssl_sock is None : #this is a client. In this case, if create client successfully, ssl-tunnel is setuped
			raw_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			raw_sock.connect(server_address)
			self.ssl_sock = ssl.wrap_socket(raw_sock,ssl_version=ssl.PROTOCOL_TLSv1)
		else:
			self.ssl_sock = ssl_sock
		self.recv_msg_callback = recv_msg_callback

	def __del__(self):
		self.ssl_sock.shutdown(socket.SHUT_RDWR)
		self.ssl_sock.close()

	def send_message(self,message):
		pass #TODO define the format for message

	def run(self):
		while True:
			pass #TODO add procedure that used for receive message

