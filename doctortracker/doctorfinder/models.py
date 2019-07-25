from django.db import models

# Create your models here.

class User(models.Model):
    email = models.EmailField(unique= True)
    password = models.CharField(max_length = 20)
    otp = models.IntegerField(default = 459)
    is_active = models.BooleanField(default=True)
    is_verfied = models.BooleanField(default=False)
    role = models.CharField(max_length = 10)
    created_at= models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now = True, blank=False)

class Doctor(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    qualification = models.CharField(max_length=100, blank= True)
    speciality = models.CharField(max_length = 100)
    mobile = models.CharField(max_length = 10)
    clinic = models.CharField(max_length= 100,blank = True)
    address = models.CharField(max_length= 500, blank= True)
    city = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50, blank= True)
    gender = models.CharField(max_length= 10)
    birthdate = models.DateField()
    location = models.CharField(max_length= 30, blank= True)
    about_doc = models.CharField(max_length= 100, blank= True)
    profile_pic=models.FileField(upload_to='doctorfinder/img/',default='doc_male.png')

class Patient(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    mobile = models.CharField(max_length = 10)
    address = models.CharField(max_length= 500, blank = True)
    city = models.CharField(max_length = 50)
    state = models.CharField(max_length = 50, blank = True)
    gender = models.CharField(max_length= 10)
    birthdate = models.DateField()

    #updated patient profile

    blood_group=models.CharField(max_length=10,blank= True)
    blood_presure=models.CharField(max_length=10,blank= True)
    sugar=models.CharField(max_length=10,blank= True)
    Haemoglobin=models.CharField(max_length=10,blank= True)
    profile_pic=models.FileField(upload_to='doctorfinder/img/',default='patient_icon.png')
    
class Case(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete = models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    disease = models.CharField(max_length = 100)
    symptoms = models.CharField(max_length = 200)
    status=models.CharField(max_length = 50,default="active")
class availability(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete= models.CASCADE)
    avail_date = models.DateField()
    start_time = models.CharField(max_length = 100)
    status = models.BooleanField(default= False)

class Appointment(models.Model):
    doctor_id = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    patient_id = models.ForeignKey(Patient, on_delete = models.CASCADE)
    availability_id = models.ForeignKey(availability, on_delete = models.CASCADE,default = None)
    appointment_status = models.BooleanField(default = False)

class Prescription(models.Model):
    case_id = models.ForeignKey(Case, on_delete=models.CASCADE)
    patient_id = models.ForeignKey(Patient, on_delete= models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete = models.CASCADE)
    attachment_file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True,blank=False)

class Payments(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    email = models.CharField(max_length=200)
    customer_id =  models.CharField(max_length=300)