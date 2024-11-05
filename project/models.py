from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Formation(models.Model):
    name = models.CharField(max_length=30, null=True)
    duration = models.DecimalField(max_digits=6, decimal_places=0, null=True)

    def __str__(self):
        return self.name

class Absence(models.Model):
    state = models.CharField(max_length=30, null=True)
    date = models.DateField(null=True)
    emp = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='absences', null=True)

    def __str__(self):
        return self.state

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()    
    profession = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=100, null=True)
    age = models.DecimalField(max_digits=6, decimal_places=0, null=True)
    adresse = models.CharField(max_length=100, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=1000, null=True)
    picture = models.ImageField(upload_to='employee_pictures/', null=True, blank=True)
    formation = models.ForeignKey(Formation, on_delete=models.SET_NULL, null=True, blank=True)
    absence = models.ForeignKey(Absence, on_delete=models.SET_NULL, null=True, blank=True, related_name="absences")

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    def remove_expired_formation(self):
        if self.formation and self.formation.duration:
            duration = timezone.timedelta(days=self.formation.duration)
            if self.formation.created_date + duration < timezone.now():
                self.formation = None
                self.save()
    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Responsable(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    firstname = models.CharField(max_length=15, null=True)
    lastname = models.CharField(max_length=15, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    email = models.EmailField(null=True)
    code = models.CharField(max_length=10, null=True)
    