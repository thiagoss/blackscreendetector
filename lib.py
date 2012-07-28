import sys
sys.path.insert(0, "/Library/Frameworks/GStreamer.framework/Versions/0.10/x86_64/lib/python2.7/site-packages/gst-0.10")
sys.path.insert(0, "/Library/Frameworks/GStreamer.framework/Versions/0.10/x86_64/lib/python2.7/site-packages")
import lib
import glib, gobject
import gst

THRESHOLD = 0.07 #brigthness less than 0.07 implies black screen

class Detector(object):
    def __init__(self, rtmp_uri, callback):
        self.rtmp_uri = rtmp_uri
        self.external_callback = callback

        self.create_pipeline()
        self.get_bus_and_link_callback()

    def start(self):
        '''
        when it starts, Detector should start a
        connect-check-disconnect cycle on RTMP
        stream looking for black screens.
        '''
        self.connect_and_check_for_blackscreen()

    def create_pipeline(self): #need tests
        self.pipeline = gst.parse_launch("uridecodebin uri=%s !"
                                         "videoanalyse name='analyse' !"
                                         "ffmpegcolorspace !"
                                         "autovideosink" % self.rtmp_uri)

    def get_bus_and_link_callback(self): #need tests
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message", self.internal_callback)

    def internal_callback(self, bus, message): #need tests
        if self.is_blackscreen(message):
            self.external_callback()

        elif message.type == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "Error: %s" % err, debug

    def connect_and_check_for_blackscreen(self):
        self.pipeline.set_state(gst.STATE_PLAYING)

    def is_blackscreen(self, message):
        if message.type == gst.MESSAGE_ELEMENT and \
            message.structure.get_name() == "GstVideoAnalyse" and \
            message.structure["brightness"] < THRESHOLD:

            return True

        return False

