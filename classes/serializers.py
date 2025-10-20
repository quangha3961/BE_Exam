from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Class, ClassStudent
from accounts.serializers import UserProfileSerializer

User = get_user_model()


class ClassListSerializer(serializers.ModelSerializer):
    """Serializer for listing classes with basic info"""
    teacher = UserProfileSerializer(read_only=True)
    student_count = serializers.SerializerMethodField()
    exam_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Class
        fields = ['id', 'className', 'teacher', 'created_at', 'student_count', 'exam_count']
        read_only_fields = ['id', 'teacher', 'created_at']
    
    def get_student_count(self, obj):
        return obj.students.count()
    
    def get_exam_count(self, obj):
        return obj.exams.count()


class ClassDetailSerializer(serializers.ModelSerializer):
    """Serializer for class detail view"""
    teacher = UserProfileSerializer(read_only=True)
    students = serializers.SerializerMethodField()
    exams = serializers.SerializerMethodField()
    
    class Meta:
        model = Class
        fields = ['id', 'className', 'teacher', 'created_at', 'students', 'exams']
        read_only_fields = ['id', 'teacher', 'created_at']
    
    def get_students(self, obj):
        class_students = obj.students.all()
        return ClassStudentSerializer(class_students, many=True).data
    
    def get_exams(self, obj):
        # This will be implemented when exams module is ready
        return []


class ClassCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating classes"""
    
    class Meta:
        model = Class
        fields = ['className']
    
    def create(self, validated_data):
        # Set the teacher to the current user
        validated_data['teacher'] = self.context['request'].user
        return super().create(validated_data)


class ClassStudentSerializer(serializers.ModelSerializer):
    """Serializer for class student relationships"""
    student = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = ClassStudent
        fields = ['id', 'student', 'joined_at']
        read_only_fields = ['id', 'joined_at']


class AddStudentSerializer(serializers.Serializer):
    """Serializer for adding student to class"""
    student_email = serializers.EmailField()
    
    def validate_student_email(self, value):
        try:
            student = User.objects.get(email=value, role='student')
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Student with this email does not exist.")
    
    def create(self, validated_data):
        class_obj = self.context['class_obj']
        student_email = validated_data['student_email']
        student = User.objects.get(email=student_email, role='student')
        
        # Check if student is already in the class
        if ClassStudent.objects.filter(class_obj=class_obj, student=student).exists():
            raise serializers.ValidationError("Student is already in this class.")
        
        return ClassStudent.objects.create(class_obj=class_obj, student=student)


class StudentClassSerializer(serializers.ModelSerializer):
    """Serializer for student's enrolled classes"""
    className = serializers.CharField(source='class_obj.className', read_only=True)
    teacher = serializers.SerializerMethodField()
    joined_at = serializers.DateTimeField(read_only=True)
    exam_count = serializers.SerializerMethodField()
    available_exams = serializers.SerializerMethodField()
    
    class Meta:
        model = ClassStudent
        fields = ['id', 'className', 'teacher', 'joined_at', 'exam_count', 'available_exams']
    
    def get_teacher(self, obj):
        return UserProfileSerializer(obj.class_obj.teacher).data
    
    def get_exam_count(self, obj):
        return obj.class_obj.exams.count()
    
    def get_available_exams(self, obj):
        from django.utils import timezone
        now = timezone.now()
        return obj.class_obj.exams.filter(
            start_time__lte=now,
            end_time__gte=now
        ).count()
