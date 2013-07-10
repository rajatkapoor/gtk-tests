from SimpleCV import *

from multiprocessing import *

class worker(Process):
    def __init__(self, q):
        Process.__init__(self)
        self.queue = q

    def run(self):
        import gtk
        import gobject
        self.gtk = gtk
        self.gobject = gobject
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)
        self.image = gtk.Image()
        self.window.add(self.image)
        self.window.show_all()

        gtk.main()
        gobject.timeout_add(100, self.update)
        
    def update(self):

        try:
            self.data = self.queue.get_nowait()
            imgdata = data.toString()
            pix =  self.gtk.gdk.pixbuf_new_from_data(imgdata, self.gtk.gdk.COLORSPACE_RGB, False, data.depth, data.width, data.height, data.width*3)
            self.image.set_from_pixbuf(pix)
        except Empty:
            pass # nothing at this time


    def destroy(self,widget,data=None):
        self.gtk.main_quit()


class disp():
    
    def __init__(self):
        self.q = Queue()
        self.w = worker(self.q)
        self.w.start()

    def showimg(self,img):
        self.q.put(img)

