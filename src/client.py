#coding=utf-8

import threading,socket,ssl,struct

class client(threading.Thread):

	MSG_TYPE_HANDSHAKE = 0
	MSG_TYPE_MESSAGE = 1

	def __init__(self,recv_msg_callback,gui_instance,ssl_sock = None,server_address = ('127.0.0.1',51000)): #client will keep ssl_sock
		threading.Thread.__init__(self)
		if ssl_sock is None : #this is a client. In this case, if create client successfully, ssl-tunnel is setuped
			raw_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			raw_sock.connect(server_address)
			self.__ssl_sock = ssl.wrap_socket(raw_sock,ssl_version=ssl.PROTOCOL_TLSv1)
			self.remote_id,self.remote_nickname = (0,"")
		else:
			self.__ssl_sock = ssl_sock
		self.recv_msg_callback = recv_msg_callback
		self.gui_instance = gui_instance

	def __del__(self):
		self.__ssl_sock.shutdown(socket.SHUT_RDWR)
		self.__ssl_sock.close()

	def do_handshake(self,id,nickname):
		#send handshake
		msg_header_length = 4*3+len(self.nickname)
		msg_header_type = client.MSG_TYPE_HANDSHAKE
		msg_bin = struct.pack("!BBBs",msg_header_length,msg_header_type,id,nickname)
		self.__ssl_sock.write(msg_bin)

	def send_message(self,message):
		#send message
		msg_header_length = 4*2+len(message)
		msg_header_type = client.MSG_TYPE_MESSAGE
		msg_bin = struct.pack("!BBs",msg_header_length,msg_header_type,message)
		self.__ssl_sock.write(msg_bin)

	def run(self):
		while True:
			msg_header_bin = self.__ssl_sock.read(struct.calcsize("!BB"))
			msg_header_length, msg_header_type = struct.unpack("!BB", msg_header_bin)
			msg_bin = self.__ssl_sock.read(msg_header_length - struct.calcsize("!BB"))
			if client.MSG_TYPE_HANDSHAKE == msg_header_type:
				self.remote_id,self.remote_nickname = struct.unpack("!Bs", msg_bin)
			elif client.MSG_TYPE_MESSAGE == msg_header_type:
				msg = struct.unpack("!s", msg_bin)
				self.recv_msg_callback(self,msg,self.gui_instance)


