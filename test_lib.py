import sys
sys.path.insert(0, "/Library/Frameworks/GStreamer.framework/Versions/0.10/x86_64/lib/python2.7/site-packages/gst-0.10")
sys.path.insert(0, "/Library/Frameworks/GStreamer.framework/Versions/0.10/x86_64/lib/python2.7/site-packages")
import lib
import glib, gobject
import gst

PROBLEMATIC_STREAM = "rtmp://blackscreen/app/ins/stream"
GOOD_STREAM = "rtmp://novela/passando/de/buenas"

def test_detector_should_call_callback_if_blackscreen_appears(monkeypatch):
    monkeypatch.setattr(lib.Detector, 'connect_and_check_for_blackscreen',
                                       fake_connect_and_check_for_blackscreen)
    was_called = []
    def callback():
        was_called.append(True)

    detector = lib.Detector(PROBLEMATIC_STREAM, callback)
    detector.start()

    assert was_called

def test_detector_should_not_call_callback_if_no_blackscreen_appears():
    was_called = []
    def callback():
        was_called.append(True)

    detector = lib.Detector(GOOD_STREAM, callback)
    detector.start()

    assert not was_called

def test_is_blackscreen_should_return_True_for_problematic_streams():
    detector = lib.Detector(PROBLEMATIC_STREAM, lambda: None )

    fake_message = FakeMessage(PROBLEMATIC_STREAM)
    assert True == detector.is_blackscreen(fake_message)

    fake_message = FakeMessage(GOOD_STREAM)
    assert False == detector.is_blackscreen(fake_message)

# HELPERS

class FakeMessage(object):
    def __init__(self, rtmp_uri):
        self.structure = FakeStructure()
        self.type = gst.MESSAGE_ELEMENT
        if "blackscreen" in rtmp_uri:
            self.structure['brightness'] = lib.THRESHOLD-0.1
        else:
            self.structure['brightness'] = lib.THRESHOLD+0.1

class FakeStructure(dict):
    def get_name(self):
        return "GstVideoAnalyse"

def fake_connect_and_check_for_blackscreen(self, *args):
    if 'blackscreen' in self.rtmp_uri:
        self.external_callback()


