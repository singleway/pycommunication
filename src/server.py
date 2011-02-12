#coding=utf-8

import threading,socket,ssl
import client

class server(threading.Thread):
	def __init__(self,notify_callback):
		threading.Thread.__init__(self)
		#create raw server socket
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.sock.bind(('',51000))
		self.sock.listen(1)
		self.running = True
		self.remote_client_pool = []
		self.notify_callback = notify_callback

	def __del__(self):
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()

	def run(self):
		while(self.running):	#FIXME how to make this flage working
			accepted_sock, address = self.sock.accept() #TODO how to use address? Or, is it useful?
			ssl_sock = ssl.wrap_socket(accepted_sock,server_side=True,ssl_version=ssl.PROTOCOL_TLSv1)
			try:
				new_client = client.client(ssl_sock)
				self.remote_client_pool.append(new_client)
				self.notify_callback(new_client)
			except:	#May be, the memory has exhausted
				ssl_sock.shutdown(socket.SHUT_RDWR)
				ssl_sock.close()

	def stop(self):
		self.running = False
		self.join()
