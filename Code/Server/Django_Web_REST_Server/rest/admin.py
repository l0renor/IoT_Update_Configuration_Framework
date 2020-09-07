from django.contrib import admin

# Register your models here.
from rest.models import IPRule, Device, IoTApplication


class IPRuleInline(admin.TabularInline):
    model = IPRule
    extra = 1

    class Meta:
        verbose_name_plural = "IP_Rule"
        ordering = ("id",)


class AppInline(admin.StackedInline):
    model = Device


class DeviceAdmin(admin.ModelAdmin):
    filter_horizontal = ('applications',)
    # inlines = [IPRuleInline]
    fieldsets = [
        (None, {'fields': ['uuid', 'owner', 'applications']}),
    ]


class IoTAppAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['id', 'name', 'version']}),
    ]



admin.site.register(Device, DeviceAdmin)
admin.site.register(IoTApplication, IoTAppAdmin)
