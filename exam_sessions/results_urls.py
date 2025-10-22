from django.urls import path
from . import views

urlpatterns = [
    path('my-results/', views.get_my_results, name='get_my_results'),
    path('class/<int:class_id>/', views.get_class_results, name='get_class_results_results'),
    path('exam/<int:exam_id>/', views.get_exam_results, name='get_exam_results_results'),
    path('student/<int:student_id>/', views.get_student_results, name='get_student_results'),
    path('<int:result_id>/grade/', views.grade_result, name='grade_result'),
    path('<int:result_id>/', views.get_result_detail, name='get_result_detail'),
]

