from email.mime import audio
import pyshark
import time
import threading
import metrics
import matplotlib.pyplot as plt
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, send
from metrics import BandWidth, Loss, Jitter , VideoLoss , InterArrivalJitterAudio, DelayAudio


app = Flask(__name__)
CORS(app)

bw = BandWidth()
loss = Loss()
videoLoss = VideoLoss()
audioJitter = InterArrivalJitterAudio()
audioDelay = DelayAudio()
jitter = Jitter(48000, 90000)
p_type = {"audio" : 108 , "video" : 122}
count = 0
ssrc = {"audio" : "" , "video" : ""}
type = "audio"
capture_start_time = 0.0

def getSsrc(capture):
    global ssrc
    global p_type
    print(ssrc)
    for pkt in capture.sniff_continuously():
        if hasattr(pkt , "rtp") and hasattr(pkt.rtp , "p_type") and int(pkt.rtp.p_type) == p_type["audio"] and hasattr(pkt.rtp , "ssrc"):
          ssrc["audio"] = pkt.rtp.ssrc
          print(pkt.rtp.ssrc)
          break

def capture_live_packets(network_interface):
    capture = pyshark.LiveCapture(interface=network_interface, bpf_filter="udp and (port 3479 or port 3480)", decode_as={
                                  'udp.port==3479': 'rtp', 'udp.port==3480': 'rtp'})
    global ssrc
    global capture_start_time
    getSsrc(capture)
    for pkt in capture.sniff_continuously():
        if float(pkt.frame_info.time_epoch) - capture_start_time >= 1:
            bw.updateCounters()
            loss.updateCounters()
            videoLoss.updateCounters()
            audioJitter.updateCounters()
            audioDelay.updateCounters()
            capture_start_time = float(pkt.frame_info.time_epoch)
        loss.calcLoss(pkt , ssrc["audio"])
        bw.calculateBW(pkt , ssrc["audio"])
        videoLoss.calcLoss(pkt,  ssrc["audio"])
        jitter.calculateJitter(pkt)
        audioJitter.calculateJitter(pkt , ssrc["audio"])
        audioDelay.calculateJitter(pkt , ssrc["audio"])

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
    global type
    obj = {}
    if type == "audio":
        obj["loss"] = loss.audio
        obj["bw"] = bw.audio
        obj["jitter"] = jitter.audio
        obj["newJitter"] = audioJitter.jitter
        obj["pktRate"] = loss.pktRate
        obj["delay"] = audioDelay.delay
    elif type == "video":
        obj["loss"] = videoLoss.loss
        obj["bw"] = bw.video
        obj["jitter"] = jitter.video
        obj["newJitter"] = audioJitter.jitter
        obj["pktRate"] = videoLoss.pktRate
        obj["delay"] = audioDelay.delay
    obj["count"] = count
    count += 1
    print(obj)
    if loss.missed["audio"] != 0:
        print("LOSS :", loss.missed["audio"])
    return obj, 200
# def helloWorld():
#     global count
#     obj = {}
#     obj["loss"] = loss.video
#     obj["bw"] = bw.video
#     obj["jitter"] = jitter.video
#     obj["count"] = count
#     count += 1
#     print(obj)
#     if loss.missed["video"] != 0:
#         print("LOSS :", loss.missed["video"])
#     return obj, 200


if __name__ == '__main__':
    capture = threading.Thread(
        target=capture_live_packets, args=("Ethernet",), daemon=True)
    capture.start()
    # calculate = threading.Thread(target=runCapture, daemon=True)
    # calculate.start()
    app.run()
