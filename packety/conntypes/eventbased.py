from packety.server import BaseConnection


class EventBasedConnection(BaseConnection):
    def __init__(self, sock):
        super().__init__(sock)
        self.startup_event = None
        self.kill_event = None
        self.extra_args = {}
        self.packet_events = {}

    def on_start(self):
        if self.startup_event is not None:
            self.startup_event(self, **self.extra_args)

    def on_close(self):
        if self.kill_event is not None:
            self.kill_event(self, **self.extra_args)

    def run(self):
        while True:
            pack = self.incoming.get()
            if pack.__class__ in self.packet_events:
                self.packet_events[pack.__class__](self, pack, **self.extra_args)

    def on(self, event, handler):
        if event == "open":
            self.startup_event = handler
        elif event == "close":
            self.kill_event = handler
        else:
            self.packet_events[event] = handler
