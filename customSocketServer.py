# coding:utf-8
try:
    import SocketServer as ss
except ImportError:
    import socketserver as ss
import threading
import socket

ADDRESS, PORT = "localhost", 10010


def _port_is_free(port):
    s = socket.socket()
    s.settimeout(0.5)
    try:
        # s.connect_ex return 0 means port is open
        return s.connect_ex(('localhost', port)) != 0
    finally:
        s.close()


class ProcessBlock(ss.BaseRequestHandler):
    def handle(self):
        print('done')


class ResponseServer(object):
    def __init__(self):
        self._socketServer = None
        self._thread = None
        self.status = False
        self._socketServerHandler = None

    def instanll_process_block(self, block):
        if block and issubclass(block, ss.BaseRequestHandler):
            self._socketServerHandler = block

    def start(self):
        if not self.status and self._socketServerHandler:
            # 未运行
            self._socketServer = ss.ThreadingTCPServer((ADDRESS, PORT), self._socketServerHandler)
            self._thread = threading.Thread(target=self._socketServer.serve_forever)
            self._thread.daemon = True
            self._thread.start()
            self.status = True

    def shut_Down(self):
        if self.status:
            self._socketServer.shutdown()
            self._socketServer.server_close()
            self._thread = None
            self.status = False

