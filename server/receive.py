# -*- coding:utf8 -*-
# @TIME     : 2021/12/21 21:25
# @Author   : Hao Su
# @File     : receive.py


from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from time import ctime
import numpy as np
import cv2


def decodeimg(data_Bytes):
    print(data_Bytes)
    buf = np.frombuffer(data_Bytes, dtype="uint8")
    img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    print(img.shape)
    cv2.imwrite("1.jpg", img)


    with open("2.jpg", 'wb') as f:
        f.write(buf)
        f.close()


clients = []
class Spreader(Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.data_Bytes = b""
        self.L = 0
        self.size = 0
        self.seg = 65536


    def connectionMade(self):
        self.factory.numProtocols += 1
        self.transport.write(
            (u"Welcome the %d st user!\n" %
            (self.factory.numProtocols,)).encode("utf-8")
        )
        print("[%s] Welcome the %d st user" % (ctime(), self.factory.numProtocols))
        clients.append(self)


    def connectionLost(self, reason):
        self.factory.numProtocols -= 1
        clients.remove(self)
        print("lost connect: %d" % self.factory.numProtocols)


    def dataReceived(self, data_Bytes: bytes):
        if data_Bytes[0] == "p".encode("utf-8")[0]:
            pre_data = data_Bytes[1:20]
            index = pre_data.find("p".encode("utf-8")[0])
            L = data_Bytes[1:index].decode("utf-8")
            self.data_Bytes = b""
            self.L = int(L)
            print("[%s] begin receive image" % ctime())
            print(self.L)
            self.data_Bytes += data_Bytes[1+index+1:]
            self.size += len(data_Bytes[1+index+1:])
            print(self.size)
            if self.size == self.L:
                self.L = 0
                self.size = 0
                decodeimg(self.data_Bytes)
                self.data_Bytes = b""
        else:
            if self.size <= self.L:
                self.data_Bytes += data_Bytes
                self.size += len(data_Bytes)
            else:
                self.L = 0
                self.size = 0
                decodeimg(self.data_Bytes)
                self.data_Bytes = b""


class SpreadFactory(Factory):
    def __init__(self):
        self.numProtocols = 0

    def buildProtocol(self, addr):
        return Spreader(self)


if __name__ == "__main__":
    from twisted.internet.endpoints import TCP4ServerEndpoint
    from twisted.internet import reactor



    port = 8007
    factory = SpreadFactory()
    endpoint = TCP4ServerEndpoint(reactor, port)
    endpoint.listen(factory)
    reactor.run()

