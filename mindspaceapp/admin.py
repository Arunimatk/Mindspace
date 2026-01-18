from django.contrib import admin
from .models import UserModel, JournalEntry, Doctor, PatientRecord, Appointment, Prescription


# Custom Admin View for Users
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age', 'phone')
    search_fields = ('name', 'email')

# Custom Admin View for Journal Entries (Messages/Moods)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'mood', 'title', 'created_at')
    list_filter = ('mood', 'created_at')
    search_fields = ('user__name', 'title', 'content')
    date_hierarchy = 'created_at'

# Custom Admin View for Doctors
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'is_urgent_care', 'contact_info')
    list_filter = ('is_urgent_care', 'specialization')
    search_fields = ('name', 'specialization')

# Custom Admin View for Appointments
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'doctor', 'date_time', 'status')
    list_filter = ('status', 'date_time')

# Custom Admin View for Patient Records
class PatientRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_severe', 'created_at')
    list_filter = ('is_severe',)

admin.site.register(UserModel, UserModelAdmin)
admin.site.register(JournalEntry, JournalEntryAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(PatientRecord, PatientRecordAdmin)
admin.site.register(Prescription)

