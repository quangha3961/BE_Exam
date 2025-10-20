from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    # Exam management endpoints
    path('', views.exam_list_create, name='exam-list-create'),
    path('<int:exam_id>/', views.exam_detail, name='exam-detail'),
    path('available/', views.exam_available, name='exam-available'),
    
    # Exam question management endpoints
    path('<int:exam_id>/questions/', views.add_question_to_exam, name='add-question-to-exam'),
    path('<int:exam_id>/questions/<int:exam_question_id>/', views.update_exam_question, name='update-exam-question'),
    path('<int:exam_id>/questions/<int:exam_question_id>/delete/', views.remove_question_from_exam, name='remove-question-from-exam'),
    
    # Favorite exams endpoints
    path('<int:exam_id>/favorite/', views.add_to_favorites, name='add-to-favorites'),
    path('<int:exam_id>/favorite/remove/', views.remove_from_favorites, name='remove-from-favorites'),
    path('favorites/', views.get_favorite_exams, name='get-favorite-exams'),
    
    # Exam statistics endpoint
    path('<int:exam_id>/statistics/', views.exam_statistics, name='exam-statistics'),
]
