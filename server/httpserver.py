#coding:utf-8
from flask import request, Flask, make_response, render_template
import json
import numpy as np
import time
import cv2
import base64



def decodeimg(data_Bytes):
    # print(data_Bytes)
    buf = np.frombuffer(data_Bytes, dtype="uint8")
    img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    cv2.imwrite("1.png", img)


app = Flask(__name__)

@app.route("/", methods=['POST'])
def get_frame():
    resp = make_response()
    resp.headers["Connection"] = 'keep-alive'
    # start_time = time.time()
    res = json.loads(request.data)
    decodeimg(eval(res["image"]))
    # duration = time.time() - start_time
    # print('duration:[%.0fms]' % (duration*1000))

    # 横坐标 纵坐标 宽 高 置信度
    loc = np.array([[20, 20, 20, 20, 0.9]],
                   dtype="float16")
    loc = np.array([[0, 0, 20, 20, 0.9],
                    [50, 50, 20, 20, 0.8]],
                   dtype="float16")
    loc_bytes = {"loc": str(loc.tobytes())}
    resp.data = json.dumps(loc_bytes)
    return resp

if __name__ == "__main__":
    app.run("localhost", port=8081)  #端口为8081