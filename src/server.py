#coding=utf-8

import threading,socket,select
import client,upnp,time

class server(threading.Thread):
	DEFAULT_PORT = 51000
	def __init__(self,gui_instance,notify_callback,recv_msg_callback):
		threading.Thread.__init__(self)
		#create raw server socket
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.sock.setblocking(0)
		self.sock.bind(('',server.DEFAULT_PORT))
		self.sock.listen(1)
		#add port-mapping to router
		self.upnp_ins = upnp.UPnP()
		self.upnp_ins.start()
		time.sleep(1)
		self.upnp_ins.add_port(server.DEFAULT_PORT,'TCP',server.DEFAULT_PORT)
		#init class data field
		self.running = True
		self.remote_client_pool = []
		self.gui_instance = gui_instance
		self.notify_callback = notify_callback
		self.recv_msg_callback = recv_msg_callback

	def run(self):
		while self.running:
			sock_read,sock_write,sock_error = select.select([self.sock],[],[],1)
			if len(sock_read) > 0:
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
		self.sock.close()
		self.upnp_ins.del_port(server.DEFAULT_PORT,'TCP')

	def stop(self):
		self.running = False
		self.join()
