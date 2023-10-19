from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse, HttpResponse
from .models import *
from django.contrib import messages
import jwt
# Create your views here.

def navbar(request):
    return render(request,'navbar.html')

def home(request):
    data=Teachers.objects.all()
    data1=Students.objects.all()
    return render(request,'home.html',{'Data':data,'Data1':data1,})


def teacher_student_data(request):
    select_teacher=[0]
    select_teacher=request.POST.get('teacherid')
    print("teacher id:",select_teacher)
    select_student=request.POST.get('studentid')
    print("student id:",select_student)
    data=Teachers.objects.all()
    data1=Students.objects.all()
    
    if select_student and select_teacher:
        if Certificate.objects.filter(StudentID=select_student,TeacherID=select_teacher).exists():
            certificate=Certificate.objects.get(StudentID=select_student)
            messages.warning(request,'Your Certificate Already Generated')
            return render(request,'verify_certificate.html',{'certify':certificate})
        if Students.teachers.through.objects.filter(students_id=select_student,teachers_id=select_teacher):
            teacher = Teachers.objects.get(id=select_teacher) 
            students=Students.objects.get(id=select_student) 

            #Generate New Certificate
            payload={
                'StudentID':select_student,
                'TeacherID':select_teacher,
                'Student_Name':students.name,
                'Teacher_Name':teacher.name

            }
            token = jwt.encode(payload, 'Akshay2201', algorithm='HS256')

            certificate_data=Certificate(StudentID=select_student,TeacherID=select_teacher,Student_Name=students.name,Teacher_Name=teacher.name,JWT_Token=token)
            certificate_data.save()

            return render(request,'certificate.html',{'certi_data':certificate_data})
        
        messages.error(request,'Student Not Under The Selected Teacher!')
        return redirect('/')

    elif select_student:
        students = Students.objects.get(id=select_student)  # Replace with the student you want
        teachers =students.teachers.all()
        student_name=Students.objects.get(id=select_student)
        return render(request,'home.html',{'Data4':teachers,'Data':data,'Data1':data1,'Student':student_name})
    elif select_teacher:
        teacher = Teachers.objects.get(id=select_teacher)  # Replace with the student you want
        students =teacher.students.all()
        teacher_name=Teachers.objects.get(id=select_teacher)
        if Certificate.objects.filter(TeacherID=select_teacher).exists():
            certify1=Certificate.objects.filter(TeacherID=select_teacher).values()
            for certify2 in certify1:
                # certify3=Certificate.objects.get(StudentID=certify2.StudentID)
                # for i in certify3:
                print("certify data:",certify1)
                print("certify data for Loop:",certify2)
                return render(request,'home.html',{'Data3':students,'Data':data,'Data1':data1,'Teacher':teacher_name,'certify':certify1})
        return render(request,'home.html',{'Data3':students,'Data':data,'Data1':data1,'Teacher':teacher_name})

    else:
        messages.warning(request,'Please Select Teacher or Student Name!')
        return redirect('/')
    

#Verify The Generated Certificate through View Button
def verify_certificate(request,id):
    if Certificate.objects.filter(StudentID=id):
            data=Certificate.objects.get(StudentID=id)
            token=data.JWT_Token
            try:
                decode_token=jwt.decode(token, 'Akshay2201',algorithms=['HS256'])
                StudentID=decode_token['StudentID']
                TeacherID=decode_token['TeacherID']
                Student_Name=decode_token['Student_Name']
                Teacher_Name=decode_token['Teacher_Name']
                
                certificate=Certificate.objects.get(StudentID=StudentID,TeacherID=TeacherID,Student_Name=Student_Name,Teacher_Name=Teacher_Name,JWT_Token=token)
                
                if certificate:
                    messages.success(request,'Certificate is Valid !!!!')
                    print("certificate data data:",certificate)
                    return render(request,'verify_certificate.html',{'certify':certificate})
                else:
                    messages.warning(request,'Certificate Not Found ')
                    return redirect('/')
            except jwt.ExpiredSignatureError:
                messages.error(request,'Token Has Expired!')
                return redirect('/')
            except jwt.InvalidTokenError:
                messages.error(request,'Invalid Token !')
                return redirect('/')
    messages.error(request,'Certificate Not Generated !!!!')
    return redirect('/')

def generate_certificate(request,id):
    studentid=Students.objects.get(id=id)
    teacherid=Teachers.objects.get(id=id)
    if Certificate.objects.filter(StudentID=id).exists():
        certificate=Certificate.objects.filter(StudentID=id)
        messages.warning(request,'Your Certificate Already Generated')
        return redirect('/')
    
    if Students.teachers.through.objects.filter(students_id=studentid,teachers_id=teacherid):
            teacher = Teachers.objects.get(id=teacherid) 
            students=Students.objects.get(id=studentid) # Replace with the student you want
        
            payload={
                'StudentID':studentid,
                'TeacherID':teacherid,
                'Student_Name':students.name,
                'Teacher_Name':teacher.name

            }
            token = jwt.encode(payload, 'Akshay2201', algorithm='HS256')

            certificate_data=Certificate(StudentID=studentid,TeacherID=teacherid,Student_Name=students.name,Teacher_Name=teacher.name,JWT_Token=token)
            certificate_data.save()

            return render(request,'certificate.html',{'certi_data':certificate_data})
        
       


        
