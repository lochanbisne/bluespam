import sys, os, re


class BTComm:

    REFUSE = 100
    TIMEOUT = 101
    
    interface = "hci0"
    name = None
    
    def __init__(self, interface = False):
        if interface:
            self.interface = interface

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
        cmd = "/usr/local/bin/ussp-push %s@ %s %s" % (device_id, "media/" + str(filename), str(filename).split("/")[-1])
        exitcode = os.system(cmd)
        print cmd
        print exitcode
        if exitcode != 0:
            return BTComm.TIMEOUT

        return 0


if __name__ == "__main__":

    s = BTComm()
    print s.scan()
