from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from apps.common.models import BaseModel


class AcademicYear(BaseModel):
    year = models.CharField(max_length=9, unique=True)
    is_current = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'O`quv yili'
        verbose_name_plural = 'O`quv yillari'

    def __str__(self):
        return self.year


class CourseChoice(models.IntegerChoices):
    FIRST = 1, '1'
    SECOND = 2, '2'
    THIRD = 3, '3'
    FOURTH = 4, '4'


class Faculty(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Fakultet'
        verbose_name_plural = 'Fakultetlar'


class Department(BaseModel):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name="departments"
    )

    class Meta:
        unique_together = ("name", "faculty")
        verbose_name = 'Kafedra'
        verbose_name_plural = 'Kafedralar'

    def __str__(self):
        return f"{self.name} ({self.faculty.name})"


class StudentType(models.IntegerChoices):
    BACHELOR = 0, "Bakalavriat"
    MASTER = 1, "Magistratura"


class Direction(BaseModel):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    type = models.IntegerField(choices=StudentType.choices, default=StudentType.BACHELOR)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        unique_together = ("name", "department", "type")
        verbose_name = 'Yo`nalish'
        verbose_name_plural = 'Yo`nalishlar'


class Group(BaseModel):
    name = models.CharField(max_length=150)
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True)
    type = models.IntegerField(choices=StudentType.choices, default=StudentType.BACHELOR)
    course = models.IntegerField(choices=CourseChoice.choices, default=CourseChoice.FIRST)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Guruh'
        verbose_name_plural = 'Guruhlar'


class StudentGroup(BaseModel):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Talaba guruhi"
        verbose_name_plural = "Talaba guruhlari"
        unique_together = ("group", "student")


class Subject(BaseModel):
    title = models.CharField("Nomi", max_length=50)
    type = models.IntegerField("Turi", choices=StudentType.choices, default=StudentType.BACHELOR)

    def __str__(self):
        return f"{self.title} | {'Bakalavr' if self.type == 0 else 'Magister'}"

    class Meta:
        ordering = ('title',)
        verbose_name = 'Fan'
        verbose_name_plural = 'Fanlar'


class SemesterChoice(models.IntegerChoices):
    SEMESTER_1 = 1, "1-semestr"
    SEMESTER_2 = 2, "2-semestr"
    SEMESTER_3 = 3, "3-semestr"
    SEMESTER_4 = 4, "4-semestr"
    SEMESTER_5 = 5, "5-semestr"
    SEMESTER_6 = 6, "6-semestr"
    SEMESTER_7 = 7, "7-semestr"
    SEMESTER_8 = 8, "8-semestr"


class Semester(BaseModel):
    semester = models.IntegerField(choices=SemesterChoice.choices, default=SemesterChoice.SEMESTER_1)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    lesson = models.IntegerField("Dars soati", default=0)
    practice = models.IntegerField("Amaliyot soati", default=0)
    self_work = models.IntegerField("Mustaqil ish soati", default=0)
    total = models.IntegerField("Jami soat", default=0)
    credit = models.IntegerField("Kredit", default=0)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True)
    is_finished = models.BooleanField("Tugatildi", default=False)

    class Meta:
        ordering = ("semester", "group")
        verbose_name = "Semestr"
        verbose_name_plural = "Semestrlar"


class LessonType(models.IntegerChoices):
    LECTURE = 1, "Ma'ruza"
    SEMINAR = 2, "Seminar"
    LABORATORY = 3, "Laboratoriya"
    PRACTICE = 4, "Amaliyot"
    TEST = 5, "Test"


class Lesson(BaseModel):
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, related_name="lessons")
    lesson_type = models.IntegerField(choices=LessonType.choices, default=LessonType.LECTURE)
    title = models.CharField("Mavzu", max_length=255)
    order = models.IntegerField("Tartib raqami", default=1)
    quiz_duration = models.DurationField("Test davomiyligi", null=True)

    class Meta:
        ordering = ("order",)
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"

    def __str__(self):
        return self.title


class LessonMaterialType(models.IntegerChoices):
    PRESENTATION = 1, "Taqdimot"
    GLOSSARY = 2, "Lug'at"
    LECTURE = 3, "Ma'ruza"
    OTHER = 4, "Boshqa"


class LessonMaterial(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="materials")
    type = models.IntegerField(choices=LessonMaterialType.choices, default=LessonMaterialType.OTHER)
    file = models.FileField(upload_to='lesson_materials/')
    description = models.CharField("Tavsif", max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Dars materiali"
        verbose_name_plural = "Dars materiallari"


class LessonQuiz(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="tests")

    class Meta:
        verbose_name = "Dars testi"
        verbose_name_plural = "Dars testlari"


class LessonQuizQuestion(BaseModel):
    quiz = models.ForeignKey(LessonQuiz, on_delete=models.CASCADE, related_name="questions")
    question = CKEditor5Field("Savol", null=True)

    class Meta:
        verbose_name = "Test savoli"
        verbose_name_plural = "Test savollari"


class AnswerChoice(models.TextChoices):
    A = 'A', 'A'
    B = 'B', 'B'
    C = 'C', 'C'
    D = 'D', 'D'


class LessonQuizQuestionAnswer(BaseModel):
    question = models.ForeignKey(LessonQuizQuestion, on_delete=models.CASCADE, related_name="answers")
    answer = CKEditor5Field("Javob", null=True)
    is_correct = models.BooleanField("To'g'ri javob", default=False)
    choice = models.CharField(max_length=1, choices=AnswerChoice.choices, verbose_name="Javob varianti", null=True)

    class Meta:
        verbose_name = "Savol javobi"
        verbose_name_plural = "Savol javoblari"


class QuizStatus(models.IntegerChoices):
    PENDING = 0, "Pending"
    FINISHED = 1, "Finished"
    PASSED = 2, "Passed"
    FAILED = 3, "Failed"


class StudentLessonQuiz(BaseModel):
    quiz = models.ForeignKey(LessonQuiz, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    score = models.DecimalField("Ball", max_digits=5, decimal_places=2, default=0)
    percent = models.DecimalField("Foiz", max_digits=5, decimal_places=2, default=0)
    status = models.IntegerField("Holati", choices=QuizStatus.choices, default=QuizStatus.PENDING)
    started_at = models.DateTimeField("Boshlangan vaqti", null=True)
    finished_at = models.DateTimeField("Tugatgan vaqti", null=True)

    class Meta:
        verbose_name = "Talaba testi"
        verbose_name_plural = "Talaba testlari"
        unique_together = ("quiz", "student")


class StudentLessonQuizAnswer(BaseModel):
    student_quiz = models.ForeignKey(StudentLessonQuiz, on_delete=models.CASCADE, related_name="student_answers")
    question = models.ForeignKey(LessonQuizQuestion, on_delete=models.SET_NULL, null=True)
    answer = models.ForeignKey(LessonQuizQuestionAnswer, on_delete=models.SET_NULL, null=True)
    is_correct = models.BooleanField("To'g'ri javob", default=False)
    is_skip = models.BooleanField("O'tkazib yuborilganmi?", default=False)

    class Meta:
        verbose_name = "Talaba javobi"
        verbose_name_plural = "Talaba javoblari"
