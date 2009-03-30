from spammer.models import *
from django.shortcuts import render_to_response
from spammer.spammer import SpammerMain
from django.http import HttpResponseRedirect

def status(request):

    c = { 'latest_devices': Device.objects.all().order_by("-lastseen")[:20],
          'active_devices': SpammerMain.getAllActiveDevices(),
          'active_schedules': SpammerMain.getActiveSchedules(),
          'blacklist': SpammerMain.getActiveBlacklists(),
          'last_sent': SpammerMain.getLastSent()[:10],
          'last_sent_ok': SpammerMain.getLastSent().filter(exitcode = 0)[:10]
          }

    return render_to_response('status.tpl', c)


def clear_sent(request):
    DeviceSent.objects.all().delete()
    return HttpResponseRedirect("/status/");

def clear_blacklist(request):
    Blacklist.objects.all().delete()
    return HttpResponseRedirect("/status/");
    
