from django.urls import path
from . import views

urlpatterns = [
    # Session management
    path('start/', views.start_exam_session, name='start_exam_session'),
    path('active/', views.get_active_session, name='get_active_session'),
    path('<int:session_id>/', views.get_session_detail, name='get_session_detail'),
    path('<int:session_id>/submit/', views.submit_exam, name='submit_exam'),
    path('<int:session_id>/result/', views.get_session_result, name='get_session_result'),
    path('<int:session_id>/logs/', views.get_session_logs, name='get_session_logs'),
    path('<int:session_id>/log-action/', views.log_page_action, name='log_page_action'),
    
    # Answer management
    path('<int:session_id>/answers/', views.submit_answer, name='submit_answer'),
    path('<int:session_id>/answers/<int:answer_id>/', views.update_answer, name='update_answer'),
    
    # Session lists
    path('my-sessions/', views.get_my_sessions, name='get_my_sessions'),
    path('class/<int:class_id>/', views.get_class_sessions, name='get_class_sessions'),
    path('exam/<int:exam_id>/', views.get_exam_sessions, name='get_exam_sessions'),
]
