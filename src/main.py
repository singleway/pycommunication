#coding=utf-8
import gtk
import gobject
import sys

class MainWindow():
	def on_MainForm_destroy(self,widget):
		gtk.main_quit()

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