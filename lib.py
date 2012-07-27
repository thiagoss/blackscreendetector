
class Detector(object):
    def __init__(self, rtmp_uri):
        self.rtmp_uri = rtmp_uri

    def start(self, callback):
        '''
        when it starts, Detector should start a
        connect-check-disconnect cycle on RTMP
        stream looking for black screens.
        '''
        self.callback = callback
        self.connect_and_check_for_blackscreen()

    def connect_and_check_for_blackscreen(self):
        pass
