from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import get_user_model

from .models import Question, QuestionAnswer
from .serializers import (
    QuestionListSerializer,
    QuestionDetailSerializer,
    QuestionCreateUpdateSerializer,
    QuestionMyQuestionsSerializer,
    QuestionAnswerSerializer,
    QuestionAnswerCreateUpdateSerializer
)
from .permissions import (
    IsTeacherOrReadOnly,
    IsQuestionOwner,
    IsAnswerOwner
)

User = get_user_model()


class CustomPagination(PageNumberPagination):
    """Custom pagination for questions"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET', 'POST'])
@permission_classes([IsTeacherOrReadOnly])
def question_list_create(request):
    """
    GET: List all questions (for teachers)
    POST: Create a new question (teachers only)
    """
    if request.method == 'GET':
        # Filter by teacher role - only teachers can see all questions
        if request.user.role != 'teacher':
            return Response({
                'success': False,
                'message': 'Only teachers can view all questions'
            }, status=status.HTTP_403_FORBIDDEN)
        
        questions = Question.objects.all()
        
        # Apply filters
        type_filter = request.GET.get('type')
        if type_filter:
            questions = questions.filter(type=type_filter)
        
        difficulty_filter = request.GET.get('difficulty')
        if difficulty_filter:
            questions = questions.filter(difficulty=difficulty_filter)
        
        teacher_id = request.GET.get('teacher_id')
        if teacher_id:
            questions = questions.filter(teacher_id=teacher_id)
        
        search = request.GET.get('search', '')
        if search:
            questions = questions.filter(question_text__icontains=search)
        
        # Apply pagination
        paginator = CustomPagination()
        page = paginator.paginate_queryset(questions, request)
        
        if page is not None:
            serializer = QuestionListSerializer(page, many=True)
            paginated_response = paginator.get_paginated_response(serializer.data)
            return Response({
                'success': True,
                'data': paginated_response.data
            })
        
        serializer = QuestionListSerializer(questions, many=True)
        return Response({
            'success': True,
            'data': {
                'results': serializer.data,
                'count': questions.count(),
                'page': 1,
                'total_pages': 1
            }
        })
    
    elif request.method == 'POST':
        serializer = QuestionCreateUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            question = serializer.save()
            response_serializer = QuestionListSerializer(question)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Question created successfully'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': 'Question creation failed'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsQuestionOwner])
def question_detail(request, question_id):
    """
    GET: Get question detail
    PUT: Update question (teachers only)
    DELETE: Delete question (teachers only)
    """
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'GET':
        serializer = QuestionDetailSerializer(question)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    elif request.method == 'PUT':
        # Check if user is the teacher who created this question
        if request.user != question.teacher:
            return Response({
                'success': False,
                'message': 'You can only update your own questions'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = QuestionCreateUpdateSerializer(question, data=request.data, context={'request': request})
        if serializer.is_valid():
            question = serializer.save()
            response_serializer = QuestionDetailSerializer(question)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Question updated successfully'
            })
        
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': 'Question update failed'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Check if user is the teacher who created this question
        if request.user != question.teacher:
            return Response({
                'success': False,
                'message': 'You can only delete your own questions'
            }, status=status.HTTP_403_FORBIDDEN)
        
        question.delete()
        return Response({
            'success': True,
            'message': 'Question deleted successfully'
        })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_questions(request):
    """
    GET: Get questions created by the current teacher
    """
    if request.user.role != 'teacher':
        return Response({
            'success': False,
            'message': 'Only teachers can view their questions'
        }, status=status.HTTP_403_FORBIDDEN)
    
    questions = Question.objects.filter(teacher=request.user)
    
    # Apply filters
    type_filter = request.GET.get('type')
    if type_filter:
        questions = questions.filter(type=type_filter)
    
    difficulty_filter = request.GET.get('difficulty')
    if difficulty_filter:
        questions = questions.filter(difficulty=difficulty_filter)
    
    search = request.GET.get('search', '')
    if search:
        questions = questions.filter(question_text__icontains=search)
    
    # Apply pagination
    paginator = CustomPagination()
    page = paginator.paginate_queryset(questions, request)
    
    if page is not None:
        serializer = QuestionMyQuestionsSerializer(page, many=True)
        paginated_response = paginator.get_paginated_response(serializer.data)
        return Response({
            'success': True,
            'data': paginated_response.data
        })
    
    serializer = QuestionMyQuestionsSerializer(questions, many=True)
    return Response({
        'success': True,
        'data': {
            'results': serializer.data,
            'count': questions.count(),
            'page': 1,
            'total_pages': 1
        }
    })


@api_view(['POST'])
@permission_classes([IsAnswerOwner])
def add_answer(request, question_id):
    """
    POST: Add an answer to a question (teachers only)
    """
    question = get_object_or_404(Question, id=question_id)
    
    # Check if user is the teacher who created this question
    if request.user != question.teacher:
        return Response({
            'success': False,
            'message': 'You can only add answers to your own questions'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = QuestionAnswerCreateUpdateSerializer(data=request.data, context={'question': question})
    if serializer.is_valid():
        answer = serializer.save()
        response_serializer = QuestionAnswerSerializer(answer)
        return Response({
            'success': True,
            'data': response_serializer.data,
            'message': 'Answer added successfully'
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'errors': serializer.errors,
        'message': 'Failed to add answer'
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAnswerOwner])
def update_answer(request, question_id, answer_id):
    """
    PUT: Update an answer (teachers only)
    """
    question = get_object_or_404(Question, id=question_id)
    answer = get_object_or_404(QuestionAnswer, id=answer_id, question=question)
    
    # Check if user is the teacher who created this question
    if request.user != question.teacher:
        return Response({
            'success': False,
            'message': 'You can only update answers to your own questions'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = QuestionAnswerCreateUpdateSerializer(answer, data=request.data, context={'question': question})
    if serializer.is_valid():
        answer = serializer.save()
        response_serializer = QuestionAnswerSerializer(answer)
        return Response({
            'success': True,
            'data': response_serializer.data,
            'message': 'Answer updated successfully'
        })
    
    return Response({
        'success': False,
        'errors': serializer.errors,
        'message': 'Answer update failed'
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAnswerOwner])
def delete_answer(request, question_id, answer_id):
    """
    DELETE: Delete an answer (teachers only)
    """
    question = get_object_or_404(Question, id=question_id)
    answer = get_object_or_404(QuestionAnswer, id=answer_id, question=question)
    
    # Check if user is the teacher who created this question
    if request.user != question.teacher:
        return Response({
            'success': False,
            'message': 'You can only delete answers to your own questions'
        }, status=status.HTTP_403_FORBIDDEN)
    
    answer.delete()
    return Response({
        'success': True,
        'message': 'Answer deleted successfully'
    })
