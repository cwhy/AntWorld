import pygtk
import gtk
from land import land

class antWorld:
    def callback(self, widget, data):
        print "Hello antWorld"
        
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False
     
        
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("antWorld DEV")
        self.window.connect("delete_event", self.delete_event)
        self.window.set_border_width(10)
        self.box1 = gtk.HBox(False, 0)
        self.button1 = gtk.Button("Go!")
        self.button1.connect("clicked", self.callback, "button 1")
        self.button1.connect_object("clicked", gtk.Widget.destroy, self.window)
        #Configuration finished, start putting items       
        self.window.add(self.box1)
        self.box1.pack_start(self.button1, True, True, 0)
        self.button1.show()
        self.box1.show()
        self.window.show()
    
    def main(self):
        gtk.main()
    
    def showland(self,land):
        vbox = gtk.VBox()
        drawing_area = gtk.DrawingArea()
        drawing_area.set_size_request(land.width, land.length)
        vbox.pack_start(drawing_area)
        
        
        drawable = drawing_area.window
        drawing_area.show()
        antWorld.pack_start(drawing_area)
        gtk.main()


if __name__ == "__main__":
    hello = antWorld()
    antland = land(200)
    hello.showland(antland)