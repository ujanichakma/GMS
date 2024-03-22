from django.db import models
from django.contrib.auth.models import User

class Batch(models.Model):
    batch_name = models.CharField(max_length=100)

    def __str__(self):
        return self.batch_name

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    students= models.ManyToManyField('Student',blank=True)
    credit=models.PositiveSmallIntegerField(default=3)

    a = models.PositiveSmallIntegerField(default=50)
    b = models.PositiveSmallIntegerField(default=40)
    c = models.PositiveSmallIntegerField(default=30)
    d = models.PositiveSmallIntegerField(default=20)

    def __str__(self):
        return self.course_name


class Exam(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ForeignKey(Course,on_delete=models.CASCADE)
    batch=models.ForeignKey(Batch, on_delete=models.CASCADE)
    total_marks = models.IntegerField(default=52)
    weightage = models.IntegerField(default=0)
    # Add other fields as needed

    def __str__(self):
        return f"{self.name}----{self.courses.course_name}---{self.batch.batch_name}"

class Teacher(User):
    
    def __str__(self):
        return self.username


class Student(User):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.username}---{self.batch.batch_name}'

class ExamResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    obtained_marks = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.student} - {self.exam}"
