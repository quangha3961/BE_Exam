from django.urls import path
from . import views

app_name = 'classes'

urlpatterns = [
    # Class management endpoints
    path('', views.class_list_create, name='class_list_create'),
    path('my-classes/', views.my_classes, name='my_classes'),
    path('<int:class_id>/', views.class_detail, name='class_detail'),
    
    # Student management endpoints
    path('<int:class_id>/students/', views.class_students, name='class_students'),
    path('<int:class_id>/students/add/', views.add_student, name='add_student'),
    path('<int:class_id>/students/<int:student_id>/', views.remove_student, name='remove_student'),
]
