#coding=utf-8
import gtk,datetime

class MainWindow():
	def __append_talk_history(self,message):
		talk_history = self.builder.get_object("talk_history")
		text_buffer = talk_history.get_buffer()
		formated_msg = "%s  %s\n" % (datetime.datetime.today().strftime("%c"), message)
		print formated_msg
		text_buffer.insert(text_buffer.get_end_iter(),formated_msg)

	def on_MainForm_destroy(self,widget):
		gtk.main_quit()

	def on_connect_btn_clicked(self,widget):
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
		self.__append_talk_history(msg)

	def __init__(self):
		#read glade file
		self.builder = gtk.Builder()
		self.builder.add_from_file("rad_gui.glade")
		#get the main window, and connect all eventes
		self.window = self.builder.get_object("MainForm")
		if self.window:
			self.builder.connect_signals(self)
			self.window.show()

if __name__ == '__main__':
	main_window = MainWindow()
	gtk.main()
