import sys
sys.path.insert(0, "/Library/Frameworks/GStreamer.framework/Versions/0.10/x86_64/lib/python2.7/site-packages")
import lib
import glib, gobject

def callback():
    print "black screen of death."

def start_all():
    gobject.threads_init()
    loop = glib.MainLoop()
    loop.run()

detector = lib.Detector(sys.argv[1], callback)
detector.start()
start_all()

