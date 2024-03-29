import sys, re, random, time, os
from datetime import datetime, timedelta
import django.db.models.base

#
# Choose between btcomm_lightblue and btcomm_cli
#
from btcomm_cli import BTComm
#from btcomm_lightblue import BTComm


from models import *

class SpammerMain:

    # interface we're gonna use
    interface = None

    # sleep time between cycles
    sleeptime = 10

    # the number of minutes we still count a device 'active'.
    active_in_minutes = 1

    # aggressive yes/no
    aggressive = False
    
    def __init__(self, interface, aggressive = False):
        self.interface = interface
        self.aggressive = aggressive
        self.bt = BTComm(self.interface)


    def log(self, message, prefix = ""):
        print "[%s %s] %s" % (datetime.now(), self.interface+prefix, message)


    def trytosend(self, device_id, schedule_id, aggressive = False):

        device = Device.objects.filter(device_id = device_id)[0]
        candidate = Schedule.objects.filter(id = schedule_id)[0]

        obexchannel = device.obexchannel
        
        channel = Channel.FindFree()
        count = 0
        if channel is None:
            self.log("%s --> %s: No channel free, waiting to send...."
                     % (candidate, device))

        device.lock()
            
        while channel is None:
            count = count + 1
            if count > 60: # 2 minutes
                self.log("...giving up.")
                device.unlock()
                return
            
            time.sleep(2)
            channel = Channel.FindFree()

        channel.lock()
        
        self.log("Will send %s to %s" % (candidate, device), "-sender")
        
        # send the shizzle
        exitcode = self.bt.send(device.device_id, channel.number, obexchannel, str(candidate.datafile))

        if aggressive and exitcode > 0:
            exitcode = 768
        
        # send OK, create SENT object
        sent = DeviceSent(device = device, schedule = candidate, exitcode = exitcode,
                          send_time = datetime.now())
        sent.save()
    
        if exitcode == 0:
            # apparently it worked, clear blacklists so he'll receive more stuff
            # device.un_blacklist()
            b = device.blacklist(True) # retry some time soon
            self.log(">>> SENT OK! %s" % b, "-sender")

        elif exitcode == BTComm.TIMEOUT or aggressive:
            # timeout
            b = device.blacklist(True) # retry some time soon
            self.log("Device timeout, %s" % b, "-sender")
            
        elif exitcode == BTComm.REFUSE: # 2
            # refused; blaclist him long time
            b = device.blacklist(False)
            self.log(">> Refused!!! %s" % b, "-sender")

        device.unlock()
        channel.unlock()


    def run(self):
        if (self.aggressive):
            self.sleeptime = self.sleeptime / 2

        try:
            while True:

                # get list of active schedules
                schedulelist = SpammerMain.getActiveSchedules()
        
                if len(schedulelist) > 0:
                    self.loop(schedulelist)
                else:
                    self.log("No active schedules! Not scanning...")
                
                self.log("Sleeping a bit...")
                time.sleep(self.sleeptime)
                
        except KeyboardInterrupt:
            self.bt.release()
            for d in Device.objects.filter(locked = True):
                self.log("Clearing lock on %s " % d)
                d.unlock()
            for c in Channel.objects.filter(locked = True):
                self.log("Clearing lock on %s " % c)
                c.unlock()
                

        pass

    def loop(self, schedulelist):

        # set interface name
        names = SpammerMain.getInterfaceNames()
        if len(names)>0:
            name = random.choice(names)
            if (name != self.bt.name):
                self.bt.set_name(name)
                self.log("Setting name to '%s'" % name)
            
        
        self.log("Scanning ....")
        
        # scan devices
        devicedata = self.bt.scan()
        
        # update datbase
        self.updateDeviceData(devicedata)
        
        # get list of active devices
        devicelist = self.getActiveDevices()

        # for each active device:
        for device in devicelist:
            
            #if device.device_id not in push_capable:
            #    self.log("%s does not like being spammed." % device)
            #    continue
            
            candidates = schedulelist[:]
            random.shuffle(candidates)
            for candidate in candidates:
                if device.can_send(candidate):
                    # send in the background!
                    if self.aggressive:
                        tpe = "aggressive"
                    else:
                        tpe = "normal"
                        
                    cmd = "./trytosend %s %s %s %s &" % (self.interface, device.device_id, candidate.id, tpe)
                    self.log(cmd)
                    os.system(cmd)
                    
                    break # next device
                else:
                    # self.log("Will not send %s to %s right now..." % (candidate, device))
                    pass
                    

        self.log("Active devices: %d, active schedules: %d" % (len(devicelist), len(schedulelist)))
        pass


    def updateDeviceData(self, data):

        for (id, name, obexchannel) in data:
            try:
                device = Device.objects.get(device_id = id);
                self.log("Updating %s" % device)
            except Device.DoesNotExist:
                device = Device(device_id = id, name = name)
                self.log("New device: %s" % device)

            device.obexchannel = obexchannel
            device.lastseen = datetime.now();
            device.save()
            
            try:
                seenby = DeviceSeenBy.objects.get(device = device, interface = self.interface)
            except DeviceSeenBy.DoesNotExist:
                seenby = DeviceSeenBy(device = device, interface = self.interface)
                self.log("%s: Newly seen by '%s'" % (device, self.interface))

            seenby.lastseen = datetime.now()
            seenby.save()

        pass
    

    def getActiveDevices(self):

        set = DeviceSeenBy.objects
        set = set.filter(interface = self.interface)
        set = set.filter(lastseen__gt = datetime.now() - timedelta(minutes=self.active_in_minutes))
        set = set.select_related()

        return [x.device for x in set if not x.device.locked]

    @staticmethod
    def initialize():
        for d in Device.objects.filter(locked = True):
            print "Clearing lock on %s " % d
            d.unlock()
        for c in Channel.objects.filter(locked = True):
            print "Clearing lock on %s " % c
            c.unlock()
    

    @staticmethod
    def getActiveSchedules():

        set = Schedule.objects.all()

        # all = active
        #set = set.filter(do_from__lte = datetime.now())
        #set = set.filter(do_until__gte = datetime.now())
        
        return [x for x in set] # force query execution


    @staticmethod
    def getInterfaceNames():
        return [x.name for x in InterfaceName.objects.all() if x.interface == "all" or x.interface == self.interface]

    @staticmethod
    def getAllActiveDevices():

        set = Device.objects
        set = set.filter(lastseen__gt = datetime.now() - timedelta(minutes=SpammerMain.active_in_minutes))
        return [x for x in set]

    @staticmethod
    def getActiveBlacklists():
        set = Blacklist.objects
        set = set.filter(ban_until__gt = datetime.now())
        set = set.order_by("ban_until")
        set = set.select_related()
        return set

    @staticmethod
    def getLastSent():
        set = DeviceSent.objects
        set = set.order_by("-send_time")
        set = set.select_related()
        return set
