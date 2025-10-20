from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import Exam, ExamQuestion, ExamFavorite
from classes.models import Class
from questions.models import Question
from accounts.serializers import UserProfileSerializer
from classes.serializers import ClassListSerializer
from questions.serializers import QuestionListSerializer

User = get_user_model()


class ExamQuestionSerializer(serializers.ModelSerializer):
    """Serializer for exam questions"""
    question = QuestionListSerializer(read_only=True)
    
    class Meta:
        model = ExamQuestion
        fields = ['id', 'question', 'order', 'code']
        read_only_fields = ['id']


class ExamQuestionCreateUpdateSerializer(serializers.Serializer):
    """Serializer for creating and updating exam questions"""
    question_id = serializers.IntegerField()
    order = serializers.IntegerField()
    code = serializers.CharField(max_length=50, required=False, allow_blank=True)
    
    def validate_question_id(self, value):
        try:
            Question.objects.get(id=value)
            return value
        except Question.DoesNotExist:
            raise serializers.ValidationError("Question does not exist.")
    
    def create(self, validated_data):
        # This method is not used directly, but required by DRF
        pass
    
    def update(self, instance, validated_data):
        # Update the exam question instance
        instance.order = validated_data.get('order', instance.order)
        instance.code = validated_data.get('code', instance.code)
        instance.save()
        return instance


class ExamListSerializer(serializers.ModelSerializer):
    """Serializer for listing exams with basic info"""
    class_obj = ClassListSerializer(read_only=True)
    created_by = UserProfileSerializer(read_only=True)
    question_count = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()
    session_count = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'total_score', 'minutes', 
                 'start_time', 'end_time', 'created_at', 'class_obj', 
                 'created_by', 'question_count', 'student_count', 'session_count', 'status']
        read_only_fields = ['id', 'created_at', 'created_by']
    
    def get_question_count(self, obj):
        return obj.exam_questions.count()
    
    def get_student_count(self, obj):
        return obj.class_obj.students.count()
    
    def get_session_count(self, obj):
        # This will be implemented when exam_sessions module is ready
        return 0
    
    def get_status(self, obj):
        now = timezone.now()
        if now < obj.start_time:
            return 'upcoming'
        elif now >= obj.start_time and now <= obj.end_time:
            return 'ongoing'
        else:
            return 'completed'


class ExamDetailSerializer(serializers.ModelSerializer):
    """Serializer for exam detail view"""
    class_obj = ClassListSerializer(read_only=True)
    created_by = UserProfileSerializer(read_only=True)
    exam_questions = ExamQuestionSerializer(many=True, read_only=True)
    sessions = serializers.SerializerMethodField()
    favorites_count = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'total_score', 'minutes', 
                 'start_time', 'end_time', 'created_at', 'class_obj', 
                 'created_by', 'exam_questions', 'sessions', 'favorites_count', 'is_favorited']
        read_only_fields = ['id', 'created_at', 'created_by']
    
    def get_sessions(self, obj):
        # This will be implemented when exam_sessions module is ready
        return []
    
    def get_favorites_count(self, obj):
        return obj.favorites.count()
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False


class ExamCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating exams"""
    questions = ExamQuestionCreateUpdateSerializer(many=True, required=False)
    
    class Meta:
        model = Exam
        fields = ['class_obj', 'title', 'description', 'total_score', 'minutes', 
                 'start_time', 'end_time', 'questions']
        extra_kwargs = {
            'class_obj': {'required': False},
            'start_time': {'required': False},
            'end_time': {'required': False}
        }
    
    def validate_class_obj(self, value):
        # Check if the current user is the teacher of this class
        if self.context['request'].user != value.teacher:
            raise serializers.ValidationError("You can only create exams for your own classes.")
        return value
    
    def validate(self, attrs):
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')
        
        if start_time and end_time:
            if start_time >= end_time:
                raise serializers.ValidationError("End time must be after start time.")
        
        return attrs
    
    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        validated_data['created_by'] = self.context['request'].user
        
        exam = Exam.objects.create(**validated_data)
        
        # Create exam questions if provided
        for question_data in questions_data:
            question_id = question_data.get('question_id')
            if question_id:
                question = Question.objects.get(id=question_id)
                # Remove question_id from question_data before creating ExamQuestion
                question_data_copy = question_data.copy()
                question_data_copy.pop('question_id', None)
                ExamQuestion.objects.create(
                    exam=exam,
                    question=question,
                    **question_data_copy
                )
        
        return exam
    
    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', None)
        
        # Update exam fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update questions if provided
        if questions_data is not None:
            # Delete existing exam questions
            instance.exam_questions.all().delete()
            
            # Create new exam questions
            for question_data in questions_data:
                question_id = question_data.get('question_id')
                if question_id:
                    question = Question.objects.get(id=question_id)
                    # Remove question_id from question_data before creating ExamQuestion
                    question_data_copy = question_data.copy()
                    question_data_copy.pop('question_id', None)
                    ExamQuestion.objects.create(
                        exam=instance,
                        question=question,
                        **question_data_copy
                    )
        
        return instance


class ExamAvailableSerializer(serializers.ModelSerializer):
    """Serializer for available exams for students"""
    class_obj = ClassListSerializer(read_only=True)
    created_by = UserProfileSerializer(read_only=True)
    question_count = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    can_start = serializers.SerializerMethodField()
    time_remaining = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    has_session = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'total_score', 'minutes', 
                 'start_time', 'end_time', 'class_obj', 'created_by', 
                 'question_count', 'status', 'can_start', 'time_remaining', 
                 'is_favorited', 'has_session']
    
    def get_question_count(self, obj):
        return obj.exam_questions.count()
    
    def get_status(self, obj):
        now = timezone.now()
        if now < obj.start_time:
            return 'upcoming'
        elif now >= obj.start_time and now <= obj.end_time:
            return 'ongoing'
        else:
            return 'completed'
    
    def get_can_start(self, obj):
        now = timezone.now()
        return obj.start_time <= now <= obj.end_time
    
    def get_time_remaining(self, obj):
        now = timezone.now()
        if now < obj.start_time:
            time_diff = obj.start_time - now
            days = time_diff.days
            hours, remainder = divmod(time_diff.seconds, 3600)
            return f"{days} days, {hours} hours"
        elif now >= obj.start_time and now <= obj.end_time:
            time_diff = obj.end_time - now
            hours, remainder = divmod(time_diff.seconds, 3600)
            minutes = remainder // 60
            return f"{hours} hours, {minutes} minutes"
        else:
            return "Exam completed"
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorites.filter(user=request.user).exists()
        return False
    
    def get_has_session(self, obj):
        # This will be implemented when exam_sessions module is ready
        return False


class ExamFavoriteSerializer(serializers.ModelSerializer):
    """Serializer for exam favorites"""
    user = UserProfileSerializer(read_only=True)
    exam = ExamListSerializer(read_only=True)
    
    class Meta:
        model = ExamFavorite
        fields = ['id', 'user', 'exam', 'created_at']
        read_only_fields = ['id', 'created_at']


class ExamFavoriteListSerializer(serializers.ModelSerializer):
    """Serializer for listing favorite exams"""
    exam = ExamListSerializer(read_only=True)
    
    class Meta:
        model = ExamFavorite
        fields = ['id', 'exam', 'created_at']
        read_only_fields = ['id', 'created_at']


class ExamStatisticsSerializer(serializers.Serializer):
    """Serializer for exam statistics"""
    exam = serializers.SerializerMethodField()
    statistics = serializers.SerializerMethodField()
    score_distribution = serializers.SerializerMethodField()
    
    def get_exam(self, obj):
        return {
            'id': obj.id,
            'title': obj.title,
            'total_score': obj.total_score,
            'minutes': obj.minutes
        }
    
    def get_statistics(self, obj):
        # This will be implemented when exam_sessions module is ready
        return {
            'total_students': obj.class_obj.students.count(),
            'completed_sessions': 0,
            'in_progress_sessions': 0,
            'abandoned_sessions': 0,
            'timeout_sessions': 0,
            'average_score': 0.0,
            'highest_score': 0.0,
            'lowest_score': 0.0,
            'completion_rate': 0.0
        }
    
    def get_score_distribution(self, obj):
        # This will be implemented when exam_sessions module is ready
        return {
            '0-20': 0,
            '21-40': 0,
            '41-60': 0,
            '61-80': 0,
            '81-100': 0
        }
