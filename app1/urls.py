from django.urls import path
from .import views

urlpatterns = [
    path('navbar',views.navbar),
    path('',views.home),
    path('teacher_student_data',views.teacher_student_data),
    path('verify_certificate/<int:id>',views.verify_certificate),
    path('generate_certificate/<int:id>',views.generate_certificate)
    
]