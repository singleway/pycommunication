#coding=utf-8

import threading,socket
import client

class server(threading.Thread):
	def __init__(self,gui_instance,notify_callback,recv_msg_callback):
		threading.Thread.__init__(self)
		#create raw server socket
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.sock.bind(('',51000))
		self.sock.listen(1)
		self.running = True
		self.remote_client_pool = []
		self.gui_instance = gui_instance
		self.notify_callback = notify_callback
		self.recv_msg_callback = recv_msg_callback

	def __del__(self):
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()

	def run(self):
		while(self.running):	#FIXME how to make this flage working
			accepted_sock, address = self.sock.accept() #TODO how to use address? Or, is it useful?
			try:
				new_client = client.client(self.recv_msg_callback,self.gui_instance,accepted_sock)
				new_client.start()
				self.remote_client_pool.append(new_client)
				self.notify_callback(new_client,self.gui_instance)
			except Exception,data:	#May be, the memory has exhausted
				print Exception,":",data
				accepted_sock.shutdown(socket.SHUT_RDWR)
				accepted_sock.close()

	def stop(self):
		self.running = False
		self.join()
