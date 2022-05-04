# -*- coding:utf8 -*-
# @TIME     : 2021/12/17 19:40
# @Author   : Hao Su
# @File     : send.py


from twisted.internet import protocol, reactor


def encodeimg(img_path):
    import cv2
    import numpy as np
    img = cv2.imread(img_path)
    # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    encode_param = [int(cv2.IMWRITE_PNG_COMPRESSION), 9]
    result, imgencode = cv2.imencode('.jpg', img, encode_param)
    data = np.array(imgencode)
    data_Bytes = data.tobytes()
    return data_Bytes


class TSClntProtocol(protocol.Protocol):
    def sendData(self):
        a = input('>')
        data = encodeimg("1.png")
        if data:
            print('...sending %s...' % data)
            self.transport.write(data)
        else:
            self.transport.loseConnection()

    def connectionMade(self):
        self.sendData()

    def dataReceived(self, data):
        print(data)
        self.sendData()


class TSClntFactory(protocol.ClientFactory):
    protocol = TSClntProtocol
    clientConnectionLost = clientConnectionFailed = lambda self, connector, reason: reactor.stop()


HOST = "localhost"
PORT = 21567
reactor.connectTCP(HOST, PORT, TSClntFactory())
reactor.run()