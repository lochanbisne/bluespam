import sys, os, re


class BTComm:

    REFUSE = 100
    TIMEOUT = 101
    
    interface = "hci0"
    name = None
    
    def __init__(self, interface = False):
        if interface:
            self.interface = interface

    def find_obex_push(self):

        cmd = "sdptool -i %s search OPUSH" % self.interface
        fp = os.popen(cmd)

        results = []

        device_r = re.compile("^Searching for OPUSH on (\w\w(:\w\w)+)")
        srv_r = re.compile("OBEX Object Push")
        
        curdev = None
        supported = False
        
        while True:
            l = fp.readline()
            if not l: break
            
            m = device_r.match(l.strip())
            if m:
                # print m.groups()
                if curdev is not None and supported:
                    results.append(curdev)
                curdev = m.groups()[0]
                supported = False

            if l.find("OBEX Object Push") >= 0 and curdev is not None:
                supported = True
        if curdev is not None and supported:
            results.append(curdev)
            
        return results
            


    def scan(self):

        cmd = "hcitool -i %s scan" % self.interface

        # the RE for parsing the output
        r = re.compile("(\w\w(:\w\w)+)\s+(.*)$")

        results = []
        
        fp = os.popen(cmd)
        
        while True:
            l = fp.readline()
            if not l: break
            m = r.match(l.strip())
            if m is None: continue
            
            g = m.groups()
            results.append( (g[0], g[2], 9) )

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

        # send file
        cmd = "ussp-push %s@ %s %s" % (device_id, filename, filename.split("/")[-1])
        exitcode = os.system(cmd)
        print cmd
        print exitcode
        if exitcode != 0:
            return BTComm.TIMEOUT

        return 0

    def release(self):
        rfcomm = "/dev/rfcomm%s" % self.interface[3]

        cmd = "sudo rfcomm release %s 2>& 1 > /dev/null" % (rfcomm)
        exitcode = os.system(cmd)
        

if __name__ == "__main__":

    s = BTComm()
    print s.scan()
