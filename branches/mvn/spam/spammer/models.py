from django.db import models
from datetime import datetime, timedelta


class Device(models.Model):
    device_id = models.CharField('Device identifier', max_length=40, primary_key=True)
    name = models.CharField('Device name', max_length=255)
    lastseen = models.DateTimeField('Last seen at')
    locked = models.BooleanField('Device locked', default=False)
    obexchannel = models.IntegerField(default=-1)

    def __str__(self):
        s = "[%s] %s" % (self.device_id, self.name)
        if self.locked:
            s += " (L)"
        return s

    def can_send(self, schedule):
        # else, try again if not blacklisted
        if self.is_blacklisted() or self.locked:
            return False

        # check if not successfully sent
        set = DeviceSent.objects.filter(device = self)
        set = set.filter(schedule = schedule)
        set = set.filter(exitcode = 0)
        if len(set) == 0:
            # never sent at all
            return True

        return False

    def blacklist(self, retry = True):

        frm = datetime.now()

        # find previous blacklist
        if not retry:
            l = [x.ban_count for x in Blacklist.objects.filter(device = self)]
            if len(l) > 0:
                num = max(l)+1
            else:
                num = 1
            num = min(num, max(Blacklist.REJECT_BLACKLIST_TIMES.keys()))
            until = frm + Blacklist.REJECT_BLACKLIST_TIMES[num]
        else:
            # retry
            num = 0
            until = frm + Blacklist.RETRY_BLACKLIST_TIME

        # delete previous blaclists for this device
        Blacklist.objects.filter(device = self).delete()        
            
        # create new blacklist
        b = Blacklist(device = self, ban_from = frm, ban_until = until, ban_count = num)
        b.save()
        
        return b

    def un_blacklist(self):
        Blacklist.objects.filter(device = self).delete()

    def is_blacklisted(self):
        set = Blacklist.objects.filter(device = self)
        set = set.filter(ban_from__lte = datetime.now())
        set = set.filter(ban_until__gte = datetime.now())
        if len(set) > 0:
            return True
        return False

    def lock(self):
        self.locked = True
        self.save()
        
    def unlock(self):
        self.locked = False
        self.save()

        
    
class DeviceSeenBy(models.Model):
    device = models.ForeignKey(Device)
    interface = models.CharField(max_length = 40)
    lastseen = models.DateTimeField('Last seen at')

    
class Blacklist(models.Model):

    REJECT_BLACKLIST_TIMES = { 1: timedelta(minutes = 2),
                               2: timedelta(minutes = 2),
                               3: timedelta(minutes = 2),
                               4: timedelta(minutes = 3),
                               5: timedelta(minutes = 3),
                               6: timedelta(minutes = 4),
                               7: timedelta(minutes = 4),
                               8: timedelta(minutes = 5),
                               9: timedelta(minutes = 10),
                               10: timedelta(hours = 1) }
    
    RETRY_BLACKLIST_TIME = timedelta(minutes = 3)
    
    device = models.ForeignKey(Device)
    ban_from = models.DateTimeField('From')
    ban_until = models.DateTimeField('Until')
    ban_count = models.IntegerField(default = 1)

    def __str__(self):
        return "%s Banned until %s" % (self.device, self.ban_until)


class Schedule(models.Model):
    """ dddd """
    
    SCHEDULE_TYPE_CHOICES = (
        ('text', 'Text message (.txt)'),
        ('photo', 'Photo (.jpg)'),
        ('video', 'Video (.3gp)'),
        ('sound', 'Sound (.mp3)'))

    schedule_type = models.CharField('Schedule type', max_length=20, choices=SCHEDULE_TYPE_CHOICES)
    datafile = models.FileField('File', upload_to = "data/")

    def __str__(self):
        return "[%s]" % str(self.datafile).split('/')[-1]


class DeviceSent(models.Model):
    device = models.ForeignKey(Device)
    schedule = models.ForeignKey(Schedule)
    exitcode = models.IntegerField()
    send_time = models.DateTimeField('Sent at')

    
class DeviceReceived(models.Model):
    device = models.ForeignKey(Device)
    filename = models.CharField(max_length=255)
    recv_time = models.DateTimeField('Received at')


class InterfaceName(models.Model):
    name = models.CharField(max_length = 40, primary_key = True)
    interface = models.CharField(max_length = 40) # "all" for all interfaces

    def __str__(self):
        return "%s (for %s)" % (self.name, self.interface)


class Channel(models.Model):
    number = models.IntegerField()
    locked = models.BooleanField(default = False)

    def FindFree():
        free = Channel.objects.filter(locked = False)
        if len(free) > 0:
            return free[0]
        return None

    FindFree = staticmethod(FindFree)
    
    def lock(self):
        self.locked = True
        self.save()

    def unlock(self):
        self.locked = False
        self.save()

    def __str__(self):
        return "BT channel %d" % self.number

