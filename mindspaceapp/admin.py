from django.contrib import admin
from .models import UserModel, JournalEntry, Doctor, PatientRecord, Appointment, Prescription

admin.site.register(UserModel)
admin.site.register(JournalEntry)
admin.site.register(Doctor)
admin.site.register(PatientRecord)
admin.site.register(Appointment)
admin.site.register(Prescription)
