# BE_Exam
1. accounts - Quản lý người dùng
Models: User (custom user model)
Chức năng: Authentication, authorization, user profiles
2. classes - Quản lý lớp học
Models: Class, ClassStudent
Chức năng: Tạo lớp, thêm/xóa học sinh khỏi lớp
3. questions - Quản lý câu hỏi
Models: Question, QuestionAnswer
Chức năng: Tạo, sửa, xóa câu hỏi và đáp án
4. exams - Quản lý bài thi
Models: Exam, ExamQuestion, ExamFavorite
Chức năng: Tạo bài thi, thêm câu hỏi vào bài thi, yêu thích bài thi
5. sessions - Quản lý phiên thi
Models: ExamSession, StudentAnswer, ExamResult, ExamLog
Chức năng: Bắt đầu thi, lưu câu trả lời, tính điểm, log hoạt động
6. notifications - Thông báo
Models: Notification