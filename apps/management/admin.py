from django.contrib import admin

from .models import (
    AcademicYear, Faculty, Department, Direction, Group, StudentGroup,
    Subject, Semester, Lesson, LessonMaterial, LessonQuiz, LessonQuizQuestion,
    LessonQuizQuestionAnswer, StudentLessonQuiz, StudentLessonQuizAnswer, SemesterSubject
)


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("year", "is_current", "created_at")
    list_filter = ("is_current",)
    search_fields = ("year",)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "faculty")
    list_filter = ("faculty",)
    search_fields = ("name", "faculty__name")


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "department", "type")
    list_filter = ("department", "type")
    search_fields = ("code", "name")


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "direction", "type", "course")
    list_filter = ("direction", "type", "course")
    search_fields = ("name", "direction__name")


@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ("group", "student", "created_at")
    list_filter = ("group",)
    search_fields = ("student__username", "group__name")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("title", "type")
    list_filter = ("type",)
    search_fields = ("title",)


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("order", "group", "academic_year", "is_finished")
    list_filter = ("order", "group", "academic_year", "is_finished")


@admin.register(SemesterSubject)
class SemesterSubjectAdmin(admin.ModelAdmin):
    list_display = ("semester", "subject", "teacher", "lesson", "practice", "self_work", "total")
    list_filter = ("semester", "subject", "teacher",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "semester_subject", "lesson_type", "order", "quiz_duration")
    list_filter = ("lesson_type", "semester_subject")
    search_fields = ("title",)


@admin.register(LessonMaterial)
class LessonMaterialAdmin(admin.ModelAdmin):
    list_display = ("lesson", "type", "file", "description")
    list_filter = ("type",)
    search_fields = ("lesson__title", "description")


@admin.register(LessonQuiz)
class LessonQuizAdmin(admin.ModelAdmin):
    list_display = ("lesson", "created_at")
    search_fields = ("lesson__title",)


@admin.register(LessonQuizQuestion)
class LessonQuizQuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "question")
    search_fields = ("quiz__lesson__title", "question")


@admin.register(LessonQuizQuestionAnswer)
class LessonQuizQuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "choice", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("question__question", "answer")


@admin.register(StudentLessonQuiz)
class StudentLessonQuizAdmin(admin.ModelAdmin):
    list_display = ("quiz", "student", "score", "percent", "status", "started_at", "finished_at")
    list_filter = ("status",)
    search_fields = ("student__username", "quiz__lesson__title")


@admin.register(StudentLessonQuizAnswer)
class StudentLessonQuizAnswerAdmin(admin.ModelAdmin):
    list_display = ("student_quiz", "question", "answer", "is_correct", "is_skip")
    list_filter = ("is_correct", "is_skip")
    search_fields = ("student_quiz__student__username", "question__question")
