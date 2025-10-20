from rest_framework import permissions


class IsTeacherOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow teachers to create/edit exams.
    Students can only read exams they have access to.
    """
    
    def has_permission(self, request, view):
        # Read permissions for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Write permissions only for teachers
        return request.user.is_authenticated and request.user.role == 'teacher'


class IsExamOwner(permissions.BasePermission):
    """
    Custom permission to only allow the teacher who created the exam to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for exam owner and students in the class
        if request.method in permissions.SAFE_METHODS:
            # Teachers can see their own exams, students can see exams in their classes
            if request.user.role == 'teacher':
                return request.user == obj.created_by
            elif request.user.role == 'student':
                return obj.class_obj.students.filter(student=request.user).exists()
            return False
        
        # Write permissions only for the exam owner (teacher)
        return request.user == obj.created_by


class IsStudentOrTeacher(permissions.BasePermission):
    """
    Custom permission for student-related operations.
    Students can view their own data, teachers can manage exams.
    """
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role in ['student', 'teacher'])


class CanManageExamQuestions(permissions.BasePermission):
    """
    Custom permission to allow teachers to manage questions in their exams.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'
    
    def has_object_permission(self, request, view, obj):
        # Only the exam owner can manage questions
        return request.user == obj.exam.created_by


class IsStudentForFavorites(permissions.BasePermission):
    """
    Custom permission to allow students to manage their favorite exams.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'


class CanViewExamStatistics(permissions.BasePermission):
    """
    Custom permission to allow teachers to view exam statistics.
    """
    
    def has_object_permission(self, request, view, obj):
        # Only the exam owner can view statistics
        return request.user == obj.created_by


class CanAccessAvailableExams(permissions.BasePermission):
    """
    Custom permission to allow students to access available exams in their classes.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'
