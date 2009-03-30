import sys, os, re
import lightblue
from models import Device

class BTComm:

    REFUSE = 100
    TIMEOUT = 101

    interface = "hci0"
    name = None
    
    def __init__(self, interface = False):
        if interface:
            self.interface = interface

    def scan(self):
        """ Scans the devices and returns a list of (id, friendlyname, obexchannel) tuples. """

        transfer_services = ['OBEX Object Push', 'OBEX File Transfer']
        
        results = []
        for (devid, devname, classid) in lightblue.finddevices():

            try:
                device = Device.objects.get(device_id = devid)
                if device.obexchannel != -1:
                    results.append( (devid, devname, device.obexchannel) )
                    continue # already scanned this one, go on with next --> assumes person has not turned it off!
                
            except Device.DoesNotExist:
                pass
            
            services = lightblue.findservices(devid)
            for (did, obexchannel, srvname) in services:
                if srvname in transfer_services:
                    results.append( (devid, devname, obexchannel) )
                    break
                
        return results

    def set_name(self, name):
        """ Sets the name for the device """
        self.name = name
        
        cmd = "sudo hciconfig %s name '%s'" % (self.interface, name)
        exitcode = os.system(cmd)
        if exitcode != 0:
            return False
        return True
    

    def send(self, device_id, number, channel, filename):
        """ Sends a file to a device. Returns 0 on success, otherwise either BTComm.REFUSE or BTComm.TIMEOUT """

        refuse_codes = [111]
        
        try:
            lightblue.obex.sendfile(device_id, int(channel), filename)
        except Exception, e:
            print e
            try:
                code = int(e.message[1:-1].split(",")[0])
            except Exception, e2:
                # Error parsing. try again.
                return BTComm.TIMEOUT
            if code in refuse_codes:
                return BTComm.REFUSE

            return BTComm.TIMEOUT
            
        return 0



if __name__ == "__main__":

    #s = BTComm()
    #print s.scan()

    try:
        lightblue.obex.sendfile('00:1E:A3:D8:10:66', 9, '/home/arjan/test.txt')
    except Exception, e:
        code = int(e.message[1:-1].split(",")[0])
        print e
        print code
        
        
        
