from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Case)
admin.site.register(Payments)
admin.site.register(availability)
admin.site.register(Appointment)

