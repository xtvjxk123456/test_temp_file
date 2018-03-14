# coding:utf-8
try:
    import SocketServer as ss
except ImportError:
    import socketserver as ss
import threading
import socket
import json
import struct

ADDRESS, PORT = "localhost", 10010
HeaderSize = 4
HeaderFormat = '!i'


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
        lock = threading.Lock()
        lock.acquire()
        while True:
            data = self.request.recv(1024)
            if data:
                # -------------------------------------------------------
                # 把数据存入缓冲区，类似于push数据
                self.server.data_buffer += data
                while True:
                    if len(self.server.data_buffer) < HeaderSize:
                        print(u"数据包（%s Byte）小于消息头部长度，跳出小循环" % len(self.server.data_buffer))
                        break

                    # 读取包头
                    # struct中:!代表Network order，2I代表2个unsigned int数据
                    headPack = struct.unpack(HeaderFormat, self.server.data_buffer[:HeaderSize])
                    currentDataPackage_bodySize = headPack[0]

                    # 分包情况处理，跳出函数继续接收数据
                    if len(self.server.data_buffer) < HeaderSize + currentDataPackage_bodySize:
                        print(u"数据包（%s Byte）不完整（总共%s Byte）,跳出小循环" % (
                            len(self.server.data_buffer), HeaderSize + currentDataPackage_bodySize))
                        break
                        # 读取消息正文的内容
                    body = self.server.data_buffer[
                           HeaderSize:HeaderSize + currentDataPackage_bodySize]

                    # 数据处理
                    try:
                        self.unpack_data(headPack, body)
                    finally:
                        # 粘包情况的处理
                        # 获取下一个数据包，把当前处理的相关数据pop出
                        self.server.data_buffer = self.server.data_buffer[HeaderSize + currentDataPackage_bodySize:]
                        lock.release()
                        return
                        # -------------------------------------------------------

    def unpack_data(self, header, body):
        # header在这一步以前已经被unpack了
        body_raw = json.loads(body.decode())
        self.process_data(header, body_raw)

    def process_data(self, header, body):
        pass


class ProcessServer(ss.ThreadingMixIn, ss.TCPServer):
    def __init__(self, (HOST, PORT), requestHandle):
        ss.TCPServer.__init__(self, (HOST, PORT), requestHandle)
        self.data_buffer = bytes()


class ResponseServer(object):
    def __init__(self):
        self._socketServer = None
        self._thread = None
        self.status = False
        self._socketServerHandler = None

    def instanll_process_block(self, block):
        if block and issubclass(block, ProcessBlock):
            self._socketServerHandler = block
            print('register success.')

    def start(self):
        if not self.status and self._socketServerHandler:
            # 未运行
            self._socketServer = ProcessServer((ADDRESS, PORT), self._socketServerHandler)
            self._thread = threading.Thread(target=self._socketServer.serve_forever)
            self._thread.daemon = True
            self._thread.start()
            self.status = True
        else:
            raise Exception('Can not start server.')

    def shut_Down(self):
        if self.status:
            self._socketServer.shutdown()
            self._socketServer.server_close()
            self._thread = None
            self.status = False
        else:
            print('server already die.')
