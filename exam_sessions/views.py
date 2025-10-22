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


# Results API

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_my_results(request):
    """
    Get paginated results for the current student.
    Supports filters: exam_id, class_id, status
    """
    results_qs = ExamResult.objects.filter(student=request.user)

    # Filters
    exam_id = request.GET.get('exam_id')
    class_id = request.GET.get('class_id')
    status_filter = request.GET.get('status')

    if exam_id:
        results_qs = results_qs.filter(exam_id=exam_id)
    if class_id:
        results_qs = results_qs.filter(exam__class_obj_id=class_id)
    if status_filter:
        results_qs = results_qs.filter(status=status_filter)

    paginator = StandardResultsSetPagination()
    page = paginator.paginate_queryset(results_qs.order_by('-submitted_at'), request)
    serializer = ExamResultSerializer(page if page is not None else results_qs, many=True)

    if page is not None:
        return paginator.get_paginated_response(serializer.data)

    return Response({
        'success': True,
        'data': {
            'results': serializer.data,
            'count': results_qs.count()
        }
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_class_results(request, class_id):
    """
    Get class results (teachers/admins).
    Teachers can only view their own classes.
    Optional filters: exam_id, status
    """
    # Basic access control
    if request.user.role not in ['teacher', 'admin']:
        return Response({'success': False, 'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    # For teacher, ensure ownership
    if request.user.role == 'teacher':
        from classes.models import Class
        try:
            class_obj = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            return Response({'success': False, 'message': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)
        if class_obj.teacher != request.user:
            return Response({'success': False, 'message': 'You can only view results for your own classes'}, status=status.HTTP_403_FORBIDDEN)

    results_qs = ExamResult.objects.filter(exam__class_obj_id=class_id)

    exam_id = request.GET.get('exam_id')
    status_filter = request.GET.get('status')

    if exam_id:
        results_qs = results_qs.filter(exam_id=exam_id)
    if status_filter:
        results_qs = results_qs.filter(status=status_filter)

    # Statistics
    total_students = results_qs.values('student_id').distinct().count()
    completed_exams = results_qs.filter(status='graded').count()
    average_score = results_qs.aggregate(avg=Avg('total_score'))['avg'] or 0
    highest_score = results_qs.aggregate(mx=Avg(Case(When(total_score__isnull=False, then='total_score'), output_field=IntegerField())))
    highest_score = float(results_qs.order_by('-total_score').values_list('total_score', flat=True).first() or 0)
    lowest_score = float(results_qs.order_by('total_score').values_list('total_score', flat=True).first() or 0)

    # Grade distribution (simple buckets by letter grade)
    grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    for r in results_qs.values_list('percentage', flat=True):
        p = float(r or 0)
        if p >= 90:
            grade_counts['A'] += 1
        elif p >= 80:
            grade_counts['B'] += 1
        elif p >= 70:
            grade_counts['C'] += 1
        elif p >= 60:
            grade_counts['D'] += 1
        else:
            grade_counts['F'] += 1

    paginator = StandardResultsSetPagination()
    page = paginator.paginate_queryset(results_qs.order_by('-submitted_at'), request)
    serializer = ExamResultSerializer(page if page is not None else results_qs, many=True)

    payload = {
        'success': True,
        'data': {
            'class': {'id': int(class_id)},
            'results': paginator.get_paginated_response(serializer.data).data if page is not None else {
                'results': serializer.data,
                'count': results_qs.count()
            },
            'statistics': {
                'total_students': total_students,
                'completed_exams': completed_exams,
                'average_score': round(float(average_score), 2),
                'highest_score': round(highest_score, 2),
                'lowest_score': round(lowest_score, 2),
                'grade_distribution': grade_counts
            }
        }
    }

    if page is not None:
        return Response(payload)
    return Response(payload)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_exam_results(request, exam_id):
    """
    Get exam results (teachers/admins).
    Teachers can only view results for their own exam.
    Optional filter: status
    """
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        return Response({'success': False, 'message': 'Exam not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.user.role not in ['teacher', 'admin']:
        return Response({'success': False, 'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    if request.user.role == 'teacher' and exam.class_obj.teacher != request.user:
        return Response({'success': False, 'message': 'You can only view results for your own exams'}, status=status.HTTP_403_FORBIDDEN)

    results_qs = ExamResult.objects.filter(exam=exam)
    status_filter = request.GET.get('status')
    if status_filter:
        results_qs = results_qs.filter(status=status_filter)

    total_sessions = results_qs.count()
    completed_sessions = results_qs.filter(status='graded').count()
    average_score = results_qs.aggregate(avg=Avg('total_score'))['avg'] or 0
    highest_score = float(results_qs.order_by('-total_score').values_list('total_score', flat=True).first() or 0)
    lowest_score = float(results_qs.order_by('total_score').values_list('total_score', flat=True).first() or 0)

    # Score distribution buckets
    distribution = {'0-20': 0, '21-40': 0, '41-60': 0, '61-80': 0, '81-100': 0}
    for s in results_qs.values_list('percentage', flat=True):
        p = float(s or 0)
        if p <= 20:
            distribution['0-20'] += 1
        elif p <= 40:
            distribution['21-40'] += 1
        elif p <= 60:
            distribution['41-60'] += 1
        elif p <= 80:
            distribution['61-80'] += 1
        else:
            distribution['81-100'] += 1

    paginator = StandardResultsSetPagination()
    page = paginator.paginate_queryset(results_qs.order_by('-submitted_at'), request)
    serializer = ExamResultSerializer(page if page is not None else results_qs, many=True)

    data_results = paginator.get_paginated_response(serializer.data).data if page is not None else {
        'results': serializer.data,
        'count': results_qs.count()
    }

    return Response({
        'success': True,
        'data': {
            'exam': {
                'id': exam.id,
                'title': exam.title,
                'total_score': exam.total_score,
                'minutes': exam.minutes
            },
            'results': data_results,
            'statistics': {
                'total_sessions': total_sessions,
                'completed_sessions': completed_sessions,
                'average_score': round(float(average_score), 2),
                'highest_score': round(highest_score, 2),
                'lowest_score': round(lowest_score, 2),
                'completion_rate': round((completed_sessions / total_sessions * 100) if total_sessions > 0 else 0, 2),
                'score_distribution': distribution
            }
        }
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_student_results(request, student_id):
    """
    Get results for a specific student (teachers/admins).
    Teachers are limited to their classes' exams.
    Optional filters: class_id, exam_id
    """
    from accounts.models import User
    try:
        student = User.objects.get(id=student_id)
    except User.DoesNotExist:
        return Response({'success': False, 'message': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.user.role not in ['teacher', 'admin']:
        return Response({'success': False, 'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    results_qs = ExamResult.objects.filter(student=student)

    class_id = request.GET.get('class_id')
    exam_id = request.GET.get('exam_id')
    if class_id:
        results_qs = results_qs.filter(exam__class_obj_id=class_id)
        if request.user.role == 'teacher':
            # Ensure teacher owns the class
            from classes.models import Class
            try:
                class_obj = Class.objects.get(id=class_id)
            except Class.DoesNotExist:
                return Response({'success': False, 'message': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)
            if class_obj.teacher != request.user:
                return Response({'success': False, 'message': 'You can only view results for your own classes'}, status=status.HTTP_403_FORBIDDEN)
    elif request.user.role == 'teacher':
        # Limit to teacher's own classes if no class filter
        results_qs = results_qs.filter(exam__class_obj__teacher=request.user)

    if exam_id:
        results_qs = results_qs.filter(exam_id=exam_id)

    paginator = StandardResultsSetPagination()
    page = paginator.paginate_queryset(results_qs.order_by('-submitted_at'), request)
    serializer = ExamResultSerializer(page if page is not None else results_qs, many=True)

    data_results = paginator.get_paginated_response(serializer.data).data if page is not None else {
        'results': serializer.data,
        'count': results_qs.count()
    }

    # Simple statistics for the student
    total_exams = results_qs.values('exam_id').distinct().count()
    completed_exams = results_qs.filter(status='graded').count()
    average_score = results_qs.aggregate(avg=Avg('total_score'))['avg'] or 0
    highest_score = float(results_qs.order_by('-total_score').values_list('total_score', flat=True).first() or 0)
    lowest_score = float(results_qs.order_by('total_score').values_list('total_score', flat=True).first() or 0)

    return Response({
        'success': True,
        'data': {
            'student': {
                'id': student.id,
                'fullName': student.fullName,
                'email': student.email,
                'role': student.role
            },
            'results': data_results,
            'statistics': {
                'total_exams': total_exams,
                'completed_exams': completed_exams,
                'average_score': round(float(average_score), 2),
                'highest_score': round(highest_score, 2),
                'lowest_score': round(lowest_score, 2),
                'improvement_trend': 'unknown'
            }
        }
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def grade_result(request, result_id):
    """
    Grade an exam result (teachers/admins). Allows updating feedback and status.
    """
    if request.user.role not in ['teacher', 'admin']:
        return Response({'success': False, 'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    try:
        result = ExamResult.objects.select_related('exam__class_obj').get(id=result_id)
    except ExamResult.DoesNotExist:
        return Response({'success': False, 'message': 'Result not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.user.role == 'teacher' and result.exam.class_obj.teacher != request.user:
        return Response({'success': False, 'message': 'You can only grade results for your own classes'}, status=status.HTTP_403_FORBIDDEN)

    feedback = request.data.get('feedback')
    status_value = request.data.get('status')

    if status_value and status_value not in dict(ExamResult.STATUS_CHOICES):
        return Response({'success': False, 'message': 'Invalid status value'}, status=status.HTTP_400_BAD_REQUEST)

    if feedback is not None:
        result.feedback = feedback
    if status_value is not None:
        result.status = status_value
    result.save()

    serializer = ExamResultSerializer(result)
    return Response({
        'success': True,
        'data': serializer.data,
        'message': 'Exam graded successfully'
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_result_detail(request, result_id):
    """
    Get result detail (student owner, class teacher, or admin).
    """
    try:
        result = ExamResult.objects.select_related('session', 'exam__class_obj', 'student').get(id=result_id)
    except ExamResult.DoesNotExist:
        return Response({'success': False, 'message': 'Result not found'}, status=status.HTTP_404_NOT_FOUND)

    if not (
        result.student_id == request.user.id or
        (request.user.role == 'teacher' and result.exam.class_obj.teacher_id == request.user.id) or
        request.user.role == 'admin'
    ):
        return Response({'success': False, 'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    serializer = ExamResultSerializer(result)
    return Response({
        'success': True,
        'data': serializer.data
    })