import os, socketserver, threading
from .. drivers.return_codes import RETURN_CODES
from . network import CMDTYPE, DEFAULT_PORT
from .. util import log, deprecated

INTERFACE = '0.0.0.0'


class Handler(socketserver.BaseRequestHandler):
    BRIGHTNESS_RETRIES = 2

    def handle(self):
        try:
            cmd, size_low, size_high = (ord(i) for i in self.request.recv(3))
            size = size_low * 256 + size_high

            if cmd == CMDTYPE.PIXEL_DATA:
                code = self._pixel_data(size)
            elif cmd == CMDTYPE.BRIGHTNESS:
                code = self._brightness()
            else:
                log.exception('Unimplemented command', cmd)
                code = RETURN_CODES.ERROR_UNSUPPORTED

        except Exception as e:
            log.exception(e)
            code = RETURN_CODES.ERROR

        self.request.sendall(bytes([code]))

    def _pixel_data(self, size):
        data, code = self.get_data(size)
        if not data:
            return code

        self.server.update(data)

        if self.server.hasFrame:
            while self.server.hasFrame():
                pass

        return RETURN_CODES.SUCCESS

    def _brightness(self):
        bright = ord(self.request.recv(1))
        if not self.server.set_brightness:
            log.exception('Unsupported brightness requested')
            return RETURN_CODES.ERROR_UNSUPPORTED

        for i in range(self.BRIGHTNESS_RETRIES):
            if self.server.set_brightness(bright):
                return RETURN_CODES.SUCCESS

        log.exception('Server failed to set brightness')
        return RETURN_CODES.ERROR

    def get_data(self, size):
        """
        Return (data, return_code) requested from a socket.

        `data` will be None if there is an error, i.e. code is not SUCCESS.
        It is an error if the request does not return the exact data size
        requested.
        """
        data = bytearray()
        empty_count = 0
        while len(data) < size:
            buf = self.request.recv(4096)
            if buf:
                data.extend(buf)
                continue

            empty_count += 1
            if empty_count >= 5:
                log.exception(NOT_ENOUGH_DATA_ERROR, size, len(data))
                return None, RETURN_CODES.ERROR_SIZE

        if len(data) > size:
            log.exception(TOO_MUCH_DATA_SIZE_ERROR, size, len(data))
            return None, RETURN_CODES.ERROR_SIZE

        return data, RETURN_CODES.SUCCESS


class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    update = None
    set_brightness = None
    hasFrame = None


class Receiver:
    def __init__(self, layout, port=DEFAULT_PORT, interface=INTERFACE):
        self.layout = layout
        self.address = (interface, port)
        socketserver.TCPServer.allow_reuse_address = True
        self._server = Server(self.address, Handler)
        self._server.update = self.update
        self._server.set_brightness = self.layout.set_brightness

    def start(self, join=False):
        self._t = threading.Thread(target=self._server.serve_forever)
        self._t.setDaemon(True)
        self._t.start()
        log.info('Listening on %s', self.address)
        if join:
            self._t.join()

    def stop(self):
        log.info('Closing server...')
        self._server.shutdown()
        self._server.server_close()
        # self._t.join()

    def update(self, data):
        self.layout.color_list = data
        self.layout.push_to_driver()


NOT_ENOUGH_DATA_ERROR = """\
Failed to receive expected amount of data! \
Expected: %s bytes / Received: %s bytes"""

TOO_MUCH_DATA_SIZE_ERROR = """\
Too much data received! \
Expected: %s bytes / Received: %s bytes"""


if deprecated.allowed():
    ThreadedDataHandler = Handler
    ThreadedDataServer = Server
    NetworkReceiver = Receiver
    SocketServer = socketserver
