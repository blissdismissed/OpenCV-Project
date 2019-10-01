from twilio.rest import Client
import boto3
from threading import Thread

class TwilioNotifier:
    def __init__(self, conf):
        # store the configuration object
        self.conf = conf
        
    def send (self, msg, tempVideo):
        # start a thread to upload the file and send it
        t = Thread(target=self._send, args=(msg, tempVideo,))
        t.start()