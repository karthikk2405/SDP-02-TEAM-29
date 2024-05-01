from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Doc_Status(models.Model):
    status = models.CharField(max_length=30,null=True)
    def __str__(self):
        return self.status

class Super_User(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    mobile = models.IntegerField(null=True)
    image = models.FileField(null=True)
    reg = models.CharField(max_length=30,null=True)
    def __str__(self):
        return self.user.username+" "+self.reg

class Signup_User(models.Model):
    objects = None
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    mobile = models.IntegerField(null=True)
    image = models.FileField(null=True)
    reg = models.CharField(max_length=30,null=True)
    def __str__(self):
        return self.user.username+" "+self.reg

class Patient(models.Model):
    sign = models.ForeignKey(Signup_User,on_delete=models.CASCADE,null=True)
    c_number = models.IntegerField(null=True)
    age = models.IntegerField(null=True)
    address = models.CharField(max_length=30,null=True)
    b_group = models.CharField(max_length=30,null=True)
    gender = models.CharField(max_length=30,null=True)
    def __str__(self):
        return self.sign.user.username

class Doctor(models.Model):
    status = models.ForeignKey(Doc_Status,on_delete=models.CASCADE,null=True)
    sign = models.ForeignKey(Signup_User,on_delete=models.CASCADE,null=True)
    age = models.IntegerField(null=True)
    salary = models.IntegerField(null=True)
    last_attend = models.IntegerField(null=True)
    last_date = models.DateField(null=True)
    address = models.CharField(max_length=30,null=True)
    qualification = models.CharField(max_length=30,null=True)
    specialist = models.CharField(max_length=30,null=True)
    gender = models.CharField(max_length=30,null=True)
    def __str__(self):
        return self.sign.user.username



class Attendance(models.Model):
    doc = models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True)
    month = models.CharField(max_length=20,null=True)
    year = models.CharField(max_length=20,null=True)
    salary = models.CharField(max_length=20,null=True)
    attend = models.CharField(max_length=20,null=True)
    def __str__(self):
        return self.doc.sign.user.username+" "+self.month+" "+self.year

class Status(models.Model):
    status = models.CharField(max_length=30,null=True)
    def __str__(self):
        return self.status

class Appointment(models.Model):
    status = models.ForeignKey(Status,on_delete=models.CASCADE,null=True)
    pat = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    doc = models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True)
    disease = models.CharField(max_length=100,null=True)
    desc = models.TextField(null=True)
    time1 = models.TimeField(null=True)
    date1 = models.DateField(null=True)
    def __str__(self):
        return self.pat.sign.user.username+" "+self.doc.sign.user.username

class Prescription(models.Model):
    pat = models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    doc = models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True)
    disease = models.CharField(max_length=100,null=True)
    prescription = models.TextField(null=True)
    date1 = models.DateField(null=True)
    def __str__(self):
        return self.pat.sign.user.username+" "+self.doc.sign.user.username

class Fee_Patient(models.Model):
    appoint = models.ForeignKey(Appointment,on_delete=models.CASCADE,null=True)
    last_date = models.DateField(null=True)
    paid = models.IntegerField(null=True)
    outstanding = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    def __str__(self):
        return self.appoint.pat.sign.user.username+" "+str(self.total)

class Send_Feedback(models.Model):
    profile = models.ForeignKey(Signup_User, on_delete=models.CASCADE, null=True)
    message1 = models.TextField(null=True)
    date = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.profile.user.username


