"""
Receive UDP broadcast messages.
"""

import queue, socket
from .. threads import runnable
from .. import log


class Receiver(runnable.Loop):
    """
    Receive UDP broadcast messages in a thread
    """

    def __init__(self, address, bufsize=0x1000, receive=None, **kwds):
        super().__init__(**kwds)
        self.address = address
        self.bufsize = bufsize
        self.receive = receive or self.receive
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.address)

    def __str__(self):
        return 'udp.Receiver(%s, %s)' % (self.address[0], hex(self.address[1]))

    def loop_once(self):
        try:
            data, addr = self.socket.recvfrom(self.bufsize)
        except OSError as e:
            if e.errno != 9:
                raise
            if self.running:
                log.error('Someone else closed the socket')
                super().stop()
            return

        if data:
            self.receive(data)

    def stop(self):
        super().stop()
        try:
            self.socket.close()
        except Exception as e:
            log.error('Exception in socket.close: %s', e)


class QueuedReceiver(Receiver):
    """
    Receive UDP broadcast messages in a thread and put them on a queue.
    """

    def __init__(self, *args, **kwds):
        self.queue = queue.Queue()
        super().__init__(*args, **kwds)

    def receive(self, msg):
        self.queue.put(msg)
