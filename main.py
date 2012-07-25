import sys
sys.path.insert(0, "/Library/Frameworks/GStreamer.framework/Versions/0.10/x86_64/lib/python2.7/site-packages/gst-0.10")
sys.path.insert(0, "/Library/Frameworks/GStreamer.framework/Versions/0.10/x86_64/lib/python2.7/site-packages")
import glib, gobject
import gst

def callback(bus, message):
    if message.type == gst.MESSAGE_ELEMENT:
        if message.structure.get_name() == "GstVideoAnalyse":
            print "brightness", message.structure['brightness']
            print "brightness-variance", message.structure['brightness-variance']
    elif message.type == gst.MESSAGE_ERROR:
        print 'ERRO', message
        sys.exit(1)

pipeline = gst.parse_launch("videotestsrc ! ffmpegcolorspace ! queue ! videoanalyse name='analyse' ! ffmpegcolorspace ! autovideosink")
bus = pipeline.get_bus()
bus.add_signal_watch()
bus.connect("message", callback)
pipeline.set_state(gst.STATE_PLAYING)

gobject.threads_init()
loop = glib.MainLoop()
loop.run()

pipeline.set_state(gst.STATE_NULL)


