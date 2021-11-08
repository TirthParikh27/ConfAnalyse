import pyshark
import time
import threading
import metrics
import matplotlib.pyplot as plt
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, send
from metrics import BandWidth,Loss,Jitter
# global missed
# missed = 0
# global count 
# count = 0
# global seqNumber
# seqNumber = 0
# global gap
# gap = 1
app = Flask(__name__)
CORS(app)
# socketIo = SocketIO(app, cors_allowed_origins="*")
# app.debug = True

def capture_live_packets(network_interface):
    capture = pyshark.LiveCapture(interface=network_interface , bpf_filter="udp port 3479", decode_as={'udp.port==3479':'rtp'})
    for pkt in capture.sniff_continuously():
      if hasattr(pkt , "rtp"):
        if hasattr(pkt.rtp ,"seq"):
          print(pkt.rtp.seq)
          metrics.count += 1
          if metrics.seqNumber != 0:
            metrics.gap = int(pkt.rtp.seq) - metrics.seqNumber
          if metrics.gap > 1:
            metrics.missed += metrics.gap-1
          else : 
            metrics.seqNumber = int(pkt.rtp.seq)
          metrics.seqNumber = int(pkt.rtp.seq)

def runCapture():
  start = time.process_time()
  loss = 0
  while True:
    if time.process_time() - start >= 1:
      start = time.process_time()
      if metrics.count != 0:
        loss = round((metrics.missed/(metrics.count+metrics.missed)),4) * 100
      print("Count : " , metrics.count)
      print("MISSED : " , metrics.missed)
      print("Loss : " , loss)

@app.route("/api/metrics" , methods=["GET"])
def helloWorld():
  obj = {}
  obj["count"] = metrics.count
  obj["seq"] = metrics.seqNumber
  return obj , 200

# @socketIo.on("message")
# def handleMessage(msg):
#   obj = {}
#   obj["count"] = metrics.count
#   obj["seq"] = metrics.seqNumber
#   send(obj, broadcast=True)
#   return None


if __name__ == '__main__':
  capture = threading.Thread(target=capture_live_packets , args=("WiFi",) , daemon=True)
  capture.start()
  calculate = threading.Thread(target=runCapture , daemon=True)
  calculate.start()
  app.run()
  # socketIo.run(app)
    # capture_live_packets("WiFi")
    # sniff = threading.Thread(target=runCapture , daemon=True)
    # sniff.start()
  