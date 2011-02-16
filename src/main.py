#coding=utf-8
import gtk,datetime,server,client

def on_new_client_callback(new_client,gui):
	gui.on_new_client(new_client)
def on_recv_msg_callback(client,msg,gui):
	gui.on_recv_msg(client,msg)

class MainWindow():
	def __append_talk_history(self,message):
		talk_history = self.builder.get_object("talk_history")
		text_buffer = talk_history.get_buffer()
		formated_msg = "%s  %s\n" % (datetime.datetime.today().strftime("%c"), message)
		text_buffer.insert(text_buffer.get_end_iter(),formated_msg)
		#scroll window
		scroll_bar = self.builder.get_object("scrolledwindow").get_vscrollbar()
		scroll_adj = scroll_bar.get_adjustment()
		scroll_bar.set_value(scroll_adj.upper - scroll_adj.page_size)

	def on_MainForm_destroy(self,widget):
		gtk.main_quit()

	def on_connect_btn_clicked(self,widget):
		self.client = client.client(on_recv_msg_callback,self)
		self.client.start()
		self.client.do_handshake(0,"nickname") #TODO use the real information
		connect_vbox = self.builder.get_object("connect_vbox")
		connect_vbox.hide()

	def on_text_input_key_press_event(self,widget,event):
		key_name = gtk.gdk.keyval_name(event.keyval)
		if key_name == "KP_Enter" or key_name == "Return":
			self.builder.get_object("send_btn").clicked()
			return True

	def on_send_btn_clicked(self,widget):
		text_input = self.builder.get_object("text_input")
		text_buffer = text_input.get_buffer()
		msg = text_buffer.get_text(text_buffer.get_start_iter(),text_buffer.get_end_iter());
		text_buffer.set_text("")
		self.client.send_message(msg)
		self.__append_talk_history(msg)

	def on_new_client(self,new_client):
		self.client = new_client
		self.__append_talk_history("new client")
		connect_vbox = self.builder.get_object("connect_vbox")
		connect_vbox.hide()
	def on_recv_msg(self,client,msg):
		self.__append_talk_history(msg)

	def on_new_client_callback(new_client,gui):
		gui.on_new_client(new_client)
	def on_recv_msg_callback(client,msg,gui):
		gui.on_recv_msg(client,msg)

	def __init__(self):
		#read glade file
		self.builder = gtk.Builder()
		self.builder.add_from_file("rad_gui.glade")
		#init server
		self.server = server.server(self,on_new_client_callback,on_recv_msg_callback)
		self.server.start()
		#get the main window, and connect all eventes
		self.window = self.builder.get_object("MainForm")
		if self.window:
			self.builder.connect_signals(self)
			self.window.show()

	def __del__(self):
		self.server.stop()

if __name__ == '__main__':
	gtk.gdk.threads_init()
	main_window = MainWindow()
	gtk.gdk.threads_enter()
	gtk.main()
	gtk.gdk.threads_leave()
	del main_window
