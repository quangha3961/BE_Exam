from rest_framework import permissions
from .models import ExamSession


class IsStudentOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow students to start exam sessions.
    Teachers can view sessions but not start them.
    """
    
    def has_permission(self, request, view):
        # Allow read permissions for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Only allow students to start exam sessions
        return (request.user and 
                request.user.is_authenticated and 
                request.user.role == 'student')


class IsSessionOwnerOrTeacher(permissions.BasePermission):
    """
    Custom permission to only allow session owners or teachers to access session details.
    """
    
    def has_object_permission(self, request, view, obj):
        # Allow session owner (student) to access their own session
        if hasattr(obj, 'student') and obj.student == request.user:
            return True
        
        # Allow teachers to access sessions for their classes
        if (request.user.role == 'teacher' and 
            hasattr(obj, 'exam') and 
            obj.exam.class_obj.teacher == request.user):
            return True
        
        # Allow admins to access all sessions
        if request.user.role == 'admin':
            return True
        
        return False


class IsSessionOwner(permissions.BasePermission):
    """
    Custom permission to only allow session owners to modify their sessions.
    """
    
    def has_object_permission(self, request, view, obj):
        # Only allow session owner (student) to modify their own session
        if hasattr(obj, 'student') and obj.student == request.user:
            return True
        
        return False


class CanViewClassSessions(permissions.BasePermission):
    """
    Custom permission to allow teachers to view sessions for their classes.
    """
    
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        
        # Allow teachers and admins to view class sessions
        return request.user.role in ['teacher', 'admin']


class CanViewExamSessions(permissions.BasePermission):
    """
    Custom permission to allow teachers to view sessions for their exams.
    """
    
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        
        # Allow teachers and admins to view exam sessions
        return request.user.role in ['teacher', 'admin']
