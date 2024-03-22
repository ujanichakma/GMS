from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import get_object_or_404


def log_out(request):
	logout(request)
	return redirect('')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/authenticated/')
    else :
        if request.method=='POST':
            user_name=request.POST['user_name']
            password=request.POST['password']
            role=request.POST['role']
            userTemp=None
            if role=='teacher':
                try:
                    userTemp=Teacher.objects.get(username=user_name,password=password)
                except Teacher.DoesNotExist:
                    userTemp=None
            elif role=='student':
                try:
                    userTemp=Student.objects.get(username=user_name,password=password)
                except Student.DoesNotExist:
                    userTemp=None
            else:
                user = authenticate(username=user_name, password=password)
                if user is not None:
                    if (user.is_staff == False):
                        error=request.session.pop('error',True)
                        return render(request, "login.html", {'error':error})
                    else:
                        login(request, user)
                        return redirect("/admin/")	
                    
            if userTemp is None:
                error=request.session.pop('error',True)
                return render(request, "login.html", {'error':error})
            else:
                login(request, userTemp)
                return redirect("/authenticated/",{'uname':userTemp.username})
        else :
            return render(request,'login.html',)

 
def dashboard(request):
    usertype="NULL"
    userTemp=None
    if request.user.is_authenticated:
        try:
            userTemp=Teacher.objects.get(username=request.user.username,password=request.user.password)
            usertype='Teacher'
            return redirect('/teacher/')
        except Teacher.DoesNotExist:
            userTemp=None
        if userTemp is None:
            try:
                userTemp=Student.objects.get(username=request.user.username,password=request.user.password)
                usertype='Student'
                enrolled_course=Course.objects.filter(students=userTemp)
                # print(userTemp.batch)
                stu_batch=userTemp.batch
                batch_exams=Exam.objects.filter(batch=stu_batch)
                # print(batch_exams.course)
                grade={}
                for exam in batch_exams:
                    gainedMark=None
                    try:
                        gainedMark=ExamResult.objects.get(exam=exam,student=userTemp).obtained_marks
                        if gainedMark>=50:
                            grade[exam.courses.course_name]='A'
                        elif gainedMark>=40:
                            grade[exam.courses.course_name]='B'
                        elif gainedMark>=30:
                            grade[exam.courses.course_name]='C'
                        elif gainedMark>=20:
                            grade[exam.courses.course_name]='D'
                        else :
                            grade[exam.courses.course_name]='F'
                        
                    except ExamResult.DoesNotExist:
                        gainedMark=0
                total=0
                credits=0

                for course,value in grade.items():
                    credit=Course.objects.get(course_name=course).credit
                    credits+=credit
                    if value =='A':
                        total+=int(credit)*4
                    elif value =='B':
                        total+=int(credit)*3
                    elif value =='C':
                        total+=int(credit)*2
                    elif value =='D':
                        total+=int(credit)*1
                    elif value =='F':
                        total+=int(credit)*0
                    
                if credits ==0:
                    cgpa=0.0
                else :
                    cgpa=float(total)/float(credits)
                cgpa = round(cgpa,2)
                return render(request,'dashboard.html',{'student':userTemp,'courses':enrolled_course,'exams':batch_exams,'grade':grade,'cgpa':cgpa})
            except Student.DoesNotExist:
                return redirect('/logout/')
    return render(request,'dashboard.html')

def teacher_dashboard(request):
    if request.user.is_authenticated:
        user=request.user
        
        if request.method=='POST':
            enrolled_course=Course.objects.filter(teacher=user)
            # print(enrolled_course)
        
        else:
            enrolled_course=Course.objects.filter(teacher=user)

            # exams=Exam.objects.filter(courses=enrolled_course)

    return render(request,'teacher.html',{'user':user,'courses':enrolled_course})

@login_required
def make_result(request,course,batch):

    if request.method=='POST':
            batch_obj=get_object_or_404(Batch,batch_name=batch)
            course_obj=get_object_or_404(Course,course_name=course)
            examTemp,created=Exam.objects.get_or_create(name='Semester Final',batch=batch_obj,courses=course_obj,)
            for id,mark_str in request.POST.items():
                if id.startswith('marks_'):
                    mark=int(mark_str)
                    student_id=int(id.split('_')[1])
                    stu_obj=Student.objects.get(id=student_id)
                    examRes,created=ExamResult.objects.get_or_create(student=stu_obj,exam=examTemp)
                    if not created:
                        examRes.obtained_marks=mark
                        examRes.save()
                    # print(mark)
            return redirect('/teacher/')
    
    else:
        batch_obj=get_object_or_404(Batch,batch_name=batch)
        course_obj=get_object_or_404(Course,course_name=course)
        examTemp,created=Exam.objects.get_or_create(name='Semester Final',batch=batch_obj,courses=course_obj)

        batch_obj=get_object_or_404(Batch,batch_name=batch)
        course_obj=get_object_or_404(Course,course_name=course)
        student_obj=Student.objects.filter(batch=batch_obj)
        marks={}
        for student in student_obj:
            examRes,created=ExamResult.objects.get_or_create(student=student,exam=examTemp)
            marks[student.id]=examRes.obtained_marks
            # print(examRes.obtained_marks)
        # print(marks)
        return render(request,'result.html',{'students':student_obj,'course':course,'marks':marks})



