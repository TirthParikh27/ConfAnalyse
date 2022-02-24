missed = 0
count = 0
seqNumber = 0
gap = 1
metrics = {"video": {"loss": 0, "jitter": 0, "bw": 0, "delay": 0},
           "audio": {"loss": 0, "jitter": 0, "bw": 0, "delay": 0 }}


class Loss:
    def __init__(self):
        self.audio = 0
        self.video = 0
        self.count = {"audio": 0, "video": 0}
        self.seqNumber = {"audio": 0, "video": 0}
        self.gap = 0
        self.missed = {"audio":  0, "video": 0}
        self.timePassed = {"audio" : 0 , "video" : 0}

    def updateCounters(self):
        # AUDIO
        self.missed["audio"] = 0
        self.count["audio"] = 1
        self.audio = 0
        # VIDEO
        self.missed["video"] = 0
        self.count["video"] = 1
        self.video = 0

    def calcLoss(self, pkt , audio_ssrc):
        if hasattr(pkt, "rtp"):
            if hasattr(pkt.rtp, "seq"):
                # print(pkt.rtp.seq)
                hasattr(pkt.rtp , "ssrc") and pkt.rtp.ssrc == audio_ssrc:
                    self.count["audio"] += 1
                    if self.seqNumber["audio"] != 0:
                        self.gap = int(pkt.rtp.seq) - self.seqNumber["audio"]
                    if self.gap > 1:
                        self.missed["audio"] += self.gap-1

                    self.seqNumber["audio"] = int(pkt.rtp.seq)
                    self.audio = round(
                        (self.missed["audio"]/(self.count["audio"]+self.missed["audio"])), 4) * 100
                
                elif int(pkt.udp.srcport) == 3480 and hasattr(pkt.rtp , "ssrc") and pkt.rtp.ssrc != audio_ssrc:
                   
                    self.count["video"] += 1
                    if self.seqNumber["video"] != 0:
                        self.gap = int(pkt.rtp.seq) - self.seqNumber["video"]
                    if self.gap > 1:
                        self.missed["video"] += self.gap-1
                    else:
                        self.seqNumber["video"] = int(pkt.rtp.seq)
                    self.seqNumber["video"] = int(pkt.rtp.seq)
                    self.video = round(
                        (self.missed["video"]/(self.count["video"]+self.missed["video"])), 4) * 100

class Jitter:
    def __init__(self, audioClock, videoClock):
        self.audio = 0
        self.video = 0
        self.start_sec = {"audio" : 0 , "video" : 0}
        self.rtp_t1 = {"audio": 0, "video": 0}
        self.unix_diff = 0
        self.rtp_diff = 0
        self.diff = 0
        self.count = {"audio": 0, "video": 0}
        self.clock = {"audio": 48000, "video": 90000}
        self.ssrc = {"audio": "", "video": ""}
        self.rtp_time_unit = {"audio": 1 /
                              self.clock["audio"], "video": 1/self.clock["video"]}
        self.countTemp = 0
    def calculateJitter(self, pkt):
        if hasattr(pkt, "rtp") and hasattr(pkt.rtp, "timestamp"):
            if int(pkt.udp.srcport) == 3479:
              if self.count["audio"] == 0:
                  self.ssrc["audio"] = pkt.rtp.ssrc
                  self.rtp_t1["audio"] = int(pkt.rtp.timestamp)
                  self.start_sec["audio"] = float(pkt.frame_info.time_epoch)
              else:
                  if pkt.rtp.ssrc == self.ssrc["audio"]:
                      self.unix_diff = float(pkt.frame_info.time_epoch) - self.start_sec["audio"]
                      self.start_sec["audio"] = float(pkt.frame_info.time_epoch)
                      self.rtp_diff = (
                          int(pkt.rtp.timestamp) - self.rtp_t1["audio"])*self.rtp_time_unit["audio"]
                      #print(int(pkt.rtp.timestamp) - rtp_t1)
                      self.rtp_t1["audio"] = int(pkt.rtp.timestamp)
                      self.diff = self.unix_diff - self.rtp_diff
                      self.audio = self.audio + \
                          ((abs(self.diff)-self.audio)/16)
                      self.countTemp += 1
                      # print(self.unix_diff)
              self.count["audio"] += 1
            elif int(pkt.udp.srcport) == 3480:
              if self.count["video"] == 0:
                  self.ssrc["video"] = pkt.rtp.ssrc
                  self.rtp_t1["video"] = int(pkt.rtp.timestamp)
                  self.start_sec["video"] = float(pkt.frame_info.time_epoch)
              else:
                  if pkt.rtp.ssrc == self.ssrc["video"]:
                      self.unix_diff = float(pkt.frame_info.time_epoch) - self.start_sec["video"]
                      self.start_sec["video"] = float(pkt.frame_info.time_epoch)
                      self.rtp_diff = (
                          int(pkt.rtp.timestamp) - self.rtp_t1["video"])*self.rtp_time_unit["video"]
                      #print(int(pkt.rtp.timestamp) - rtp_t1)
                      self.rtp_t1["video"] = int(pkt.rtp.timestamp)
                      self.diff = self.unix_diff - self.rtp_diff
                      self.video = self.video + \
                          ((abs(self.diff)-self.video)/16)
                      # print(self.video)
              self.count["video"] += 1

class BandWidth:
  def __init__(self):
    self.audio = 0
    self.video = 0
    self.seconds = {"audio" : [0] , "video" : [0]}
    self.start_sec = {"audio" : 0 , "video" : 0}
    self.sec_count = {"audio" : 0 , "video" : 0}
    self.count = {"audio" : 0 , "video" : 0}
    self.data = {"audio" : 0 , "video" : 0}

  def updateCounters(self):
      #AUDIO
    self.sec_count["audio"] += 1
    self.seconds["audio"].append(self.sec_count["audio"])
    self.audio = round(self.data["audio"]/125,2)
    print(self.audio)
    self.data["audio"] = 0
    # VIDEO
    self.sec_count["video"] += 1
    self.seconds["video"].append(self.sec_count["video"])
    self.video = round(self.data["video"]/125,2)
    self.data["video"] = 0

  def calculateBW(self , pkt , audio_ssrc):
    if hasattr(pkt, "rtp"):

      if int(pkt.udp.srcport) == 3479 or (hasattr(pkt.rtp , "ssrc") and pkt.rtp.ssrc == audio_ssrc):
        self.data["audio"] += float(pkt.frame_info.len)
        self.count["audio"] += 1
      elif int(pkt.udp.srcport) == 3480 and hasattr(pkt.rtp , "ssrc") and pkt.rtp.ssrc != audio_ssrc:
        self.data["video"] += float(pkt.frame_info.len)
        self.count["video"] += 1

