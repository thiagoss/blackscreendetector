import lib

def test_detector_should_call_callback_if_blackscreen_appears(monkeypatch):
    monkeypatch.setattr(lib.Detector, 'connect_and_check_for_blackscreen',
                                       fake_connect_and_check_for_blackscreen)
    was_called = []
    def callback():
        was_called.append(True)

    detector = lib.Detector("rtmp://blackscreen/app/ins/stream", callback)
    detector.start()

    assert was_called

def test_detector_should_not_call_callback_if_no_blackscreen_appears():
    was_called = []
    def callback():
        was_called.append(True)

    detector = lib.Detector("rtmp://novela/app/ins/stream", callback)
    detector.start()

    assert not was_called

def fake_connect_and_check_for_blackscreen(self, *args):
    if 'blackscreen' in self.rtmp_uri:
        self.external_callback()
