from django.contrib import admin

from .models import Batch,Course,Exam,ExamResult,Student,Teacher

admin.site.register(Batch)
admin.site.register(Course)
admin.site.register(Exam)
admin.site.register(ExamResult)
admin.site.register(Student)
admin.site.register(Teacher)