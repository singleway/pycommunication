#coding=utf-8

import threading,socket,struct,select
import pyDes

class client(threading.Thread):

	MSG_TYPE_HANDSHAKE = 0
	MSG_TYPE_MESSAGE = 1
	commond_key = pyDes.des("T5Y6W@E#", pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)

	def __init__(self,recv_msg_callback,gui_instance,sock = None,server_address = ('127.0.0.1',51000)): #client will keep ssl_sock
		threading.Thread.__init__(self)
		if sock is None : #this is a client. In this case, if create client successfully, ssl-tunnel is setuped
			self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.sock.connect(server_address)
			self.remote_id,self.remote_nickname = (0,"")
		else:
			self.sock = sock
		self.recv_msg_callback = recv_msg_callback
		self.gui_instance = gui_instance
		self.running = True
		
	def __del__(self):
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()

	def do_handshake(self,id,nickname):
		#send handshake
		msg_header_length = 4*3+len(nickname)
		msg_header_type = client.MSG_TYPE_HANDSHAKE
		msg_bin = struct.pack("!III%ds"%len(nickname),msg_header_length,msg_header_type,id,nickname)
		self.sock.send(msg_bin)

	def send_message(self,message):
		#encode message
		message = client.commond_key.encrypt(message)

		#send message
		msg_header_length = 4*2+len(message)
		msg_header_type = client.MSG_TYPE_MESSAGE
		msg_bin = struct.pack("!II%ds"%len(message),msg_header_length,msg_header_type,message)
		self.sock.send(msg_bin)

	def run(self):
		while self.running:
			sock_read,sock_write,sock_error = select.select([self.sock],[],[],1)
			if sock_read:
				msg_header_bin = self.sock.recv(struct.calcsize("!II"))
				msg_header_length, msg_header_type = struct.unpack("!II", msg_header_bin)
				bin_length = msg_header_length - struct.calcsize("!II")
				msg_bin = self.sock.recv(bin_length)
				if client.MSG_TYPE_HANDSHAKE == msg_header_type:
					s_length = bin_length - 4
					self.remote_id,self.remote_nickname = struct.unpack("!I%ds"%s_length, msg_bin)
				elif client.MSG_TYPE_MESSAGE == msg_header_type:
					msg = struct.unpack("!%ds"%bin_length, msg_bin)[0]
					#decode message
					msg = client.commond_key.decrypt(msg)
					self.recv_msg_callback(self,msg,self.gui_instance)

	def stop(self):
		self.running = False
		self.join()