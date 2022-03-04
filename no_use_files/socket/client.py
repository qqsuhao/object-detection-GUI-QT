# -*- coding:utf8 -*-
# @TIME     : 2021/12/22 15:53
# @Author   : Hao Su
# @File     : client.py

from twisted.internet.protocol import Protocol, ReconnectingClientFactory


def encodeimg(img):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 1]
    result, imgencode = cv2.imencode('.jpg', img, encode_param)
    data = np.array(imgencode)
    data_Bytes = data.tobytes()
    buf = np.frombuffer(data_Bytes, dtype="uint8")
    tmp = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    cv2.imwrite("2.jpg", tmp)
    return data_Bytes


class Echo(Protocol):
    def __init__(self):
        self.connected = False

    def connectionMade(self):
        self.connected = True

    def connectionLost(self, reason):
        self.connected = False

    def dataReceived(self, data: bytes):
        print("[%s]" % ctime(), data.decode("utf-8"))


class EchoClientFactory(ReconnectingClientFactory):
    def __init__(self):
        self.protocal = None

    def startedConnecting(self, connector):
        print("[%s] Started to connect." % ctime())

    def buildProtocol(self, addr):
        print("[%s] Connected." % ctime())
        self.resetDelay()
        self.protocol = Echo()
        return self.protocol

    def clientConnectionLost(self, connector, reason):
        print("[%s] Lost connection." % ctime())
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print("[%s] Connection failed." % ctime())
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)


if __name__ == "__main__":
    from twisted.internet import reactor
    import threading
    import fileinput
    import time
    import sys
    import datetime
    from time import ctime
    import numpy as np
    import cv2

    bStop = False
    def routine(factory):
        while not bStop:
            # if factory.protocol and factory.protocol.connected:
            #     factory.protocol.transport.write(
            #         ("This is %s %s" %
            #          (sys.argv[0], datetime.datetime.now())).encode("utf-8")
            #     )
            img = cv2.imread("1.jpg")
            writeimg(factory, encodeimg(img))
            time.sleep(5)


    def writeimg(factory, data_Bytes):
        L = len(data_Bytes)
        print(data_Bytes)

        factory.protocol.transport.write(("p"+str(L)+"p").encode("utf-8"))
        factory.protocol.transport.write(data_Bytes)
        print("[%s] write finish!" % (ctime()))


    host = "127.0.0.1"
    port = 8007
    factory = EchoClientFactory()
    reactor.connectTCP(host, port, factory)
    threading.Thread(target=routine, args=(factory,)).start()
    reactor.run()
    bStop = True



