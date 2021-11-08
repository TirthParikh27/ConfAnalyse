import pyshark
import time
import threading
import metrics
import matplotlib.pyplot as plt
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, send
from metrics import BandWidth, Loss, Jitter


app = Flask(__name__)
CORS(app)

bw = BandWidth()
loss = Loss()
jitter = Jitter(48000, 90000)
count = 0


def capture_live_packets(network_interface):
    capture = pyshark.LiveCapture(interface=network_interface, bpf_filter="udp and (port 3479 or port 3480)", decode_as={
                                  'udp.port==3479': 'rtp', 'udp.port==3480': 'rtp'})
    for pkt in capture.sniff_continuously():
        loss.calcLoss(pkt)
        bw.calculateBW(pkt)
        jitter.calculateJitter(pkt)

# def runCapture():
#   start = time.process_time()
#   loss = 0
#   while True:
#     if time.process_time() - start >= 1:
#       start = time.process_time()
#       if metrics.count != 0:
#         loss = round((metrics.missed/(metrics.count+metrics.missed)),4) * 100
#       print("Count : " , metrics.count)
#       print("MISSED : " , metrics.missed)
#       print("Loss : " , loss)


@app.route("/api/metrics", methods=["GET"])
def helloWorld():
    global count
    obj = {}
    obj["loss"] = loss.audio
    obj["bw"] = bw.video
    obj["jitter"] = jitter.audio
    obj["count"] = count
    count += 1
    print(obj)
    if loss.missed["audio"] != 0:
        print("LOSS :", loss.missed["audio"])
    return obj, 200


if __name__ == '__main__':
    capture = threading.Thread(
        target=capture_live_packets, args=("WiFi",), daemon=True)
    capture.start()
    # calculate = threading.Thread(target=runCapture, daemon=True)
    # calculate.start()
    app.run()
