from spammer.models import *
from django.shortcuts import render_to_response
from spammer.spammer import SpammerMain
from django.http import HttpResponseRedirect

from datetime import datetime, timedelta

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
    return HttpResponseRedirect("/");

def clear_blacklist(request):
    Blacklist.objects.all().delete()
    return HttpResponseRedirect("/");
    

def stats_g(collection, datefield):
    key = datefield+"__gte"
    now = datetime.now()
    return {'bytime' : [('5 minutes',  collection.filter(**{key: now - timedelta(minutes = 5)}).count()),
                        ('30 minutes', collection.filter(**{key: now - timedelta(minutes = 30)}).count()),
                        ('hour', collection.filter(**{key: now - timedelta(hours = 1)}).count()),
                        ('day', collection.filter(**{key: now - timedelta(hours = 24)}).count()),
                        ('year', collection.filter(**{key: now - timedelta(days = 365)}).count())
                        ],
            'total': collection.count()
            }
            


def stats(request):
    """ uitgebreide statistieken pagina (aantal gevonden telefoons, totaal
    verzonden filmpjes, totaal  per filmpje) """
    
    c = { 'latest_devices': stats_g(Device.objects.all(), 'lastseen'),
          'sent_files':     stats_g(DeviceSent.objects.all().filter(exitcode = 0), 'send_time'),
          'file_stats':     []
          }

    for s in Schedule.objects.all():
        c['file_stats'].append( { 'file': s.datafile, 'sent': stats_g(DeviceSent.objects.all().filter(exitcode = 0).filter(schedule = s), 'send_time')})

    return render_to_response('stats.tpl', c)

