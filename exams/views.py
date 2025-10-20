from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Exam, ExamQuestion, ExamFavorite
from .serializers import (
    ExamListSerializer,
    ExamDetailSerializer,
    ExamCreateUpdateSerializer,
    ExamAvailableSerializer,
    ExamQuestionSerializer,
    ExamQuestionCreateUpdateSerializer,
    ExamFavoriteSerializer,
    ExamFavoriteListSerializer,
    ExamStatisticsSerializer
)
from .permissions import (
    IsTeacherOrReadOnly,
    IsExamOwner,
    IsStudentOrTeacher,
    CanManageExamQuestions,
    IsStudentForFavorites,
    CanViewExamStatistics,
    CanAccessAvailableExams
)

User = get_user_model()


class CustomPagination(PageNumberPagination):
    """Custom pagination for exams"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET', 'POST'])
@permission_classes([IsTeacherOrReadOnly])
def exam_list_create(request):
    """
    GET: List all exams (for teachers)
    POST: Create a new exam (teachers only)
    """
    if request.method == 'GET':
        # Filter by teacher role - only teachers can see all exams
        if request.user.role != 'teacher':
            return Response({
                'success': False,
                'message': 'Only teachers can view all exams'
            }, status=status.HTTP_403_FORBIDDEN)
        
        exams = Exam.objects.filter(created_by=request.user)
        
        # Apply filters
        class_id = request.GET.get('class_id')
        if class_id:
            exams = exams.filter(class_obj_id=class_id)
        
        status_filter = request.GET.get('status')
        if status_filter:
            now = timezone.now()
            if status_filter == 'upcoming':
                exams = exams.filter(start_time__gt=now)
            elif status_filter == 'ongoing':
                exams = exams.filter(start_time__lte=now, end_time__gte=now)
            elif status_filter == 'completed':
                exams = exams.filter(end_time__lt=now)
        
        search = request.GET.get('search', '')
        if search:
            exams = exams.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        
        # Apply pagination
        paginator = CustomPagination()
        page = paginator.paginate_queryset(exams, request)
        
        if page is not None:
            serializer = ExamListSerializer(page, many=True)
            paginated_response = paginator.get_paginated_response(serializer.data)
            return Response({
                'success': True,
                'data': paginated_response.data
            })
        
        serializer = ExamListSerializer(exams, many=True)
        return Response({
            'success': True,
            'data': {
                'results': serializer.data,
                'count': exams.count(),
                'page': 1,
                'total_pages': 1
            }
        })
    
    elif request.method == 'POST':
        serializer = ExamCreateUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            exam = serializer.save()
            response_serializer = ExamDetailSerializer(exam, context={'request': request})
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Exam created successfully'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': 'Exam creation failed'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsExamOwner])
def exam_detail(request, exam_id):
    """
    GET: Get exam detail
    PUT: Update exam (teachers only)
    DELETE: Delete exam (teachers only)
    """
    exam = get_object_or_404(Exam, id=exam_id)
    
    if request.method == 'GET':
        serializer = ExamDetailSerializer(exam, context={'request': request})
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    elif request.method == 'PUT':
        # Check if user is the teacher who created this exam
        if request.user != exam.created_by:
            return Response({
                'success': False,
                'message': 'You can only update your own exams'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ExamCreateUpdateSerializer(exam, data=request.data, context={'request': request})
        if serializer.is_valid():
            exam = serializer.save()
            response_serializer = ExamDetailSerializer(exam, context={'request': request})
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Exam updated successfully'
            })
        
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': 'Exam update failed'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Check if user is the teacher who created this exam
        if request.user != exam.created_by:
            return Response({
                'success': False,
                'message': 'You can only delete your own exams'
            }, status=status.HTTP_403_FORBIDDEN)
        
        exam.delete()
        return Response({
            'success': True,
            'message': 'Exam deleted successfully'
        })


@api_view(['GET'])
@permission_classes([CanAccessAvailableExams])
def exam_available(request):
    """
    GET: Get available exams for students
    """
    # Get all classes where the student is enrolled
    from classes.models import ClassStudent
    enrolled_classes = ClassStudent.objects.filter(student=request.user).values_list('class_obj', flat=True)
    
    # Get exams for those classes
    now = timezone.now()
    exams = Exam.objects.filter(
        class_obj_id__in=enrolled_classes,
        start_time__lte=now,  # Only show exams that have started or are starting
        end_time__gte=now     # Only show exams that haven't ended yet
    ).order_by('start_time')
    
    # Apply filters
    class_id = request.GET.get('class_id')
    if class_id:
        exams = exams.filter(class_obj_id=class_id)
    
    status_filter = request.GET.get('status')
    if status_filter == 'upcoming':
        exams = exams.filter(start_time__gt=now)
    elif status_filter == 'ongoing':
        exams = exams.filter(start_time__lte=now, end_time__gte=now)
    
    # Apply pagination
    paginator = CustomPagination()
    page = paginator.paginate_queryset(exams, request)
    
    if page is not None:
        serializer = ExamAvailableSerializer(page, many=True, context={'request': request})
        paginated_response = paginator.get_paginated_response(serializer.data)
        return Response({
            'success': True,
            'data': paginated_response.data
        })
    
    serializer = ExamAvailableSerializer(exams, many=True, context={'request': request})
    return Response({
        'success': True,
        'data': {
            'results': serializer.data,
            'count': exams.count(),
            'page': 1,
            'total_pages': 1
        }
    })


@api_view(['POST'])
@permission_classes([CanManageExamQuestions])
def add_question_to_exam(request, exam_id):
    """
    POST: Add a question to an exam (teachers only)
    """
    exam = get_object_or_404(Exam, id=exam_id)
    
    # Check if user is the teacher who created this exam
    if request.user != exam.created_by:
        return Response({
            'success': False,
            'message': 'You can only add questions to your own exams'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = ExamQuestionCreateUpdateSerializer(data=request.data)
    if serializer.is_valid():
        question_id = serializer.validated_data.get('question_id')
        if not question_id:
            return Response({
                'success': False,
                'message': 'question_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        from questions.models import Question
        question = get_object_or_404(Question, id=question_id)
        
        # Check if question is already in the exam
        if ExamQuestion.objects.filter(exam=exam, question=question).exists():
            return Response({
                'success': False,
                'message': 'Question is already in this exam'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        exam_question = ExamQuestion.objects.create(
            exam=exam,
            question=question,
            order=serializer.validated_data['order'],
            code=serializer.validated_data.get('code', '')
        )
        
        response_serializer = ExamQuestionSerializer(exam_question)
        return Response({
            'success': True,
            'data': response_serializer.data,
            'message': 'Question added to exam successfully'
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'errors': serializer.errors,
        'message': 'Failed to add question to exam'
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([CanManageExamQuestions])
def remove_question_from_exam(request, exam_id, exam_question_id):
    """
    DELETE: Remove a question from an exam (teachers only)
    """
    exam = get_object_or_404(Exam, id=exam_id)
    
    # Check if user is the teacher who created this exam
    if request.user != exam.created_by:
        return Response({
            'success': False,
            'message': 'You can only remove questions from your own exams'
        }, status=status.HTTP_403_FORBIDDEN)
    
    exam_question = get_object_or_404(ExamQuestion, id=exam_question_id, exam=exam)
    exam_question.delete()
    
    return Response({
        'success': True,
        'message': 'Question removed from exam successfully'
    })


@api_view(['PUT'])
@permission_classes([CanManageExamQuestions])
def update_exam_question(request, exam_id, exam_question_id):
    """
    PUT: Update exam question order/code (teachers only)
    """
    exam = get_object_or_404(Exam, id=exam_id)
    
    # Check if user is the teacher who created this exam
    if request.user != exam.created_by:
        return Response({
            'success': False,
            'message': 'You can only update questions in your own exams'
        }, status=status.HTTP_403_FORBIDDEN)
    
    exam_question = get_object_or_404(ExamQuestion, id=exam_question_id, exam=exam)
    
    serializer = ExamQuestionCreateUpdateSerializer(exam_question, data=request.data, partial=True)
    if serializer.is_valid():
        exam_question = serializer.save()
        response_serializer = ExamQuestionSerializer(exam_question)
        return Response({
            'success': True,
            'data': response_serializer.data,
            'message': 'Exam question updated successfully'
        })
    
    return Response({
        'success': False,
        'errors': serializer.errors,
        'message': 'Exam question update failed'
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsStudentForFavorites])
def add_to_favorites(request, exam_id):
    """
    POST: Add exam to favorites (students only)
    """
    exam = get_object_or_404(Exam, id=exam_id)
    
    # Check if exam is already favorited
    if ExamFavorite.objects.filter(user=request.user, exam=exam).exists():
        return Response({
            'success': False,
            'message': 'Exam is already in your favorites'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    favorite = ExamFavorite.objects.create(user=request.user, exam=exam)
    response_serializer = ExamFavoriteSerializer(favorite)
    
    return Response({
        'success': True,
        'data': response_serializer.data,
        'message': 'Exam added to favorites successfully'
    }, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsStudentForFavorites])
def remove_from_favorites(request, exam_id):
    """
    DELETE: Remove exam from favorites (students only)
    """
    exam = get_object_or_404(Exam, id=exam_id)
    favorite = get_object_or_404(ExamFavorite, user=request.user, exam=exam)
    favorite.delete()
    
    return Response({
        'success': True,
        'message': 'Exam removed from favorites successfully'
    })


@api_view(['GET'])
@permission_classes([IsStudentForFavorites])
def get_favorite_exams(request):
    """
    GET: Get favorite exams (students only)
    """
    favorites = ExamFavorite.objects.filter(user=request.user).order_by('-created_at')
    
    # Apply pagination
    paginator = CustomPagination()
    page = paginator.paginate_queryset(favorites, request)
    
    if page is not None:
        serializer = ExamFavoriteListSerializer(page, many=True)
        paginated_response = paginator.get_paginated_response(serializer.data)
        return Response({
            'success': True,
            'data': paginated_response.data
        })
    
    serializer = ExamFavoriteListSerializer(favorites, many=True)
    return Response({
        'success': True,
        'data': {
            'results': serializer.data,
            'count': favorites.count(),
            'page': 1,
            'total_pages': 1
        }
    })


@api_view(['GET'])
@permission_classes([CanViewExamStatistics])
def exam_statistics(request, exam_id):
    """
    GET: Get exam statistics (teachers only)
    """
    exam = get_object_or_404(Exam, id=exam_id)
    
    # Check if user is the teacher who created this exam
    if request.user != exam.created_by:
        return Response({
            'success': False,
            'message': 'You can only view statistics for your own exams'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = ExamStatisticsSerializer(exam)
    return Response({
        'success': True,
        'data': serializer.data
    })