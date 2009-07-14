from django.contrib import admin
import models

class ScheduleAdmin(admin.ModelAdmin):
    name = "Foo"
    
    fieldsets = (
        (
        None, {
        'fields': ('schedule_type', 'datafile'),
        'description': 'Using a "Schedule", you can specify a file which is to be uploaded to any bluetooth device that is in the neighbourhood. Please choose the file type, and then select a file to upload. Click "Save" to submit the form. The file will be available immediately for sending.'
        }),
        )
    pass

class SpammerAdmin(admin.sites.AdminSite):
    pass

site = SpammerAdmin()

# admin.site.register(DeviceSeenBy, admin.ModelAdmin)
#admin.site.register(models.Blacklist, admin.ModelAdmin)
site.register(models.Schedule, ScheduleAdmin)
# admin.site.register(DeviceSent, admin.ModelAdmin)
# admin.site.register(DeviceReceived, admin.ModelAdmin)

site.register(models.Device, admin.ModelAdmin)

#admin.site.register(models.InterfaceName, admin.ModelAdmin)
#admin.site.register(models.Channel, admin.ModelAdmin)

admin.site = site
