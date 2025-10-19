from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Question, QuestionAnswer
from accounts.serializers import UserProfileSerializer

User = get_user_model()


class QuestionAnswerSerializer(serializers.ModelSerializer):
    """Serializer for question answers"""
    
    class Meta:
        model = QuestionAnswer
        fields = ['id', 'text', 'is_correct', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class QuestionAnswerCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating question answers"""
    
    class Meta:
        model = QuestionAnswer
        fields = ['text', 'is_correct']
    
    def create(self, validated_data):
        validated_data['question'] = self.context['question']
        return super().create(validated_data)


class QuestionListSerializer(serializers.ModelSerializer):
    """Serializer for listing questions with basic info"""
    teacher = UserProfileSerializer(read_only=True)
    answers = QuestionAnswerSerializer(many=True, read_only=True)
    usage_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'type', 'difficulty', 'image_url', 
                 'teacher', 'created_at', 'answers', 'usage_count']
        read_only_fields = ['id', 'teacher', 'created_at']
    
    def get_usage_count(self, obj):
        # This will be implemented when exams module is ready
        return 0


class QuestionDetailSerializer(serializers.ModelSerializer):
    """Serializer for question detail view"""
    teacher = UserProfileSerializer(read_only=True)
    answers = QuestionAnswerSerializer(many=True, read_only=True)
    usage_count = serializers.SerializerMethodField()
    used_in_exams = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'type', 'difficulty', 'image_url', 
                 'teacher', 'created_at', 'answers', 'usage_count', 'used_in_exams']
        read_only_fields = ['id', 'teacher', 'created_at']
    
    def get_usage_count(self, obj):
        # This will be implemented when exams module is ready
        return 0
    
    def get_used_in_exams(self, obj):
        # This will be implemented when exams module is ready
        return []


class QuestionCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating questions"""
    answers = QuestionAnswerCreateUpdateSerializer(many=True, required=False)
    
    class Meta:
        model = Question
        fields = ['question_text', 'type', 'difficulty', 'image_url', 'answers']
    
    def create(self, validated_data):
        answers_data = validated_data.pop('answers', [])
        validated_data['teacher'] = self.context['request'].user
        question = Question.objects.create(**validated_data)
        
        # Create answers if provided
        for answer_data in answers_data:
            QuestionAnswer.objects.create(question=question, **answer_data)
        
        return question
    
    def update(self, instance, validated_data):
        answers_data = validated_data.pop('answers', None)
        
        # Update question fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update answers if provided
        if answers_data is not None:
            # Delete existing answers
            instance.answers.all().delete()
            
            # Create new answers
            for answer_data in answers_data:
                QuestionAnswer.objects.create(question=instance, **answer_data)
        
        return instance


class QuestionMyQuestionsSerializer(serializers.ModelSerializer):
    """Serializer for teacher's own questions list"""
    answers_count = serializers.SerializerMethodField()
    usage_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'type', 'difficulty', 'image_url', 
                 'created_at', 'answers_count', 'usage_count']
        read_only_fields = ['id', 'created_at']
    
    def get_answers_count(self, obj):
        return obj.answers.count()
    
    def get_usage_count(self, obj):
        # This will be implemented when exams module is ready
        return 0
