# mindspaceapp/models.py

from django.db import models

class UserModel(models.Model):
    name = models.CharField("Full Name", max_length=100)
    password = models.CharField(max_length=50)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = "myytable"

    def __str__(self):
        return self.name

class JournalEntry(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    mood = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.name}"

    




  

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    is_urgent_care = models.BooleanField(default=False)
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"

class PatientRecord(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    problem_description = models.TextField()
    is_severe = models.BooleanField(default=False, verbose_name="Is this dangerous/severe?")
    symptoms = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        severity = "SEVERE" if self.is_severe else "Stable"
        return f"{self.user.name} - {severity}"

class Appointment(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=20, default='Pending', choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Completed', 'Completed')])

    def __str__(self):
        return f"{self.user.name} with {self.doctor.name} on {self.date_time}"

class Prescription(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    medication_details = models.TextField()
    date_issued = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.user.name} by {self.doctor.name}"
