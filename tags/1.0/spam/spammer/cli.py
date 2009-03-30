import sys, re, random, time, os, signal
from datetime import datetime, timedelta
import django.db.models.base

from models import *



class SpammerScheduleCLI:
    
    def __call__(self, args, opts):
        cmd = args[0]
        
        if cmd == "list":
            
            print "Active schedules:"
            for s in Schedule.objects.all():
                print "%2d - %s" % (s.id, s.datafile)
            print

        
        elif cmd == "add":
            for f in args[1:]:
                if not os.path.exists(f):
                    print "File not found: %s" % f
                    sys.exit(1)
                #os.system("cp %s /root/spam/media/data")
                print "not implemented yet..."
                
            pass
        elif cmd == "del":
            print "not implemented yet..."
            pass
        else:
            raise KeyError()


class SpammerCLI:
    
    cmd = {}

    def __init__(self):
        self.cmd['schedule'] = SpammerScheduleCLI()
        
    def __getitem__(self, k):
        return self.cmd[k]