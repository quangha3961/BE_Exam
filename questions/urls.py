from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    # Question management endpoints
    path('', views.question_list_create, name='question_list_create'),
    path('my-questions/', views.my_questions, name='my_questions'),
    path('<int:question_id>/', views.question_detail, name='question_detail'),
    
    # Answer management endpoints
    path('<int:question_id>/answers/', views.add_answer, name='add_answer'),
    path('<int:question_id>/answers/<int:answer_id>/update/', views.update_answer, name='update_answer'),
    path('<int:question_id>/answers/<int:answer_id>/delete/', views.delete_answer, name='delete_answer'),
]
