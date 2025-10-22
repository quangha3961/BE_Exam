from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from accounts.models import User
from classes.models import Class, ClassStudent
from questions.models import Question, QuestionAnswer
from exams.models import Exam, ExamQuestion


class ResultsFlowTest(APITestCase):
    def setUp(self):
        # Users
        self.teacher = User.objects.create_user(
            email='teacherxx@example.com', password='pass', fullName='Teacher', role='teacher'
        )
        self.student = User.objects.create_user(
            email='studentxx@example.com', password='pass', fullName='Student', role='student'
        )

        # Class and enrollment
        self.class_obj = Class.objects.create(className='Test Class', teacher=self.teacher)
        ClassStudent.objects.create(class_obj=self.class_obj, student=self.student)

        # Question and answers
        self.question = Question.objects.create(
            question_text='What is 2 + 2?', type='multiple_choice', difficulty='easy', teacher=self.teacher
        )
        self.ans_wrong = QuestionAnswer.objects.create(question=self.question, text='3', is_correct=False)
        self.ans_right = QuestionAnswer.objects.create(question=self.question, text='4', is_correct=True)

        # Exam with one question
        now = timezone.now()
        self.exam = Exam.objects.create(
            class_obj=self.class_obj,
            title='Midterm',
            description='Math',
            total_score=100,
            minutes=60,
            start_time=now - timezone.timedelta(hours=1),
            end_time=now + timezone.timedelta(hours=1),
            created_by=self.teacher,
        )
        self.exam_question = ExamQuestion.objects.create(exam=self.exam, question=self.question, order=1, code='Q1')

        # Clients
        self.student_client = APIClient()
        self.student_client.force_authenticate(user=self.student)

        self.teacher_client = APIClient()
        self.teacher_client.force_authenticate(user=self.teacher)

    def test_full_results_flow(self):
        # 1) Student starts a session
        resp = self.student_client.post('/sessions/start/', {'exam_id': self.exam.id}, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.data.get('success'))
        session_id = resp.data['data']['id']

        # 2) Student submits an answer (correct)
        submit_answer_url = f'/sessions/{session_id}/answers/'
        resp = self.student_client.post(
            submit_answer_url,
            {
                'exam_question_id': self.exam_question.id,
                'selected_answer_id': self.ans_right.id,
            },
            format='json',
        )
        self.assertIn(resp.status_code, [200, 201])
        self.assertTrue(resp.data.get('success'))
        self.assertTrue(resp.data['data']['is_correct'])

        # 3) Student submits the exam
        resp = self.student_client.post(f'/sessions/{session_id}/submit/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data.get('success'))
        result_id = resp.data['data']['id']
        self.assertEqual(resp.data['data']['percentage'], '100.00')

        # 4) Get session result (student)
        resp = self.student_client.get(f'/sessions/{session_id}/result/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data.get('success'))
        self.assertEqual(resp.data['data']['id'], result_id)

        # 5) Get my results (student)
        resp = self.student_client.get('/results/my-results/?page=1&page_size=20')
        self.assertEqual(resp.status_code, 200)
        # Either paginated or simple list depending on paginator branch
        self.assertTrue('data' in resp.data)

        # 6) Get class results (teacher)
        resp = self.teacher_client.get(f'/results/class/{self.class_obj.id}/?exam_id={self.exam.id}&status=graded')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data.get('success'))
        self.assertIn('statistics', resp.data['data'])

        # 7) Get exam results (teacher)
        resp = self.teacher_client.get(f'/results/exam/{self.exam.id}/?status=graded')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data.get('success'))
        self.assertIn('statistics', resp.data['data'])

        # 8) Get student results (teacher)
        resp = self.teacher_client.get(f'/results/student/{self.student.id}/?class_id={self.class_obj.id}')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data.get('success'))

        # 9) Grade result (teacher)
        resp = self.teacher_client.post(
            f'/results/{result_id}/grade/',
            {'feedback': 'Good work!', 'status': 'graded'},
            format='json',
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data.get('success'))
        self.assertEqual(resp.data['data']['feedback'], 'Good work!')

        # 10) Get result detail (teacher)
        resp = self.teacher_client.get(f'/results/{result_id}/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data.get('success'))

# Create your tests here.
