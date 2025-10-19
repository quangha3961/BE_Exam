from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import get_user_model

from .models import Class, ClassStudent
from .serializers import (
    ClassListSerializer,
    ClassDetailSerializer,
    ClassCreateUpdateSerializer,
    ClassStudentSerializer,
    AddStudentSerializer,
    StudentClassSerializer
)
from .permissions import (
    IsTeacherOrReadOnly,
    IsClassTeacher,
    IsStudentOrTeacher,
    CanManageStudents
)

User = get_user_model()


class CustomPagination(PageNumberPagination):
    """Custom pagination for classes"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET', 'POST'])
@permission_classes([IsTeacherOrReadOnly])
def class_list_create(request):
    """
    GET: List all classes (for teachers) or enrolled classes (for students)
    POST: Create a new class (teachers only)
    """
    if request.method == 'GET':
        if request.user.role == 'teacher':
            # Teachers see all their classes
            classes = Class.objects.filter(teacher=request.user)
        else:
            # Students see only their enrolled classes
            class_students = ClassStudent.objects.filter(student=request.user)
            classes = [cs.class_obj for cs in class_students]
        
        # Apply search filter if provided
        search = request.GET.get('search', '')
        if search:
            classes = classes.filter(className__icontains=search)
        
        # Apply pagination
        paginator = CustomPagination()
        page = paginator.paginate_queryset(classes, request)
        
        if page is not None:
            serializer = ClassListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = ClassListSerializer(classes, many=True)
        return Response({
            'success': True,
            'data': {
                'results': serializer.data,
                'count': len(classes)
            }
        })
    
    elif request.method == 'POST':
        serializer = ClassCreateUpdateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            class_obj = serializer.save()
            response_serializer = ClassListSerializer(class_obj)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Class created successfully'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': 'Class creation failed'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsClassTeacher])
def class_detail(request, class_id):
    """
    GET: Get class detail
    PUT: Update class (teachers only)
    DELETE: Delete class (teachers only)
    """
    class_obj = get_object_or_404(Class, id=class_id)
    
    if request.method == 'GET':
        serializer = ClassDetailSerializer(class_obj)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    elif request.method == 'PUT':
        # Check if user is the teacher of this class
        if request.user != class_obj.teacher:
            return Response({
                'success': False,
                'message': 'You can only update your own classes'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ClassCreateUpdateSerializer(class_obj, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            response_serializer = ClassDetailSerializer(class_obj)
            return Response({
                'success': True,
                'data': response_serializer.data,
                'message': 'Class updated successfully'
            })
        
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': 'Class update failed'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Check if user is the teacher of this class
        if request.user != class_obj.teacher:
            return Response({
                'success': False,
                'message': 'You can only delete your own classes'
            }, status=status.HTTP_403_FORBIDDEN)
        
        class_obj.delete()
        return Response({
            'success': True,
            'message': 'Class deleted successfully'
        })


@api_view(['GET'])
@permission_classes([IsStudentOrTeacher])
def class_students(request, class_id):
    """
    GET: Get all students in a class
    """
    class_obj = get_object_or_404(Class, id=class_id)
    
    # Check if user has permission to view this class
    if request.user.role == 'student':
        if not class_obj.students.filter(student=request.user).exists():
            return Response({
                'success': False,
                'message': 'You are not enrolled in this class'
            }, status=status.HTTP_403_FORBIDDEN)
    elif request.user.role == 'teacher' and request.user != class_obj.teacher:
        return Response({
            'success': False,
            'message': 'You can only view students in your own classes'
        }, status=status.HTTP_403_FORBIDDEN)
    
    class_students = class_obj.students.all()
    paginator = CustomPagination()
    page = paginator.paginate_queryset(class_students, request)
    
    if page is not None:
        serializer = ClassStudentSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    serializer = ClassStudentSerializer(class_students, many=True)
    return Response({
        'success': True,
        'data': {
            'results': serializer.data,
            'count': class_students.count()
        }
    })


@api_view(['POST'])
@permission_classes([CanManageStudents])
def add_student(request, class_id):
    """
    POST: Add a student to a class (teachers only)
    """
    class_obj = get_object_or_404(Class, id=class_id)
    
    # Check if the current user is the teacher of this class
    if request.user != class_obj.teacher:
        return Response({
            'success': False,
            'message': 'You can only add students to your own classes'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = AddStudentSerializer(data=request.data, context={'class_obj': class_obj})
    if serializer.is_valid():
        class_student = serializer.save()
        response_serializer = ClassStudentSerializer(class_student)
        return Response({
            'success': True,
            'data': response_serializer.data,
            'message': 'Student added to class successfully'
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'errors': serializer.errors,
        'message': 'Failed to add student to class'
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([CanManageStudents])
def remove_student(request, class_id, student_id):
    """
    DELETE: Remove a student from a class (teachers only)
    """
    class_obj = get_object_or_404(Class, id=class_id)
    
    # Check if the current user is the teacher of this class
    if request.user != class_obj.teacher:
        return Response({
            'success': False,
            'message': 'You can only remove students from your own classes'
        }, status=status.HTTP_403_FORBIDDEN)
    
    class_student = get_object_or_404(ClassStudent, class_obj=class_obj, student_id=student_id)
    class_student.delete()
    
    return Response({
        'success': True,
        'message': 'Student removed from class successfully'
    })


@api_view(['GET'])
@permission_classes([IsStudentOrTeacher])
def my_classes(request):
    """
    GET: Get classes for the current user
    For students: returns enrolled classes
    For teachers: returns taught classes
    """
    if request.user.role == 'student':
        class_students = ClassStudent.objects.filter(student=request.user)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(class_students, request)
        
        if page is not None:
            serializer = StudentClassSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = StudentClassSerializer(class_students, many=True)
        return Response({
            'success': True,
            'data': {
                'results': serializer.data,
                'count': class_students.count()
            }
        })
    
    elif request.user.role == 'teacher':
        classes = Class.objects.filter(teacher=request.user)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(classes, request)
        
        if page is not None:
            serializer = ClassListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = ClassListSerializer(classes, many=True)
        return Response({
            'success': True,
            'data': {
                'results': serializer.data,
                'count': classes.count()
            }
        })
