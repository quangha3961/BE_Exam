from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from django.db.models import Q, Count, Avg, Case, When, IntegerField
from django.db import transaction
from datetime import timedelta
import uuid

from .models import ExamSession, StudentAnswer, ExamResult, ExamLog
from .serializers import (
    ExamSessionSerializer, ExamSessionCreateSerializer, ExamSessionDetailSerializer,
    ExamSessionListSerializer, ExamSessionActiveSerializer, StudentAnswerCreateSerializer,
    StudentAnswerUpdateSerializer, StudentAnswerSerializer, ExamResultSerializer,
    ExamSessionStatisticsSerializer
)
from .permissions import (
    IsStudentOrReadOnly, IsSessionOwnerOrTeacher, IsSessionOwner,
    CanViewClassSessions, CanViewExamSessions
)
from exams.models import Exam, ExamQuestion
from questions.models import QuestionAnswer
from classes.models import ClassStudent


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['POST'])
@permission_classes([IsStudentOrReadOnly])
def start_exam_session(request):
    """
    Start a new exam session for a student
    """
    serializer = ExamSessionCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': 'Invalid request data'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    exam_id = serializer.validated_data['exam_id']
    
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Exam does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Check if student is enrolled in the class
    if not ClassStudent.objects.filter(
        class_obj=exam.class_obj, 
        student=request.user
    ).exists():
        return Response({
            'success': False,
            'message': 'You are not enrolled in this class'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Check if there's already an active session for this exam
    existing_session = ExamSession.objects.filter(
        exam=exam, 
        student=request.user, 
        status='in_progress'
    ).first()
    
    if existing_session:
        return Response({
            'success': False,
            'message': 'You already have an active session for this exam'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Create new session
    session_code = f"EXAM_{timezone.now().strftime('%Y%m%d')}_{str(uuid.uuid4())[:8].upper()}"
    
    with transaction.atomic():
        session = ExamSession.objects.create(
            exam=exam,
            student=request.user,
            code=session_code,
            start_time=timezone.now()
        )
        
        # Create student answer records for all questions
        for exam_question in exam.exam_questions.all():
            StudentAnswer.objects.create(
                session=session,
                exam_question=exam_question
            )
        
        # Log session start
        ExamLog.objects.create(
            session=session,
            student=request.user,
            actions='exam_started',
            detail='Student started the exam'
        )
    
    # Serialize response with questions
    response_data = ExamSessionSerializer(session).data
    
    # Add questions with answers
    questions = []
    for exam_question in exam.exam_questions.all().order_by('order'):
        question_data = {
            'id': exam_question.id,
            'exam_question': {
                'id': exam_question.id,
                'order': exam_question.order,
                'code': exam_question.code,
                'question': {
                    'id': exam_question.question.id,
                    'question_text': exam_question.question.question_text,
                    'type': exam_question.question.type,
                    'difficulty': exam_question.question.difficulty,
                    'image_url': exam_question.question.image_url,
                    'answers': [
                        {
                            'id': answer.id,
                            'text': answer.text,
                            'is_correct': answer.is_correct
                        } for answer in exam_question.question.answers.all()
                    ]
                }
            },
            'selected_answer': None,
            'answer_text': None,
            'score': 0.0,
            'answered_at': None,
            'is_correct': False
        }
        questions.append(question_data)
    
    response_data['questions'] = questions
    
    return Response({
        'success': True,
        'data': response_data,
        'message': 'Exam session started successfully'
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_active_session(request):
    """
    Get the current active session for the student
    """
    active_session = ExamSession.objects.filter(
        student=request.user,
        status='in_progress'
    ).first()
    
    if not active_session:
        return Response({
            'success': False,
            'message': 'No active session found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ExamSessionActiveSerializer(active_session)
    return Response({
        'success': True,
        'data': serializer.data
    })


@api_view(['POST'])
@permission_classes([IsSessionOwner])
def submit_answer(request, session_id):
    """
    Submit an answer for a question in the session
    """
    try:
        session = ExamSession.objects.get(id=session_id, student=request.user)
    except ExamSession.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Session not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if session.status != 'in_progress':
        return Response({
            'success': False,
            'message': 'Session is not active'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = StudentAnswerCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': 'Invalid answer data'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    exam_question_id = serializer.validated_data['exam_question_id']
    selected_answer_id = serializer.validated_data.get('selected_answer_id')
    answer_text = serializer.validated_data.get('answer_text', '')
    
    try:
        exam_question = ExamQuestion.objects.get(id=exam_question_id, exam=session.exam)
    except ExamQuestion.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Question not found in this exam'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Get or create student answer
    student_answer, created = StudentAnswer.objects.get_or_create(
        session=session,
        exam_question=exam_question,
        defaults={
            'selected_answer_id': selected_answer_id,
            'answer_text': answer_text,
            'answered_at': timezone.now()
        }
    )
    
    if not created:
        # Update existing answer
        student_answer.selected_answer_id = selected_answer_id
        student_answer.answer_text = answer_text
        student_answer.answered_at = timezone.now()
        student_answer.save()
    
    # Calculate score and correctness
    question = exam_question.question
    is_correct = False
    score = 0.0
    
    if question.type in ['multiple_choice', 'true_false']:
        if selected_answer_id:
            try:
                selected_answer = QuestionAnswer.objects.get(id=selected_answer_id)
                is_correct = selected_answer.is_correct
                if is_correct:
                    # Calculate score based on question order and total questions
                    total_questions = session.exam.exam_questions.count()
                    score = (session.exam.total_score / total_questions) if total_questions > 0 else 0
            except QuestionAnswer.DoesNotExist:
                pass
    
    student_answer.is_correct = is_correct
    student_answer.score = score
    student_answer.save()
    
    # Log answer submission
    ExamLog.objects.create(
        session=session,
        student=request.user,
        actions='answer_submitted',
        detail=f'Answered question {exam_question.code or exam_question.order}'
    )
    
    # Return updated answer
    answer_serializer = StudentAnswerSerializer(student_answer)
    
    return Response({
        'success': True,
        'data': answer_serializer.data,
        'message': 'Answer submitted successfully'
    }, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsSessionOwner])
def update_answer(request, session_id, answer_id):
    """
    Update an existing answer
    """
    try:
        session = ExamSession.objects.get(id=session_id, student=request.user)
    except ExamSession.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Session not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if session.status != 'in_progress':
        return Response({
            'success': False,
            'message': 'Session is not active'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        student_answer = StudentAnswer.objects.get(id=answer_id, session=session)
    except StudentAnswer.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Answer not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    serializer = StudentAnswerUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': 'Invalid update data'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    selected_answer_id = serializer.validated_data.get('selected_answer_id')
    answer_text = serializer.validated_data.get('answer_text')
    
    # Update answer
    if selected_answer_id is not None:
        student_answer.selected_answer_id = selected_answer_id
    if answer_text is not None:
        student_answer.answer_text = answer_text
    
    student_answer.answered_at = timezone.now()
    
    # Recalculate score and correctness
    question = student_answer.exam_question.question
    is_correct = False
    score = 0.0
    
    if question.type in ['multiple_choice', 'true_false']:
        if student_answer.selected_answer:
            is_correct = student_answer.selected_answer.is_correct
            if is_correct:
                total_questions = session.exam.exam_questions.count()
                score = (session.exam.total_score / total_questions) if total_questions > 0 else 0
    
    student_answer.is_correct = is_correct
    student_answer.score = score
    student_answer.save()
    
    # Log answer update
    ExamLog.objects.create(
        session=session,
        student=request.user,
        actions='answer_updated',
        detail=f'Updated answer for question {student_answer.exam_question.code or student_answer.exam_question.order}'
    )
    
    answer_serializer = StudentAnswerSerializer(student_answer)
    
    return Response({
        'success': True,
        'data': answer_serializer.data,
        'message': 'Answer updated successfully'
    })


@api_view(['POST'])
@permission_classes([IsSessionOwner])
def submit_exam(request, session_id):
    """
    Submit the exam session
    """
    try:
        session = ExamSession.objects.get(id=session_id, student=request.user)
    except ExamSession.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Session not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if session.status != 'in_progress':
        return Response({
            'success': False,
            'message': 'Session is not active'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    with transaction.atomic():
        # Calculate total score
        total_score = sum(answer.score for answer in session.answers.all())
        correct_count = session.answers.filter(is_correct=True).count()
        wrong_count = session.answers.count() - correct_count
        
        # Update session
        session.status = 'completed'
        session.end_time = timezone.now()
        session.total_score = total_score
        session.submitted_at = timezone.now()
        session.save()
        
        # Create exam result
        percentage = (total_score / session.exam.total_score * 100) if session.exam.total_score > 0 else 0
        
        result = ExamResult.objects.create(
            session=session,
            student=request.user,
            exam=session.exam,
            total_score=total_score,
            correct_count=correct_count,
            wrong_count=wrong_count,
            submitted_at=session.submitted_at,
            status='graded',
            percentage=percentage
        )
        
        # Log exam submission
        ExamLog.objects.create(
            session=session,
            student=request.user,
            actions='exam_submitted',
            detail='Student submitted the exam'
        )
    
    result_serializer = ExamResultSerializer(result)
    
    return Response({
        'success': True,
        'data': result_serializer.data,
        'message': 'Exam submitted successfully'
    })


@api_view(['GET'])
@permission_classes([IsSessionOwnerOrTeacher])
def get_session_detail(request, session_id):
    """
    Get detailed information about a session
    """
    try:
        session = ExamSession.objects.get(id=session_id)
    except ExamSession.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Session not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Check permissions
    if not (session.student == request.user or 
            (request.user.role == 'teacher' and session.exam.class_obj.teacher == request.user) or
            request.user.role == 'admin'):
        return Response({
            'success': False,
            'message': 'Permission denied'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = ExamSessionDetailSerializer(session)
    return Response({
        'success': True,
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsSessionOwnerOrTeacher])
def get_session_result(request, session_id):
    """
    Get the result of a completed session
    """
    try:
        session = ExamSession.objects.get(id=session_id)
    except ExamSession.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Session not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Check permissions
    if not (session.student == request.user or 
            (request.user.role == 'teacher' and session.exam.class_obj.teacher == request.user) or
            request.user.role == 'admin'):
        return Response({
            'success': False,
            'message': 'Permission denied'
        }, status=status.HTTP_403_FORBIDDEN)
    
    if not hasattr(session, 'result'):
        return Response({
            'success': False,
            'message': 'Session result not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ExamResultSerializer(session.result)
    return Response({
        'success': True,
        'data': serializer.data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_my_sessions(request):
    """
    Get all sessions for the current user
    """
    sessions = ExamSession.objects.filter(student=request.user)
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        sessions = sessions.filter(status=status_filter)
    
    # Filter by exam
    exam_id = request.GET.get('exam_id')
    if exam_id:
        sessions = sessions.filter(exam_id=exam_id)
    
    paginator = StandardResultsSetPagination()
    page = paginator.paginate_queryset(sessions, request)
    
    if page is not None:
        serializer = ExamSessionListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    serializer = ExamSessionListSerializer(sessions, many=True)
    return Response({
        'success': True,
        'data': {
            'results': serializer.data,
            'count': sessions.count()
        }
    })


@api_view(['GET'])
@permission_classes([CanViewClassSessions])
def get_class_sessions(request, class_id):
    """
    Get all sessions for a specific class (teachers only)
    """
    try:
        class_obj = ClassStudent.objects.get(class_obj_id=class_id).class_obj
    except:
        return Response({
            'success': False,
            'message': 'Class not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Check if teacher owns this class
    if request.user.role == 'teacher' and class_obj.teacher != request.user:
        return Response({
            'success': False,
            'message': 'You can only view sessions for your own classes'
        }, status=status.HTTP_403_FORBIDDEN)
    
    sessions = ExamSession.objects.filter(exam__class_obj=class_obj)
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        sessions = sessions.filter(status=status_filter)
    
    # Filter by exam
    exam_id = request.GET.get('exam_id')
    if exam_id:
        sessions = sessions.filter(exam_id=exam_id)
    
    paginator = StandardResultsSetPagination()
    page = paginator.paginate_queryset(sessions, request)
    
    if page is not None:
        serializer = ExamSessionListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    serializer = ExamSessionListSerializer(sessions, many=True)
    return Response({
        'success': True,
        'data': {
            'results': serializer.data,
            'count': sessions.count()
        }
    })


@api_view(['GET'])
@permission_classes([CanViewExamSessions])
def get_exam_sessions(request, exam_id):
    """
    Get all sessions for a specific exam (teachers only)
    """
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Exam not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Check if teacher owns this exam
    if request.user.role == 'teacher' and exam.class_obj.teacher != request.user:
        return Response({
            'success': False,
            'message': 'You can only view sessions for your own exams'
        }, status=status.HTTP_403_FORBIDDEN)
    
    sessions = ExamSession.objects.filter(exam=exam)
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        sessions = sessions.filter(status=status_filter)
    
    # Calculate statistics
    total_sessions = sessions.count()
    completed = sessions.filter(status='completed').count()
    in_progress = sessions.filter(status='in_progress').count()
    abandoned = sessions.filter(status='abandoned').count()
    timeout = sessions.filter(status='timeout').count()
    
    average_score = sessions.filter(status='completed').aggregate(
        avg_score=Avg('total_score')
    )['avg_score'] or 0
    
    completion_rate = (completed / total_sessions * 100) if total_sessions > 0 else 0
    
    paginator = StandardResultsSetPagination()
    page = paginator.paginate_queryset(sessions, request)
    
    if page is not None:
        serializer = ExamSessionListSerializer(page, many=True)
        paginated_data = paginator.get_paginated_response(serializer.data)
        paginated_data.data['statistics'] = {
            'total_sessions': total_sessions,
            'completed': completed,
            'in_progress': in_progress,
            'abandoned': abandoned,
            'timeout': timeout,
            'average_score': round(float(average_score), 2),
            'completion_rate': round(completion_rate, 2)
        }
        return paginated_data
    
    serializer = ExamSessionListSerializer(sessions, many=True)
    return Response({
        'success': True,
        'data': {
            'exam': {
                'id': exam.id,
                'title': exam.title,
                'total_score': exam.total_score,
                'minutes': exam.minutes
            },
            'sessions': {
                'results': serializer.data,
                'count': sessions.count()
            },
            'statistics': {
                'total_sessions': total_sessions,
                'completed': completed,
                'in_progress': in_progress,
                'abandoned': abandoned,
                'timeout': timeout,
                'average_score': round(float(average_score), 2),
                'completion_rate': round(completion_rate, 2)
            }
        }
    })


@api_view(['GET'])
@permission_classes([IsSessionOwnerOrTeacher])
def get_session_logs(request, session_id):
    """
    Get logs for a specific session
    """
    try:
        session = ExamSession.objects.get(id=session_id)
    except ExamSession.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Session not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Check permissions
    if not (session.student == request.user or 
            (request.user.role == 'teacher' and session.exam.class_obj.teacher == request.user) or
            request.user.role == 'admin'):
        return Response({
            'success': False,
            'message': 'Permission denied'
        }, status=status.HTTP_403_FORBIDDEN)
    
    logs = session.logs.all().order_by('timestamp')
    
    from .serializers import ExamLogSerializer
    serializer = ExamLogSerializer(logs, many=True)
    
    return Response({
        'success': True,
        'data': {
            'session': {
                'id': session.id,
                'code': session.code,
                'student': {
                    'id': session.student.id,
                    'fullName': session.student.fullName
                }
            },
            'logs': serializer.data
        }
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def log_page_action(request, session_id):
    """
    Log page leave/return actions
    """
    try:
        session = ExamSession.objects.get(id=session_id, student=request.user)
    except ExamSession.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Session not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    action = request.data.get('action')
    if action not in ['page_leave', 'page_return']:
        return Response({
            'success': False,
            'message': 'Invalid action'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    detail = 'Student left the exam page' if action == 'page_leave' else 'Student returned to exam page'
    
    ExamLog.objects.create(
        session=session,
        student=request.user,
        actions=action,
        detail=detail
    )
    
    return Response({
        'success': True,
        'message': 'Action logged successfully'
    })