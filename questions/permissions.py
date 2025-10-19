from rest_framework import permissions


class IsTeacherOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow teachers to create/edit questions.
    Students can only read questions.
    """
    
    def has_permission(self, request, view):
        # Read permissions for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Write permissions only for teachers
        return request.user.is_authenticated and request.user.role == 'teacher'


class IsQuestionOwner(permissions.BasePermission):
    """
    Custom permission to only allow the teacher who created the question to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Write permissions only for the question owner (teacher)
        return request.user == obj.teacher


class IsAnswerOwner(permissions.BasePermission):
    """
    Custom permission to only allow the teacher who owns the question to manage answers.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'
    
    def has_object_permission(self, request, view, obj):
        # Only the question owner can manage answers
        return request.user == obj.question.teacher
