from django.db import models
from datetime import datetime, timedelta


class Device(models.Model):
    device_id = models.CharField(_('Device identifier'), maxlength=40, primary_key=True)
    name = models.CharField(_('Device name'), maxlength=255)
    lastseen = models.DateTimeField(_('Last seen at'))
    locked = models.BooleanField(_('Device locked'), default=False)
    obexchannel = models.IntegerField(default=-1)

    def __str__(self):
        return "[%s] %s" % (self.device_id, self.name)


    def can_send(self, schedule):
        # else, try again if not blacklisted
        if self.is_blacklisted():
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

    class Admin:
        pass

        
    
class DeviceSeenBy(models.Model):
    device = models.ForeignKey(Device)
    interface = models.CharField(maxlength = 40)
    lastseen = models.DateTimeField(_('Last seen at'))

    class Admin:
        pass

    
class Blacklist(models.Model):

    REJECT_BLACKLIST_TIMES = { 1: timedelta(minutes = 5),
                               2: timedelta(minutes = 15),
                               3: timedelta(hours = 1),
                               4: timedelta(days = 1),
                               5: timedelta(weeks = 1) }
    
    RETRY_BLACKLIST_TIME = timedelta(minutes = 2)
    
    device = models.ForeignKey(Device)
    ban_from = models.DateTimeField(_('From'))
    ban_until = models.DateTimeField(_('Until'))
    ban_count = models.IntegerField(default = 1)

    def __str__(self):
        return "%s Banned until %s" % (self.device, self.ban_until)
    
    class Admin:
        pass


class Schedule(models.Model):

    SCHEDULE_TYPE_CHOICES = (
        ('text', 'Text message (.txt)'),
        ('photo', 'Photo (.jpg)'),
        ('video', 'Video (.3gp)'),
        ('sound', 'Sound (.mp3)'))
        

    class Admin:
        pass
    
    do_from = models.DateTimeField(_('From'))
    do_until = models.DateTimeField(_('Until'))
    schedule_type = models.CharField(_('Schedule type'), maxlength=20, choices=SCHEDULE_TYPE_CHOICES)
    datafile = models.FileField(_('File (when type != text)'), upload_to = "data/")

    def __str__(self):
        return "[%s]" % self.get_datafile_filename().split('/')[-1]


class DeviceSent(models.Model):
    device = models.ForeignKey(Device)
    schedule = models.ForeignKey(Schedule)
    exitcode = models.IntegerField()
    send_time = models.DateTimeField(_('Sent at'))

    class Admin:
        pass

class DeviceReceived(models.Model):
    device = models.ForeignKey(Device)
    filename = models.CharField(maxlength=255)
    recv_time = models.DateTimeField(_('Received at'))

    class Admin:
        pass

class InterfaceName(models.Model):
    name = models.CharField(maxlength = 40, primary_key = True)
    interface = models.CharField(maxlength = 40) # "all" for all interfaces

    def __str__(self):
        return "%s (for %s)" % (self.name, self.interface)
    
    class Admin:
        pass


class Channel(models.Model):
    number = models.IntegerField()
    locked = models.BooleanField(default = False)

    class Admin:
        pass

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
        return "/dev/rfcomm%d" % self.number

