from rest_framework import permissions


class IsTeacherOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow teachers to create/edit classes.
    Students can only read classes they are enrolled in.
    """
    
    def has_permission(self, request, view):
        # Read permissions for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Write permissions only for teachers
        return request.user.is_authenticated and request.user.role == 'teacher'


class IsClassTeacher(permissions.BasePermission):
    """
    Custom permission to only allow the teacher who owns the class to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for class teacher and enrolled students
        if request.method in permissions.SAFE_METHODS:
            return (request.user == obj.teacher or 
                   obj.students.filter(student=request.user).exists())
        
        # Write permissions only for the class teacher
        return request.user == obj.teacher


class IsStudentOrTeacher(permissions.BasePermission):
    """
    Custom permission for student-related operations.
    Students can view their own data, teachers can manage students.
    """
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role in ['student', 'teacher'])


class CanManageStudents(permissions.BasePermission):
    """
    Custom permission to allow teachers to manage students in their classes.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'
    
    def has_object_permission(self, request, view, obj):
        # Only the class teacher can manage students
        return request.user == obj.teacher
