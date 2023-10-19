from django.db import models
from datetime import date

class Students(models.Model):
    name = models.CharField(max_length=100)
    teachers = models.ManyToManyField('Teachers', related_name='students')

    def __str__(self):
        return self.name

class Teachers(models.Model):
    name = models.CharField(max_length=100)
    # Add other teacher-related fields as needed

    def __str__(self):
        return self.name
    

class Certificate(models.Model):
    StudentID=models.IntegerField()
    TeacherID=models.IntegerField()
    Student_Name=models.CharField( max_length=50)
    Teacher_Name=models.CharField( max_length=50)
    Issued_Date=models.DateField(default=date.today)
    JWT_Token=models.TextField()


  
