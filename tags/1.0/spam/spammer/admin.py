from django.contrib import admin
from models import *

admin.site.register(Device, admin.ModelAdmin)
# admin.site.register(DeviceSeenBy, admin.ModelAdmin)
admin.site.register(Blacklist, admin.ModelAdmin)
admin.site.register(Schedule, admin.ModelAdmin)
# admin.site.register(DeviceSent, admin.ModelAdmin)
# admin.site.register(DeviceReceived, admin.ModelAdmin)

admin.site.register(InterfaceName, admin.ModelAdmin)
admin.site.register(Channel, admin.ModelAdmin)
