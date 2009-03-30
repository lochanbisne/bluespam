import os, sys
import datetime, lightblue

from models import *

import settings

def serial_filename(fn):
    return fn

class Receiver:

    def log(self, message, prefix = ""):
        print "[recv %s] %s" % (datetime.now(), message)
    

    def receive(self):

        self.log("Dump your data...")

        s = lightblue.socket()
        s.bind(("", 0))
        lightblue.advertise("My OBEX Service", s, lightblue.OBEX)

        try:
            while True:
    
                (addr, fname) = lightblue.obex.recvfile(s, "tmp.dat")

                if fname is not None:
                    fullname = serial_filename(settings.MEDIA_ROOT + "incoming/" + fname)
                    fname = "incoming/" + fullname.split("/")[-1]
                    os.rename("tmp.dat", fullname)

                    # find device
                    try:
                        device = Device.objects.get(device_id = addr);
                    except Device.DoesNotExist:
                        device = Device(device_id = id, name = name)
                        self.log("New device: %s" % device)

                    device.save()

                    recv = DeviceReceived(device = device, filename = fname)
                    recv.recv_time = datetime.now()
                    recv.save()
                    
                    self.log("Got %s from %s" % (fname, device))
                else:
                    self.log("Receive error...")
        except Exception, e:
            print e
            print "Bye..."
            s.close()

