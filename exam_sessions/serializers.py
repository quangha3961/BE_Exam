from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import ExamSession, StudentAnswer, ExamResult, ExamLog
from exams.models import Exam, ExamQuestion
from questions.models import Question, QuestionAnswer
from accounts.models import User


class QuestionAnswerSerializer(serializers.ModelSerializer):
    """Serializer for question answers"""
    class Meta:
        model = QuestionAnswer
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for questions"""
    answers = QuestionAnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'type', 'difficulty', 'image_url', 'answers']


class ExamQuestionSerializer(serializers.ModelSerializer):
    """Serializer for exam questions"""
    question = QuestionSerializer(read_only=True)
    
    class Meta:
        model = ExamQuestion
        fields = ['id', 'order', 'code', 'question']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user information"""
    class Meta:
        model = User
        fields = ['id', 'email', 'fullName', 'role', 'created_at', 'last_login', 'is_active', 'is_staff', 'is_superuser']


class ClassSerializer(serializers.ModelSerializer):
    """Serializer for class information"""
    teacher = UserSerializer(read_only=True)
    
    class Meta:
        from classes.models import Class
        model = Class
        fields = ['id', 'className', 'teacher', 'created_at']


class ExamSerializer(serializers.ModelSerializer):
    """Serializer for exam information"""
    class_obj = ClassSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'total_score', 'minutes', 'start_time', 'end_time', 'class_obj', 'created_by']


class StudentAnswerSerializer(serializers.ModelSerializer):
    """Serializer for student answers"""
    selected_answer = QuestionAnswerSerializer(read_only=True)
    exam_question = ExamQuestionSerializer(read_only=True)
    
    class Meta:
        model = StudentAnswer
        fields = ['id', 'exam_question', 'selected_answer', 'answer_text', 'score', 'answered_at', 'is_correct']


class ExamLogSerializer(serializers.ModelSerializer):
    """Serializer for exam logs"""
    class Meta:
        model = ExamLog
        fields = ['id', 'actions', 'timestamp', 'detail']


class ExamSessionSerializer(serializers.ModelSerializer):
    """Serializer for exam sessions"""
    exam = ExamSerializer(read_only=True)
    student = UserSerializer(read_only=True)
    answers = StudentAnswerSerializer(many=True, read_only=True)
    time_remaining = serializers.SerializerMethodField()
    
    class Meta:
        model = ExamSession
        fields = ['id', 'exam', 'student', 'code', 'start_time', 'end_time', 'total_score', 'status', 'submitted_at', 'time_remaining', 'answers']
    
    def get_time_remaining(self, obj):
        """Calculate remaining time in seconds"""
        if obj.status != 'in_progress':
            return 0
        
        now = timezone.now()
        exam_end_time = obj.exam.end_time
        session_end_time = obj.start_time + timedelta(minutes=obj.exam.minutes)
        
        # Use the earlier of exam end time or session time limit
        actual_end_time = min(exam_end_time, session_end_time)
        
        if now >= actual_end_time:
            return 0
        
        return int((actual_end_time - now).total_seconds())


class ExamSessionCreateSerializer(serializers.Serializer):
    """Serializer for creating exam sessions"""
    exam_id = serializers.IntegerField()
    
    def validate_exam_id(self, value):
        """Validate that exam exists and is available"""
        try:
            exam = Exam.objects.get(id=value)
        except Exam.DoesNotExist:
            raise serializers.ValidationError("Exam does not exist")
        
        # Check if exam is available for students
        now = timezone.now()
        if now < exam.start_time:
            raise serializers.ValidationError("Exam has not started yet")
        if now > exam.end_time:
            raise serializers.ValidationError("Exam has already ended")
        
        return value


class StudentAnswerCreateSerializer(serializers.Serializer):
    """Serializer for creating student answers"""
    exam_question_id = serializers.IntegerField()
    selected_answer_id = serializers.IntegerField(required=False, allow_null=True)
    answer_text = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        """Validate answer data based on question type"""
        exam_question_id = data.get('exam_question_id')
        selected_answer_id = data.get('selected_answer_id')
        answer_text = data.get('answer_text', '')
        
        try:
            exam_question = ExamQuestion.objects.get(id=exam_question_id)
        except ExamQuestion.DoesNotExist:
            raise serializers.ValidationError("Exam question does not exist")
        
        question = exam_question.question
        
        # Validate based on question type
        if question.type in ['multiple_choice', 'true_false']:
            if not selected_answer_id:
                raise serializers.ValidationError("selected_answer_id is required for this question type")
            
            # Validate that the selected answer belongs to this question
            try:
                answer = QuestionAnswer.objects.get(id=selected_answer_id, question=question)
            except QuestionAnswer.DoesNotExist:
                raise serializers.ValidationError("Selected answer does not belong to this question")
        
        elif question.type in ['fill_blank', 'essay']:
            if not answer_text.strip():
                raise serializers.ValidationError("answer_text is required for this question type")
        
        return data


class StudentAnswerUpdateSerializer(serializers.Serializer):
    """Serializer for updating student answers"""
    selected_answer_id = serializers.IntegerField(required=False, allow_null=True)
    answer_text = serializers.CharField(required=False, allow_blank=True)


class ExamResultSerializer(serializers.ModelSerializer):
    """Serializer for exam results"""
    session = serializers.SerializerMethodField()
    student = UserSerializer(read_only=True)
    exam = ExamSerializer(read_only=True)
    grade = serializers.SerializerMethodField()
    time_taken = serializers.SerializerMethodField()
    answers_summary = serializers.SerializerMethodField()
    
    class Meta:
        model = ExamResult
        fields = ['id', 'session', 'student', 'exam', 'total_score', 'correct_count', 'wrong_count', 
                 'submitted_at', 'status', 'feedback', 'percentage', 'grade', 'time_taken', 'answers_summary']
    
    def get_session(self, obj):
        """Get session information"""
        return {
            'id': obj.session.id,
            'code': obj.session.code,
            'status': obj.session.status
        }
    
    def get_grade(self, obj):
        """Calculate letter grade based on percentage"""
        percentage = float(obj.percentage)
        if percentage >= 90:
            return 'A'
        elif percentage >= 80:
            return 'B'
        elif percentage >= 70:
            return 'C'
        elif percentage >= 60:
            return 'D'
        else:
            return 'F'
    
    def get_time_taken(self, obj):
        """Calculate time taken in minutes"""
        if obj.session.start_time and obj.session.end_time:
            duration = obj.session.end_time - obj.session.start_time
            return int(duration.total_seconds() / 60)
        return 0
    
    def get_answers_summary(self, obj):
        """Get summary of all answers"""
        answers = []
        for answer in obj.session.answers.all().order_by('exam_question__order'):
            question = answer.exam_question.question
            answer_data = {
                'question_order': answer.exam_question.order,
                'question_text': question.question_text,
                'is_correct': answer.is_correct,
                'score': float(answer.score),
                'selected_answer': answer.selected_answer.text if answer.selected_answer else answer.answer_text,
                'correct_answer': self._get_correct_answer(question)
            }
            answers.append(answer_data)
        return answers
    
    def _get_correct_answer(self, question):
        """Get the correct answer for a question"""
        if question.type in ['multiple_choice', 'true_false']:
            correct_answer = question.answers.filter(is_correct=True).first()
            return correct_answer.text if correct_answer else None
        return None


class ExamSessionListSerializer(serializers.ModelSerializer):
    """Serializer for exam session list views"""
    exam = serializers.SerializerMethodField()
    student = UserSerializer(read_only=True)
    time_taken = serializers.SerializerMethodField()
    
    class Meta:
        model = ExamSession
        fields = ['id', 'exam', 'student', 'code', 'start_time', 'end_time', 'total_score', 
                 'status', 'submitted_at', 'time_taken', 'percentage']
    
    def get_exam(self, obj):
        """Get basic exam information"""
        return {
            'id': obj.exam.id,
            'title': obj.exam.title,
            'class_obj': {
                'id': obj.exam.class_obj.id,
                'className': obj.exam.class_obj.className
            } if obj.exam.class_obj else None
        }
    
    def get_time_taken(self, obj):
        """Calculate time taken in minutes"""
        if obj.start_time and obj.end_time:
            duration = obj.end_time - obj.start_time
            return int(duration.total_seconds() / 60)
        return 0


class ExamSessionDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed exam session view"""
    exam = ExamSerializer(read_only=True)
    student = UserSerializer(read_only=True)
    answers = StudentAnswerSerializer(many=True, read_only=True)
    logs = ExamLogSerializer(many=True, read_only=True)
    
    class Meta:
        model = ExamSession
        fields = ['id', 'exam', 'student', 'code', 'start_time', 'end_time', 'total_score', 
                 'status', 'submitted_at', 'answers', 'logs']


class ExamSessionActiveSerializer(serializers.ModelSerializer):
    """Serializer for active session view"""
    exam = serializers.SerializerMethodField()
    time_remaining = serializers.SerializerMethodField()
    answered_count = serializers.SerializerMethodField()
    total_questions = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = ExamSession
        fields = ['id', 'exam', 'code', 'start_time', 'status', 'time_remaining', 
                 'answered_count', 'total_questions', 'progress_percentage']
    
    def get_exam(self, obj):
        """Get basic exam information"""
        return {
            'id': obj.exam.id,
            'title': obj.exam.title,
            'minutes': obj.exam.minutes
        }
    
    def get_time_remaining(self, obj):
        """Calculate remaining time in seconds"""
        if obj.status != 'in_progress':
            return 0
        
        now = timezone.now()
        exam_end_time = obj.exam.end_time
        session_end_time = obj.start_time + timedelta(minutes=obj.exam.minutes)
        
        actual_end_time = min(exam_end_time, session_end_time)
        
        if now >= actual_end_time:
            return 0
        
        return int((actual_end_time - now).total_seconds())
    
    def get_answered_count(self, obj):
        """Get count of answered questions"""
        return obj.answers.filter(answered_at__isnull=False).count()
    
    def get_total_questions(self, obj):
        """Get total number of questions"""
        return obj.exam.exam_questions.count()
    
    def get_progress_percentage(self, obj):
        """Calculate progress percentage"""
        total = self.get_total_questions(obj)
        if total == 0:
            return 0.0
        answered = self.get_answered_count(obj)
        return round((answered / total) * 100, 1)


class ExamSessionStatisticsSerializer(serializers.Serializer):
    """Serializer for exam session statistics"""
    exam = serializers.DictField()
    sessions = serializers.DictField()
    statistics = serializers.DictField()
