from django.contrib import admin

from .models import Schedule


class ScheduleModelAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'reception_time')


admin.site.register(Schedule, ScheduleModelAdmin)
