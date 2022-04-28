from email.mime import audio
import pyshark
import time
import threading
import yaml
import metrics
import matplotlib.pyplot as plt
from flask import Flask , request
from flask_cors import CORS
from flask_socketio import SocketIO, send
from metrics import BandWidth, Loss, Jitter , VideoLoss , InterArrivalJitterAudio, DelayAudio, ScreenLoss , VideoFps


app = Flask(__name__)
CORS(app)
conferencingApp = ""
config = {}
with open("thresholds.yml" , "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as err:
            print(err)
            config = {"packet_loss" : {conferencingApp : {"audio" : [] , "video" : []}}}

p_type = {"audio" : 108 , "video" : 122}
count = 0
ssrc = {"audio" : "" , "video" : ""}
type = "video"
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
    capture = pyshark.LiveCapture(interface=network_interface, bpf_filter="udp and (port 3479 or port 3480 or port 3481)", decode_as={
                                  'udp.port==3479': 'rtp', 'udp.port==3480': 'rtp' , 'udp.port==3481': 'rtp'})
    global ssrc
    global capture_start_time
    getSsrc(capture)
    for pkt in capture.sniff_continuously():
        if float(pkt.frame_info.time_epoch) - capture_start_time >= 1:
            bw.updateCounters()
            loss.updateCounters()
            videoLoss.updateCounters()
            videoFps.updateCounters()
            screenLoss.updateCounters()
            audioJitter.updateCounters()
            audioDelay.updateCounters()
            capture_start_time = float(pkt.frame_info.time_epoch)
        loss.calcLoss(pkt , ssrc["audio"])
        bw.calculateBW(pkt , ssrc["audio"])
        videoFps.calcFps(pkt , ssrc["audio"])
        videoLoss.calcLoss(pkt,  ssrc["audio"])
        screenLoss.calcLoss(pkt)
        jitter.calculateJitter(pkt)
        audioJitter.calculateJitter(pkt , ssrc["audio"])
        audioDelay.calculateJitter(pkt , ssrc["audio"])


def calcAudioUx(loss , jitter):
    if loss == "":
        return ""
    if loss == "low":
        return "low"
    elif jitter == "low" :
        return "low"
    elif loss == "high" and jitter != "high":
        return jitter
    elif loss == "medium" and jitter == "medium":
        return "medium"
    elif loss == "medium" and jitter == "high":
        return "medium"
    
    return "high"

def calVideoUx(loss , fps , bw):
    if loss == "":
        return ""
    
    if loss == "low" or fps == "low" or bw == "low":
        return "low"
    elif loss == "high":
        if fps == "medium" or bw == "medium":
            return "medium"
    elif loss == "medium":
        return "medium"
    
    return "high"

@app.route("/api/setApp" , methods=["POST"])
def setApplication():
    global conferencingApp , config , bw , loss , videoFps , videoLoss , screenLoss , audioJitter , audioDelay , jitter
    conferencingApp = request.json["application"]
    bw = BandWidth(config["throughput"][conferencingApp]["video"])
    loss = Loss(config["packet_loss"][conferencingApp]["audio"])
    videoFps = VideoFps(config["fps"][conferencingApp]["video"])
    videoLoss = VideoLoss(config["packet_loss"][conferencingApp]["video"])
    screenLoss = ScreenLoss()
    audioJitter = InterArrivalJitterAudio()
    audioDelay = DelayAudio()
    jitter = Jitter(48000, 90000 , config["jitter"][conferencingApp]["audio"])
    capture = threading.Thread(
        target=capture_live_packets, args=("Ethernet",), daemon=True)
    capture.start()
    print("APPLICATION CONFIGURED : " , conferencingApp)
    return {"msg" : "Application configured successfully"} , 200



@app.route("/api/metrics", methods=["GET"])
def helloWorld():
    global count
    global type
    obj = {}
    obj["loss"] = loss.audio
    obj["audioUx"] = calcAudioUx(loss.ux , jitter.ux)
    obj["bw"] = bw.audio
    obj["jitter"] = jitter.audio * 1000
    obj["newJitter"] = audioJitter.jitter
    obj["pktRate"] = loss.pktRate
    obj["delay"] = audioDelay.delay
    obj["videoloss"] = videoLoss.loss
    obj["videoUx"] = calVideoUx(videoLoss.ux , videoFps.ux , bw.ux)
    obj["videofps"] = videoFps.fps
    obj["videobw"] = bw.video
    obj["videojitter"] = jitter.video
    obj["videopktRate"] = videoLoss.pktRate
    obj["screenloss"] = screenLoss.loss
    obj["screenpktRate"] = screenLoss.pktRate
    obj["screenbw"] = bw.screen

    obj["count"] = count
    count += 1
    print(obj)
    return obj, 200


if __name__ == '__main__':
    # calculate = threading.Thread(target=runCapture, daemon=True)
    # calculate.start()
    print("CONFIGURATION : " , config)
    app.run()
